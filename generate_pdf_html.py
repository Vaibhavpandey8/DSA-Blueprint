import os
import re
import markdown

book_dir = os.path.dirname(os.path.abspath(__file__))

order = [
    ("00_About_The_Author.md", "Front Matter: About the Author & Edition"),
    ("00_Table_Of_Contents.md", "Table of Contents"),
    ("00_Interview_Mental_Model.md", "Module 00: The 45-Minute Interview Mental Model"),
    ("01_Complexity_and_Decision_Matrix.md", "Module 01: Complexity Analysis & The Decision Matrix"),
    ("02_Two_Pointers_and_Sliding_Window.md", "Module 02: Two Pointers & Sliding Window Mastery"),
    ("03_Prefix_Sum_and_Difference_Array.md", "Module 03: Prefix Sums & Difference Arrays"),
    ("04_Binary_Search_Patterns.md", "Module 04: Fast Searching & Modified Binary Search"),
    ("05_Monotonic_Stack_and_Deque.md", "Module 05: Monotonic Stack & Deque"),
    ("06_Linked_List_Patterns.md", "Module 06: Linked Lists - The Pointer Mechanics"),
    ("07_Trees_and_BST.md", "Module 07: Binary Trees & BST Patterns"),
    ("08_Heap_and_TopK.md", "Module 08: Priority Queues & Heaps"),
    ("09_Graph_Algorithms.md", "Module 09: Graph Traversal & Connectivity"),
    ("10_Shortest_Paths.md", "Module 10: Shortest Paths & Minimum Spanning Tree"),
    ("11_Dynamic_Programming.md", "Module 11: Dynamic Programming - The Human Way"),
    ("12_Backtracking.md", "Module 12: Backtracking & State Space Search"),
    ("13_Bit_Manipulation.md", "Module 13: Bit Manipulation Hacks"),
    ("14_Emergency_Cheat_Sheet.md", "Bonus: 48-Hour Emergency Cheat Sheet"),
]

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
    text = re.sub(r'\$([^$]+)\$', r'<span class="math">\1</span>', text)
    return text

modules_html = []

for filename, title in order:
    filepath = os.path.join(book_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            content = clean_latex_math(content)
            rendered = markdown.markdown(
                content,
                extensions=['tables', 'fenced_code', 'nl2br', 'toc']
            )
            module_block = f"""
            <section class="chapter-section">
                {rendered}
            </section>
            """
            modules_html.append(module_block)

full_chapters_html = "\n".join(modules_html)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THE DSA BLUEPRINT: 7 PILLARS OF ALGORITHMIC MASTERY</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">
    <style>
        :root {{
            --primary: #0a2540;
            --accent: #0070f3;
            --text-dark: #1e293b;
            --text-muted: #475569;
            --border: #cbd5e1;
            --code-bg: #f8fafc;
            --code-border: #e2e8f0;
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        @page {{
            size: A4 portrait;
            margin: 16mm 14mm 16mm 14mm;
        }}

        @page :first {{
            margin: 0 !important;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-dark);
            line-height: 1.6;
            max-width: 860px;
            margin: 0 auto;
            padding: 0 20px;
            background: #ffffff;
        }}

        /* Print Specific Rules */
        @media print {{
            body {{
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
                font-size: 10pt;
                line-height: 1.55;
            }}
            .no-print {{
                display: none !important;
            }}
            .cover-page {{
                page-break-before: avoid !important;
                break-before: avoid !important;
                page-break-after: always !important;
                break-after: page !important;
                width: 100vw !important;
                height: 100vh !important;
                margin: 0 !important;
                padding: 0 !important;
                display: block !important;
                position: relative !important;
                overflow: hidden !important;
            }}
            .cover-page img {{
                width: 100vw !important;
                height: 100vh !important;
                max-width: none !important;
                max-height: none !important;
                object-fit: cover !important;
                display: block !important;
                margin: 0 !important;
                border-radius: 0 !important;
            }}
            .chapter-section {{
                page-break-before: always;
                break-before: page;
            }}
            h1, h2, h3 {{
                page-break-after: avoid !important;
                break-after: avoid !important;
            }}
            pre, blockquote {{
                page-break-inside: auto !important;
                break-inside: auto !important;
            }}
            table {{
                page-break-inside: auto !important;
                break-inside: auto !important;
            }}
            tr {{
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }}
            p, li {{
                orphans: 3;
                widows: 3;
            }}
            pre {{
                overflow: visible !important;
                white-space: pre-wrap !important;
                word-break: break-word !important;
                border: 1px solid #cbd5e1 !important;
                background-color: #f8fafc !important;
                color: #0f172a !important;
            }}
        }}

        /* Top Bar */
        .top-navbar {{
            position: sticky;
            top: 12px;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(8px);
            color: #ffffff;
            padding: 12px 20px;
            border-radius: 8px;
            margin: 16px 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        .brand-title {{
            font-weight: 700;
            font-size: 14.5px;
            letter-spacing: 0.5px;
        }}
        .brand-sub {{
            opacity: 0.7;
            font-size: 12.5px;
            margin-left: 10px;
        }}
        .action-btn {{
            background: #00b4d8;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .action-btn:hover {{
            background: #0096c7;
            transform: translateY(-1px);
        }}

        .instructions-banner {{
            background: #f0fdf4;
            border: 1px solid #86efac;
            color: #166534;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 13px;
            margin-bottom: 20px;
            line-height: 1.5;
        }}
        .instructions-banner strong {{
            color: #14532d;
        }}

        /* Cover Display Web Preview */
        .cover-page {{
            text-align: center;
            padding: 0;
            margin-bottom: 30px;
        }}
        .cover-page img {{
            max-width: 600px;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.25);
        }}

        /* Typography */
        h1 {{
            color: #0f172a;
            font-size: 1.85rem;
            font-weight: 800;
            margin-top: 18px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2.5px solid #00b4d8;
            letter-spacing: -0.5px;
        }}
        h2 {{
            color: #0f4c81;
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 18px;
            margin-bottom: 8px;
            padding-bottom: 4px;
            border-bottom: 1px solid var(--border);
        }}
        h3 {{
            color: #0f172a;
            font-size: 1.12rem;
            font-weight: 700;
            margin-top: 14px;
            margin-bottom: 6px;
        }}
        p, li {{
            color: #334155;
            font-size: 14.5px;
            line-height: 1.6;
            margin: 6px 0;
        }}
        ul, ol {{
            padding-left: 22px;
            margin: 6px 0;
        }}

        /* Author and Copyright Boxes on Page 2 */
        .author-box, .copyright-box, .note-box {{
            margin-bottom: 16px;
            padding: 12px 18px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }}
        .author-box h3, .copyright-box h3, .note-box h3 {{
            margin-top: 0;
            margin-bottom: 8px;
            color: #0f4c81;
        }}

        /* Math Span */
        .math {{
            font-family: 'JetBrains Mono', monospace;
            background: #f1f5f9;
            color: #0369a1;
            padding: 1px 5px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.95em;
        }}

        /* Blockquotes */
        blockquote {{
            margin: 12px 0;
            padding: 10px 18px;
            background: #f0f9ff;
            border-left: 4px solid #00b4d8;
            border-radius: 0 6px 6px 0;
            color: #0369a1;
            font-style: italic;
            font-size: 14px;
        }}
        blockquote p {{
            margin: 0;
            color: inherit;
        }}

        /* Code Blocks */
        pre {{
            background: #f8fafc !important;
            color: #0f172a !important;
            padding: 12px 16px !important;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12.5px;
            line-height: 1.48;
            margin: 12px 0;
            overflow-x: auto;
            border: 1px solid #cbd5e1;
        }}
        pre code {{
            background: transparent !important;
            color: inherit !important;
            padding: 0;
            font-size: inherit;
        }}
        code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12.5px;
            background: #f1f5f9;
            color: #0f172a;
            padding: 2px 5px;
            border-radius: 4px;
            font-weight: 500;
        }}

        /* Beautiful Compact Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0;
            font-size: 12.5px;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            border: 1px solid #cbd5e1;
        }}
        th, td {{
            padding: 6px 10px;
            text-align: left;
            border: 1px solid #e2e8f0;
            vertical-align: middle;
        }}
        th {{
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
            border-bottom: 2px solid #cbd5e1;
        }}
        tr:nth-child(even) td {{
            background: #f8fafc;
        }}

        hr {{
            border: 0;
            height: 1px;
            background: #e2e8f0;
            margin: 20px 0;
        }}
    </style>
</head>
<body>

    <div class="top-navbar no-print">
        <div>
            <span class="brand-title">📘 THE DSA BLUEPRINT</span>
            <span class="brand-sub">By Vaibhav Pandey • Modern C++ Edition</span>
        </div>
        <button class="action-btn" onclick="window.print()">🖨️ Export High-Res PDF</button>
    </div>

    <div class="instructions-banner no-print">
        💡 <strong>Pro-Tip for Clean PDF Export:</strong> Print dialog khulte hi <strong>"More settings"</strong> par click karein aur <strong>"Headers and footers"</strong> ko <u>UNCHECK</u> (band) kar dein. Isse page ke upar ka time/date aur niche ka file location URL completely hat jayega!
    </div>

    <div class="cover-page">
        <img src="assets/book_cover_fullpage.jpg" alt="THE DSA BLUEPRINT Full Page Cover">
    </div>

    {full_chapters_html}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-c.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-cpp.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            if (window.Prism) Prism.highlightAll();
        }});
    </script>
</body>
</html>
"""

html_path = os.path.join(book_dir, "THE_DSA_BLUEPRINT_PRINTABLE.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated fully optimized, publication-grade HTML: {html_path}")
print(f"Size: {os.path.getsize(html_path)} bytes")
