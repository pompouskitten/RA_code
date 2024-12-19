import csv
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def main():
    manual_file = "manually_annotated.csv"
    true_labels = []
    predicted_labels = []

    with open(manual_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        total = 0
        for row in reader:
            total += 1
            manual = row["Manual_Sentiment"]
            if not manual:
                continue

            if str(manual) == "0.0":
                true_labels.append("Negative")
            elif str(manual) == "1.0":
                true_labels.append("Neutral")
            elif str(manual) == "2.0":
                true_labels.append("Positive")

            predicted_labels.append(row["Overall Sentiment"])

    accuracy = accuracy_score(true_labels, predicted_labels)
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predicted_labels, average='weighted'
    )

    print(f"Total Labeled: {len(true_labels)}")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall: {recall * 100:.2f}%")
    print(f"F1 Score: {f1:.2f}")
    print(f"Total in file: {total}")
    print(f"Total Remaining: {1000-len(true_labels)}")

if __name__ == "__main__":
    main()