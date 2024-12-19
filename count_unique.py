import json, sys, csv
from tqdm import tqdm
from datetime import datetime

def unique_files(files):
    print(f"Finding unique users for {', '.join(files)}")
    users = set()
    total_count = 0
    unique_count = 0

    for file in files:
        with open(file, 'r') as f:
            for line in tqdm(f):
                line = line.strip()
                if line:
                    data = json.loads(line)
                    try:
                        author = data['author_fullname']
                        if author not in users:
                            users.add(author)
                            unique_count += 1

                        total_count += 1
                    except KeyError:
                        pass

    print(f"Total posts: {total_count}")
    print(f"Unique users: {unique_count}")
    print("")


def unique_new(first, second):
    print(f"Finding unique users for {', '.join(first)}")
    print(f"Finding new unique users for {', '.join(second)}")
    
    initial_users = set()
    new_users = set()
    total_count_initial = 0
    total_count_new = 0
    unique_count_initial = 0
    unique_count_new = 0
    retained_users = set()


    for file in first:
        with open(file, 'r') as f:
            for line in tqdm(f):
                line = line.strip()
                if line:
                    data = json.loads(line)
                    try:
                        author = data['author_fullname']
                        if author not in initial_users:
                            initial_users.add(author)
                            unique_count_initial += 1

                        total_count_initial += 1
                    except KeyError:
                        pass

    for file in second:
        with open(file, 'r') as f:
            for line in tqdm(f):
                line = line.strip()
                if line:
                    data = json.loads(line)
                    try:
                        author = data['author_fullname']
                        if author not in initial_users and author not in new_users:
                            new_users.add(author)
                            unique_count_new += 1
                        if author in initial_users:
                            retained_users.add(author)

                        total_count_new += 1
                    except KeyError:
                        pass

    print(f"Total posts in initial files: {total_count_initial}")
    print(f"Unique users in initial files: {len(initial_users)}")
    print(f"Total posts in new files: {total_count_new}")
    print(f"New unique users in new files: {len(new_users)}")
    print(f"Old unique users in new files: {len(retained_users)}")
    print("")
    print(f"Testing: {len(initial_users)} + {len(new_users)} = {len(initial_users.union(new_users))}")



def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <1: Find Unique; 2: Find New> <file1> <file2> ... | <fileA> <fileB> ...")
        sys.exit(1)

    if int(sys.argv[1]) == 1:
        files = sys.argv[2:]
        unique_files(files)
    elif int(sys.argv[1]) == 2:
        first = []
        second = []
        change = False
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "|":
                change = True
                continue
            if not change:
                first.append(sys.argv[i])
            else:
                second.append(sys.argv[i])
        unique_new(first, second)


if __name__ == "__main__":
    main()
