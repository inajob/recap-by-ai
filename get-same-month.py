# 日記からLLMに食わせるデータを作る 

import requests
import re
import sys
from datetime import date, timedelta
sys.stdout.reconfigure(encoding='utf-8')

url = "https://inline.inajob.freeddns.org/page/twitter-5643382"

def getPages():
  response = requests.get(url)
  obj = None
  try:
    obj = response.json()
  except Exception as e:
    pass
  body = []
  if(obj and obj.get("keywords")):
    body = obj["keywords"]
  return body


def getPage(title):
  u = url + "/" + title
  response = requests.get(u)
  obj = None
  try:
    obj = response.json()
  except Exception as e:
    pass
  body = ""
  if(obj and obj.get("body")):
    body = obj["body"]
  return body

def dumpPage(title, body):
  if len(body) == 0:
    return
  if len(body) > 1000:
    body = body[:1000]
  print()
  print("===")
  print()
  print("# " + title)
  print(body)
  print()

# --- Argument Parsing ---
mode = 'search' # Default mode
if '--deep' in sys.argv:
    mode = 'deep'

# --- Configuration based on mode ---
if mode == 'deep':
    date_range_start = -5
    deep_dive_enabled = True
    print("Running in Deep Dive mode (5 days before to 10 days after, with link following)")
else: # 'search' mode
    date_range_start = -10
    deep_dive_enabled = False
    print("Running in Diary Search mode (10 days before to 10 days after, no link following)")


# --- Main Logic ---
print("Fetching master list of pages...")
all_page_titles = getPages()
if not isinstance(all_page_titles, list):
    print("Error: getPages() did not return a list. Exiting.")
    sys.exit(1)
print(f"Found {len(all_page_titles)} total pages.")

visited = set()
today = date.today()
for y in range(2004, today.year + 1):
  for i in range(date_range_start, 11):
    try:
        d = date(y, today.month, today.day) + timedelta(days=i)
        date_string_to_find = d.strftime("%Y-%m-%d")
    except ValueError: # 2/29など、該当年には存在しない日付の場合
        continue
    
    # Find all titles in the master list that contain the generated date string.
    matching_titles = [t for t in all_page_titles if date_string_to_find in t]

    # Process each of the matching titles.
    for title in matching_titles:
        if title in visited:
            continue
        
        visited.add(title)
        body = getPage(title)
        dumpPage(title, body)
        
        # --- Conditional Link Following ---
        if deep_dive_enabled:
            matches_l1 = re.findall(r'\[([^\]]+)\]', body)
            for w_l1 in matches_l1: # level1
                if w_l1 in visited:
                  continue
                visited.add(w_l1)
                title_l1 = w_l1
                body_l1 = getPage(title_l1)
                dumpPage(title_l1, body_l1)
                
                # Level 2 deep dive
                matches_l2 = re.findall(r'\[([^\]]+)\]', body_l1)
                for w_l2 in matches_l2: # level2
                  if w_l2 in visited:
                    continue
                  visited.add(w_l2)
                  title_l2 = w_l2
                  body_l2 = getPage(title_l2)
                  dumpPage(title_l2, body_l2)
