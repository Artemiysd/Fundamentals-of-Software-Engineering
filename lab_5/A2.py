import re

def split_sentences(text):
    sentences = re.split(r'(?<=[.?!])\s+', text)

    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences


text = "He jests at scars.   That never felt a wound! Hello, friend! Are you OK?"

sentences = split_sentences(text)

for s in sentences:
    print(s)

print("Предложений в тексте:", len(sentences))