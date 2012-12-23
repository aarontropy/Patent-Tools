from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from dateutil import parser

import csv
import os

FILEPATH = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'testdata', 'csv')

testdata = {
	'docno' 	: '7654321',
	'title' 	: 'test title',
	'abstract'	: 'long abstract',
	'filedate'	: '12/14/1976',
	'issuedate'	: '12/14/2013',
	'usclass1'	: '123/456',
	'usclass2'	: '123/123',
}

from PatentTools import schema

def TestImport():
	db = schema.engine()
	db.echo = True

	Session = sessionmaker(bind=db)
	session = Session()

	p = schema.Patent()
	p.docNumber 	= testdata['docno']
	p.title 		= testdata['title']
	p.abstract	 	= testdata['abstract']
	p.fileDate 		= parser.parse(testdata['filedate'])

	c1 = schema.USClass(testdata['usclass1'], p, True)
	c2 = schema.USClass(testdata['usclass2'], p, False)


	f1 = schema.FieldOfSearch(testdata['usclass1'], p)
	f2 = schema.FieldOfSearch(testdata['usclass2'], p)

	session.add_all([p,c1,c2,f1,f2]) 
	session.commit()

	# session.delete(c1)
	# session.delete(c2)
	session.delete(p)
	session.commit()




if __name__ == "__main__":
	TestImport()
	# print os.path.join(FILEPATH, 'test.sd')