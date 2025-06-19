import os
import re

# Set your directory containing .md files
md_directory = 'docs'
logs_directory = 'logs_tests'

"""
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
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

"""


# Regular expression to match: <filename>.log\n```bash\n...``` blocks
pattern = re.compile(r'(?P<logfile>[\w\-.\/]+\.log)\n```markdown\n(.*?)\n```', re.DOTALL)

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
                return f"{log_marker}\n```markdown\n{log_content}\n```"
            else:
                print(f"Warning: Summary file not found - {summary_path}")
                return match.group(0)  # return original if file is missing
        new_content = pattern.sub(replace_block, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)



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
