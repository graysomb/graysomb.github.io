#!/usr/bin/env python3
"""
Script to generate a new HTML page for an arXiv paper in the arxiv/ directory.
Usage: python3 scripts/generate_arxiv_page.py https://arxiv.org/abs/2507.11581
       or python3 scripts/generate_arxiv_page.py 2507.11581
Fetches metadata from the arXiv abstract page, extracts title, authors, and year,
and writes a new arxiv/{id}.html file using the site's retro template.
"""
import os
import re
import sys
import argparse

try:
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    sys.exit("Error: Unable to import urllib. Are you running Python 3?")

def main():
    parser = argparse.ArgumentParser(
        description="Generate an arXiv paper page in arxiv/ from a URL or ID."
    )
    parser.add_argument(
        "link",
        help="ArXiv URL (https://arxiv.org/abs/2507.11581) or ID (2507.11581)"
    )
    args = parser.parse_args()

    # Parse arXiv ID
    paper_id = args.link
    if paper_id.startswith("http"):
        m = re.search(r"arxiv\.org/abs/([^/#?]+)", paper_id)
        if not m:
            sys.exit(f"Error: could not parse arXiv ID from URL: {paper_id}")
        paper_id = m.group(1)

    url = f"https://arxiv.org/abs/{paper_id}"
    try:
        with urlopen(url, timeout=10) as res:
            html_data = res.read().decode("utf-8")
    except (HTTPError, URLError) as e:
        sys.exit(f"Error fetching {url}: {e}")

    # Extract metadata via citation meta tags
    m_title = re.search(r'<meta name="citation_title" content="(.*?)"', html_data)
    if not m_title:
        sys.exit("Error: title not found in page metadata.")
    title = m_title.group(1).strip()

    authors = re.findall(r'<meta name="citation_author" content="(.*?)"', html_data)
    if not authors:
        sys.exit("Error: no authors found in metadata.")
    # Format authors: first author, et al. if multiple
    if len(authors) > 1:
        authors_str = f"{authors[0]}, et al."
    else:
        authors_str = authors[0]

    m_date = re.search(r'<meta name="citation_date" content="(\d{4})/(\d{2})/(\d{2})"', html_data)
    year = m_date.group(1) if m_date else ""

    # Build HTML content
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title} - Retro Site</title>
  <link rel="stylesheet" href="../css/style.css">
  <script src="../js/main.js" defer></script>
</head>
<body>
  <nav>
    <ul>
      <li><a href="../index.html">Home</a></li>
      <li><a href="../projects.html">Projects</a></li>
      <li><a href="../work.html">Work</a></li>
      <li><a href="../stories.html">Stories</a></li>
      <li><a href="../essays.html">Essays</a></li>
      <li><a href="../cringe.html">Cringe</a></li>
      <li><a href="../arxiv.html" class="active">Arxiv Crawl</a></li>
      <li><a href="../cool-facts.html">Cool Facts</a></li>
      <li><a href="../donate.html">Donate</a></li>
      <li id="visitor-counter" class="visit-counter">Visits: <span id="visit-count">0</span></li>
    </ul>
  </nav>
  <div class="banner-ad">LEADERBOARD AD</div>
  <div id="sidebar-ad" class="ad-box"></div>
  <main>
    <h1>{title}</h1>
    <p><strong>Authors:</strong> {authors_str}</p>
    <p><strong>Year:</strong> {year}</p>
    <p><a href="../arxiv.html">&#8592; Back to Arxiv Crawl</a></p>
  </main>
</body>
</html>"""

    # Determine output path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    arxiv_dir = os.path.join(project_root, "arxiv")
    os.makedirs(arxiv_dir, exist_ok=True)
    out_path = os.path.join(arxiv_dir, f"{paper_id}.html")

    # Confirm overwrite if exists
    if os.path.exists(out_path):
        resp = input(f"{out_path} already exists. Overwrite? [y/N]: ")
        if resp.lower() != "y":
            print("Aborted.")
            sys.exit(1)

    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write(content)
    print(f"Generated {out_path}")


if __name__ == "__main__":
    main()