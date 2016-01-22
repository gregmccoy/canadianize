import sys
import os
import argparse
import csv
import pytz
import webbrowser
from datetime import datetime, timedelta
from HTMLParser import HTMLParser
from job import Job


def read_file(infile, outfile, url, article):
    html = None
    if not outfile:
        outfile = "default.html"
        
    job = Job()

    if url is not None and infile is not None:
        print("Cannot use both -u and -f choose one")
    elif url is not None:
        if article:
            obj = job.url_article(url)
        else:
            obj = job.url_email(url)
            html = job.html_result(obj)
    elif infile is not None:
        obj = job.html_email(infile)
        html = job.html_result(obj)

    with open(outfile, 'w+') as o:
        data = obj.get_content()
        o.write(data)
    
    if html is not None:
        with open("data/result.html", 'w+') as o:
            o.write(html)
        webbrowser.open('file://' + os.path.realpath("data/result.html"), new=2)
        
    webbrowser.open('file://' + os.path.realpath(outfile), new=2)
    
    
    print("Goodbye!")

#Check for command line
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest='input', help="Enter input filename", metavar="input")
parser.add_argument("-o", dest='outfile', help="optional output file. Defaults to ca + input filename if not set", metavar="outfile")
parser.add_argument("-u", dest='url', help="specifies the input is a url", metavar="url")
parser.add_argument("-a", dest='article', help="used to check an article", action="store_true")
args = parser.parse_args()
read_file(args.input, args.outfile, args.url, args.article)
