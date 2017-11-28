#!/usr/bin/python3

import requests
import sys
import urllib.parse

def get_forward(url, history=None):
    if (history is None):
        history = list()
    if (len(url) < 2):
        return (url, history)
    sys.stderr.write("GET " + url + "\n")
    try:
        head = requests.head(url)
    except Exception:
        sys.stderr.write("Warning: Exception for url: " + url + "\n")
        return (url, history)
    code = head.status_code
    if (code == 301 or code == 302):
        headers  = head.headers
        if ('Location' in headers):
            location = head.headers['Location']
            location = urllib.parse.urljoin(url, location)
            history.append(url)
            return get_forward(location, history)
        else:
            raise ValueError('No Location header')
    else:
        if (code != 200):
            sys.stderr.write("Warning: " + str(code) + " for url: " + url + "\n")
        return (url, history)


def add_protocol(url):
    if (len(url) > 1 and not(url.startswith('http'))):
        url = 'http://' + url
    return url


def print_csv(id, url1, hist1, url2, hist2, url3, hist3):
    list1 = " ".join(hist1)
    list2 = " ".join(hist2)
    list3 = " ".join(hist3)
    print (";".join(list((id, url1, list1, url2, list2, url3, list3))))

print ('TwitterID;URL1;HISTORY1;URL2;HISTORY2;URL3;HISTORY3;')

with open('URLS_to_check.csv', 'r') as csvfile:
   for row in csvfile:
       (id, url1, url2, url3, rest) = row.split(';', 4)
       if (id != "TwitterID"):
           (url1, hist1) = get_forward(add_protocol(url1))
           (url2, hist2) = get_forward(add_protocol(url2))
           (url3, hist3) = get_forward(add_protocol(url3))
           print_csv(id, url1, hist1, url2, hist2, url3, hist3)
