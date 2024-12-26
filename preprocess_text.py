import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')

def preprocess_text(text):
    """
    @Args:- text:- str object which contains the 'content' of the object.
    @Description:-
                This method removes and formats the 'content' attribute of sentiment
                description list
    @Returns:- formatted 'content' text
    """
    # Remove URLs and special characters
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)  # Remove mentions and hashtags
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove punctuation and numbers

    # Remove specific unwanted text patterns
    text = re.sub(r'\n+', ' ', text)  # Replace newlines with space
    text = re.sub(r'Continue reading|View comments|\.', '', text)  # Remove specific phrases

    # Convert to lowercase and tokenize
    tokens = nltk.word_tokenize(text.lower())

    # Remove stop words and lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stopwords.words('english')]

    return ' '.join(tokens)

import csv

def write_cleaned_contents_to_file(description_list, filename='cleaned_contents.csv'):
    """
    @Args:
        description_list: list object containing sentiment descriptions
        filename: str object containing default file name
    @Description:
        This method processes each element of description_list and saves it to the specified CSV file.
    @Returns:
    """

    # Open the file in write mode with utf-8 encoding
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write the header row
        writer.writerow(["Date", "Content"])

        # Iterate through the description list and write each row
        for description in description_list:
            created_at = description['date']
            cleaned_description = preprocess_text(description['content'])
            writer.writerow([created_at, cleaned_description])