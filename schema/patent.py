from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship, backref, relation
from sqlalchemy.schema import ForeignKey

from PatentTools.schema import Base
# from PatImport.schema.entity import Inventor





# Session = sessionmaker(bind=engine)
# patent_inventor = Table('patent_inventor', Base.metadata,
# 	Column('patent_id', Integer, ForeignKey('patents.id')),
# 	Column('inventor_id', Integer, ForeignKey('inventors.id'))
# )



class Patent(Base):
	__tablename__ = 'patents'

	id 					= Column(Integer, primary_key=True)
	docNumber			= Column(String(15))
	appNumber		 	= Column(String(15))
	fileDate			= Column(Date)
	issueDate			= Column(Date)
	title 				= Column(String(500))


	# inventors = relationship('Inventor', secondary=patent_inventor, backref='patents')

	def __init__(self, number=''):
		self.number = number

	def __repr__(self):
		return "<Patent ('%s')>" % (self.number,)



#===============================================================================
# CLASSIFICATION SECTION
def splitUSClass(text):
	sep = text.find('/')
	if sep != -1:
		return (text[:sep], text[sep+1:])
	else:
		return (None, None)


class InternationalClass(Base):
	__tablename__ = 'IntlClasses'

	id 				= Column(Integer, primary_key=True)
	ipcVersion		= Column(String(10))
	patent_id 		= Column(Integer, ForeignKey(Patent.id))
	patent 			= relation("Patent", backref=backref("intl_classifications", cascade="delete"))
	text 			= Column(String(30))

	def __init__(self, text, patent):
		self.text = text
		self.patent = patent
	
class USClass(Base):
	__tablename__ 	= 'USClasses'

	id 				= Column(Integer, primary_key=True)
	patent_id 		= Column(Integer, ForeignKey(Patent.id))
	patent 			= relation("Patent", backref=backref("us_classifications", cascade="delete"))
	text 			= Column(String(30))
	klass			= Column(String(6))
	subKlass 		= Column(String(6))
	main 			= Column(Boolean)

	def __init__(self, text, patent, main=False):
		self.text = text
		self.patent = patent
		self.main = main
		self.klass, self.subKlass = splitUSClass(text)


class FieldOfSearch(Base):
	__tablename__ 	= 'FOSClasses'

	id 				= Column(Integer, primary_key=True)
	patent_id 		= Column(Integer, ForeignKey(Patent.id))
	patent 			= relation("Patent", backref=backref("fos_classifications", cascade="delete"))
	text 			= Column(String(30))
	klass			= Column(String(6))
	subKlass 		= Column(String(6))

	def __init__(self, text, patent):
		self.text = text
		self.patent = patent
		self.klass, self.subKlass = splitUSClass(text)

#===============================================================================
# REFERENCE SECTION

class PublicationReference(Base):
	__tablename__ = 'pub_references'
	__mapper_args__ = { 'polymorphic_identity': 'publication'}

	id = Column(Integer, primary_key=True)
	patent_id	= Column(Integer, ForeignKey(Patent.id))
	patent 		= relation("Patent", backref=backref("pubreferences", cascade="delete"))
	text 		= Column(String(255))
	docNumber 	= Column(String(20))
	country		= Column(String(10))
	kind		= Column(String(10))
	name		= Column(String(20))
	date 		= Column(Date)
	num 		= Column(Integer)

	def __init__(self, text, patent):
		self.text = text
		self.patent = patent

class ApplicationReference(Base):
	__tablename__ = 'app_references'

	id = Column(Integer, primary_key=True)
	patent_id	= Column(Integer, ForeignKey(Patent.id))
	patent 		= relation("Patent", backref=backref("appreferences", cascade="delete"))
	text 		= Column(String(255))
	docNumber 	= Column(String(20))
	country		= Column(String(10))
	date 		= Column(Date)
	num 		= Column(Integer)

	def __init__(self, text, patent):
		self.text = text
		self.patent = patent


class NonPatReference(Base):
	__tablename__ = 'non_patent'

	id 			= Column(Integer, primary_key=True)
	patent_id	= Column(Integer, ForeignKey(Patent.id))
	patent 		= relation("Patent", backref=backref("nonpatreferences", cascade="delete"))
	text 		= Column(String(255))
	num 		= Column(Integer)

	def __init__(self, text, patent):
		self.text = text
		self.patent = patent




