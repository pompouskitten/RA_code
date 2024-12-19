import re, sys

def get_data(text):
    pattern = r"Topic (\d+) \[Count: (\d+)\]: (.+)"

    match = re.match(pattern, text)

    if match:
        topic_number = int(match.group(1))
        count = int(match.group(2))
        words = [word.strip() for word in match.group(3).split('|')]

        return topic_number, count, words
    else:
        return None, None, None

def get_topic_names():
    print("Enter multiple lines (press Ctrl+D to stop):")
    lines = sys.stdin.read().splitlines()
    names = [line for line in lines if line.startswith("Topic")]
    return [name.split(":")[1].strip() for name in names]

def main():
    files_list = ["pre", "during", "post"]

    for f in files_list:
        print(f"File: {f}")
        names = get_topic_names()
        with open(f"log/{f}_model.txt", "r") as log, open(f"{f.removesuffix(".csv")}_topics.csv", "w") as sheet:
            sheet.write("Topic ID,Topic Names,Count,Words\n")
            data = log.read().splitlines()
            for line in range(len(data)):
                topic_number, count, words = get_data(data[line])
                print(f"Topic {topic_number} - {names[line]}: {", ".join(words)}")
                sheet.write(f"{topic_number},{names[line]},{count},{' | '.join(words)}\n")
            

if __name__ == "__main__":
    main()