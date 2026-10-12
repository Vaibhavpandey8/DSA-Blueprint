import os
import re
import markdown

book_dir = os.path.dirname(os.path.abspath(__file__))
complete_md_path = os.path.join(book_dir, "THE_DSA_BLUEPRINT_COMPLETE_BOOK.md")

with open(complete_md_path, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Clean LaTeX math to readable Unicode
def clean_latex_math(text):
    text = re.sub(r'\\approx', '≈', text)
    text = re.sub(r'\\le', '≤', text)
    text = re.sub(r'\\ge', '≥', text)
    text = re.sub(r'\\rightarrow', '→', text)
    text = re.sub(r'\\implies', '⟹', text)
    text = re.sub(r'\\times', '×', text)
    text = re.sub(r'\\cdot', '·', text)
    text = re.sub(r'\\oplus', '⊕', text)
    text = re.sub(r'\\log', 'log', text)
    text = re.sub(r'\\sum_\{j=0\}\^\{i\}', 'Σ(j=0..i)', text)
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\$([^$]+)\$', r'<code>\1</code>', text)
    return text

cleaned_md = clean_latex_math(raw_md)

# Convert Markdown to HTML
html_body = markdown.markdown(
    cleaned_md,
    extensions=['tables', 'fenced_code', 'toc', 'sane_lists']
)

# Kindle-optimized HTML template (No web buttons, no broken external images, clean typography)
kindle_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The DSA Blueprint: 7 Pillars of Algorithmic Mastery in C++</title>
<style>
    body {{
        font-family: Georgia, serif;
        line-height: 1.6;
        color: #111111;
        margin: 5% 8%;
    }}
    h1 {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 1.8em;
        color: #0b3954;
        border-bottom: 2px solid #0070f3;
        padding-bottom: 6px;
        margin-top: 1.5em;
        page-break-before: always;
    }}
    h2 {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 1.35em;
        color: #1f4e78;
        border-bottom: 1px solid #dcdcdc;
        padding-bottom: 4px;
        margin-top: 1.3em;
    }}
    h3 {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 1.15em;
        color: #2b2b2b;
        margin-top: 1.1em;
    }}
    p, li {{
        font-size: 1.05em;
        line-height: 1.6;
    }}
    pre {{
        background-color: #f6f8fa;
        border: 1px solid #d0d7de;
        border-radius: 6px;
        padding: 12px;
        overflow-x: auto;
        font-family: "Courier New", Courier, monospace;
        font-size: 0.9em;
        line-height: 1.45;
        white-space: pre-wrap;
        word-break: break-word;
    }}
    code {{
        font-family: "Courier New", Courier, monospace;
        background-color: #f1f5f9;
        color: #0369a1;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 0.95em;
    }}
    pre code {{
        background-color: transparent;
        color: inherit;
        padding: 0;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
    }}
    th, td {{
        border: 1px solid #d0d7de;
        padding: 8px 10px;
        text-align: left;
    }}
    th {{
        background-color: #f0f4f8;
        font-weight: bold;
    }}
    blockquote {{
        border-left: 4px solid #0070f3;
        margin: 14px 0;
        padding: 8px 16px;
        background-color: #f8fafc;
        color: #334155;
        font-style: italic;
    }}
    .author-box, .copyright-box, .note-box {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 16px 0;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

output_html_path = os.path.join(book_dir, "THE_DSA_BLUEPRINT_KINDLE.html")
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(kindle_html)

print(f"Generated Kindle HTML: {output_html_path}")
