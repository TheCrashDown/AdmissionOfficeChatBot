import src.Corrector.corrector as corrector
from src.Stemmer.porter import Porter

def delete_noisy_words(text):
    with open("res/noisy_words.txt") as file:
        noisy_words = [word.replace("\n", "") for word in file.readlines()]

    for odd_word in noisy_words:
        odd_word.replace("\n", '')
        text = text.replace(" {} ".format(odd_word), " ")
    return text


def normalize_data(text):
    text = text.lower()
    import re
    text = text.replace('ё', 'е')
    text = " ".join(re.split('[^а-я]', text))
    text = " " + text
    text = delete_noisy_words(text)
    stemmed_text_list = [Porter.stem(x) for x in text.split(" ") if x]
    return stemmed_text_list


# return number in table
def get_answer(question):
    normal_question_list = normalize_data(question)
    pass
