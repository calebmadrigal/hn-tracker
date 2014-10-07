#!/usr/bin/env python3

import time
import datetime
import csv
import re
import requests
import bs4

hn_base = "https://news.ycombinator.com/"
hn_home = hn_base + "news?p={0}"

def timestamp():
    return datetime.datetime.now().isoformat()

def parse_news_item(row1, row2):
    rank = '999999'
    try:
        rank = row1[0].text.replace('.', '')
    except Exception:
        pass

    title = ''
    try:
        title = row1[2].text.strip()
    except Exception:
        pass

    points = '0'
    try:
        points = re.search(r'(\d+) points', row2[1].text).groups()[0]
    except Exception:
        pass

    row2_links = row2[1].find_all('a')

    user = ''
    try:
        user = row2_links[0].text
    except Exception:
        pass

    comments = '0'
    try:
        comments = row2_links[1].text.split(' ')[0]
        if comments == 'discuss':
            comments = '0'
    except Exception:
        pass

    hn_id = '0'
    try:
        hn_id = row2_links[1]['href'].split('=')[1]
    except Exception:
        pass

        # Try to get hn_id from row1
        try:
            hn_id = row1[2].find_all('a')[0]['href'].split('=')[1]
        except Exception:
            pass

    return [timestamp(), hn_id, rank, points, comments, title, user]


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
        print("\tGetting page", i)
        page_rows = page_rows + get_hn_data(i)
    return page_rows
        

def write_csv(filename, data):
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def run():
    outfile = "hndata.csv"
    page_depth = 3
    wait_time = 60 # seconds

    while 1:
        print("Getting HackerNews", timestamp())
        try:
            hn_data = get_pages(page_depth)
            write_csv(outfile, hn_data)
        except requests.exceptions.ConnectionError:
            print("Network error")
        time.sleep(wait_time)

if __name__ == "__main__":
    run()

