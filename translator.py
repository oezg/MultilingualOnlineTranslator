import requests
from bs4 import BeautifulSoup


def get_target_language_and_word() -> tuple:
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
    target_lang = input()
    print("Type the word you want to translate:")
    word = input()
    print(f'You chose "{target_lang}" as a language to translate "{word}".')
    return target_lang, word


def get_soup(target_lang: str, word: str) -> str:
    source, target = "english", "french"
    if target_lang == "en":
        target, source = source, target
    url = f"https://context.reverso.net/translation/{source}-{target}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response:
        print(response.status_code, 'OK')
        return BeautifulSoup(response.content, 'html.parser')


def get_translations(soup: BeautifulSoup) -> list:
    translations = soup.find('div', {'id': 'translations-content'}).find_all('a')
    return [translation.text.strip() for translation in translations]


def get_sentences(soup: BeautifulSoup) -> list:
    sentences = soup.find('section', {'id': 'examples-content'}).find_all('span', {'class': 'text'})
    return [sentence.text.strip() for sentence in sentences]


def main():
    target_lang, word = get_target_language_and_word()
    soup = get_soup(target_lang, word)
    if soup:
        if target_lang == "en":
            target_lang = "English"
        else:
            target_lang = "French"
        print()
        print(f'{target_lang} Translations')
        translations = get_translations(soup)
        print(*translations[:5], sep='\n')
        print()
        print(f'{target_lang} Examples')
        sentences = get_sentences(soup)
        for i, sentence in enumerate(sentences[:10]):
            print(sentence)
            if i % 2:
                print()


if __name__ == '__main__':
    main()
