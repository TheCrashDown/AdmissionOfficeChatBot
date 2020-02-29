import requests

def correct(text):

    url = "https://speller.yandex.net/services/spellservice.json/checkText?text="

    req = url + str.replace(text.strip(), " ", "+")

    resp = requests.get(req).json()

    fixed = text
    for err in resp:
        fixed = str.replace(fixed, err["word"], err["s"][0])

    return fixed

"""
if __name__ == '__main__':
    print(correct("мой дядя самх чесных правилкогда не в шутку занемог"))
"""
