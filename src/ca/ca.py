import sys
import os
import argparse
import csv
import pytz
import webbrowser
from datetime import datetime, timedelta
from HTMLParser import HTMLParser
import enchant
import html2text
import re


def fix_css(content, verse):
    content = content.replace("^CSS_COLOR^", "color=")
    content = content.replace('^CSS_CENTER_1^', '"center"')
    content = content.replace("^CSS_CENTER_2^", "'center'")
    content = content.replace("mygfa.ca", "mygfa.org")
    content = content.replace("^CSS_VERSE^", verse)

    return content


def ignore_css(content):
    content = content.replace("color=", "^CSS_COLOR^")
    content = content.replace('"center"', "^CSS_CENTER_1^")
    content = content.replace("'center'", "^CSS_CENTER_2^")
    verse_index = content.find(' class="verse"')
    if verse_index != -1 and content.find('</td>') != -1:
        verse = content[verse_index:content.find('</td>', verse_index)]
        print(verse)
        content = content.replace(verse, "^CSS_VERSE^")
    return verse, content


def fix_spelling(content):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    verse, content = ignore_css(content)
    raw = h.handle(content)
    content = links(content)
    raw, content = change(raw, content)
    dictGB = enchant.DictWithPWL("en_CA", "data/words")
    dictUS = enchant.DictWithPWL("en_US", "data/words")
    wordlist = re.sub("[^\w]", " ",  raw).split()
    for word in wordlist:
        if not dictGB.check(word) and dictUS.check(word):
            new = dictGB.suggest(word)
            print("Non-Canadian Word - *" + word + "* Replace with? ")
            for counter, option in enumerate(new):
                print(str(counter) + " - " + option)
            print("Don't replace - q")
            choice = raw_input("Select Replacment\n")
            if choice != "q":
                content = content.replace(word, new[int(choice)])
    content = fix_css(content, verse)
    process_content(content)
    return content


def is_dst(zonename):
    tz = pytz.timezone(zonename)
    now = pytz.utc.localize(datetime.utcnow())
    return now.astimezone(tz).dst() != timedelta(0)


def times(content):
    if is_dst('Canada/Eastern'):
        content = content.replace(" CST", " EDT")
        content = content.replace(" CDT", " EDT")
    else:
        content = content.replace(" CST", " EST")
        content = content.replace(" CDT", " EST")
    return content

def preheader(content):
    header = content[content.find('class="preheader"'):content.find('</span>')]
    line = header.replace("#333333", "#edf1f5")
    content = content.replace(header, line)
    return content

def links(content):
    replaces = []
    with open("data/links.csv") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            replaces.append(row)
    for row in replaces:
        print('* Replacing "' + row[0] + '" with "' + row[1] + '" *')
        content = content.replace(row[0], row[1])
    return content
    

def change(raw, content):
    replaces = []
    with open("data/replace.csv") as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            replaces.append(row)
    for row in replaces:
        if raw.find(row[0]) != -1:
            print('* Replacing "' + row[0] + '" with "' + row[1] + '" *')
            content = content.replace(row[0], row[1])
            raw = raw.replace(row[0], row[1])
    content = preheader(content)
    content = times(content)
    return raw, content


def get_source_codes(code):
    motivs = []

    for i in range(0, code.count("motiv=")):
        motiv = code.split("motiv=")[i + 1].split(" ")[0].split("&")[0].split('"')[0]
        motivs.append(motiv)

    return sorted(list(set(motivs)))


def get_links(code):
    links = []
    for i in range(0, code.count("<a ")):
        link = code.split("<a ")[i + 1].split("</a>")[0].split('href="')[1].split('"')[0]

        links.append(link)
    return sorted(list(set(links)))


def get_images(code):
    images = []

    ignore_images = [
        "http://www.gfamedia.org/email/digest/218/email-digest-header-transforming-communities.gif",
        "http://www.gfamedia.org/email/digest/email-digest-header.gif",
        "http://www.gfamedia.org/email/digest/gospel-for-asia-digest-break.gif",
        "http://www.gfamedia.org/email/digest/208/digest-whiteside.gif",
        "http://www.gfamedia.org/email/digest/208/digest-whiteside-right.gif",
        "http://www.gfamedia.org/email/digest/facebook-icon-email.gif",
        "http://www.gfamedia.org/email/digest/twitter-icon-email.gif",
        "http://www.gfamedia.org/email/digest/pinterest-icon-email.gif",
        "http://www.gfamedia.org/email/digest/facebook-icon-email.png",
        "http://www.gfamedia.org/email/digest/twitter-icon-email.png",
        "http://www.gfamedia.org/email/digest/pinterest-icon-email.png",
        "http://www.gfamedia.org/email/digest/youtube-icon-email.png",
        "http://www.gfamedia.org/email/digest/sponsor-footer-1.jpg",
        "http://www.gfamedia.org/email/digest/sponsor-footer-2.jpg",
        "http://www.gfamedia.org/email/digest/sponsor-footer-3.jpg",
        "http://www.gfamedia.org/ca/email/digest/gospel-for-asia-digest-header-3.gif",
        "http://www.gfamedia.org/ca/email/digest/tagline.gif",
        "{{ spot.image }}",
        "http://www.gfamedia.org/ca/email/digest/share-fb.gif",
        "http://www.gfamedia.org/ca/email/digest/share-twitter.gif",
        "http://www.gfamedia.org/ca/email/digest/find-fb.gif",
        "http://www.gfamedia.org/ca/email/digest/find-twitter.gif",
        "http://www.gfamedia.org/ca/email/digest/find-pin.gif",
        "http://www.gfamedia.org/ca/email/digest/find-wp.gif",
        "http://gfamedia.org/email/digest/twitter-icon-email.gif",
        "http://gfamedia.org/email/pray/pray-header.gif",
        "http://gfamedia.org/email/pray/pray-footer.gif",
        "http://www.gfamedia.org/email/icon_kpsig.gif",
        "http://gfamedia.org/email/pray/pray-left.gif",
        "http://gfamedia.org/email/pray/pray-right.gif",
        "http://www.gfamedia.org/email/nolonger/outreach/bullet.jpg",
        "http://www.gfamedia.org/email/digest/1x1.jpg",
    ]

    for i in range(0, code.count("<img")):
        image = code.split("<img")[i + 1].replace('alt="-->"', '').split(">")[0]

        try:
            image_url = image.split('src="')[1].split('"')[0]
        except:
            image_url = ""

        try:
            alt = image.split('alt="')[1].split('"')[0]
        except:
            alt = None

        if image_url not in ignore_images:
            images.append(dict(
                src=image_url,
                alt=alt,
            ))

    return images

def make_table(items):
    table_str = ""
    for i in items:
        table_str += "<tr><td>" + str(i) + "</td></tr>"
    return table_str

def image_table(items):
    table_str = ""
    for i in items:
        table_str += "<tr><td><img src='" + str(i["src"]) + "'></td><td>" + str(i["alt"]) + "</td></tr>"
    return table_str

def process_content(content):
    links = get_links(content)
    codes = get_source_codes(content)
    images = get_images(content)
    with open("data/template.html", 'r') as f:
        html = f.read()
        html = html.replace("*LINKS*", make_table(links))
        html = html.replace("*SOURCE*", make_table(codes))
        html = html.replace("*IMAGES*", image_table(images))

        with open("data/result.html", 'w+') as o:
            o.write(html)
            webbrowser.open('file://' + os.path.realpath("data/result.html"), new=2)
        

def read_file(infile, outfile):
    content = ""
    with open(infile, 'r') as f:
        content = f.read()
        content = fix_spelling(content)
    if not outfile:
        outfile = "ca-" + infile
    with open(outfile, 'w+') as o:
        o.write(content)
    webbrowser.open('file://' + os.path.realpath(outfile), new=2)
    

#Check for command line
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Enter input filename")
parser.add_argument("-o", dest='outfile', help="optional output file. Defaults to ca + input filename if not set", metavar="outfile")
args = parser.parse_args()
read_file(args.input, args.outfile)