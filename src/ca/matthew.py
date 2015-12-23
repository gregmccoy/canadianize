from datetime import datetime, timedelta
import pytz
import csv
import enchant
import re

class Matthew(object):

    def __init__(self, content=None, raw=None):
        self.ignores= {"color=":"^CSS_COLOR^", '"center"':"^CSS_CENTER_1^", 'center':"^CSS_CENTER_2^", "mygfa.org":"^MYGFA^"}
        tz = pytz.timezone('Canada/Eastern')
        now = pytz.utc.localize(datetime.utcnow())
        self.is_dst = now.astimezone(tz).dst() != timedelta(0)
        replaces = []
        with open("data/replace.csv") as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                replaces.append(row)
        self.replaces = replaces
        self.content = content
        self.raw = raw


    def set_content(self, content):
        self.content = content
        return 0
    def get_content(self):
        return self.content
    def set_raw(self, raw):
        self.raw = raw
        return 0
    def get_raw(self):
        return self.raw


    def preheader(self):
        header = self.content[self.content.find('class="preheader"'):self.content.find('</span>')]
        line = header.replace("#333333", "#edf1f5")
        self.content = self.content.replace(header, line)
        return self.content

    def links(self):
        replaces = []
        with open("data/links.csv") as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                replaces.append(row)
        for row in replaces:
            if self.content.find(row[0]) != -1:
                print('* Replacing "' + row[0] + '" with "' + row[1] + '" *')
                self.content = self.content.replace(row[0], row[1])
        return 0


    def fix_css(self):
        for key, value in self.ignores.iteritems():
            self.content = self.content.replace(value, key)
        return self.content


    def ignore_css(self):
        for key, value in self.ignores.iteritems():
            self.content = self.content.replace(key, value)
        return self.content


    def is_salu(self):
        if self.content.find("%%SALU%%") != -1:
            return True
        return False


    def times(self):
        if self.is_dst:
            self.content = self.content.replace(" CST", " EDT")
            self.content = self.content.replace(" CDT", " EDT")
            self.raw = self.raw.replace(" CST", " EDT")
            self.raw = self.raw.replace(" CDT", " EDT")
        else:
            self.content = self.content.replace(" CST", " EST")
            self.content = self.content.replace(" CDT", " EST")
            self.raw = self.raw.replace(" CST", " EST")
            self.raw = self.raw.replace(" CDT", " EST")
        return 0
    
    
    def get_source_codes(self):
        motivs = []
        for i in range(0, self.content.count("motiv=")):
            motiv = self.content.split("motiv=")[i + 1].split(" ")[0].split("&")[0].split('"')[0]
            motivs.append(motiv)
        return sorted(list(set(motivs)))


    def replace_source_codes(self):
        codes = self.get_source_codes()
        for code in codes:
            choice = raw_input("Replace Source Code - " + str(code) + " ? (y/n)")
            if choice == "y":
                source = raw_input("Enter new source code: ")
                self.content = self.content.replace(code, source)
                self.raw.replace(code, source)
        return 0


    def change(self):
        for row in self.replaces:
            if self.raw.find(row[0]) != -1:
                print('* Replacing "' + row[0] + '" with "' + row[1] + '" *')
                self.content = self.content.replace(row[0], row[1])
                self.raw = self.raw.replace(row[0], row[1])
        return 0


    def fix_spelling(self):
        dictCA = enchant.DictWithPWL("en_CA", "data/words")
        dictUS = enchant.DictWithPWL("en_US", "data/words")
        wordlist = re.sub("[^\w]", " ",  self.raw).split()
        for word in wordlist:
            if not dictCA.check(word) and dictUS.check(word):
                new = dictCA.suggest(word)
                print("Non-Canadian Word - *" + word + "* Replace with? ")
                for counter, option in enumerate(new):
                    print(str(counter) + " - " + option)
                    if counter > 10:
                        break;
                print("Don't replace - q")
                choice = raw_input("Select Replacment\n")
                if choice != "q":
                    self.content = self.content.replace(word, new[int(choice)])
        return 0

    def get_links(self):
        links = []
        code = self.content
        for i in range(0, code.count("<a ")):
            link = code.split("<a ")[i + 1].split("</a>")[0].split('href="')[1].split('"')[0]
    
            links.append(link)
        return sorted(list(set(links)))


    def get_images(self):
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
        code = self.content
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
    
    def make_table(self, items):
        table_str = ""
        for i in items:
            table_str += "<tr><td>" + str(i) + "</td></tr>"
        return table_str
    
    def image_table(self, items):
        table_str = ""
        for i in items:
            table_str += "<tr><td><img src='" + str(i["src"]) + "'></td><td>" + str(i["alt"]) + "</td></tr>"
        return table_str