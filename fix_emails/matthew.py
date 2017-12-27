from datetime import datetime, timedelta
from fix_emails.utils import readConf, readCSV, get_image_ignores
import pytz
import enchant
import re


class Matthew(object):

    def __init__(self, content=None, raw=None, input_type="email", verbose=False, source_code=None, country=None):
        self.ignores= {"color=":"^CSS_COLOR^", '"center"':"^CSS_CENTER_1^", "'center'":"^CSS_CENTER_2^", "mygfa.org":"^MYGFA^", "<center>": "^CENTER_TAG^"}
        self.content = content
        self.raw = raw
        self.input_type = input_type
        self.debug = verbose

        if not country:
            if self.input_type == "qt":
                self.country = "CA"
            else:
                self.country = readConf("country")
        else:
            self.country = country

        self.source_code = source_code

        replaces = readCSV('data/replace_{}.csv'.format(self.country), '|')
        self.replaces = replaces

        tz = pytz.timezone('Canada/Eastern')
        now = pytz.utc.localize(datetime.utcnow())
        self.is_dst = now.astimezone(tz).dst() != timedelta(0)

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    def set_raw(self, raw):
        self.raw = raw

    def get_raw(self):
        return self.raw


    def preheader(self):
        header = self.content[self.content.find('class="preheader"')-100:self.content.find('</span>')]
        line = header.replace("#333333", "#edf1f5")
        self.content = self.content.replace(header, line)
        return self.content


    def links(self):
        replaces = readCSV('data/links_{}.csv'.format(self.country), '|')
        for row in replaces:
            if self.content.find(row[0]) != -1:
                print('* Replacing "' + row[0] + '" with "' + row[1] + '" *')
                self.content = self.content.replace(row[0], row[1])


    def fix_css(self):
        for key, value in self.ignores.items():
            self.content = self.content.replace(value, key)
        return self.content


    def ignore_css(self):
        for key, value in self.ignores.items():
            self.content = self.content.replace(key, value)
        return self.content


    def is_salu(self):
        if self.content.find("%%SALU%%") != -1:
            return True
        return False


    def times(self):
        if self.country == "CA":
            if self.content.find("CST") != -1 or self.content.find("CDT") != -1:
                print("* Handling CST/CDT")
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


    def get_source_codes(self):
        motivs = []
        for i in range(0, self.content.count("motiv=")):
            #Gets the source code based on motiv=
            motiv = self.content.split("motiv=")[i + 1].split(" ")[0].split("&")[0].split('"')[0]
            motivs.append(motiv)
        return sorted(list(set(motivs)))


    def replace_source_codes(self):
        codes = self.get_source_codes()
        for code in codes:
            if self.input_type == "qt":
                print("Replacing {} with {}".format(code, self.source_code))
                self.content = self.content.replace(code, self.source_code)
                self.raw.replace(code, self.source)
            else:
                choice = input("Replace Source Code - " + str(code) + " ? (y/n)")
                if choice == "y":
                    source = input("Enter new source code: ")
                    self.content = self.content.replace(code, source)
                    self.raw.replace(code, source)


    def safe_replace(self, old, new):
        index = self.content.find(old)
        while index != -1:
            ignores = ["'", '"', "-", "#", "/", ":", "u"]
            start_or_end = [" ", ">", "<", ",", ".", "?", "!"]
            beginchar = self.content[index - 1]
            endchar = self.content[index + len(old)]
            first = self.content[index]
            if beginchar in start_or_end or endchar in start_or_end:
                if beginchar not in ignores and endchar not in ignores:
                    try:
                        sindex = index - 5
                        if sindex < 0:
                            sindex = 0
                        eindex = index + len(old) + 5
                        if eindex > len(self.content):
                            eindex = len(self.content)
                        startfive = self.content[sindex:index]
                        endfive = self.content[index + len(old):eindex]

                        repstr = self.content[sindex:eindex]

                        print(('* Replacing "' + old + '" with "' + new + '" *'))
                        self.content = self.content.replace(repstr, startfive + str(new) + endfive, 1)
                    except:
                        print("Breaking")
                        break
            index = self.content.find(old, index + len(old))


    def change(self):
        for row in self.replaces:
            if self.raw.lower().find(row[0].lower()) != -1:
                if self.debug:
                    print(('+ Input Type = ' + str(self.input_type)))
                if self.input_type == "article":
                    print(('* Replacing "' + row[0] + '" with "' + row[1] + '" *'))
                    self.content = self.content.replace(row[0], "<font color='red'>" + str(row[1]) + "</font>")
                else:
                    self.safe_replace(row[0], row[1])
                    self.safe_replace(row[0].title(), row[1].title())
                self.raw = self.raw.replace(row[0], row[1])
                if self.debug:
                    print(("+ Search Raw for replaced content Result = " + str(self.raw.find(row[0]))))
                    print(("+ Search Content for replaced content Result = " + str(self.content.find(row[0]))))
                    print("\n")


    def fix_spelling(self):
        if self.country == "US":
            dict_check = enchant.DictWithPWL("en_CA", "data/words")
            dict_correct = enchant.DictWithPWL("en_US", "data/words")
        else:
            dict_correct = enchant.DictWithPWL("en_CA", "data/words")
            dict_check = enchant.DictWithPWL("en_US", "data/words")
        wordlist = re.sub("[^\w]", " ",  self.raw).split()
        done = []
        for word in wordlist:
            word = word.replace("_", "")
            if not word.isdigit() and len(word) > 0:
                if not dict_correct.check(word) and dict_check.check(word):
                    if not word in done:
                        new = dict_correct.suggest(word)
                        choice = ""

                        if self.input_type == "qt":
                            choice = "0"
                        else:
                            if self.country == "US":
                                print("Non-American Word - *" + word + "* Replace with? ")
                            else:
                                print("Non-Canadian Word - *" + word + "* Replace with? ")

                            for counter, option in enumerate(new):
                                print(str(counter) + " - " + option)
                                if counter > 10:
                                    break;

                            print("Don't replace - q")
                            choice = input("Select Replacment\n")

                        if choice != "q":
                            if self.input_type == "article":
                                new_word = str(new[int(choice)])
                                self.content = self.content.replace(str(word), "<font color='red'>" + str(new_word) + "</font>")
                            else:
                                self.safe_replace(word, new[int(choice)])
                                done.append(word)


    def get_links(self):
        links = []
        code = self.content
        for i in range(0, code.count("<a ")):
            try:
                link = code.split("<a ")[i + 1].split("</a>")[0].split('href="')[1].split('"')[0]
                links.append(link)
            except Exception as e:
                print("Failed to record a link\n---\n" + str(e) + "\n---")
        return sorted(list(set(links)))


    def get_images(self):
        images = []
        ignore_images = get_image_ignores()
        for i in range(0, self.content.count("<img")):
            image = self.content.split("<img")[i + 1].replace('alt="-->"', '').split(">")[0]

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

    def remove_images(self):
        while self.content.find("<img") != -1:
            self.content = self.content.replace(self.content[self.content.find("<img"):(self.content.find(">", self.content.find("<img"))+1)], "")

    def remove_js(self):
        while self.content.find("<script") != -1:
            self.content = self.content.replace(self.content[self.content.find("<script"):(self.content.find("</script>", self.content.find("<script"))+9)], "")

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
