from Corrector import correct

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


# return number in table
def get_answer(question, filepath):
    question = correct(question)
    question = delete_noisy_words(question, filepath)

    from Stemmer import Porter
    question_stemmed_list = [Porter.stem(x) for x in question.split(" ") if x]
    print(question_stemmed_list)

    print(question)
    pass

# get_answer("На каких правах предоставляется общежитие для поступивших на бюджетной основе?")
