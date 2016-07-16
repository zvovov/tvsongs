#!usr/bin/env python3

import json
import sys
import time

import requests
from bs4 import BeautifulSoup
from slugify import slugify

_base_url = "https://www.tunefind.com/show/{}/{}/{}"

def getSoup(_url, _name, _season="", _episode_link=""):
    """
    Returns the html-parsed-BeautifulSoup object for the given URL.

    Parameters:
        _url: String: the http(s) link to get html from
        _name: String: name of the show|movie
        _season: Integer: season number of the show|movie
        _episode_link: Integer: Unique number for the episode to form its hyperlink.
    """
    if _season:
        _season = 'season-' + str(_season)
    
    try:
        r = requests.get(_url.format(_name, _season, _episode_link))
    except Exception:
        sys.exit("\nCONNECTION ERROR: Check your Internet Connection again.\n")

    return BeautifulSoup(r.text, 'html.parser').get_text()


def checkLimit(_entered, _limit):
    """
    Returns True if entered season/episode number is within the limit for the show. False otherwise.

    Parameters:
        _entered: String: the string entered by user when asked for season/episode number.
        _limit: Integer: Maximum number of seasons/episodes in the show/season.
    """
    _num = _entered.strip()
    if _num.lower() == 'exit' or _num.lower() == 'quit':
        sys.exit()
    try:
        _num = int(_num)
        if isinstance(_num, int):
            if 0 <= _num <= _limit:
                return True
    except ValueError:
        return False
    
    return False


def main():
    # show level
    _show_cont = 'y'
    while _show_cont.lower() == 'y':
        _entered_name = input("Name of the Show: ").strip()
        _input_name = slugify(_entered_name)
        _soup = getSoup(_base_url, _input_name)
        _js = "{" + _soup[_soup.find('"alertMessage"'): _soup.find('}};') + 2]
        # main source of data
        _json = json.loads(_js)

        _season_cont = 'n'
        _episode_cont = 'n'
    
        try:
            _json_show = _json['show']['result']
            _show_name = _json_show['show']['name']
            _season_id_list = _json_show['seasons']
            _season_count = len(_season_id_list)

            print("\n {}\n Total Seasons: {}".format(_show_name, _season_count))
            _season_song_count_list = [0] * _season_count
            _season_cont = 'y'
            # each season's details
            for season_ct, _season_id in enumerate(_season_id_list):
                # TODO: Store this info. Create database.
                _season_id = str(_season_id)
                _season_name = _json['entities']['seasons'][_season_id]['group_name']
                _season_num = _json['entities']['seasons'][_season_id]['group_sequence']
                _season_episode_count = _json['entities']['seasons'][_season_id]['episodes_count']
                _season_song_count_list[season_ct] = _json['entities']['seasons'][_season_id]['songs_count']
                _season_aired = time.strftime('%b %Y', time.localtime(_json['entities']['seasons'][_season_id]['air_date_start'])) + \
                                " to " + time.strftime('%b %Y', time.localtime(_json['entities']['seasons'][_season_id]['air_date_end']))

                print("\n {}    Episode(s): {}    Aired: {}\n Song(s): {}".format(_season_name, _season_episode_count,
                                                                              _season_aired, _season_song_count_list[season_ct]))
            if _season_count > 1:
                print("\n Total Song(s) in {}: {}".format(_show_name, sum(_season_song_count_list)))
        except KeyError:
            print(" {} was not found.".format(_entered_name))
        
        # season level
        while _season_cont.lower() == 'y':
            while True:
                _season_wanted = input("\n Choose Season of {}. 1 to {} (0 for all): ".format(_show_name, _season_count))
                if checkLimit(_season_wanted, _season_count):
                    _season_wanted = int(_season_wanted)
                    break
            _season_start = 1 if _season_wanted == 0 else _season_wanted
            _season_end = _season_count + 1 if _season_wanted == 0 else _season_wanted + 1

            for curr_season in range(_season_start, _season_end):
                if _season_song_count_list[curr_season - 1] == 0:
                    print("\n No song(s) in {} S{}".format(_show_name, curr_season))
                    continue
                _season_soup = getSoup(_base_url, _input_name, curr_season)
                _season_js = "{" + _season_soup[_season_soup.find('"alertMessage"'): _season_soup.find('}};') + 2]
                _season_json = json.loads(_season_js)

                _episode_id_list = _season_json['season']['episodes']
                _episode_count = len(_episode_id_list)
                _episode_song_count_list = [0] * _episode_count
                _episode_cont = 'y'

                for episode_ct, _episode_id in enumerate(_episode_id_list):
                    _episode_id = str(_episode_id)
                    _episode_name = _season_json['entities']['episodes'][_episode_id]['name']
                    _episode_num = _season_json['entities']['episodes'][_episode_id]['number']
                    _episode_aired = _season_json['entities']['episodes'][_episode_id]['airdate_day'] + \
                                    " " + _season_json['entities']['episodes'][_episode_id]['airdate_month_short'] + \
                                    " " + _season_json['entities']['episodes'][_episode_id]['airdate_year']
                    _episode_song_count_list[episode_ct] = _season_json['entities']['episodes'][_episode_id]['song_count']
                    _episode_description = _season_json['entities']['episodes'][_episode_id]['episode_description']

                    _episode_description = _episode_description if _episode_description else "No description"

                    if _season_wanted:                        
                        print("\n S{}.E{} {}    Aired: {}    Song(s): {}\n {}".format(curr_season, _episode_num,
                                                                                      _episode_name, _episode_aired,
                                                                                      _episode_song_count_list[episode_ct],
                                                                                      _episode_description))

                # episode level
                while _episode_cont.lower() == 'y':
                    if _season_wanted:
                        while True:
                            _episode_wanted = input("\n Choose Episode of {} S{}. 1 to {} (0 for all): ".format(_show_name,
                                                                                                                curr_season,
                                                                                                                _episode_count))
                            if checkLimit(_episode_wanted, _episode_count):
                                _episode_wanted = int(_episode_wanted)
                                break
                    else:
                        _episode_wanted = 0
                    _episode_start = 1 if _episode_wanted == 0 else _episode_wanted
                    _episode_end = _episode_count + 1 if _episode_wanted == 0 else _episode_wanted + 1

                    for curr_episode in range(_episode_start, _episode_end):
                        if _episode_song_count_list[curr_episode - 1] == 0:
                            print("\n No song(s) in {} S{}.E{}".format(_show_name, curr_season, curr_episode))
                            continue
                        _episode_soup = getSoup(_base_url, _input_name, curr_season, _episode_id_list[curr_episode - 1])
                        _episode_js = "{" + _episode_soup[_episode_soup.find('"alertMessage"'): _episode_soup.find('}};') + 2]
                        _episode_json = json.loads(_episode_js)
                        _episode_song_big = _episode_json['entities']['songs']
                        _episode_song_true = _episode_json['entities']['song_event']
                        _episode_artist = _episode_json['entities']['artists']

                        print("\n\n {}\n S{}.E{} - {} Song(s)".format(_show_name, curr_season, curr_episode,
                                                                      _episode_song_count_list[curr_episode - 1]))
                        # song level
                        for song_ct, curr_song in enumerate(_episode_song_true):
                            _song_id = str(_episode_song_true[curr_song]['song_id'])
                            _song_name = _episode_song_big[_song_id]['name']
                            _song_artist = _episode_artist[_episode_song_big[_song_id]['artist']]['name']
                            _song_album = _episode_song_big[_song_id]['album']
                            _song_description = _episode_song_true[curr_song]['description']
                            
                            _song_artist = _song_artist if _song_artist else "No artist"
                            _song_album = _song_album if _song_album else "No album"
                            _song_description = _song_description if _song_description else "No description"


                            print("\n {}. Song: {}\n Artist: {}\n Album: {}\n {}".format(song_ct + 1, _song_name,
                                                                                         _song_artist, _song_album,
                                                                                         _song_description))

                    if not _season_wanted or not _episode_wanted:
                        break    
                    _episode_cont = input("\n Search songs in another Episode of {} S{}? y/n : ".format(_show_name, curr_season))
            if not _season_wanted:
                break
            _season_cont = input("\n Search songs in another Season of {}? y/n : ".format(_show_name))
        _show_cont = input("\n Search songs in another Show? y/n : ")

if __name__ == "__main__":
    main()
