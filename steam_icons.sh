#!/bin/bash

username="$1"
profile_url="http://steamcommunity.com/id/$username/games?tab=all&xml=1"

wget -nv -O- $profile_url |\
    grep appID |\
    egrep -o [0-9]+ |\
    sed -e 's#\(.*\)#http://cdn.steampowered.com/v/gfx/apps/\1/header_292x136.jpg#' |\
