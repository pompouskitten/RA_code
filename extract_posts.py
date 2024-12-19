import json
import csv
import sys
from datetime import datetime

def process_jsonl_to_csv(jsonl_file, csv_file):
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Title', 'Body', 'Date', 'Time', 'Subreddit', 'Url', 'Upvotes', 'Awards', 'Comments'])
            writer.writeheader()
            count = 0
            removed_count = 0
            for line in file:
                line = line.strip()
                if line:
                    count += 1
                    data = json.loads(line)
                    if data['selftext'] == '[removed]' or data['selftext'] == '[deleted]':
                        removed_count += 1
                        continue
                    dt_object = datetime.fromtimestamp(data['created_utc'])
                    try:
                        subreddit = data['subreddit']
                    except KeyError:
                        subreddit = data['subreddit_name_prefixed']
                    try:
                        awards = len(data['all_awardings'])
                    except KeyError:
                        awards = 0
                    data_dict = {
                        "ID": data['id'],
                        "Title": data['title'],
                        "Body": data['selftext'].replace('\n', ' '),
                        "Date": dt_object.strftime('%Y-%m-%d'),
                        "Time": dt_object.strftime('%H:%M:%S'),
                        "Subreddit": subreddit,
                        "Url": data['permalink'],
                        "Upvotes": data['ups'],
                        "Awards": awards,
                        "Comments": data['num_comments']
                    }
                    writer.writerow(data_dict)
    
    print(f"Processed {count} posts from {jsonl_file}")
    print(f"Removed {removed_count} posts from {jsonl_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <jsonl_file_1> <jsonl_file_2> ... <jsonl_file_n>")
        sys.exit(1)

    for jsonl_file in sys.argv[1:]:
        print(f"Processing {jsonl_file} ...")
        csv_file = jsonl_file.replace('.jsonl', '.csv')
        process_jsonl_to_csv(jsonl_file, csv_file)
