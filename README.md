# COVID-19 and Digital Health Communication on Rheumatoid Arthritis: A Natural Language Processing Analysis of Reddit Discussion

The codes used in the research article are available in this repository. Most scripts can be executed using straightforward command-line arguments. Below is a table summarizing the use case for each file:
| Script    | Use Case |
| -------- | ------- |
| analyse_emotion.py | Uses the https://huggingface.co/j-hartmann/emotion-english-distilroberta-base/ model to classify the text into emotions (anger, disgust, fear, joy, neutral, sadness, & surprise) from the input csv files. |
| analyse_sentiment.py | Uses the NLTK VADER to classify the text into the sentiments (positive, neutral & negative) from the input csv files. |
| count_unique.py | Finds the unique users in a csv file. Can also calculate the new users in the input files. |
| extract_comments.py | Extracts the required fields from the extracted JSONL file containing comments from Reddit to CSV files. |
| extract_drugs.py | Extracts all the posts and comments from the input CSV that mention any drugs present in the drugs.txt file. |
| extract_links.py | Extracts all the posts and comments from the input CSV that contain any URLs. |
| extract_posts.py | Extracts the required fields from the extracted JSONL file containing posts from Reddit to CSV files. |
| helpers.py and process_paragraph.py | Contain functions that are used in other files. |
| RoBERTa.ipynb | Trains and evaluates the fine-tuned RoBERTa model. |
| topic_model_save.py | Uses BERTopic to identify the topics from the input CSV and saves the model. |
| validate_manual.py | Evaluates the NLTK VADER for sentiment analysis. |


If any doubts or problems, create a GitHub issue.
