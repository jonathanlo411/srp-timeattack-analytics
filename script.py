import requests
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup

TRACKS = {
    'bayshorenorthbound': 'Bayshore Northbound',
    'bayshoresouthbound': 'Bayshore Southbound',
    'beltinner':          'Belt Inner',
    'beltouter':          'Belt Outer',
    'c1inner':            'C1 Inner',
    'c1outer':            'C1 Outer',
    'miraiouter':         'Mirai Outer',
    'miraiouter':         'Mirai Outer',
    'shibuya':            'Shibuya',
    'shinjuku':           'Shinjuku',
    'yokohanenorthbound': 'Yokohane Northbound',
    'yokohanesouthbound': 'Yokohane Southbound'
}

def main():
    # Initialize
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of the person to generate statistics for.")
    parser.add_argument("-l", "--leaderboard", help="Name of the leaderboard to target. Ex. TrafficSlow")
    parser.add_argument("-t", "--track", help="Lowercase and spaces remove name of track. Ex. c1outer")
    parser.add_argument("-s", "--save", help="Saves the results of the statistics.")

    # Parse args
    args = parser.parse_args()
    name = args.name if args.name else 'Jonathan'
    leaderboard = args.leaderboard if args.leaderboard else None
    track = TRACKS[args.track.lower().replace(' ', '')] if args.track else None

    data = obtain_data(name, leaderboard, track)

def obtain_data(name='Jonathan', leaderboard=None, track=None):
    #https://hub.shutokorevivalproject.com/timing?leaderboard=Default&stage=Bayshore%20Northbound&track=shuto_revival_project_beta&page=1&month=0
    url = 'https://hub.shutokorevivalproject.com/timing'
    
    # if track and leaderboard:
    #     params = {
    #         'leaderboard': leaderboard,
    #         'stage': track 
    #     }
    #     res = requests.get(url, params)
    # elif track:
    #     params = {
    #         'leaderboard': leaderboard,
    #         'stage': track 
    #     }
    #     res = requests.get(url, params)

    # else:
    for track_value in TRACKS.values():
        params = {
            'leaderboard': leaderboard if leaderboard else 'Default',
            'stage': track_value,
            'page': 0,
            'month': 0
        }
        res = requests.get(url, params)
        soup = BeautifulSoup(res.text, features="html.parser")
        for i in soup.find_all('tr'):
            print(i.get_text())
        break
        

        

if __name__ == '__main__':
    main()