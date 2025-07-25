# Project Tasks
This file tracks tasks needed to integrate a Git-based CMS (Netlify CMS) for easier content editing.

## 1. Choose CMS Platform
- [x] Decide on a Git-based CMS (e.g. Netlify CMS, Forestry, TinaCMS)
- [x] Install CMS dependencies (e.g. `npm install netlify-cms-app`)

## 2. Add Admin UI
- [x] Create `admin/index.html` to initialize Netlify CMS
- [x] Create `admin/config.yml` with:
  - `backend`: repository & branch info
  - `media_folder` & `public_folder` settings
  - Collections for pages (home, projects, work, stories, essays, cringe, arxiv, cool-facts, donate)
  - Register a GitHub OAuth App and configure `client_id` in `admin/config.yml` for GitHub Pages backend

## 3. Content Structure
- [ ] Create `content/` directory to hold Markdown files
- [ ] Convert existing HTML pages to Markdown with front matter:
  - `home.md`, `projects.md`, `work.md`, `stories.md`, `essays.md`,
    `cringe.md`, `arxiv.md`, `cool-facts.md`, `donate.md`

## 4. Templates & Build
- [ ] Install & configure a static site generator (Eleventy, Hugo, or Jekyll)
- [ ] Create layout templates to wrap Markdown content with nav, ads, and footer
- [ ] Update `package.json` scripts for local dev (`npm run dev`) and production build (`npm run build`)

## 5. CI/CD Integration
- [ ] Add `netlify.toml` or GitHub Actions to run the build on each commit
- [ ] Ensure the `/admin` route is served and accessible

## 6. Testing & Documentation
- [ ] Test editing and publishing content from the CMS UI
- [ ] Document the CMS workflow, file locations, and editorial process for contributors

## 7. Future Enhancements
- [ ] Enable editorial workflow with drafts & previews
- [ ] Add custom widgets or validation rules in `config.yml`