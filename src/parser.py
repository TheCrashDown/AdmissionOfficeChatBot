import requests
from bs4 import BeautifulSoup
import csv

def parse_question_answer(qwa_parsed_list):

    html_query = requests.get("https://pk.mipt.ru/bachelor/question-answer/", verify=False)

    if not html_query.ok:
        print("ERROR reading question_answer")
        exit(1)

    html_text = html_query.text


    #with open("bachelor-question-answer.html", "r") as f:
    #    html_text = f.read()

    soup = BeautifulSoup(html_text, 'html.parser')

    questions_with_answers = soup.body.find('div', class_="col-sm-offset-1 col-sm-10 content-page")

    qwa_list = questions_with_answers.contents

    div_in_the_end = qwa_list[-2]
    qwa_list = qwa_list[:-3]
    qwa_list += div_in_the_end.contents
    qwa_list = qwa_list[:-2]


    for question_with_answer in qwa_list:
        if question_with_answer.name is not None:
            if question_with_answer.name in ['h2', 'p', 'li', 'a', 'div']:
                if question_with_answer.name == 'h2':
                    qwa_parsed_list.append(["Бакалавриат. " + question_with_answer.string, ""])
                else:
                    qwa_parsed_list[-1][1] += str(question_with_answer)

def parse_faq(qwa_parsed_list):


    html_query = requests.get("https://pk.mipt.ru/faq/", verify=False)

    if not html_query.ok:
        print("ERROR reading faq")
        exit(2)

    html_text = html_query.text


    #with open("bachelor-faq.html", "r") as f:
    #    html_text = f.read()

    soup = BeautifulSoup(html_text, 'html.parser')

    faq_list = soup.body.find('div', id="question_list").find_all('div')

    print(faq_list)

    for faq in faq_list:
        pass
        #print(type(faq))
        #print(faq.find('div', class_="q_answer"))
        #print("----------------------------------------")
        #qwa_parsed_list.append()




def parse():
    qwa_parsed_list = []

    parse_question_answer(qwa_parsed_list)
    parse_faq(qwa_parsed_list)

    with open("../data/queries.csv", "w") as f:
        f_csv = csv.writer(f)

        for row in qwa_parsed_list:
            f_csv.writerow(row)

parse()