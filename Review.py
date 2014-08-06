import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

FILE_NAME = 'companies.json'
TEMP_FILE = 'temp_companies.json'


def get_new_companies():
    data = []
    if os.path.isfile(TEMP_FILE):
        with open(TEMP_FILE) as f:
            try:
                data = json.load(f)
            except Exception:
                pass
        os.remove(TEMP_FILE)

    return data


def review_entries(data):
    browser = webdriver.Chrome()
    for line in data:
        if line.get('like', None) is not None:
            continue

        link = 'http://' + line['link']
        print(line['name'], link)
        browser.get(link)

        like = input('Do you like? ').strip().lower()
        if like in ['y', 'yes']: line['like'] = True
        elif like in ['n', 'no']: line['like'] = False
        elif like in ['e', 'exit']: break
    browser.quit()


def review():
    data = []
    if os.path.isfile(FILE_NAME):
        with open(FILE_NAME) as f:
            try:
                data = json.load(f)
            except Exception:
                pass

    new_companies = get_new_companies()
    if new_companies:
        print('Merging new companies')
        data += new_companies
    else:
        review_entries(data)

    with open(FILE_NAME, 'w') as f:
        json.dump(data, f)


def view_liked():
    data = []
    if os.path.isfile(FILE_NAME):
        with open(FILE_NAME) as f:
            try:
                data = json.load(f)
            except Exception:
                pass

    if data:
        browser = webdriver.Chrome()
        for line in data:
            if line.get('like', False):
                view = input('View ' + line['name']).strip().lower()
                if view in ['y', 'yes']: browser.get('http://' + line['link'])
        done = input('Done')
        browser.quit()



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'liked':
        view_liked()
    else:
        review()