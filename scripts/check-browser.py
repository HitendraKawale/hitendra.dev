"""Run against a production preview with the installed agent-browser CLI."""
import json
import os
from pathlib import Path
import subprocess
import sys

base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4322"
evidence = Path(os.environ.get("SITE_EVIDENCE", "/tmp/hitendra-professional-evidence"))
evidence.mkdir(parents=True, exist_ok=True)
session = "hitendra-professional-check"


def browser(*args, session_name=session):
    result = subprocess.run(["agent-browser", "--session", session_name, *args], text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(f"{args}: {result.stdout}\n{result.stderr}")
    return result.stdout


def check(expression, message):
    browser("eval", f"if (!({expression})) throw new Error({json.dumps(message)}); 'PASS: {message}'")
    print(f"PASS: {message}", flush=True)


def open_page(route):
    browser("open", base + route)
    browser("snapshot", "-i")


try:
    open_page("/")
    browser("wait", "--fn", "document.querySelector('.castle-scene')?.classList.contains('ready')")
    check("document.querySelectorAll('[data-castle=hero] canvas').length === 1 && document.querySelector('[data-castle=hero] canvas').width > 0", "hero castle renders on home")
    browser("eval", "(() => {const gl=document.querySelector('canvas').getContext('webgl2'); const draw=gl.drawElements.bind(gl); window.__castleDraws=0; gl.drawElements=(...args)=>{window.__castleDraws++; return draw(...args)};})()")
    browser("wait", "--fn", "window.__castleDraws > 20")
    browser("eval", "scrollTo(0, document.body.scrollHeight)")
    browser("wait", "--fn", "document.querySelector('.castle-scene').getBoundingClientRect().bottom < 0")
    browser("eval", "new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
    before = browser("eval", "window.__castleDraws").strip()
    browser("eval", "new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
    assert browser("eval", "window.__castleDraws").strip() == before, "Offscreen castle kept drawing"
    print("PASS: offscreen castle stops drawing", flush=True)
    browser("eval", "scrollTo(0, 0)")
    browser("wait", "--fn", f"window.__castleDraws > {before}")
    print("PASS: visible castle resumes drawing", flush=True)
    browser("set", "media", "light", "reduced-motion")
    browser("screenshot", ".castle-scene canvas", str(evidence / "still-first.png"))
    browser("eval", "new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
    browser("screenshot", ".castle-scene canvas", str(evidence / "still-second.png"))
    assert (evidence / "still-first.png").read_bytes() == (evidence / "still-second.png").read_bytes(), "Reduced-motion scene moved"
    print("PASS: reduced motion keeps the 3D scene still", flush=True)
    browser("set", "media", "light")
    browser("storage", "local", "clear")
    browser("reload")
    check("document.documentElement.dataset.theme !== 'dark' && document.querySelector('meta[name=theme-color]').content === '#f1f5f3'", "first visit is light with matching browser chrome")
    browser("find", "role", "button", "click", "--name", "Dark mode")
    check("document.documentElement.dataset.theme === 'dark' && document.querySelector('[data-theme-toggle]').getAttribute('aria-pressed') === 'true' && document.querySelector('meta[name=theme-color]').content === '#10262c'", "theme changes and updates browser chrome")
    open_page("/projects")
    browser("wait", "--fn", "document.querySelector('[data-castle=accent]')?.classList.contains('ready')")
    check("document.querySelectorAll('[data-castle=accent] canvas').length === 1 && document.querySelector('[data-castle=accent]').dataset.view === 'stone'", "Projects has one stone camera view")
    browser("screenshot", ".castle-scene canvas", str(evidence / "projects-camera.png"))
    open_page("/blog")
    browser("wait", "--fn", "document.querySelector('[data-castle=accent]')?.classList.contains('ready')")
    check("document.querySelectorAll('[data-castle=accent] canvas').length === 1 && document.querySelector('[data-castle=accent]').dataset.view === 'roof'", "Writing has one roof camera view")
    browser("screenshot", ".castle-scene canvas", str(evidence / "writing-camera.png"))
    assert (evidence / "projects-camera.png").read_bytes() != (evidence / "writing-camera.png").read_bytes(), "Accent camera views match"
    print("PASS: accent camera views differ", flush=True)
    open_page("/projects")
    check("document.documentElement.dataset.theme === 'dark'", "theme persists across navigation")
    browser("reload")
    check("document.documentElement.dataset.theme === 'dark'", "theme persists across reload")
    browser("snapshot", "-i")
    browser("find", "role", "button", "click", "--name", "Dark mode")
    browser("eval", "localStorage.setItem('eclipse','1')")
    browser("reload")
    check("document.documentElement.dataset.theme !== 'dark' && !document.documentElement.hasAttribute('data-eclipse')", "legacy preference ignored")
    browser("snapshot", "-d", "5")
    browser("click", "summary")
    check("document.querySelector('details').open", "project details open")
    browser("focus", "summary")
    browser("press", "Enter")
    check("!document.querySelector('details').open", "Enter closes project details")
    browser("press", "Space")
    check("document.querySelector('details').open", "Space opens project details")
    check("document.querySelectorAll('[data-project]').length === 8 && document.querySelectorAll('[data-project] a.source').length === 7", "all projects present and missing URL has no fake link")
    open_page("/contact")
    browser("find", "role", "button", "click", "--name", "Copy email")
    browser("wait", "--text", "Email address copied.")
    check("document.querySelector('[role=status]').textContent === 'Email address copied.'", "real clipboard write succeeds")
    browser("eval", "Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async()=>{throw new DOMException('Denied','NotAllowedError')}}})")
    browser("find", "role", "button", "click", "--name", "Copy email")
    browser("wait", "--text", "Could not copy.")
    check("document.querySelector('[role=status]').textContent.includes('Select the email') && !document.querySelector('[data-copy]').disabled", "clipboard denial gives actionable status and allows retry")
    browser("eval", "Storage.prototype.setItem = () => {throw new Error('Storage blocked')}")
    browser("find", "role", "button", "click", "--name", "Dark mode")
    check("document.documentElement.dataset.theme === 'dark'", "theme still works when storage write fails")
    browser("set", "media", "reduced-motion")
    check("getComputedStyle(document.querySelector('a')).transitionDuration === '0s'", "reduced motion disables transitions")
    routes = ["/", "/projects", "/blog", "/contact", "/tldr"]
    routes += ["/blog/" + path.name for path in Path("dist/blog").iterdir() if path.is_dir()]
    for route in routes:
        open_page(route)
        check("document.querySelectorAll('main').length === 1 && document.querySelectorAll('h1').length === 1", route + " landmarks")
        check("!document.querySelector('a[href=\"undefined\"],a[href=\"#\"]')", route + " links")
        if route in ["/", "/projects", "/blog"]:
            browser("wait", "--fn", "document.querySelector('.castle-scene')?.classList.contains('ready')")
            check("document.querySelectorAll('.castle-scene canvas').length === 1", route + " one castle canvas")
        else:
            check("!document.querySelector('canvas') && !performance.getEntriesByType('resource').some(e => e.name.includes('three.module'))", route + " has no castle or Three.js request")
        for width, height in [(320, 844), (390, 844), (768, 1024), (1440, 900)]:
            browser("set", "viewport", str(width), str(height))
            check("document.documentElement.scrollWidth <= innerWidth", f"{route} no overflow at {width}px")
        if route in ["/", "/projects", "/blog", "/contact", "/tldr", "/blog/saga-scribble-segmentation"]:
            label = route.strip("/").replace("/", "-") or "home"
            for width, height, size in [(1440, 900, "desktop"), (390, 844, "mobile")]:
                browser("set", "viewport", str(width), str(height))
                for theme in ["light", "dark"]:
                    browser("eval", f"document.documentElement.dataset.theme = '{theme}'")
                    browser("screenshot", str(evidence / f"{label}-{size}-{theme}.png"))
    open_page("/not-a-real-page")
    check("document.querySelector('h1').textContent.includes('Page not found')", "404 recovery")
    check("!document.querySelector('canvas') && !performance.getEntriesByType('resource').some(e => e.name.includes('three.module'))", "404 has no Three.js request")
    open_page("/")
    browser("set", "viewport", "390", "844")
    check("document.querySelector('.intro .actions').getBoundingClientRect().bottom <= innerHeight", "intro contact links above fold on mobile")
    browser("set", "viewport", "320", "844")
    check("document.querySelector('.intro .actions').getBoundingClientRect().bottom <= innerHeight && document.querySelector('.castle-scene').getBoundingClientRect().top < innerHeight", "actions and castle appear in first screen at 320px")
    browser("press", "Tab")
    check("document.activeElement.textContent.includes('Skip to content')", "skip link first in keyboard order")
    browser("press", "Enter")
    check("document.activeElement.id === 'content'", "skip link focuses main")
    (evidence / "browser-errors.txt").write_text(browser("errors"))
    for fallback, pattern in [("castle-no-three", "**/three.module.*.js"), ("castle-no-js", "**/*.js")]:
        try:
            browser("open", "about:blank", session_name=fallback)
            browser("network", "route", pattern, "--abort", session_name=fallback)
            browser("open", base + "/", session_name=fallback)
            browser("wait", "--load", "networkidle", session_name=fallback)
            browser("eval", "if (!(document.querySelector('.castle-scene img').naturalWidth > 0 && getComputedStyle(document.querySelector('.castle-scene img')).display !== 'none' && document.querySelector('.castle-scene canvas').hidden && document.querySelector('h1').textContent.includes('I build AI systems') && document.querySelector('.intro a[href=\"/contact\"]'))) throw new Error('Castle fallback obscured home content')", session_name=fallback)
            browser("screenshot", str(evidence / (fallback + ".png")), session_name=fallback)
            browser("eval", "document.documentElement.dataset.theme='dark'", session_name=fallback)
            browser("eval", "if (getComputedStyle(document.querySelector('.castle-scene img')).filter === 'none') throw new Error('Dark fallback was not tinted')", session_name=fallback)
            browser("screenshot", str(evidence / (fallback + "-dark.png")), session_name=fallback)
            print(f"PASS: {fallback} keeps the castle illustration and home content in both themes", flush=True)
        finally:
            browser("close", session_name=fallback)
    print("Browser checks passed", flush=True)
finally:
    browser("close")
