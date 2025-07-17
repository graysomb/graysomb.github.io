/* main.js - shared site scripts */
// Fake Meme Ad Rotator - dynamic loading from js/ads.json

document.addEventListener('DOMContentLoaded', () => {
  fetch('js/ads.json')
    .then(res => res.json())
    .then(data => {
      const ads = data.ads.map(filename => ({
        src: `images/ads/${filename}`,
        href: '#'
      }));
      const adSlot = document.getElementById('sidebar-ad');
      if (adSlot && ads.length) {
        const ad = ads[Math.floor(Math.random() * ads.length)];
        const link = document.createElement('a');
        link.href = ad.href;
        link.target = '_blank';
        const img = document.createElement('img');
        img.src = ad.src;
        img.alt = 'Meme Ad';
        img.width = 200;
        img.height = 200;
        link.appendChild(img);
        adSlot.innerHTML = '';
        adSlot.appendChild(link);
      }
    })
    .catch(err => console.error('Failed to load ads manifest:', err));
});

// Visitor Counter via countapi.xyz
// Use immediate script (deferred) to run after DOM load
(function() {
  const countEl = document.getElementById('visit-count');
  if (!countEl) return;
  // Use current hostname as namespace, fallback to 'retro-site'
  const namespace = window.location.hostname || 'retro-site';
  const key = 'visits';
  const url = `https://api.countapi.xyz/hit/${namespace}/${key}`;
  fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`CountAPI response ${res.status}`);
      return res.json();
    })
    .then(data => { countEl.textContent = data.value; })
    .catch(err => console.error('Visitor counter failed:', err));
})();
// TODO: Add marquee polyfill, etc.