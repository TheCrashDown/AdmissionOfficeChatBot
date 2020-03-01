from src.Corrector import correct
import pandas as pd
from gensim.models import KeyedVectors, Word2Vec
from src.Stemmer import Porter

def delete_noisy_words(text, pathname):
    text = text.lower()

    import re
    text = " ".join(re.split('[^а-я]', text))
    text = " " + text

    with open(pathname) as file:
        noisy_words = [word.replace("\n", "") for word in file.readlines()]

    for odd_word in noisy_words:
        odd_word.replace("\n", '')
        text = text.replace(" {} ".format(odd_word), " ")
    return text

df = pd.read_csv("data/clean_qa.csv", sep='\t')

noisy_words_filepath = "res/noisy_words.txt"
sentences = [
        [Porter.stem(word) for word in delete_noisy_words(sentence.lower(), noisy_words_filepath).split() if word]
        for sentence in df["Question"] if sentence]

model = Word2Vec(sentences, size=100, batch_words=5, window=4, min_count=5)
word_vectors = KeyedVectors.load("model/word2vec.model")

vocab = word_vectors.wv.vocab

def preprocessQuery(sentence):
    """Splits sentence into words and intersects it with vocabulaty of the trained model"""
    preprocessed = [Porter.stem(word) for word in
                    delete_noisy_words(sentence.lower(), noisy_words_filepath).split() if word]
    return preprocessed


def intersectWithVocab(sentence):
    sentence = [word for word in sentence if word in vocab]
    return sentence

# return number in table
def get_answer(query):
    preprocessed_query = preprocessQuery(query)

    min_sim = 1
    max_sim = 0
    min_i = 0
    max_i = 0

    # print("{}".format(query))
    for i in range(0, len(sentences)):
        line1 = intersectWithVocab(preprocessed_query)
        line2 = intersectWithVocab(sentences[i])
        sim = word_vectors.n_similarity(line1, line2)

        if sim < min_sim:
            min_sim = sim
            min_i = i

        if sim > max_sim:
            max_sim = sim
            max_i = i
    return max_i

