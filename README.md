# Multilingual Online Translator
An app that translates the words you type and gives you many usage examples based on the context.  
It accesses the web with _requests_ and handle the data with _BeautifulSoup_ libraries.  
This app works from the command line. To translate a word from a source language to a target language, use this syntax from the shell:  
`python translator.py <source_language> <target_language> <word>`  
The program supports these 13 languages: Arabic German English Spanish French Hebrew Japanese Dutch Polish Portuguese Romanian Russian Turkish  
The program prints 5 translations of the given word in the desired target language. In addition to that it displays 5 example sentences in the source and target language to show the usage of the word in context.  
If you want to see the translation of a word in all of the thirteen languages together, enter:   
`python translator.py <source_language> all <word>`   
The source of the translations and the example sentences is reverso.net.   

![El interprete](https://user-images.githubusercontent.com/67658548/147891113-39742034-6bb9-497b-9554-d5e3b3eca430.png)
