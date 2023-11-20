import os
import re
from langchain.document_loaders import PyPDFLoader

def count_words(text):
    words = re.findall(r'\w+', text)
    return len(words)

directory = 'c:\\Users\\anima\\OneDrive\\Escritorio\\Programming\\Python\\Hackathon\\data_0611'

files = os.listdir(directory)

for file in files:
    file_path = os.path.join(directory, file)
    loader = PyPDFLoader(file_path)
    data=loader.load()
    raw = ""
    for page in data:
        raw += page.page_content
    raw = raw.replace("\n", " ")
    print(raw[:1000])
    word_count = count_words(raw)
    result = (word_count * 0.75)
    print(f"File: {file}, Word Count: {word_count}, Result of: {result}")
