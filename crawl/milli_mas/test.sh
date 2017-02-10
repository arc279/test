#!/bin/bash

#set -eu

function step1() {
    test ! -d work/ && mkdir work
    curl -s "http://imas-million.zukan-jp.com/card_all/" | \
        tee work/card_all.html | \
        python extract.py card_pages > work/pagelist.txt
}

function step2() {
    :> work/imagelist.txt

    cat work/pagelist.txt | while read page; do
        DST="work/page.${page}.html"
        TARGET=$(printf "http://imas-million.zukan-jp.com/card_all/page/%s/" $page)
        echo "$TARGET -> $DST"
        curl -sL $TARGET | tee ${DST} | python extract.py img_urls >> work/imagelist.txt
        #sleep 1
    done
}

function step3() {
    cat work/imagelist.txt | cut -f 1 | wget -w 1 -nc -x -i -
}

