#!/bin/bash

#set -eu

SIZE=(
    l
    xs
)

function step1() {
    test ! -d work/ && mkdir work
    curl -s "http://imas.gamedbs.jp/cg/" | \
        tee work/index.html | \
        python extract.py idle_ids | \
        sort -n > work/idle_ids.tsv
}

function step2() {
    cat work/idle_ids.tsv | while IFS=$'\t' read id name; do
        DST1="work/${id}.${name}.html"
        DST2="work/${id}.${name}.hash.tsv"
        TARGET=$(printf "http://imas.gamedbs.jp/cg/idol/detail/%s" $id)
        echo $DST2
        curl -s $TARGET | tee ${DST1} | python extract.py idle_hases > ${DST2}
        #sleep 1
    done
}

function step3() {
    cat work/*.hash.tsv | while IFS=$'\t' read hash name; do
        for x in ${SIZE[@]}; do
            printf "http://imas.gamedbs.jp/cg/image_sp/card/%s/%s.jpg\n" $x $hash
        done
    done | tee work/imagelist.txt | wget -w 1 -nc -x -i -
}

