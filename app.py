# Robust, Efficient approach.

import json, re, requests

from bs4 import BeautifulSoup
from slugify import slugify

# https://www.tunefind.com/show/louie/season-1/
_base_url = "https://www.tunefind.com/show/{}/{}/{}"

def getSoup(_url, _name, _season="", _episode_link=""):
    """
    Returns a html-parsed-BeautifulSoup object for the given URL.
    @params:
    _url: String: the http(s) link to get html from
    _name: String: name of the show|movie
    _season: Integer: season number of the show|movie
    _episode_link: Integer: Unique number for the episode to form its hyperlink.
    """
    if _season:
        _season = 'season-' + str(_season)
    try:
        # print(_url.format(_name, _season, _episode_link))
        r = requests.get(_url.format(_name, _season, _episode_link))

    except Exception:
        exit("\n***ERROR. Check Internet and Input again:\n")    

    return BeautifulSoup(r.text, 'html.parser')

if __name__ == "__main__":
    _input_name = slugify(input("Name of the show: ").strip())
    _soup = getSoup(_base_url, _input_name)
    _soup_text = _soup.get_text()
    _js = "{" + _soup_text[_soup_text.find('"alertMessage"'): _soup_text.find('}};') + 2]
    # main source of data
    _json = json.loads(_js)
    
    # show level
    _show_cont = 'y'
    while _show_cont == 'y' or _show_cont == 'Y':
        try:
            _json_show = _json['show']['result']
            _show_name = _json_show['show']['name']
            _season_id_list = _json_show['seasons']
            _season_count = len(_season_id_list)
            _latest_ep = _json_show['latest_episode']

            print("\n", _show_name, "\n Total Seasons:", _season_count)
            # each season's details
            for _season_id in _season_id_list:
                # TODO: Store this info. Create database.
                _season_id = str(_season_id)
                _season_name = _json['entities']['seasons'][_season_id]['group_name']
                _season_num = _json['entities']['seasons'][_season_id]['group_sequence']
                _season_song_count = _json['entities']['seasons'][_season_id]['songs_count']
                _season_episode_count = _json['entities']['seasons'][_season_id]['episodes_count']

                print("\n ", _season_name, "    Episodes: ", _season_episode_count, "    Songs: ",
                    _season_song_count, sep="")
        except KeyError:
            print("Show not found.")
        
        # season level
        _season_cont = 'y'
        while _season_cont == 'y' or _season_cont == 'Y':
            _season_wanted = int(input("\n Choose SEASON. 1 to {} (0 for all): ".format(_season_count)))
            _season_start = 1 if _season_wanted == 0 else _season_wanted
            _season_end = _season_count + 1 if _season_wanted == 0 else _season_wanted + 1

            for curr_season in range(_season_start, _season_end):
                _season_soup = getSoup(_base_url, _input_name, curr_season)
                _season_soup_text = _season_soup.get_text()
                _season_js = "{" + _season_soup_text[_season_soup_text.find('"alertMessage"'): _season_soup_text.find('}};') + 2]
                _season_json = json.loads(_season_js)

                _episode_id_list = _season_json['season']['episodes']
                _episode_count = len(_episode_id_list)

                for _episode_id in _episode_id_list:
                    _episode_id = str(_episode_id)
                    _episode_name = _season_json['entities']['episodes'][_episode_id]['name']
                    _episode_num = _season_json['entities']['episodes'][_episode_id]['number']
                    _episode_aired = _season_json['entities']['episodes'][_episode_id]['airdate_day'] + \
                                    " " + _season_json['entities']['episodes'][_episode_id]['airdate_month_short'] + \
                                    " " + _season_json['entities']['episodes'][_episode_id]['airdate_year']
                    _episode_description = _season_json['entities']['episodes'][_episode_id]['episode_description']
                    _episode_song_count = _season_json['entities']['episodes'][_episode_id]['song_count']

                    print("\n S", curr_season, ".E", _episode_num, " ", _episode_name, "    Aired on: ", 
                        _episode_aired, "    Songs: ", _episode_song_count, "\n ",
                        _episode_description, sep="")

                # episode level
                _episode_cont = 'y'
                while _episode_cont == 'y' or _episode_cont == 'Y':
                    _episode_wanted = int(input("\n Choose EPISODE. 1 to {} (0 for all): ".format(_season_count)))
                    _episode_start = 1 if _episode_wanted == 0 else _episode_wanted
                    _episode_end = _episode_count + 1 if _episode_wanted == 0 else _episode_wanted + 1

                    for curr_episode in range(_episode_start, _episode_end):
                        _episode_soup = getSoup(_base_url, _input_name, curr_season, _episode_id_list[curr_episode - 1])
                        _episode_soup_text = _episode_soup.get_text()
                        _episode_js = "{" + _episode_soup_text[_episode_soup_text.find('"alertMessage"'): _episode_soup_text.find('}};') + 2]
                        _episode_json = json.loads(_episode_js)
                        _episode_song_big = _episode_json['entities']['songs']
                        _episode_song_true = _episode_json['entities']['song_event']
                        _episode_artist = _episode_json['entities']['artists']
                        
                        print("\n S", curr_season, ".E", curr_episode, sep="")
                        # song level
                        for ct, curr_song in enumerate(_episode_song_true):
                            _song_id = str(_episode_song_true[curr_song]['song_id'])
                            _song_name = _episode_song_big[_song_id]['name']
                            _song_artist = _episode_artist[_episode_song_big[_song_id]['artist']]['name']
                            _song_album = _episode_song_big[_song_id]['album']
                            _song_description = _episode_song_true[curr_song]['description']

                            print("\n ", ct + 1, ". Song: ", _song_name, "\n Artist: ", _song_artist,
                             "\n Album: ", _song_album , "\n ", _song_description, sep="")

                    _episode_cont = input("\n Looking for another Episode? y/n : ")
            _season_cont = input("\n Looking for another Season? y/n : ")
        _show_cont = input("\n Looking for another Show? y/n : ")

# TODO:
# Formatting. Song, Artist, Album alignment.
# Caching. Database.
# Download
