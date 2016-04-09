#!/usr/bin/env python
'''
Crawler to fetch the top N posts of a subreddit.

Useage: crawler.py [subreddit] [N]

Selftext from posts are placed in numbered textfiles, and the titles are
written on the corresponding line of titlefiles.txt.

The files are all placed in path_start/[subreddit], change path_start
to suit your needs.
'''

import os
import requests
import sys
import time

path_start = "../../datasets/"

# Reddit wants an identifying header. If you are not part of the storybot project,
# change this to something else.
header = {
    "User-Agent": "python:storybot-nlp-post-generator:v1.0 (by /u/Popolion)",
}

params = {
    "limit" : 100,
    "t" : "all"
}

received = 0

def get_api_result(*args, **kwargs):
    response = requests.get(*args, **kwargs)
    result = None
    if (response.status_code != requests.codes.ok):
        print('Error in request, status code: ', response.status_code, file=sys.stderr)
        return result
    try:
        jsondata = response.json()
    except ValueError:
       print("Json value error")
    else:
        result = jsondata
    return result

def handle_result(result):
    global received, params
    titlefile = open(path_start + "titlefile.txt", 'a')
    for child in result['data']['children']:
        # Create file
        selftextfile = open(path_start + str(received) + ".txt", 'w')
        # Write selftext to file
        selftextfile.write(child['data']['selftext'])
        # Write title to title file
        titlefile.write(child['data']['title'] + "\n")
        received += 1
    # Update params
    params['after'] = result['data']['after']
    params['count'] = received
    print("Batch processed, total results: " + str(received), file=sys.stderr)

def crawl(subreddit, N):
    global path_start
    # Create the file path and url
    path_start += subreddit + "/"
    url = "http://www.reddit.com/r/" + subreddit + "/top/.json"
    # Create the destination directory if necessary
    if not os.path.exists(path_start):
        os.makedirs(path_start)
    # If a titlefile already exists, delete it
    if os.path.exists(path_start + "titlefile.txt"):
        os.remove(path_start + "titlefile.txt")
    while received < N:
        # Obey reddit api rules, keep requests per minute below 60
        time.sleep(1)
        result = get_api_result(url, headers=header, params=params)
        if (result== None):
            continue
        handle_result(result)

def main(argv):
    if (len(argv) != 2):
        print("Insufficient arguments:")
        print("crawler.py [subreddit] [N]")
        return
    crawl(argv[0], int(argv[1]))

if __name__ == "__main__":
       main(sys.argv[1:])
