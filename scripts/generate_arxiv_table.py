#!/usr/bin/env python3
"""
Script to auto-generate the paper table in arxiv.html based on HTML files in the arxiv/ directory.
Reads each .html file in arxiv/, extracts the title and authors,
and updates the <tbody> section of arxiv.html with the current papers.
"""
import os
import re
import sys
import datetime

def main():
    # Locate project root and relevant paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    arxiv_dir = os.path.join(project_root, 'arxiv')
    arxiv_html_path = os.path.join(project_root, 'arxiv.html')

    # Ensure paths exist
    if not os.path.isdir(arxiv_dir):
        print(f"Error: arxiv directory not found at {arxiv_dir}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(arxiv_html_path):
        print(f"Error: arxiv.html not found at {arxiv_html_path}", file=sys.stderr)
        sys.exit(1)

    # Gather paper entries
    entries = []
    for fname in sorted(os.listdir(arxiv_dir)):
        if not fname.endswith('.html'):
            continue
        file_path = os.path.join(arxiv_dir, fname)
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
        # Extract title from <h1>
        m_title = re.search(r'<h1>(.*?)</h1>', content, re.S)
        title = m_title.group(1).strip() if m_title else ''
        # Extract authors from <strong>Authors:</strong>
        m_auth = re.search(r'<strong>Authors:</strong>\s*(.*?)</p>', content, re.S)
        authors = m_auth.group(1).strip() if m_auth else ''
        entries.append((fname, title, authors))

    # Read arxiv.html and replace <tbody> content
    with open(arxiv_html_path, encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_tbody = False
    for line in lines:
        # Update last-crawled date
        if 'id="last-crawled"' in line:
            today = datetime.date.today().isoformat()
            line = re.sub(
                r'(<span id="last-crawled">)(.*?)(</span>)',
                f"\\g<1>{today}\\g<3>",
                line
            )
            new_lines.append(line)
            continue
        # Replace table body with generated entries
        if '<tbody>' in line and not in_tbody:
            new_lines.append(line)
            indent = line[:line.index('<tbody>')]
            row_indent = indent + '  '
            cell_indent = indent + '    '
            # Generate rows for each entry
            for fname, title, authors in entries:
                new_lines.append(f"{row_indent}<tr>\n")
                new_lines.append(f"{cell_indent}<td>{title}</td>\n")
                new_lines.append(f"{cell_indent}<td>{authors}</td>\n")
                link = os.path.join('arxiv', fname)
                paper_id = os.path.splitext(fname)[0]
                new_lines.append(f"{cell_indent}<td><a href=\"{link}\">arXiv:{paper_id}</a></td>\n")
                new_lines.append(f"{row_indent}</tr>\n")
            in_tbody = True
            continue
        if in_tbody:
            # Skip existing rows until closing tag
            if '</tbody>' in line:
                new_lines.append(line)
                in_tbody = False
            continue
        new_lines.append(line)

    # Write updated content back to arxiv.html
    with open(arxiv_html_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Updated {len(entries)} entries in {arxiv_html_path}")

if __name__ == '__main__':
    main()