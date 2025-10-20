import util
import sys
import os
import argparse

sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser(description='Chat with a model using content from files.')
parser.add_argument('filenames', metavar='file', type=str, nargs='+',
                    help='files to be used as context')
parser.add_argument('-t', '--temperature', type=float, default=0.0,
                    help='temperature for the model (default: 0.0)')

args = parser.parse_args()

all_content = []

for filename in args.filenames:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            all_content.append(f.read())
    except FileNotFoundError:
        print(f"Warning: File not found at {filename}. Skipping.")
    except Exception as e:
        print(f"Warning: Error reading file {filename}: {e}. Skipping.")

combined_content = "\n".join(all_content)

if combined_content:
    res = util.chat(combined_content, temperature=args.temperature)
    print(res.text)
else:
    print("All specified files were empty or could not be read.")