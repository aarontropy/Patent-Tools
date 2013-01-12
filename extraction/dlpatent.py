import urllib2
import MySQLdb as mdb
from datetime import datetime
from BeautifulSoup import BeautifulSoup, SoupStrainer
import os

import PatentTools.schema as schema
from sqlalchemy.orm import sessionmaker

PROJ_DIR = os.path.dirname(os.path.realpath(__file__))
DL_DIR = os.path.join(PROJ_DIR, 'Temp')

if not os.path.exists(DL_DIR):
	os.makedirs(DL_DIR)


URL_BIB = 'http://www.google.com/googlebooks/uspto-patents-grants-biblio.html'
# DBSERVER = '127.0.0.1'
# USERNAME = 'PatentTools'
# PASSWORD = 'PatentTools'
# DATABASE = 'PatentTools'


def bib_urls():
	response = urllib2.urlopen(URL_BIB).read()
	urls = []

	for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
		if link.has_key('href') and link['href'].find('.zip') != -1:
			urls.apend(link['href'])


def download_next_bib(n=1):

	# Create the needed tables if they don't exist
	# create_retrieve_tables()

	# Get the needed database stuff 
	db = schema.engine()
	db.echo = False

	Session = sessionmaker(bind=db)
	session = Session()

	# Get a list of files we've already downloaded
	q = session.query(schema.FileDownloadRecord.url).distinct()
	dl_urls = [url for url in q]

	# get a list of files on the webpage
	urls = [url for url in bib_urls()]
	# files = [filename[filename.rfind('/')+1:] for filename in urls]

	# list of files to retrieve 
	urls_to_retrieve = list(set(urls) - set(dl_urls) )

	for dl_url in urls_to_retrieve[:n]:
		remotefile = urllib2.urlopen(dl_url)
		dl_filename = dl_url[dl_url.rfind('/')+1:]
		localfile = open( os.path.join(DL_DIR, dl_filename), 'w' )
		localfile.write(remotefile.read())
		localfile.close()

		# save the record of this download
		dlRec = schema.FileDownloadRecord()
		dlRec.url = dl_url
		dlRec.tmpFilename = localfile
		dlRec.downloadDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		dlRec.imported = False
		session.add(dlRec)
		session.commit()


if __name__ == '__main__':
	download_next_bib()

