#!/usr/bin/env python

import sys
import lxml.html
import click
import csv

@click.group()
def cli():
    pass

@cli.command()
@click.option("--input", default=sys.stdin, type=click.File('rb'))
@click.option("--output", default=sys.stdout, type=click.File('wb'))
def card_pages(input, output):
    doc = lxml.html.parse(input)
    elems = doc.xpath('//a[@class="page-numbers"]')
    page_max = int(elems[-1].text)

    for x in range(1, page_max):
        print(x, file=output)

@cli.command()
@click.option("--input", default=sys.stdin, type=click.File('rb'))
@click.option("--output", default=sys.stdout, type=click.File('wb'))
def img_urls(input, output):
    doc = lxml.html.parse(input)
    elems = doc.xpath('//div[@class="grid-image"]')

    def inner(elem):
        img = elem.xpath('a/img')[0]
        return img.attrib["src"], img.attrib["alt"]

    w = csv.writer(output, delimiter="\t", lineterminator='\n')
    for x in map(inner, elems):
        w.writerow(x)


if __name__ == '__main__':
    cli()
