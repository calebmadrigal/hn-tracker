#!/usr/bin/env python3

import time
import datetime
import requests
import bs4

hn_base = "https://news.ycombinator.com/"
hn_home = hn_base + "news?p={0}"

def timestamp():
    return datetime.datetime.now().isoformat()

def parse_news_item(row1, row2):
    try:
        rank = row1[0].text.replace('.', '')
        title = row1[2].text.strip()
        points = row2[1].find('span').text

        row2_links = row2[1].find_all('a')
        user = row2_links[0].text
        comments = row2_links[1].text.split(' ')[0]
        hn_id = row2_links[1]['href'].split('=')[1]

        return [timestamp(), hn_id, rank, title, points, comments, user]
    except (Exception):
        print("Error parsing row1: %r" % row1)
        print("Error parsing row2: %r" % row2)
        return [None, None, None, None, None, None, None]


def get_hn_data(page=1):
    data = requests.get(hn_home.format(page)).text
    soup = bs4.BeautifulSoup(data)
    tables = soup.find_all('table')
    news_table = tables[2]
    news_rows = news_table.find_all('tr')

    items = []

    # Each news item is made up of 3 rows
    for i in range(0, 90, 3):
        row1 = news_rows[i].find_all('td')
        row2 = news_rows[i+1].find_all('td')
        parsed = parse_news_item(row1, row2)
        items.append(parsed)

    return items

def get_pages(pages=3):
    page_rows = []
    for i in range(1, pages+1):
        print("Getting page", i)
        page_rows.append(get_hn_data(i))
    return page_rows
        

def run():
    outfile = "hndata.csv"
    page_depth = 3
    while 1:
        print("Getting HackerNews", timestamp())
        hn_data = get_pages()
        with open(outfile, 'a') as f:
            for row in hn_data:
                f.write(','.join(row))
        time.sleep(1)

if __name__ == "__main__":
    run()
    #print(get_hn_data())

