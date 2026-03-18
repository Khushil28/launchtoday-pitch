import os
import re

file_path = r'e:\Code\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract styles
style_matches = re.finditer(r'<style\b[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
css_content = ''
for match in style_matches:
    css_content += match.group(1) + '\n'

# Replace styles with link (keep indent if possible, but we just replace the tag)
first_style = True
def style_repl(match):
    global first_style
    if first_style:
        first_style = False
        return '<link rel="stylesheet" href="styles.css">'
    return ''
content = re.sub(r'<style\b[^>]*>.*?</style>', style_repl, content, flags=re.DOTALL | re.IGNORECASE)

# Extract typical scripts (without src)
script_matches = re.finditer(r'<script(?![^>]*\bsrc\b)[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
js_content = ''
for match in script_matches:
    js_content += match.group(1) + '\n'

# Replace typical scripts
first_script = True
def script_repl(match):
    global first_script
    if first_script:
        first_script = False
        return '<script src="script.js"></script>'
    return ''
content = re.sub(r'<script(?![^>]*\bsrc\b)[^>]*>.*?</script>', script_repl, content, flags=re.DOTALL | re.IGNORECASE)

# Create refactored directory
out_dir = r'e:\Code\refactored'
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(content)

with open(os.path.join(out_dir, 'styles.css'), 'w', encoding='utf-8') as f:
    f.write(css_content.strip())

with open(os.path.join(out_dir, 'script.js'), 'w', encoding='utf-8') as f:
    f.write(js_content.strip())

print("Refactoring complete. Files created in e:\\Code\\refactored\\")
