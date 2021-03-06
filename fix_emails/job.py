import html2text
from fix_emails.matthew import Matthew
from urllib.request import urlopen

class Job(object):

    def __init__(self, verbose, input_type="email"):
        self.debug = verbose
        self.input_type = input_type


    def get_raw(self, content):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(content).replace("\n", "")

    def read_file(self, infile):
        with open(infile, 'r') as f:
            content = f.read()
        return content

    def html_email(self, infile, source_code=None, country=None):
        content = self.read_file(infile)
        matthew = self.process_email(content, source_code=source_code, country=country)
        return matthew

    def url_email(self, url):
        response = urlopen(url)
        content = response.read()
        matthew = self.process_email(content)
        return matthew

    def url_article(self, url):
        response = urlopen(url)
        content = response.read()
        matthew = self.process_article(content)
        return matthew

    def process_email(self, content, source_code=None, country=None):
        matthew = Matthew(content, self.get_raw(content), input_type=self.input_type, verbose=self.debug, source_code=source_code, country=country)
        matthew.ignore_css()
        matthew.links()
        matthew.change()
        if self.debug:
            print("Second Pass\n")
            matthew.change()
            print("Second Pass complete")
            print("+ Test Raw for replaced content Result = " + str(matthew.get_raw().find("center")))
        matthew.preheader()
        matthew.times()
        if source_code:
            matthew.replace_source_codes()
        matthew.raw = self.get_raw(matthew.content)
        matthew.fix_spelling()
        matthew.fix_css()
        return matthew

    def process_article(self, content):
        #content = content[content.find('<div class="article-content">'):]
        matthew = Matthew(content, self.get_raw(content), "article", verbose=self.debug)
        matthew.remove_js()
        matthew.set_raw(self.get_raw(matthew.get_content()))
        matthew.ignore_css()
        matthew.change()
        matthew.times()
        matthew.replace_source_codes()
        matthew.fix_spelling()
        matthew.fix_css()
        matthew.remove_images()
        return matthew

    def run_results(self, content, country=None):
        matthew = Matthew(self.read_file(content), self.get_raw(content), verbose=self.debug, input_type=self.input_type, country=country)
        return matthew

    def html_result(self, matthew):
        links = matthew.get_links()
        codes = matthew.get_source_codes()
        images = matthew.get_images()
        html = self.read_file("data/template.html")
        html = html.replace("*LINKS*", matthew.make_table(links))
        html = html.replace("*SOURCE*", matthew.make_table(codes))
        html = html.replace("*IMAGES*", matthew.image_table(images))
        if not matthew.is_salu():
            print("* WARNING NO SALU DETECTED *")
            html = html.replace("Salu found", "* WARNING NO SALU DETECTED *")
        return html


