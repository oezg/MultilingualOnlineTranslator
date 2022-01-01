import requests
from bs4 import BeautifulSoup
from sys import exit
from collections import OrderedDict


supported_languages = {
    '1': 'Arabic',
    '2': 'German',
    '3': 'English',
    '4': 'Spanish',
    '5': 'French',
    '6': 'Hebrew',
    '7': 'Japanese',
    '8': 'Dutch',
    '9': 'Polish',
    '10': 'Portuguese',
    '11': 'Romanian',
    '12': 'Russian',
    '13': 'Turkish'
}


def get_language(target=False) -> str:
    if target:
        print("Type the number of language you want to translate to or '0' to translate to all languages: ")
    else:
        print('Type the number of your language: ')
    number = input()
    if number in supported_languages.keys():
        return supported_languages[number]
    elif target and number == "0":
        return number
    print('Wring input!')
    exit()


def get_soup(source: str, target: str, word: str) -> BeautifulSoup:
    url = f"https://context.reverso.net/translation/{source.lower()}-{target.lower()}/{word.lower()}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response:
        return BeautifulSoup(response.content, 'html.parser')
    print("There is a connection error. Please try again later!")
    exit()


def get_soups(source: str, word: str) -> OrderedDict:
    soups_dict = OrderedDict()
    for language in supported_languages.values():
        if language == source:
            continue
        soups_dict.update({language: get_soup(source=source, target=language, word=word)})
    return soups_dict


def get_translations(soup: BeautifulSoup) -> list:
    translations = soup.find('div', {'id': 'translations-content'}).find_all('a')
    return [translation.text.strip() for translation in translations]


def get_sentences(soup: BeautifulSoup) -> list:
    sentences = soup.find('section', {'id': 'examples-content'}).find_all('span', {'class': 'text'})
    return [sentence.text.strip() for sentence in sentences]


def introduction() -> None:
    print("Hello, you're welcome to the translator. Translator supports: ")
    print(*("{0}. {1}".format(k, v) for k, v in supported_languages.items()), sep='\n')


def text_translations(target_language: str, soup: BeautifulSoup, quantity=5) -> str:
    text = f'\n{target_language} Translations\n'
    translations = get_translations(soup)
    text += '\n'.join(translations[:quantity])
    text += f'\n{target_language} Example{"s" if quantity > 1 else ""}\n'
    sentences = get_sentences(soup)
    for i, sentence in enumerate(sentences[:quantity*2]):
        text += sentence + '\n'
        if i % 2:
            text += '\n'
    return text


def main():
    introduction()
    source_language = get_language()
    target_language = get_language(target=True)
    word = input("Type the word you want to translate:\n")
    text = ""
    if target_language == "0":
        soups = get_soups(source_language, word)
        for target, soup in soups.items():
            text += text_translations(target, soup, quantity=1)
    else:
        soup = get_soup(source_language, target_language, word)
        text = text_translations(target_language, soup)
    print(text)
    with open(f'{word}.txt', 'w') as file_handle:
        file_handle.write(text)


if __name__ == '__main__':
    main()
