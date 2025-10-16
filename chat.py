import util
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

if len(sys.argv) < 2:
    print("Usage: python chat.py <file1> <file2> ...")
    sys.exit(1)

filenames = sys.argv[1:]
all_content = []

for filename in filenames:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            all_content.append(f.read())
    except FileNotFoundError:
        print(f"Warning: File not found at {filename}. Skipping.")
    except Exception as e:
        print(f"Warning: Error reading file {filename}: {e}. Skipping.")

combined_content = "\n".join(all_content)

if combined_content:
    res = util.chat(combined_content)
    print(res.text)
else:
    print("All specified files were empty or could not be read.")

