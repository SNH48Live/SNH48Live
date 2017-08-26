#!/usr/bin/env python3

import argparse
import re

import bs4
import requests


ENTRY_LINK = re.compile(r'^/Index/invedio/id/(\d+)$')
WHITESPACE = re.compile(r'\s+')


# Returns False when page has no videos
def crawl_page(page_num):
    url = f'http://live.snh48.com/Index/index/p/{page_num}.html'
    resp = requests.get(url)
    assert resp.status_code == 200
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    theend = True
    for entry in soup.select('li.videos'):
        title = WHITESPACE.sub(' ', entry.text.strip())
        vid = ENTRY_LINK.match(entry.a['href']).group(1)
        print(f'{vid}\t{title}')
        theend = False
    return not theend


def main():
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('-t', '--to-page', type=int,
        help='stop at the specified page')
    args = parser.parse_args()

    page_num = 1
    while not args.to_page or page_num <= args.to_page:
        if not crawl_page(page_num):
            break
        page_num += 1


if __name__ == '__main__':
    main()
