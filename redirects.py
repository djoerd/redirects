#!/usr/bin/python3

import csv
import requests
import sys

def get_forward(url):
    head = requests.head(url)
    code = head.status_code
    if (code == 301):
        headers  = head.headers
        if ('Location' in headers):
            location = head.headers['Location']
            return get_forward(location)
        else:
            raise ValueError('No Location header')
    else:
        if (code != 200):
            sys.stderr.write("Warning: " + code)
        return url


with open('URLS_to_check.csv', 'rb') as csvfile:
   reader = csv.reader(csvfile, delimiter=';', quotechar='')

url  = "http://bit.ly/Movember2014"
print (get_forward(url))
