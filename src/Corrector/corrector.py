import requests, sys

count = 0

def correct(text):

    url = "https://speller.yandex.net/services/spellservice.json/checkText?text="

    h = 0#]

    t = text.split(' ')

    fixed = text

    while h <= len(t):
        req = url + "+".join(t[h:(h + 100)])
        h += 100

        resp = requests.get(req)

        resp = resp.json()

        for err in resp:
            fixed = str.replace(fixed, err["word"], err["s"][0])

    return fixed

"""
if __name__ == '__main__':
    print(correct("мой дядя самх чесных правилкогда не в шутку занемог"))
"""
