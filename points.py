import re
import requests
import argparse
from bs4 import BeautifulSoup

LOG_MSG = lambda name, place, points, page: f"""
==================
Name: {name}
Place: {place}
Points: {points}
This information was found on https://hub.shutokorevivalproject.com/timing/points?page={page}&month=0.
==================
"""

ERROR_MSG = lambda name: f'We could not find {name} on the points leaderboard.'

def main():
    # Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of the person to generate statistics for.")

    # Parse args
    args = parser.parse_args()
    name = args.name if args.name else 'Jonathan'
 
    i = 0
    last = ''
    while True:
        # Request
        url = 'https://hub.shutokorevivalproject.com/timing/points'
        opts = {
            "page": i,
            "month": 0
        }
        res = requests.get(url, opts)
        if res.status_code != 200:
            print(ERROR_MSG(name))
            break
        if res.text == last:
            print(ERROR_MSG(name))
            break

        # Parse
        last = res.text
        soup = BeautifulSoup(res.text, features="html.parser")
        items = soup.find_all('td')
        for j, item in enumerate(items):
            if name in item:
                pattern = r'>(\d+)<'
                place = re.findall(pattern, str(items[j - 1]))[0]
                points = re.findall(pattern, str(items[j + 1]))[0]
                print(LOG_MSG(name, place, points, i))
                break
        else:
            i += 1
            continue
        break
        

if __name__ == '__main__':
    main()