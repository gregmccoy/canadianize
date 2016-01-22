import html2text
import webbrowser
from matthew import Matthew
import urllib2

class Job(object):
    
    def __init__(self):
        print("")

    def get_raw(self, content):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(content.decode('utf8'))

    def read_file(self, infile):
        with open(infile, 'r') as f:
            content = f.read()
        return content

    def html_email(self, infile):
        content = self.read_file(infile)
        matthew = self.process_email(content)
        return matthew
    
    def url_email(self, url):
        response = urllib2.urlopen(url)
        content = response.read()
        matthew = self.process_email(content)
        return matthew
    
    def url_article(self, url):
        response = urllib2.urlopen(url)
        content = response.read()
        matthew = self.process_article(content)
        return matthew
    
    def process_email(self, content):
        matthew = Matthew(content, self.get_raw(content))
        matthew.ignore_css()
        matthew.links()
        matthew.change()
        matthew.preheader()
        matthew.times()
        matthew.replace_source_codes()
        matthew.fix_spelling()
        matthew.fix_css()
        return matthew
    
    def process_article(self, content):
        content = content[content.find('<div class="article-content">'):]
        matthew = Matthew(content, self.get_raw(content), "article")
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

        