// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // Deployed at lsy860224.github.io root (user-level GitHub Pages).
  // 이전 구조는 base: '/gentlelab.github.io' 였으나 절대 경로 버그로
  // sub-page·favicon이 깨지는 이슈 → root 배포로 전환 (2026-04-28).
  site: 'https://lsy860224.github.io',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  i18n: {
    locales: ['ko', 'en'],
    defaultLocale: 'ko',
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
