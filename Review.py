import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

FILE_NAME = 'companies.json'

browser = webdriver.Chrome()

data = []
with open(FILE_NAME) as f:
    data = json.load(f)

for line in data:
    if line.get('like', None) is not None:
        continue

    link = 'http://' + line['link']
    print(line['name'], link)

    browser.get(link)
    like = input('Like?')
    line['like'] = True if like == 'y' else False

with open(FILE_NAME, 'w') as f:
    json.dump(data, f)

browser.quit()