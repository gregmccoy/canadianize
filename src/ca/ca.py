import sys
import os
import argparse
import csv
import pytz
import webbrowser
from datetime import datetime, timedelta
from HTMLParser import HTMLParser
from job import Job

def read_file(infile, outfile):
    if not outfile:
        outfile = "ca-" + infile
    
    job = Job()
    obj = job.html_email(infile)
    html = job.html_result(obj)
    
    with open(outfile, 'w+') as o:
        o.write(obj.get_content())
    
    with open("data/result.html", 'w+') as o:
        o.write(html)
        
    webbrowser.open('file://' + os.path.realpath(outfile), new=2)
    webbrowser.open('file://' + os.path.realpath("data/result.html"), new=2)
    
    print("Goodbye!")

#Check for command line
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Enter input filename")
parser.add_argument("-o", dest='outfile', help="optional output file. Defaults to ca + input filename if not set", metavar="outfile")
args = parser.parse_args()
read_file(args.input, args.outfile)
