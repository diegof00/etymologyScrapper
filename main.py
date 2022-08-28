import requests
import functions_framework
from bs4 import BeautifulSoup


URL_ETIMOLOGIA = 'http://etimologias.dechile.net/?'
REGEX_SPANISH_EXPRESSION = '[^[-_/.,{InBASIC_LATIN}{InLATIN_1_SUPPLEMENT}0-9]]+'


def search_etymology(word):
    print(f'search etymology for , {word}')  # Press Ctrl+F8 to toggle the breakpoint.
    response = requests.get(URL_ETIMOLOGIA + word)
    if not response.ok:
        return ''
    soup = BeautifulSoup(response.text, 'lxml')
    word_selector = 'body > div.container > p:nth-child(3)'
    html_tags = soup.select(word_selector)
    etymology = html_tags[0].extract().get_text()
    return etymology.strip()


@functions_framework.http
def get_etymology(request):
    param = request.args.get('word')
    word = param.strip()
    if not word or not word.isalpha():
        return 'not found '
    etymology = {
        'word': word,
        'etymology': search_etymology(word)
    }
    return etymology
