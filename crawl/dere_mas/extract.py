#!/usr/bin/env python
# coding: utf-8

import os
import sys
import csv
import lxml.html
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("--input", default=sys.stdin, type=click.File('rb'))
@click.option("--output", default=sys.stdout, type=click.File('wb'))
def idle_ids(input, output):
    dom = lxml.html.parse(input)
    elems = dom.xpath('//a[@class="idol-link"]')

    def inner(elem):
        href = elem.attrib["href"]
        id = href.split("/")[-1]
        name = elem.xpath('div[@class="idol-name"]')
        return id, name[0].text.strip()

    w = csv.writer(output, delimiter="\t", lineterminator='\n')
    for x in map(inner, elems):
        w.writerow(x)


@cli.command()
@click.option("--input", default=sys.stdin, type=click.File('rb'))
@click.option("--output", default=sys.stdout, type=click.File('wb'))
def idle_hases(input, output):
    dom = lxml.html.parse(input)
    elems = dom.xpath('//a[@class="card-img"]')

    def inner(elem):
        parts = elem.attrib["href"].split("/")
        hash = os.path.splitext(parts[-1])[0]
        return hash, elem.attrib["title"]

    w = csv.writer(output, delimiter="\t", lineterminator='\n')
    for x in dict(map(inner, elems)).items():
        w.writerow(x)

if __name__ == '__main__':
    cli()
