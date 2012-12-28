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
	docCountry 			= Column(String(2))		# country
	docNumber 			= Column(String(8))	# doc-number
	docKind 			= Column(String(2))		# kind
	docDate 			= Column(String(8))		# date (YYYYMMDD)

	# us-bibliographic-data-grant/application-reference/documnet-id
	# appType options =  ['design', 'plant', 'reissue', 'sir', 'utility']
	appType 			= Column(String(10))	# attrib: appl-type
	appCountry			= Column(String(5))		# country
	appNumber 			= Column(String(10))	# doc-number
	appDate 			= Column(String(8))		# date (YYYYMMDD)

	# us-term-of-grant
	grantLength			= Column(String(5))		# length-of-grant
	termExtension		= Column(String(5))		# us-term-extension
	termDisclaimer		= Column(Text)			# disclaimer/text

	# us-bibliographic-data-grant/figures
	numberOfSheets		= Column(String(5)) 	# number-of-drawing-sheets
	numberOfFigures		= Column(String(5)) 	# number-of-figures

	# us-patent-grant/us-bibliographic-data-grant
	appSeriesCode		= Column(String(2))		# us-application-series-code
	inventionTitle 		= Column(Text)		# invention-title
	inventionTitleId	= Column(String(10))	# invention-title attrib: id
	numberOfClaims		= Column(String(5))		# number-of-claims
	usExemplaryClaim 	= Column(String(5))		# us-exemplary-claim

class ClassificationLocarno(Base):
	__tablename__ = 'ICE42_ClassificationLocarno'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("classificationLocarnos", cascade="delete"))

	edition				= Column(String(1))
	mainKlass			= Column(String(10))



class ClassificationIPCR(Base):
	__tablename__ = 'ICE42_ClassificationIPCR'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("classificationIPCRs", cascade="delete"))

	# Symbol position options = 'F': first, 'L': later
	# value options = 'I': invention information, 'N': non-invention information
	ipcVersion			= Column(String(8))	# format (YYYYMMDD)
	klassLevel	 		= Column(String(1))
	section 			= Column(String(1))
	klass 				= Column(String(2))
	subKlass 			= Column(String(1))
	mainGroup 			= Column(String(5))
	subGroup 			= Column(String(10))
	symbolPosition		= Column(String(1))
	value 				= Column(String(1))
	actionDate 			= Column(String(8)) #(YYYYMMDD)
	genOfficeCountry	= Column(String(2))
	klassStatus 		= Column(String(1))
	klassDataSource 	= Column(String(1))


class ClassificationNational(Base):
	__tablename__ = 'ICE42_ClassificationNational'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("classificationNationals", cascade="delete"))

	country 			= Column(String(2))
	klass 				= Column(String(15))
	main 				= Column(Boolean)


# us-patent-grant/us-field-of-classification-search
class FieldOfSearch(Base):
	__tablename__ = 'ICE42_FieldOfSearch'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("fieldsOfSearch", cascade="delete"))

	# if additionalInfo is not null, value will be 'unstructured'
	# note that us-classification-ipcr is omitted here for lack of practical use at USPTO
	country 			= Column(String(2))
	mainKlass			= Column(String(10))
	additionalInfo 		= Column(String(20))




class ReferenceCited(Base):
	__tablename__ = 'ICE42_ReferencesCited'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("referencesCited", cascade="delete"))

	# reftype can be "patcit" or "nplcit"
	# num is the sequence
	# category options = ['cited by examiner', 'cited by other']
	refType 			= Column(String(10))
	num 				= Column(String(5))
	category 			= Column(String(20))
	otherCit 			= Column(Text) #only for nplcit
	klassCountry		= Column(String(2))
	klassMain 			= Column(String(10))

	# document-id
	docCountry 			= Column(String(2))
	docNumber 			= Column(String(20))
	docName 			= Column(String(30)) # optional
	docKind 			= Column(String(2))
	docDate 			= Column(String(8)) # (YYYYMMDD)



class Applicant(Base):
	__tablename__ = 'ICE42_Applicant'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("applicants", cascade="delete"))

	# appType optins = ['applicant', 'applicant-inventor']
	# designation options = ['us-only']
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
	# note that us-rights is omitted



# inventor, deceased-inventor and us-deceased-inventor elements no longer present effective Aug 25, 2009
class Inventor(Base):
	__tablename__ = 'ICE42_Inventor'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("inventors", cascade="delete"))

	# invType options = ['inventor', 'deceased-inventor']
	invType				= Column(String(20))
	sequence			= Column(String(5))
	# addressbook
	lastName			= Column(String(50))
	firstName			= Column(String(50))
	city 				= Column(String(50))
	country 			= Column(String(2))



class Agent(Base):
	__tablename__ = 'ICE42_Agent'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("agents", cascade="delete"))

	# repType options = ['agent', 'attorney', 'common-representative']
	sequence 			= Column(String(3))
	repType 			= Column(String(25))

	# addressbook
	orgName 			= Column(String(50))
	lastName 			= Column(String(50))
	firstName 			= Column(String(50))
	country 			= Column(String(5))



assigneeRole = {
	'01': 'Unassigned',
	'02': 'United States company or corporation',
	'03': 'Foreign company or corporation',
	'04': 'United States individual',
	'05': 'Foreign individual',
	'06': 'U.S. Federal Government',
	'07': 'Foreign Government',
	'08': 'U.S. county government',
	'09': 'U.S. state government',
	'11': 'Unassigned (partial)',
	'12': 'United States company or corporation (partial)',
	'13': 'Foreign company or corporation (partial)',
	'14': 'United States individual (partial)',
	'15': 'Foreign individual (partial)',
	'16': 'U.S. Federal Government (partial)',
	'17': 'Foreign Government (partial)',
	'18': 'U.S. county government (partial)',
	'19': 'U.S. state governmen (partial)t'
}

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

	# examinerType options = ['primary-examiner', 'assistant-examiner']
	examinerType		= Column(String(20))
	firstName 			= Column(String(50))
	lastName 			= Column(String(50))
	department			= Column(String(4))



class PriorityClaim(Base):
	__tablename__ = 'ICE42_PriorityClaim'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("priorityClaims", cascade="delete"))

	# kind options = ['national', 'regional', 'international']
	sequence 			= Column(String(5))
	kind 				= Column(String(10))
	country 			= Column(String(2))
	docNumber 			= Column(String(15))
	date 				= Column(String(8)) # (YYYYMMDD)



class PCTOrRegionalFiling(Base):
	__tablename__ = 'ICE42_PCTOrRegionalFiling'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PCTOrRegionalFilings", cascade="delete"))

	docCountry 			= Column(String(2))
	docNumber 			= Column(String(20))
	docKind 			= Column(String(2))
	docDate 			= Column(String(8)) # (YYYYMMDD)
	date371 			= Column(String(8)) # (YYYYMMDD) - date of US national stage appl


class PCTOrRegionalPublishing(Base):
	__tablename__ = 'ICE42_PCROrRegionalPublishing'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PCROrRegionalPublishings", cascade="delete"))

	docCountry 			= Column(String(2))
	docNumber 			= Column(String(20))
	docKind 			= Column(String(2))
	docDate 			= Column(String(8)) # (YYYYMMDD)




class ExemplaryClaim(Base):
	__tablename__ = 'ICE42_ExemplaryClaim'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("exemplaryClaims", cascade="delete"))

	count 				= Column(String(5))



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
	__tablename__ = 'ICE42_AbstractChemistry'

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


class RelatedDocument(Base):
	__tablename__ = 'ICE42_RelatedDocument'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("relatedDocuments", cascade="delete"))

	# relationKind options = [('division', 'continuation', 'continuation-in-part', 'continuing-reissue', 'reissue', 'reexamination', 'us-provisional-application', 'correction', 'related-publication']
	relationKind 		=Column(String(30))	

	# for related-publication, us-provisional-application, division (child), continuation (child), continuation-in-part (child), reissue (child)
	docCountry 			= Column(String(2))		# country
	docNumber 			= Column(String(8))		# doc-number
	docKind 			= Column(String(2))		# kind
	docDate 			= Column(String(8))		# date (YYYYMMDD)

	# child-doc
	childCountry		= Column(String(2))		# country
	childNumber 		= Column(String(8))		# doc-number
	childKind 			= Column(String(2))		# kind
	childDate 			= Column(String(8))		# date (YYYYMMDD)

	# parent-doc
	# for division, continuation, continuation-in-part, reissue
	# parentStatus options = ['ABANDONED', 'GRANTED', 'PENDING']
	parentCountry 		= Column(String(2))		# country
	parentNumber 		= Column(String(8))		# doc-number
	parentKind 			= Column(String(2))		# kind
	parentDate 			= Column(String(8))		# date (YYYYMMDD)
	parentStatus		= Column(String(15))

	# parent-grant-document (optional within parent-doc)
	# for continuation, , reissue
	parentGrantCountry	= Column(String(2))		# country
	parentGrantNumber	= Column(String(8))		# doc-number
	parentGrantKind		= Column(String(2))		# kind
	parentGrantDate		= Column(String(8))		# date (YYYYMMDD)

	# parent-pct-document (optional within parent-doc)
	# for continuation, , reissue
	parentPCTCountry	= Column(String(2))		# country
	parentPCTNumber		= Column(String(8))		# doc-number
	parentPCTKind		= Column(String(2))		# kind
	parentPCTDate		= Column(String(8))		# date (YYYYMMDD)



# figures
# note that these appear under the drawings heading, not the figures
class Figure(Base):
	__tablename__ = 'ICE42_Figure'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("figures", cascade="delete"))

	figureId			= Column(String(50))
	num 				= Column(String(5))

	imgId 				= Column(String(50))
	# orientation options = ['portrait', 'landscape'] default to 'portrait'
	# img-content options = ['drawing', 'photograph', 'character', 'dna', 'undefined', 'chem', 'table', 'math', 'program-listing', 'flowchart'] default to 'drawing'
	# img-format options = ['jpg', 'tif', 'st33', 'st35'] 
	imgHe 				= Column(String(15))
	imgWi 				= Column(String(15))
	imgOrientation 		= Column(String(15))
	imgFile 			= Column(String(50))
	imgAlt 				= Column(String(255))
	imgContent 			= Column(String(15))
	imgFormat 			= Column(String(5))


