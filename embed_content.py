import sys
import json
import re
sys.stdout.reconfigure(encoding='utf-8')

# Read the extracted lesson contents
with open(r"C:\Users\Madiyar\Desktop\клод проекты\Атырау\lesson_contents.json", 'r', encoding='utf-8') as f:
    contents = json.load(f)

# Read the HTML file
html_path = r"C:\Users\Madiyar\Desktop\клод проекты\Атырау\index.html.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Build the LESSON_CONTENTS array as JS
js_lines = ["const LESSON_CONTENTS = ["]
for i, content in enumerate(contents):
    # Escape for JS string: backslashes, backticks, ${
    escaped = content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    js_lines.append(f"  `{escaped}`,")
js_lines.append("];")
js_content_block = "\n".join(js_lines)

# Insert after LESSONS array closing
# Find the line "const TOTAL_LESSONS" and insert before it
marker = "const TOTAL_LESSONS"
if marker in html:
    html = html.replace(marker, js_content_block + "\n\n" + marker)
    print(f"Inserted LESSON_CONTENTS array ({len(contents)} items, {len(js_content_block)} chars)")
else:
    print("ERROR: Could not find marker 'const TOTAL_LESSONS'")
    sys.exit(1)

# Write back
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! HTML file updated.")
