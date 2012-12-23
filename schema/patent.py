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
class BaseReference(Base):
	__tablename__ = 'references'

	id 			= Column(Integer, primary_key=True)
	patent_id	= Column(Integer, ForeignKey(Patent.id))
	text 		= Column(String(255))
	type 		= Column(String(15))
	patent 		= relation("Patent", backref="references", cascade_backrefs=False)

	__mapper_args__ = { 
		'polymorphic_identity': 'generic', 
		'polymorphic_on': type 
	}

	def __init__(self, text, patent):
		self.patent_id = patent 
		self.text = text

	def __repr__(self):
		return "<Reference (%s)>" % ( self.type, )

class PublicationReference(BaseReference):
	__tablename__ = 'pub_references'
	__mapper_args__ = { 'polymorphic_identity': 'publication'}

	id = Column(Integer, ForeignKey(BaseReference.id), primary_key=True)
	docNumber 	= Column(String(20))
	country		= Column(String(10))
	kind		= Column(String(10))
	name		= Column(String(20))
	date 		= Column(Date)
	patent 		= relation("Patent", backref="pub_references", cascade_backrefs=False)

	def __init__(self, text, patent):
		super(PublicationReference, self).__init__(text, patent)

class ApplicationReference(BaseReference):
	__tablename__ = 'app_references'
	__mapper_args__ = { 'polymorphic_identity': 'application'}

	id = Column(Integer, ForeignKey(BaseReference.id), primary_key=True)
	docNumber 	= Column(String(20))
	country		= Column(String(10))
	date 		= Column(Date)
	patent 		= relation("Patent", backref="appl_references", cascade_backrefs=False)

	def __init__(self, text, patent):
		super(ApplicationReference, self).__init__(text, patent)

class NonPatReference(BaseReference):
	__tablename__ = 'non_patent'
	__mapper_args__ = { 'polymorphic_identity': 'application'}

	id 			= Column(Integer, ForeignKey(BaseReference.id), primary_key=True)
	patent 		= relation("Patent", backref="npat_references", cascade_backrefs=False)

	def __init__(self, text, patent):
		super(NonPatReference, self).__init__(text, patent)




