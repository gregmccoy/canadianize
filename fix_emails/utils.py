import configparser
import csv

config = configparser.ConfigParser()

def readConf(option):
    config.read("fix_emails.conf")
    value = config['DEFAULT'][option]
    print("Country - {}".format(value))
    return(value)

def readCSV(file, delimiter):
    replaces = []
    with open(file) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            replaces.append(row)
    return replaces

def get_image_ignores():
    return [
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
