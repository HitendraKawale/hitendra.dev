// @ts-check
import { defineConfig } from 'astro/config';

// Local admin panel — routes are injected only when running `astro dev`,
// so nothing admin-related ever exists in the production build.
const localAdmin = () => ({
  name: 'local-admin',
  hooks: {
    /** @param {{ command: string, injectRoute: Function }} options */
    'astro:config:setup'({ command, injectRoute }) {
      if (command !== 'dev') return;
      injectRoute({ pattern: '/admin', entrypoint: './src/admin/panel.astro', prerender: false });
      injectRoute({ pattern: '/admin/api/projects', entrypoint: './src/admin/api/projects.ts', prerender: false });
      injectRoute({ pattern: '/admin/api/posts', entrypoint: './src/admin/api/posts.ts', prerender: false });
    },
  },
});

export default defineConfig({
  output: 'static',
  site: 'https://hitendra-chronicle.vercel.app',
  integrations: [localAdmin()],
});
