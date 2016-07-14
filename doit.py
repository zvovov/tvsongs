import csv, re, requests

from bs4 import BeautifulSoup
from slugify import slugify

# https://www.tunefind.com/show/louie/season-1
_base_url = "https://www.tunefind.com/{}/{}/season-{}/{}"
_type = "show"

song_regex = r">([a-z0-9]+)<"

def getSlug(_name):
    """
    Returns slugified string for the Input

    @params:
    _name: String: input string to be slugified
    """
    return slugify(_name)

def getSoup(_url, _type, _name, _season, _episode_link):
    """
    Returns a html-parsed-BeautifulSoup object for the given URL.
    @params:
    _url: String: the http(s) link to get html from
    _type: String: show|movie
    _name: String: name of the show|movie
    _season: Integer: season number of the show|movie
    """
    try:
        r = requests.get(_url.format(_type, _name, _season, _episode_link))
    except Exception:
        exit("\n***ERROR. Check Internet and Input again:\n", _url.format(_type, _name, _season))    

    return BeautifulSoup(r.text, 'html.parser')

# def validateSeason(_entered, _actual):
#     """
#     Returns seasons list if requested seasons are valid for the show. False, otherwise.

#     @params:
#     _entered: String: Season(s) entered by the user. Eg: 1 or 1-3 or 2,5,7,3
#     _actual: Integer: Maximum number of seasons available for the show.
#     """
#     nums = _entered.strip()
#     nums = set(nums)
#     try:
#         if ',' in nums:
#             nums = _entered.split(',')
#             valid = [isinstance(int(i), int) for i in nums]
#             for i in nums:
#                 if int(i) > _actual:
#                     raise ValueError

#         elif _entered.count('-') == 1:
#             nums = _entered.split('-')
#             if len(nums) == 2:
#                 for i in nums:
#                     if int(i) > _actual:
#                         raise ValueError
#                 nums = range(int(nums[0]), int(nums[1]))
#             else:
#                 raise ValueError

#         elif _entered.count('-') > 1:
#             raise ValueError

#     except ValueError:
#         print("Why you gotta be that way? Type correctly now: ")
#         return False

#     return nums

# TODO: for all seasons
if __name__ == "__main__":
    cont_season = 'y'
    _season = 1
    _name = getSlug("orange is the new black")
    print(_name)
    soup = getSoup(_base_url, _type, _name, _season, "")

    _season_count = soup.find_all('ul')[1]
    _season_count = int((_season_count.find_all('li')[-1].find('a')['href'])[-1])
    print("Seasons Found:", _season_count)
    while cont_season == 'y' or cont_season == 'Y':
        _season_wanted = input("Which season's songs do you want to see? 1 to {} (0 for all): ".format(_season_count))
        _season_wanted = int(_season_wanted)
        _season_start = 1 if _season_wanted == 0 else _season_wanted
        _season_end = _season_count + 1 if _season_wanted == 0 else _season_wanted + 1

        for curr_season in range(_season_start, _season_end):
            _season_soup = getSoup(_base_url, _type, _name, curr_season, "")
            _lists = _season_soup.find_all('li')
            _episode_count = 0
            _link_dict = {}
            for i in _lists:
                if i.find('h3'):
                    # TODO: store episode link if _song_count != 0
                    _episode_count += 1
                    _song_count = 0
                    _link = ""
                    _song_count_html = i.find('li')
                    match = re.findall(song_regex, str(_song_count_html))
                    if match:
                        _song_count = match[0]
                        if int(match[0]):
                            pass
                            # Go to each episode page to get song names
                            # https://www.tunefind.com/show/louie/season-1/_link
                            _link = str(i.find('a')['href'])
                            _link_dict[_episode_count] = _link[_link.rfind('/')+1:]

                    _label = i.find('a').string
                    _air_date = i.find('time').string
                    print(_song_count, "songs in", _label, "aired on", _air_date, _link)

            _episode_wanted = input("Which episode's songs do you want to see? 1 to {} (0 for all): ".format(_episode_count))
            _episode_wanted = int(_episode_wanted)
            _episode_start = 1 if _episode_wanted == 0 else _episode_wanted
            _episode_end = _episode_count + 1 if _episode_wanted == 0 else _episode_wanted + 1

            for curr_episode in range(_episode_start, _episode_end):
                if _link_dict.get(curr_episode):
                    # if curr_episode contains non-zero songs, get songs.
                    _episode_soup = getSoup(_base_url, _type, _name, curr_season, _link_dict[curr_episode])
                    _e_title = _episode_soup.title.string[:-11]
                    print(_e_title)
                    print(_episode_soup.get_text())

                    # print(episode_soup.prettify())
        
        cont_season = input("More Seasons? y/n ")


# Input tv show name

# Look it up on Tunefind
#     Not Found
#         Exit
#     Found
#         Read HTML containing Season list
#         Go to each season
#                 Go to each episode
#                     Read HTML containing Songs list
#                     Extract song names
#                     Store song names
#             Display song names
#         Display summary

# Download songs - WIP
