import re
import requests
import argparse
from bs4 import BeautifulSoup

LOG_MSG = lambda name, place, points, page, duration, spm, l: f"""
==================
Name: {name}
Place: {place}
Score: {points}
Duration: {duration}
Score Per Minute: {spm}
This information was found on https://hub.shutokorevivalproject.com/overtake?leaderboard={l}&page={page}.
==================
"""

ERROR_MSG = lambda name: f'We could not find {name} on the points leaderboard.'

def main():
    # Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of the person to generate statistics for.")
    parser.add_argument("-s", "--slow", help="Add this flag to search for SlowCar server.", action='store_true')

    # Parse args
    args = parser.parse_args()
    name = args.name if args.name else 'Jonathan'
 
    i = 0
    last = ''
    while True:
        # Request
        url = 'https://hub.shutokorevivalproject.com/overtake'
        leaderboard = "TrafficSlow" if args.slow else "Default"
        opts = {
            "page": i,
            "leaderboard": leaderboard,
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
                pattern = r'>(.+)<'
                place = re.findall(pattern, str(items[j - 2]))[0]
                points = re.findall(pattern, str(items[j + 4]))[0]
                duration = re.findall(pattern, str(items[j + 2]))[0]
                spm = re.findall(pattern, str(items[j + 3]))[0]
                print(LOG_MSG(name, place, points, i, duration, spm, leaderboard))
                break
        else:
            i += 1
            continue
        break
        

if __name__ == '__main__':
    main()