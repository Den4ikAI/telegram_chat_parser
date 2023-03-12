import os
import fnmatch
from bs4 import BeautifulSoup
import lxml
from tqdm import tqdm
import json

chatdir = 'dump'


def myclean(s):
    cleandict = {
        ')': ' ',
        '?': '? ',
        '😂': '',
        '😅': '',
        '🙈': '',
        '🤗': '',
        '🤣': '',
        '@': '',
        '😬': '',
        '❤': '',
        'хД': '',
        'ДДД': '',
        '😁': '',
        '😹': '',
        '👋': '',
        '🥺': '',
        '☀': '',
        '🍀': '',
        '  ': ' ',
        '  ': ' '
    }
    for x in cleandict:
        s = s.replace(x, cleandict[x])
    return s.strip()


with open('output.jsonl', 'a') as dataset:
    for file in os.listdir(chatdir):
        if fnmatch.fnmatch(file, '*.html'):
            with open(chatdir + '/' + file, 'r', encoding='UTF-8') as f:
                data = f.read().strip()
            soup = BeautifulSoup(data, 'html.parser')
            messages = soup.find_all('div', class_='message')
            for message in tqdm(messages, desc=f'Обработка файла: {file}'):
                if message.find("div", {"class": "reply_to details"}) and message.find("div", {"class": "text"}):
                    new_message = (message.find("div", {"class": "text"}).text).strip()
                    old_message0 = message.find("div", {"class": "reply_to details"}).a.get('href').replace('#go_to_', '')
                    old_message = ''
                    if soup.find("div", {"id": str(old_message0)}):
                        old_message0 = soup.find("div", {"id": str(old_message0)})
                        if old_message0.find("div", {"class": "text"}):
                            old_message = (old_message0.find("div", {"class": "text"}).text).strip()
                    if len(new_message) > 7 and len(old_message) > 7:
                        old_message = myclean(old_message)
                        new_message = myclean(new_message)
                        dataset.write(json.dumps({'question': old_message, 'answer': new_message}) + '\n')