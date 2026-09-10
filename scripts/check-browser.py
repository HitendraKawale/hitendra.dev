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


def browser(*args):
    result = subprocess.run(["agent-browser", "--session", session, *args], text=True, capture_output=True)
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
    browser("storage", "local", "clear")
    browser("reload")
    check("document.documentElement.dataset.theme !== 'dark'", "first visit is light")
    browser("find", "role", "button", "click", "--name", "Dark mode")
    check("document.documentElement.dataset.theme === 'dark' && document.querySelector('[data-theme-toggle]').getAttribute('aria-pressed') === 'true'", "theme changes and announces state")
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
        for width, height in [(320, 844), (390, 844), (768, 1024), (1440, 900)]:
            browser("set", "viewport", str(width), str(height))
            check("document.documentElement.scrollWidth <= innerWidth", f"{route} no overflow at {width}px")
        if route in ["/", "/projects", "/contact", "/blog/saga-scribble-segmentation"]:
            label = route.strip("/").replace("/", "-") or "home"
            for width, height, size in [(1440, 900, "desktop"), (390, 844, "mobile")]:
                browser("set", "viewport", str(width), str(height))
                for theme in ["light", "dark"]:
                    browser("eval", f"document.documentElement.dataset.theme = '{theme}'")
                    browser("screenshot", str(evidence / f"{label}-{size}-{theme}.png"))
    open_page("/not-a-real-page")
    check("document.querySelector('h1').textContent.includes('Page not found')", "404 recovery")
    open_page("/")
    browser("set", "viewport", "390", "844")
    check("document.querySelector('.intro .actions').getBoundingClientRect().bottom <= innerHeight", "intro contact links above fold on mobile")
    browser("press", "Tab")
    check("document.activeElement.textContent.includes('Skip to content')", "skip link first in keyboard order")
    browser("press", "Enter")
    check("document.activeElement.id === 'content'", "skip link focuses main")
    (evidence / "browser-errors.txt").write_text(browser("errors"))
    print("Browser checks passed", flush=True)
finally:
    browser("close")
