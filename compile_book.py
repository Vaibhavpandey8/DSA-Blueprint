import os

book_dir = os.path.dirname(os.path.abspath(__file__))

order = [
    "00_About_The_Author.md",
    "00_Table_Of_Contents.md",
    "00_Interview_Mental_Model.md",
    "01_Complexity_and_Decision_Matrix.md",
    "02_Two_Pointers_and_Sliding_Window.md",
    "03_Prefix_Sum_and_Difference_Array.md",
    "04_Binary_Search_Patterns.md",
    "05_Monotonic_Stack_and_Deque.md",
    "06_Linked_List_Patterns.md",
    "07_Trees_and_BST.md",
    "08_Heap_and_TopK.md",
    "09_Graph_Algorithms.md",
    "10_Shortest_Paths.md",
    "11_Dynamic_Programming.md",
    "12_Backtracking.md",
    "13_Bit_Manipulation.md",
    "14_Emergency_Cheat_Sheet.md",
]

compiled_content = []
compiled_content.append("# THE DSA BLUEPRINT: 7 PILLARS OF ALGORITHMIC MASTERY IN C++\n")
compiled_content.append("### Author: Vaibhav Pandey\n")
compiled_content.append("*(First Edition, 2026)*\n\n")
compiled_content.append('<div style="page-break-after: always;"></div>\n\n')

for filename in order:
    filepath = os.path.join(book_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            compiled_content.append(content)
            compiled_content.append('\n\n<div style="page-break-after: always;"></div>\n\n')

output_path = os.path.join(book_dir, "THE_DSA_BLUEPRINT_COMPLETE_BOOK.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(compiled_content))

print(f"Successfully compiled all 15 modules into: {output_path}")
print(f"Total size: {os.path.getsize(output_path)} bytes")
