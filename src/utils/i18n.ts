import ko from '../content/i18n/ko.json';
import en from '../content/i18n/en.json';

const translations = { ko, en } as const;
type Locale = keyof typeof translations;

export function getLocale(url: URL): Locale {
  return url.pathname.startsWith('/en') ? 'en' : 'ko';
}

export function t(url: URL) {
  return translations[getLocale(url)];
}

export function localePath(path: string, url: URL): string {
  const locale = getLocale(url);
  return locale === 'ko' ? path : `/en${path}`;
}

export function altLocalePath(path: string, url: URL): string {
  const locale = getLocale(url);
  if (locale === 'ko') {
    return `/en${path}`;
  }
  return path;
}

export function altLocale(url: URL): Locale {
  return getLocale(url) === 'ko' ? 'en' : 'ko';
}
