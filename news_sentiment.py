import re
from utils import get_stock_news_data
import json

def vietnamese_word_tokenize(text):
    """
    Tokenizes Vietnamese text, removes punctuation, URLs, HTML tags, and numbers.

    Args:
        text: The input Vietnamese text string.

    Returns:
        A list of Vietnamese words (tokens).
    """

    # 1. Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    # 3. Remove punctuation (keeping Vietnamese diacritics)
    punctuation = r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]'
    text = re.sub(punctuation, '', text)

    # 4. Remove numbers
    text = re.sub(r'\d+', '', text)

    # 5. Tokenize by splitting on whitespace
    tokens = text.split()

    # 6. Further refine tokens to handle cases with diacritics attached to spaces
    refined_tokens = []
    for token in tokens:
        # Split tokens that might have diacritics directly attached to spaces
        sub_tokens = re.split(r'(\s+)', token)
        for sub_token in sub_tokens:
            if sub_token.strip():  # Add only non-empty tokens
                if len(sub_token.strip())==1:
                    continue
                temp = sub_token.strip()
                temp = temp.lower() # Convert to lowercase
                refined_tokens.append(temp)

    return refined_tokens


def better_vietnamese_word_tokenize(text):
    """
    Warning: This function is SLOW.
    Tokenizes Vietnamese text.

    Args:
        text: The input Vietnamese text string.

    Returns:
        A list of Vietnamese words (tokens) which are appeared in the dictionary.txt.
    """
    if not hasattr(better_vietnamese_word_tokenize, 'vocab'):
        vocab = []
        with open('dictionary.txt', 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    entry = json.loads(line.strip())
                    if 'text' in entry:
                        vocab.append(entry['text'].lower())
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line.strip()}")
        vocab = set(vocab)
        better_vietnamese_word_tokenize.vocab = vocab
    tokens = []
    i = 0
    n = len(text)
    text = text.lower()
    while i < n:
        matched = False
        for lw in range(20, 0, -1):
            if text[i:i+lw] in better_vietnamese_word_tokenize.vocab:
                matched = True
                tokens.append(text[i:i+lw])
                i += lw
                break
        if not matched:
            i += 1
    return tokens

if __name__ == '__main__':
    df_news = get_stock_news_data()
    data = {}
    for i, row in df_news.iterrows():
        text = row['content']
        tokens = better_vietnamese_word_tokenize(text)
        
        for token in tokens:
            if token in data:
                data[token] += 1
            else:
                data[token] = 1
    tokens = []
    for word, count in data.items():
        tokens.append((count, word))
    
    tokens.sort(reverse=True)
    print(tokens)