import requests
from bs4 import BeautifulSoup
from sys import exit
from collections import OrderedDict
from argparse import ArgumentParser


supported_languages = ('Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                       'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish')


def get_soup(source: str, target: str, word: str) -> BeautifulSoup:
    url = f"https://context.reverso.net/translation/{source.lower()}-{target.lower()}/{word.lower()}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    elif response.status_code == 404:
        print("Sorry, unable to find {}".format(word))
    else:
        print("Something wrong with your internet connection")
    exit()


def get_soups(source: str, word: str) -> OrderedDict:
    soups_dict = OrderedDict()
    for language in supported_languages:
        if language.lower() != source.lower():
            soups_dict.update({language: get_soup(source=source, target=language, word=word)})
    return soups_dict


def get_translations(soup: BeautifulSoup) -> list:
    translations = soup.find('div', {'id': 'translations-content'}).find_all('a')
    return [translation.text.strip() for translation in translations]


def get_sentences(soup: BeautifulSoup) -> list:
    sentences = soup.find('section', {'id': 'examples-content'}).find_all('span', {'class': 'text'})
    return [sentence.text.strip() for sentence in sentences]


def text_translations(target_language: str, soup: BeautifulSoup, quantity: int = 5) -> str:
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


def validate(language: str) -> None:
    if language.title() not in supported_languages:
        print("Sorry, the program doesn't support {}".format(language))
        exit()


def main():
    parser = ArgumentParser("Prints translations of a given word.")
    parser.add_argument("source_language")
    parser.add_argument("target_language")
    parser.add_argument("word")
    args = parser.parse_args()
    validate(args.source_language)
    text = ""
    if args.target_language == "all":
        soups = get_soups(args.source_language, args.word)
        for target, soup in soups.items():
            text += text_translations(target, soup, quantity=1)
    else:
        validate(args.target_language)
        soup = get_soup(args.source_language, args.target_language, args.word)
        text = text_translations(args.target_language, soup)
    print(text)
    with open(f'{args.word}.txt', 'w') as file_handle:
        file_handle.write(text)


if __name__ == '__main__':
    main()
