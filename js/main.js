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

// TODO: Add visitor counter, marquee polyfill, etc.