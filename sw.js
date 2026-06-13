/* Shopping PWA service worker — offline-first shell cache */
const CACHE = 'shopping-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Never cache Supabase API calls — always go to network.
  if (url.hostname.endsWith('supabase.co')) return;
  if (e.request.method !== 'GET') return;

  const isDoc = e.request.mode === 'navigate' ||
    (e.request.destination === 'document') ||
    url.pathname.endsWith('/') || url.pathname.endsWith('index.html');

  if (isDoc) {
    // Network-first for the app shell so updates always reach the user;
    // fall back to cache when offline.
    e.respondWith(
      fetch(e.request).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put('./index.html', copy)).catch(() => {});
        return res;
      }).catch(() => caches.match('./index.html') || caches.match('./'))
    );
    return;
  }

  // Cache-first for static assets (icons, manifest).
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
      return res;
    }))
  );
});
