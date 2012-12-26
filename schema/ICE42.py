from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine, Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, relation
from sqlalchemy.schema import ForeignKey

from PatentTools.schema import Base


class UsPatentGrant(Base):
	__tablename__ = 'ICE42_UsPatentGrant'

	id 					= Column(Integer, primary_key=True)

	# Attribute data
	lang 				= Column(String(2))
	dtdVersion 			= Column(String(30))
	singleFile 			= Column(String(30))
	groupFile 			= Column(String(30))
	status 				= Column(String(20))
	dateProduced 		= Column(String(15))
	datePublished 		= Column(String(15))

	# us-bibliographic-data-grant/publication-reference/document-id
	docCountry 			= Column(String(5))		# country
	docNumber 			= Column(String(15))	# doc-number
	docKind 			= Column(String(5))		# kind
	docDate 			= Column(String(8))		# date

	# us-bibliographic-data-grant/application-reference/documnet-id
	appType 			= Column(String(10))	# attrib: appl-type
	appCountry			= Column(String(5))		# country
	appNumber 			= Column(String(10))	# doc-number
	appDate 			= Column(String(8))		# date

	# us-term-of-grant
	grantLength			= Column(String(5))
	termExtension		= Column(String(5))		# us-term-extension

	# us-bibliographic-data-grant/figures
	numberOfSheets		= Column(String(5)) 	# number-of-drawing-sheets
	numberOfFigures		= Column(String(5)) 	# number-of-figures

	# us-patent-grant/us-bibliographic-data-grant
	appSeriesCode		= Column(String(2))		# us-application-series-code
	inventionTitle 		= Column(Text)		# invention-title
	inventionTitleId	= Column(String(10))	# invention-title attrib: id
	numberOfClaims		= Column(String(5))		# number-of-claims
	usExemplaryClaim 	= Column(String(5))		# us-exemplary-claim



class ClassificationIPCR(Base):
	__tablename__ = 'ICE42_ClassificationIPCR'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("classificationIPCRs", cascade="delete"))

	ipcVersion			= Column(String(10))
	klassLevel	 		= Column(String(5))
	section 			= Column(String(1))
	klass 				= Column(String(2))
	subKlass 			= Column(String(1))
	mainGroup 			= Column(String(5))
	subGroup 			= Column(String(10))
	symbolPosition		= Column(String(1))
	value 				= Column(String(1))
	actionDate 			= Column(String(8))
	genOfficeCountry	= Column(String(2))
	klassStatus 		= Column(String(1))
	klassDataSource 	= Column(String(1))


class ClassificationNational(Base):
	__tablename__ = 'ICE42_ClassificationNational'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("classificationNationals", cascade="delete"))

	country 			= Column(String(2))
	text 				= Column(String(15))
	main 				= Column(Boolean)


# us-patent-grant/us-field-of-classification-search
class FieldOfSearch(Base):
	__tablename__ = 'ICE42_FieldOfSearch'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("fieldsOfSearch", cascade="delete"))

	country 			= Column(String(2))
	mainKlass			= Column(String(10))
	additionalInfo 		= Column(String(20))

# figures
class Figure(Base):
	__tablename__ = 'ICE42_Figure'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("figures", cascade="delete"))



class ReferenceCited(Base):
	__tablename__ = 'ICE42_ReferencesCited'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("referencesCited", cascade="delete"))

	# reftype can be "patcit" or "nplcit"
	refType 			= Column(String(10))
	num 				= Column(String(5))
	category 			= Column(String(20))
	otherCit 			= Column(Text)
	klassCountry		= Column(String(2))
	klassMain 			= Column(String(10))

	# document-id
	docCountry 			= Column(String(2))
	docNumber 			= Column(String(20))
	docName 			= Column(String(30))
	docKind 			= Column(String(5))
	docDate 			= Column(String(8))



class Applicant(Base):
	__tablename__ = 'ICE42_Applicant'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("applicants", cascade="delete"))

	sequence 			= Column(String(3))
	appType 			= Column(String(15))
	designation 		= Column(String(15))

	# addressbook
	lastName 			= Column(String(50))
	firstName 			= Column(String(50))
	city 				= Column(String(30))
	state 				= Column(String(5))
	country 			= Column(String(5))

	nationality 		= Column(String(15))
	residenceCountry 	= Column(String(5))




class Agent(Base):
	__tablename__ = 'ICE42_Agent'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("agents", cascade="delete"))

	sequence 			= Column(String(3))
	repType 			= Column(String(10))

	# addressbook
	orgName 			= Column(String(50))
	lastName 			= Column(String(50))
	firstName 			= Column(String(50))
	country 			= Column(String(5))





class Assignee(Base):
	__tablename__ = 'ICE42_Assignee'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("assignees", cascade="delete"))

	# addressbook
	orgName	 			= Column(String(50))
	role 				= Column(String(5))
	city 				= Column(String(30))
	state 				= Column(String(5))
	country 			= Column(String(5))


class Examiner(Base):
	__tablename__ = 'ICE42_Examiner'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("examiners", cascade="delete"))

	examinerType		= Column(String(20))
	firstName 			= Column(String(50))
	lastName 			= Column(String(50))
	department			= Column(String(10))



class PriorityClaim(Base):
	__tablename__ = 'ICE42_PriorityClaim'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("priorityClaims", cascade="delete"))

	sequence 			= Column(String(5))
	kind 				= Column(String(10))
	country 			= Column(String(2))
	docNumber 			= Column(String(15))
	date 				= Column(String(8))



class ForeignFiling(Base):
	__tablename__ = 'ICE42_ForeignFiling'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PCTFilings", cascade="delete"))

	docCountry 			= Column(String(2))
	docNumber 			= Column(String(20))
	docKind 			= Column(String(5))
	docDate 			= Column(String(8))
	date371 			= Column(String(8))




class ForeignPublishing(Base):
	__tablename__ = 'ICE42_ForeignPublishing'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PCTFilings", cascade="delete"))

	docCountry 			= Column(String(2))
	docNumber 			= Column(String(20))
	docKind 			= Column(String(5))
	docDate 			= Column(String(8))




class AbstractP(Base):
	__tablename__ = 'ICE42_AbstractP'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("abstractPs", cascade="delete"))

	abId 				= Column(String(15))
	num 				= Column(String(15))
	content 			= Column(Text)

	@property 
	def hasChemistry(self):
		return len(self.chemistries) > 0


class AbstractChemistry(Base):
	__tablename__ = 'ICE_AbstractChemistry'

	id 					= Column(Integer, primary_key=True)
	abstractP_id 		= Column(Integer, ForeignKey(AbstractP.id))
	abstractP 			= relation("AbstractP", backref=backref("chemistries", cascade="delete"))

	chemId 				= Column(String(15))
	num 				= Column(String(5))

	# img
	imgId 				= Column(String(20))
	imgHe				= Column(String(10))
	imgWi 				= Column(String(10))
	imgFile 			= Column(String(30))
	imgAlt				= Column(String(30))
	imgContent 			= Column(String(10))
	imgFormat			= Column(String(10))
