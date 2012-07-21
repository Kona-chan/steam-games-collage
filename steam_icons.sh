#!/bin/bash

function cleanup() {
    if [ -d "steam_icons" ] ; then rm -r steam_icons ; fi
}
trap cleanup INT EXIT QUIT TERM

if [ -z "$1" ] ; then
    echo "Syntax: ./steam_icons.sh steam_username"
    exit
fi

username="$1"
profile_url="http://steamcommunity.com/id/$username/games?tab=all&xml=1"

echo "Fetching icons..."

if [ -d "steam_icons" ] ; then
    rm -r steam_icons
fi
mkdir steam_icons

wget -q -O- $profile_url |\
    grep appID |\
    egrep -o [0-9]+ |\
    sed -e 's#\(.*\)#http://cdn.steampowered.com/v/gfx/apps/\1/header_292x136.jpg#' |\
    wget -q -i- -P ./steam_icons

function round_corner() {
    convert $1 \
    \( +clone  -alpha extract \
        -draw 'fill black polygon 0,0 0,15 15,0 fill white circle 15,15 15,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
    \) -alpha off -compose CopyOpacity -composite $1.png
}

echo "Applying rounded corners..."

for i in $( find steam_icons -iname '*jpg*' ) ; do
    round_corner "$i"
done

function make_grid() {
    montage \
        -background "#292929" \
        -tile 8x \
        -geometry +1+1 \
        steam_icons/*.png $1
}

echo "Merging grid..."

make_grid "montage.jpg"

echo "Done!"
