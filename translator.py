import requests
from bs4 import BeautifulSoup


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
        print('Type the number of language you want to translate to: ')
    else:
        print('Type the number of your language: ')
    try:
        return supported_languages[input()]
    except KeyError:
        print('wrong input')


def get_soup(source: str, target: str, word: str) -> str:
    url = f"https://context.reverso.net/translation/{source.lower()}-{target.lower()}/{word.lower()}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response:
        return BeautifulSoup(response.content, 'html.parser')


def get_translations(soup: BeautifulSoup) -> list:
    translations = soup.find('div', {'id': 'translations-content'}).find_all('a')
    return [translation.text.strip() for translation in translations]


def get_sentences(soup: BeautifulSoup) -> list:
    sentences = soup.find('section', {'id': 'examples-content'}).find_all('span', {'class': 'text'})
    return [sentence.text.strip() for sentence in sentences]


def introduction():
    print("Hello, you're welcome to the translator. Translator supports: ")
    print(*("{0}. {1}".format(k, v) for k, v in supported_languages.items()), sep='\n')


def main():
    introduction()
    source_language = get_language()
    target_language = get_language(target=True)
    word = input("Type the word you want to translate:\n")
    soup = get_soup(source_language, target_language, word)
    if soup:
        print()
        print(f'{target_language} Translations')
        translations = get_translations(soup)
        print(*translations[:5], sep='\n')
        print()
        print(f'{target_language} Examples')
        sentences = get_sentences(soup)
        for i, sentence in enumerate(sentences[:10]):
            print(sentence)
            if i % 2:
                print()


if __name__ == '__main__':
    main()
