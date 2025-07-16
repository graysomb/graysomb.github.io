# Project Tasks
This file tracks tasks needed to build the early-2000s–style personal website.

## 1. Setup & Scaffolding
- [x] Create project root directories:
  - `css/`, `js/`, `images/ads/`, `assets/`
- [x] Scaffold HTML pages:
  - `index.html`, `projects.html`, `work.html`, `stories.html`,
    `essays.html`, `cringe.html`, `arxiv.html`, `cool-facts.html`, `donate.html`
- [x] Create CSS entrypoint: `css/style.css`
- [x] Create JS entrypoints: `js/main.js`, `js/code-generator.js`

## 2. Global Navigation & Layout
- [x] Implement persistent navigation bar or sidebar on all pages
- [x] Highlight active page in the navigation
- [x] Add a reusable ad slot container (`<div id="sidebar-ad">`)

## 3. Projects Page
- [x] Move existing random code generator from `index.html` to `projects.html`
- [x] Wire up `js/code-generator.js` and attach to a container element
- [x] Style the generator controls with pixel-style borders

## 4. Fake Meme Ad System
- [ ] Implement ad rotator logic in `js/main.js`
- [ ] Define array of ad filenames + dummy URLs
- [ ] Randomly inject a meme-ad image into the ad slot on page load
- [ ] Populate `images/ads/` with sample ad assets (e.g. GIFs)

## 5. Styling & Retro Aesthetics
- [ ] Set global styles in `css/style.css`:
  - Background tiled GIF or noise pattern
  - Pixel-font and system-font fallbacks
  - Neon-colored borders and tables
- [ ] Add marquee or CSS animations for “blinky” elements
- [ ] Ensure mobile/responsive fallback or allow scrollbars

## 6. Content Population
- [ ] **Homepage**: intro text, “Under Construction” GIF, top banner ad
- [ ] **Work**: list of roles/jobs with decorative boxes
- [ ] **Stories/Essays/Cringe**: index pages linking to entries
- [ ] **Arxiv Crawl**: placeholder table of papers, “Last crawled” note
- [ ] **Cool Facts**: static list or random fact generator script
- [ ] **Donate**: donate button/link with blinking border

## 7. Testing & Deployment
- [ ] Test visual layout and functionality in multiple browsers
- [ ] Validate links and console for JS errors
- [ ] Deploy to hosting (e.g. GitHub Pages, Netlify)

## 8. Future Enhancements
- [ ] Add guestbook with JSON storage or backend
- [ ] Integrate visitor counter or flat-file log
- [ ] Animate cursors or add interactive easter eggs
  
---
*Update this file as tasks progress.*