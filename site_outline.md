# Site Outline

Here’s a high-level roadmap for your “early-2000s meme-ad” personal site. You can adapt as you go, but this should give you a clear structure and step-by-step tasks:

## 1. Site Architecture & File Layout
- root/
  - index.html ← Homepage (overview & navigation)
  - projects.html ← “Projects” page (will host your random code generator)
  - work.html
  - stories.html
  - essays.html
  - cringe.html
  - arxiv.html ← “Arxiv Crawl”
  - cool-facts.html
  - donate.html
  - css/
    - style.css
  - js/
    - main.js ← shared scripts (e.g. fake-ad rotator)
    - code-generator.js ← your existing random code generator logic
  - images/ads/ ← “meme ad” assets (e.g. Apple Cabin Foods, pixel banners)
  - assets/
    - favicon.ico, visitor-counter script, guestbook if desired

## 2. Aesthetic & “Early-2000s” Design Notes
- Backgrounds: make the backround a big pixel art image of a convenience store or bodega, like your view as you walk in
- Fonts: bitmap/pixel fonts (e.g. “Press Start 2P”) + system fonts (Georgia, Courier).
- Layout: tables or floated DIVs, “hit counter” in footer, guestbook link.
- Colors: bright/neon borders, gradient bars, “under construction” sign.
- Blinky elements: marquee, CSS animations (e.g. button hover glows).

## 3. Global Navigation
- A persistent nav bar or sidebar on every page with links to all sections.
- Highlight current page.
- Below nav, a “fake ad” slot (200×200px or leaderboard 728×90) that rotates through your meme images.

## 4. Page-by-Page Outline
- **Homepage** (index.html)
  - Brief intro "Welcome Traveler!”
  - Large pixel headline + flashing “Under Construction” GIF
  - Nav links + a 468×60 “meme ad” at top
  - Featured snippet: “Check out my Projects!” button
  - add a pixel art style bonfire from dark souls that says rest and relax

- **Projects** (projects.html)
  - Title banner “Dreams Made REAL” in a stylized table header
  - subtitle "what will survive its confrontation with reality?"
  - Embed your existing random code generator applet:
    - Include code-generator.js and a container DIV
    - “Generate Random Code!” button stylized with pixel borders
  - Below, stub links or thumbnails for future projects

- **Work** (work.html)
  - subtitle "gotta eat!"
  - List of jobs/roles, each in a bordered box
  - add faux “Employee of the Month” badge

- **Stories, Essays, Cringe** (stories.html, essays.html, cringe.html)
  - "By entering you agree to only make fun of me if it is constructive"
  - Each: an index of posts, clickable titles
  - Render content in old-school `<div class="content-box">` with lorem ipsum or real entries

- **Arxiv Crawl** (arxiv.html)
  - "Knowledge is for everyone!"
  - Short description, “Last crawled: [date]”
  - Table of recent papers with links
  - Faux “Sponsored by Cabin Foods” ad banner

- **Cool Facts** (cool-facts.html)
  - curated list
  - Use JS to rotate facts every page load

- **Music** (music.html)
  - list of music to be played
  - host files and have webplayer
  - add a cool little visualization! maybe like little bugs that jump everytime there is a beat

- **spells** (spells.html)
  - "Use with cuation"
  - have a little alter you can sacrifice a curated list of things from. for example on of the things would be "a grain of salt from the brow of ambition
  - generates a idiom, piece of advice, or quote

- **Donate** (donate.html)
  - “Money isnt real anyway” text in Courier
  - Link to PayPal or crypto wallet
  - Animated “Donate” button (blinking border)

## 5. Fake “Meme Ad” System
- In `js/main.js`, define an array of ad image filenames + dummy URLs.
- On page load, randomly pick one and inject into `<div id="sidebar-ad">`.
- Keep ad assets in `images/ads/` (e.g. apple-cabin-1.gif, pixel-cornflakes.png).

## 6. Core CSS (css/style.css)
- Reset defaults lightly, then
- `body { background: url('../images/noise-tile.gif'); color: #00ff00; font-family: 'Press Start 2P', monospace; }`
- `.nav { border: 2px solid magenta; background: #000; }`
- `.ad-box { width:200px; height:200px; border: 3px dotted yellow; margin:10px auto; }`
- tables for layout where needed, plus a `<marquee>` fallback

## 7. JavaScript Enhancements
- `code-generator.js` → your existing generator, moved from index.html to projects.html
- `main.js` →
  - Ad rotator
  - Visit counter (or embed a 3rd-party JS snippet)
  - Marquee fallback polyfill

## 8. Development Steps
1. Scaffold file structure and create empty HTML pages with persistent nav.
2. Copy your random code generator out of index.html into projects.html and wire up the JS file.
3. Build style.css: set global styles, nav, ad-box, content-box.
4. Implement the fake-ad rotator in main.js and test on every page.
5. Fill in placeholder content on each page.
6. Gather or mock up “meme ads” and place them in images/ads/.
7. Test across browsers, tweak marquee/CSS for the right retro feel.
8. Deploy (GitHub Pages, Netlify, etc.).

## 9. Future Enhancements (Optional)
- Guestbook with form + JSON storage
- Visitor log & counter (flat-file or simple backend)
- Animated cursors, “under construction” gifs, hit counters

---
Start by carving out your nav and scoping the Projects page; once the shell is in place you can flesh out the rest one by one. Have fun channeling that ’00s nostalgia!