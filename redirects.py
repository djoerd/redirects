#!/usr/bin/python3

import requests
import sys
import urllib.parse

def get_forward_online(url, history=None):
    if (history is None):
        history = list()
    if (len(url) < 2):
        return (url, history)
    sys.stderr.write("GET " + url + "\n")
    try:
        head = requests.head(url, timeout=10)
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
            return get_forward_online(location, history)
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

h_cache = dict()
u_cache = dict()

def add_to_cache(url, hist):
    res = hist.split()
    if (len(res) > 1):
        u_cache[res[0]] = url
        h_cache[res[0]] = res
 
def get_forward(url):
    url = add_protocol(url)
    if (url in h_cache):
        hist = h_cache[url]
        res  = u_cache[url]
        sys.stderr.write("CACHED: " + url + "\n")
        return (res, hist)
    else:
        return get_forward_online(url)
 
try:
    with open('URLS_checked.csv', 'r') as csvfile:
        for row in csvfile:
            (id, url1, hist1, url2, hist2, url3, hist3) = row.split(';', 6)
            add_to_cache(url1, hist1)
            add_to_cache(url2, hist2)
            add_to_cache(url3, hist3)
except FileNotFoundError:
    pass


with open('URLS_to_check.csv', 'r') as csvfile:
    for row in csvfile:
        (id, url1, url2, url3, rest) = row.split(';', 4)
        if (id != "TwitterID"):
            (url1, hist1) = get_forward(url1)
            (url2, hist2) = get_forward(url2)
            (url3, hist3) = get_forward(url3)
            print_csv(id, url1, hist1, url2, hist2, url3, hist3)
