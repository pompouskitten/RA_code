import os, sys
from tqdm import tqdm
from nltk.tokenize import word_tokenize
import pandas as pd

keyword = "drugs"

def check_word_occurrences(csv_file, output_csv=None):
    if output_csv is None:
        output_csv = f"{keyword}/{csv_file.replace('.csv', f'_{keyword}.csv')}"
    
    in_csv_file = os.path.join("dataset", csv_file)
    
    word_dict = {}
    words_dict = {}
    with open(f'{keyword}.txt', 'r') as file:
        for line in file.readlines():
            line = line.removesuffix("\n")
            word = line.strip().lower()
            if " " in word:
                words_dict[word] = 0
            else:
                word_dict[word] = 0

    df = pd.read_csv(in_csv_file)
    
    def find_keywords(body):
        body = str(body).lower()
        try:
            body_tokens = word_tokenize(body)
        except Exception:
            return None
        found_words = []
        for word in words_dict:
            if word in body or f"{word}s" in body:
                found_words.append(word.title())
                words_dict[word] += 1
        for word in word_dict:
            if word in body_tokens or f"{word}s" in body_tokens:
                found_words.append(word.title())
                word_dict[word] += 1
        return ' | '.join(found_words) if found_words else None

    tqdm.pandas(desc="Finding keywords")
    df[keyword.title()] = df['Body'].progress_apply(find_keywords)

    df.dropna(subset=[keyword.title()], inplace=True)

    os.makedirs(keyword, exist_ok=True)
    df.to_csv(output_csv, index=False)

    words_dict.update(word_dict)
    words_dict = {key: value for key, value in words_dict.items() if value != 0}
    words_dict = dict(sorted(words_dict.items(), key=lambda item: item[1], reverse=True))

    out_summary = f"{keyword}/{csv_file.replace('.csv', f'_{keyword}_summary.csv')}"
    with open(out_summary, 'w') as file:
        file.write(f"{keyword.title()},Count\n")
        for key, value in words_dict.items():
            file.write(f"{key.title()},{value}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <jsonl_file_1> <jsonl_file_2> ... <jsonl_file_n>")
        sys.exit(1)
    
    files = sys.argv[1:]

    for file in tqdm(files):
        print(f"Finding {keyword.title()} in {file}")
        check_word_occurrences(file)
        print(f"Completed Finding {keyword.title()} in {file}\n")

if __name__ == '__main__':
    main()
