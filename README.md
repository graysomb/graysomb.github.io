# Retro 2000s Style Personal Website

This is a static personal website styled with an early-2000s aesthetic. It features a range of sections—Projects, Work, Stories, Essays, Cringe, Arxiv Crawl, Cool Facts, and Donate—plus retro design touches like pixel fonts, marquee effects, blinking borders, and fake “meme” ads.

## Features
- Responsive retro-inspired layout with tiled backgrounds and neon borders
- Global navigation bar with active-page highlighting and a visitor counter (via countapi.xyz)
- Fake meme ad rotator, dynamically loading images from `images/ads/` using a generated manifest (`js/ads.json`)
- Projects section with a Random Code Generator (JavaScript) and dedicated subpage
- Work, Stories, Essays, Cringe sections with stylized lists and decorative boxes
- Arxiv Crawl section listing papers with individual detail pages under `arxiv/`
- Cool Facts section that displays a randomized list of fun facts
- Donate page with a blinking “Donate Now” button
- Git-based CMS integration (Netlify CMS) for in-browser content editing
- Eleventy (11ty) static site generator for Markdown-based content and templates
- CI/CD via GitHub Actions to build and deploy the site to GitHub Pages

## Tech Stack
- HTML, CSS, JavaScript
- [Eleventy](https://www.11ty.dev/) as the static site generator
- [Netlify CMS](https://www.netlifycms.org/) for content management
- Python script for generating ads manifest (`scripts/generate_ads_manifest.py`)
- GitHub Actions for automated builds and deployment

## Getting Started
### Prerequisites
- Node.js (>=14)
- npm (>=6)
- Python 3 (for ads manifest script)

### Local Development
1. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/your-user/your-repo.git
   cd your-repo
   npm install
   ```
2. Generate the ads manifest:
   ```bash
   python3 scripts/generate_ads_manifest.py
   ```
3. Start the development server (Eleventy):
   ```bash
   npm run dev
   ```
4. Open `http://localhost:8080` in your browser.

### Building for Production
```bash
npm run build
```  
This will output the static site to the `_site/` directory.

## Content Editing (Netlify CMS)
1. Create a GitHub OAuth App and note the Client ID.
2. In `admin/config.yml`, set:
   ```yaml
   backend:
     name: github
     repo: your-user/your-repo
     branch: main
     client_id: YOUR_GITHUB_OAUTH_CLIENT_ID
   ```
3. Deploy to GitHub Pages, then visit `https://<your-user>.github.io/<your-repo>/admin/` to log in and edit content via a friendly UI.

## CI/CD & Deployment
The `.github/workflows/deploy.yml` GitHub Action will:
1. Check out the code on pushes to `main`
2. Install Node.js and dependencies
3. Run `npm run build` (Eleventy)
4. Deploy the `_site/` directory to the `gh-pages` branch using `peaceiris/actions-gh-pages`

After the action runs, configure your repository's GitHub Pages settings:
- Go to **Settings → Pages**
- Under **Source**, select **Branch: gh-pages**, **Folder: /**
- Save—your site will then be served from the `gh-pages` branch.

## Directory Structure
```
├── admin/                  # Netlify CMS admin UI and config
├── arxiv/                  # Arxiv detail pages
├── content/                # Markdown source for Eleventy
│   ├── _includes/          # Eleventy layout templates
│   ├── home.md
│   ├── projects.md
│   └── ...                 # other page.md files
├── css/style.css           # Global styles
├── images/ads/             # Meme ad assets
├── js/                     # Site and generator scripts
├── projects/               # Project subpages
├── scripts/                # Helper scripts (ads manifest)
├── .eleventy.js            # Eleventy config
├── package.json            # NPM dependencies & scripts
├── README.md               # Project overview
└── .github/workflows/      # CI/CD definitions
```  

## Contributing
Feel free to open issues or submit PRs to improve content, styling, or functionality. For editorial contributions, use the CMS at `/admin/`.