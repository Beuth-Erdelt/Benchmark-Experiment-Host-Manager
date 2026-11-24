import os
import re

# Set your directory containing .md files
md_directory = 'docs'
logs_directory = 'logs_tests'

r"""
# Regular expression to match: <filename>.log\n```bash\n...``` blocks
pattern = re.compile(r'(?P<logfile>[\w\-.\/]+\.log)\n```bash\n(.*?)\n```', re.DOTALL)

for filename in os.listdir(md_directory):
    if filename.endswith('.md'):
        print(f"Reading {filename}")
        filepath = os.path.join(md_directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        def replace_block(match):
            log_marker = match.group('logfile')
            base_name = os.path.splitext(log_marker)[0]
            summary_filename = f"{base_name}_summary.txt"
            summary_path = os.path.join(logs_directory, summary_filename)
            print(f"->Looking for {summary_path}")
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as log_f:
                    log_content = log_f.read().strip()
                return f"{log_marker}\n```bash\n{log_content}\n```"
            else:
                print(f"Warning: Summary file not found - {summary_path}")
                return match.group(0)  # return original if file is missing
        new_content = pattern.sub(replace_block, content)
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)

"""


# Regular expression to match:
# <details>\n<summary>Show <a href="<url>">...</a></summary>\n\n```markdown\n...```\n\n</details>
pattern = re.compile(
    r'<details>\n<summary>Show <a href="(?P<url>[^"\s]+)"(?P<link_attrs>[^>]*)>(?P<logfile>[\w\-.\/]+\.log)</a></summary>\n\n```markdown\n(.*?)\n```\n\n</details>',
    re.DOTALL,
)

missing_summary_files = []
# A NUL byte in a summary means its log was written by two processes at once (the file was
# truncated while a run still wrote at its old offset); such a summary is never copied.
damaged_summary_files = []

for filename in os.listdir(md_directory):
    if filename.endswith('.md'):
        print(f"Reading {filename}")
        filepath = os.path.join(md_directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        def replace_block(match):
            log_marker = match.group('logfile')
            link_url = match.group('url')
            link_attrs = match.group('link_attrs')
            base_name = os.path.splitext(log_marker)[0]
            summary_filename = f"{base_name}_summary.md"
            summary_path = os.path.join(logs_directory, summary_filename)
            print(f"->Looking for {summary_path}")
            if os.path.exists(summary_path):
                # utf-8-sig drops a BOM (e.g. from PowerShell 5.1) instead of embedding U+FEFF in the docs
                with open(summary_path, 'r', encoding='utf-8-sig') as log_f:
                    log_content = log_f.read().strip()
                if '\x00' in log_content:
                    print(f"Error: Summary file contains NUL bytes, not copied - {summary_path}")
                    damaged_summary_files.append((summary_path, log_content.count('\x00')))
                    return match.group(0)  # keep the block as it is
                return (
                    f'<details>\n<summary>Show <a href="{link_url}"{link_attrs}>{log_marker}</a></summary>\n\n'
                    f'```markdown\n{log_content}\n```\n\n</details>'
                )
            else:
                print(f"Warning: Summary file not found - {summary_path}")
                missing_summary_files.append(summary_path)
                return match.group(0)  # return original if file is missing
        new_content = pattern.sub(replace_block, content)
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)



if missing_summary_files:
    print("\n\n\nMissing summary files\n\n\n")
    for path in sorted(set(missing_summary_files)):
        print(path)

if damaged_summary_files:
    print("\n\n\nSummary files with NUL bytes (not copied; rerun the experiment)\n\n\n")
    for path, count in sorted(set(damaged_summary_files)):
        print(f"{path}: {count} NUL bytes")

print("\n\n\nShow all failed tests\n\n\n")

from pathlib import Path

# Define the target directory
docs_folder = Path("docs")

# Search through all .md files recursively
for md_file in docs_folder.rglob("*.md"):
    with md_file.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if "TEST failed: " in line:
                print(f"{md_file}:{line_number}: {line.strip()}")

# Pages that still contain NUL bytes, e.g. from a damaged summary copied before this check existed
damaged_pages = []
for md_file in sorted(docs_folder.rglob("*.md")):
    data = md_file.read_bytes()
    if b'\x00' in data:
        line_number = data[:data.index(b'\x00')].count(b'\n') + 1
        count = data.count(b'\x00')
        damaged_pages.append(f"{md_file}: {count} NUL bytes from line {line_number}")
if damaged_pages:
    print("\n\n\nPages with NUL bytes\n\n\n")
    for page in damaged_pages:
        print(page)

if damaged_summary_files or damaged_pages:
    raise SystemExit(1)
