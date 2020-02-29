import src.corrector as corrector


def delete_noisy_words(text):
    text = text.lower()

    import re
    text = " ".join(re.split('[^а-я]', text))
    text = " " + text

    with open("../res/noisy_words.txt") as file:
        noisy_words = [word.replace("\n", "") for word in file.readlines()]

    for odd_word in noisy_words:
        odd_word.replace("\n", '')
        text = text.replace(" {} ".format(odd_word), " ")
    return text


# return number in table
def get_answer(question):
    question = corrector.correct(question)
    question = delete_noisy_words(question)

    from src.porter import Porter as porter
    question_stemmed_list = [porter.stem(x) for x in question.split(" ") if x]
    print(question_stemmed_list)

    print(question)
    pass

get_answer("На каких правах предоставляется общежитие для поступивших на бюджетной основе?")
