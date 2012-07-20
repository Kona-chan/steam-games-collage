#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import re
import json
from operator import itemgetter # for sorting purposes
import os

def parse_file(filename):

    regex = re.compile("^var rgGames = (.*);$")
    for games_json in open(filename):
        if regex.match(games_json):
            return regex.sub("\g<1>", games_json)
    return ""
    

def parse_profile(steam_username):
    """Receive games list in JSON format."""
    # Obtain webpage containing games list.
    f = urllib.request.urlopen(
            "http://steamcommunity.com/id/%s/games?tab=all" %
            steam_username)
    games_list = f.read().decode("utf-8").splitlines()

    # Look for actual games list in the obtained page.
    # It is stored in rgGames variable.
    # The result is a JSON string.
    regex = re.compile("^var rgGames = (.*);$")
    for games_json in games_list:
        if regex.match(games_json):
            return regex.sub("\g<1>", games_json)
    return ""


def save_icons(games_json):
    """Returns count of icons."""
    # Obtain sorted games list from JSON string.
    # games is a list containing JSON objects.
    games = sorted(json.loads(games_json), key=itemgetter('name'))

    # Saving icons in files named '\d+.jpg'.
    for index, game in enumerate(games):
        print('Fetching %s icon' % game['name'])
        try:
            urllib.request.urlretrieve(game['logo'], 
                    'icons/%i.jpg' % index)
        except IOError:
            pass

    return len(games)


def save_big_icons(games_json):

    games = sorted(json.loads(games_json), key=itemgetter('name'))

    for index, game in enumerate(games):
        print('Fetching %s icon' % game['name'])
        try:
            urllib.request.urlretrieve('http://cdn.steampowered.com/v/gfx/apps/%s/header_292x136.jpg' %
                    game['appid'],
                    'icons/%i.jpg' % index)
        except IOError:
            pass
        except ValueError:
            print('no icon')
            pass


def count_icons():
    """Returns number of icons in icons directory."""
    return len(os.listdir('./icons'))


def compose_grid(total_icons, cols=8):
    """Create grid from obtained icons using Imagemagick."""
    os.system('montage -background "#292929" -tile %ix -geometry +1+1 "icons/%%d.jpg[0-%i]" montage.jpg' %
            (cols, total_icons-1))


#games_json = parse_file("file.in")
#save_big_icons(games_json)
total_icons = count_icons()
compose_grid(total_icons)
