import argparse
from job import Job


def read_file(infile, outfile, url, article, verbose, result):
    job = Job(verbose)

    if not outfile:
        outfile = "default.html"

    if job.debug:
        print("+ Running with debugging output")

    if url is not None and infile is not None:
        print("Cannot use both -u and -f choose one")

    elif url is not None:
        if article:
            obj = job.url_article(url)
            print_outfile(outfile, obj)
        else:
            obj = job.url_email(url)
            print_outfile(outfile, obj)

    elif infile is not None:
        if result:
            obj = job.run_results(infile)
            print_results(obj, job)
        else:
            obj = job.html_email(infile)
            print_outfile(outfile, obj)

            obj = job.run_results(outfile)
            print_results(obj, job)

    #webbrowser.open('file://' + os.path.realpath("data/result.html"), new=2)
    #webbrowser.open('file://' + os.path.realpath(outfile), new=2)
    print("Goodbye!")

def print_outfile(outfile, obj):
    with open(outfile, 'w+') as o:
        data = obj.get_content()
        o.write(data)

def print_results(obj, job):
    html = job.html_result(obj)
    if html is not None:
        with open("data/result.html", 'w+') as o:
            o.write(html)
    print("Results page generated")

#Check for command line
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest='input', help="Enter input filename", metavar="input")
parser.add_argument("-o", dest='outfile', help="optional output file. Defaults to ca + input filename if not set", metavar="outfile")
parser.add_argument("-u", dest='url', help="specifies the input is a url", metavar="url")
parser.add_argument("-a", dest='article', help="used to check an article", action="store_true")
parser.add_argument("-v", dest='verbose', help="enables debugging output", action="store_true")
parser.add_argument("-r", dest='result', help="Generates result page", action="store_true")
args = parser.parse_args()
read_file(args.input, args.outfile, args.url, args.article, args.verbose, args.result)
