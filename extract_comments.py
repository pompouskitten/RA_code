import json
import csv
import sys
from tqdm import tqdm
from datetime import datetime

def get_removed_ids(posts_file):
    removed_ids = set()
    with open(posts_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())
            if data['selftext'] in ['[removed]', '[deleted]', '']:
                removed_ids.add(data['id'])
    return removed_ids

def process_comments_jsonl_to_csv(jsonl_file, csv_file, removed_ids):
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Body', 'Date', 'Time', 'Subreddit', 'Url', 'Parent_ID', 'Upvotes', 'Awards'])
            writer.writeheader()
            count = 0
            removed_count = 0
            removed_count_parent = 0
            for line in tqdm(file):
                line = line.strip()
                if line:
                    count += 1
                    data = json.loads(line)
                    dt_object = datetime.fromtimestamp(data['created_utc'])
                    if data['body'] in ['[removed]', '[deleted]', '']:
                        removed_count += 1
                        continue
                    try:
                        subreddit = data['subreddit']
                    except KeyError:
                        subreddit = data['subreddit_name_prefixed']
                    try:
                        awards = len(data['all_awardings'])
                    except KeyError:
                        awards = 0
                        
                    parent_id = data['parent_id'].split('_')[1] if len(data['parent_id'].split('_')) == 2 else data['parent_id']
                    
                    if parent_id in removed_ids:
                        removed_count_parent += 1
                        continue

                    data_dict = {
                        "ID": data['id'],
                        "Body": data['body'].replace('\n', ' '),
                        "Date": dt_object.strftime('%Y-%m-%d'),
                        "Time": dt_object.strftime('%H:%M:%S'),
                        "Subreddit": subreddit,
                        "Url": data['permalink'],
                        "Parent_ID": data['parent_id'],
                        "Upvotes": data['ups'],
                        "Awards": awards
                    }
                    writer.writerow(data_dict)
    
    print(f"Total comments processed: {count} from {jsonl_file}")
    print(f"Total comments removed: {removed_count} from {jsonl_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <jsonl_file_1> <jsonl_file_2> ... <jsonl_file_n>")
        sys.exit(1)
    
    files = sys.argv[1:]
    
    for file in files:
        print(f"Processing {file['comments']} ...")
        csv_file = file['comments'].replace('.jsonl', '.csv')
        removed_ids = get_removed_ids(file['posts'])
        process_comments_jsonl_to_csv(file['comments'], csv_file, removed_ids)
