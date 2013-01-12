from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine, Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, relation
from sqlalchemy.schema import ForeignKey

from PatentTools.schema import Base


USPTODATEFORMAT = "%Y%m%d"

def parseUSPTODate(usptoDate):
	try:
		return datetime.strptime(usptoDate, USPTODATEFORMAT)
	except:
		return None
		

class UsPatentGrant(Base):
	__tablename__ = 'XML25_UsPatentGrant'

	id 					= Column(Integer, primary_key=True)

	# Attribute data
	singleFile 			= Column(String(30))
	groupFile 			= Column(String(30))
	status 				= Column(String(20))
	dateProduced 		= Column(String(15))
	datePublished 		= Column(String(15))

	# SDOBI/B100 - Documnet identification
	docCountry 			= Column(String(2))		# SDOBI/B100/B190/PDAT
	docNumber 			= Column(String(8))		# SDOBI/B100/B110/DNUM/PDAT
	docKind 			= Column(String(2))		# SDOBI/B100/B130/PDAT
	docDate 			= Column(String(8))		# SDOBI/B100/B140/DATE/PDAT

	# SDOBI/B200
	# Series Code, two-digit, representing the following time periods and document types:
	# 02 ... up to ...1947-12-31
	# 03 1948-01-01...1959-12-31
	# 04 1960-01-01...1969-12-31
	# 05 1970-01-01...1978-12-31
	# 06 1979-01-01...1986-12-31
	# 07 1987-01-01...1992-12-31
	# 08 1993-01-01...1997-12-29
	# 09 1997-12-30...and after
	# 29 Design Application
	# 60 Provisional Application
	# 90 Reexamination Request
	appNumber 			= Column(String(10))	# SDOBI/B200/B210/DNUM/PDAT
	appSeriesCode		= Column(String(2))		# SDOBI/B200/B211US/PDAT
	appDate 			= Column(String(8))		# SDOBI/B200/B220/DATE/PDAT



	appType 			= Column(String(10))	# attrib: appl-type
	appCountry			= Column(String(5))		# country


	# SDOBI/B400 - Public availability dates and term of protection
	disclaimerDate 		= Column(String(8)) 	# SDOBI/B400/B472/B473
	termDisclaimer		= Column(Boolean)		# SDOBI/B400/B472/B473US (present or not?)
	grantLength			= Column(String(5))		# SDOBI/B400/B472/B474/PDAT
	termExtension		= Column(String(5))		# SDOBI/B400/B472/B474US/PDAT


	inventionTitle 		= Column(Text)			# SDOBI/B500/B540/STEXT/PDAT
	numberOfClaims		= Column(String(5))		# SDOBI/B500/B570/B577/PDAT

	# us-bibliographic-data-grant/figures
	numberOfSheets		= Column(String(5)) 	# SDOBI/B500/B590/B595/PDAT
	numberOfColorSheets = Column(String(5)) 	# SDOBI/B500/B590/B595US/PDAT
	numberOfFigures		= Column(String(5)) 	# SDOBI/B500/B590/B596/PDAT


# SDOBI/B300 - Foreign Priority Data
class PriorityClaim(Base):
	__tablename__ = 'XML25_PriorityClaim'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PriorityClaims", cascade="delete"))

	docNumber 			= Column(String(25))	# SDOBI/B300/B310/DNUM/PDAT
	docDate 			= Column(String(8))		# SDOBI/B300/B320/DATE/PDAT
	docCountry 			= Column(String(2))		# SDOBI/B300/B330/CTRY/PDAT


# SDOBI/B500/B510 - International Patent Classification (IPC) data 
# or Locarno Classification for Design patents
class ClassificationIPCR(Base):
	__tablename__ = 'XML25_ClassificationIPCR'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("classificationIPCRs", cascade="delete"))

	# Symbol position options = 'F': first, 'L': later
	# value options = 'I': invention information, 'N': non-invention information
	classification 		= Column(String(10))	# SDOBI/B500/B510/(B511 or B512)/PDAT
	ipcVersion			= Column(String(8))		# SDOBI/B500/B510/B516/PDAT
	firstPosition		= Column(Boolean)		# ONLY IF SDOBI/B500/B510/B511



# SDOBI/B500/B520 - Domestic or national classification data
# National classification.
# Use for structured US Classification information:
# ...Pos. 1 - 3 ... Class
# 3 alphanumeric characters, right justified; D for design classes,
# followed by one or two right-justified digits; PLT for Plant classes
# ...Pos. 4 - ... Subclass
# alphanumeric, variable length
class ClassificationNational(Base):
	__tablename__ = 'XML25_ClassificationNational'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("classificationNationals", cascade="delete"))

	classification 		= Column(String(10)) 	# SDOBI/B500/B520/(B521 or B522)/PDAT
	main 				= Column(Boolean) 		# ONLY IF SDOBI/B500/B520/B521


# SDOBI/B500/B560 - Citations
class ReferenceCited(Base):
	__tablename__ = 'XML25_ReferencesCited'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("referencesCited", cascade="delete"))

	# 'PCIT' if SDOBI/B500/B560/B561
	# 'NCIT' if SDOBI/B500/B560/B562
	refType 			= Column(String(10))

	# 'CITED-BY-EXAMINER' if SDOBI/B500/B560/(B561 or B562)/CITED-BY-EXAMINER present
	# 'CITED-BY-OTHER' if SDOBI/B500/B560/(B561 or B562)/CITED-BY-OTHER present
	category 			= Column(String(20))

	# document-id
	docCountry 			= Column(String(2))
	docNumber 			= Column(String(20))	# SDOBI/B500/B560/B561/PCIT/DOC/DNUM/PDAT
	docKind 			= Column(String(2))		# SDOBI/B500/B560/B561/PCIT/DOC/KIND/PDAT
	docDate 			= Column(String(8)) 	# SDOBI/B500/B560/B561/PCIT/DOC/DATE/PDAT
	docName 			= Column(String(50)) 	# SDOBI/B500/B560/B561/PCIT/PARTY-US/NAM/SNM/STEXT/PDAT

	otherCit 			= Column(Text) 			# SDOBI/B500/B560/B562/NCIT/STEXT/PDAT


# SDOBI/B500/B570/B578US - Exemplary claim number
class ExemplaryClaim(Base):
	__tablename__ = 'XML25_ExemplaryClaim'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("exemplaryClaims", cascade="delete"))

	claim 				= Column(String(5)) 	# SDOBI/B500/B570/B578US/PDAT



# SDOBI/B500/B580 - Field of Search
class FieldOfSearch(Base):
	__tablename__ = 'XML25_FieldOfSearch'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("fieldsOfSearch", cascade="delete"))

	# if additionalInfo is not null, value will be 'unstructured'
	IPCRClassification 	= Column(String(10))	# SDOBI/B500/B580/B581/PDAT
	classification 		= Column(String(10)) 	# SDOBI/B500/B580/B582/PDAT
	unstructuredClass 	= Column(String(50)) 	# SDOBI/B500/B580/B583US/PDAT


# SDOBI/B600/
class RelatedDocument(Base):
	__tablename__ = 'XML25_RelatedDocument'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("relatedDocuments", cascade="delete"))

	# relationKind options = [('division', 'continuation', 'continuation-in-part', 'continuing-reissue', 'reissue', 'reexamination', 'us-provisional-application', 'correction', 'related-publication']
	# B610 Addition to (PARENT-US only)	
	# B620 Division of (PARENT-US only)
	# B630 Continuation of (contains B631, B632, B633 (one or more))
		# B631 Earlier application of which the present document is a continuation (PARENT-US only)
		# B632 Document of which this is a continuation-in-part (PARENT-US only)
		# B633 Document of which this is a continuing reissue (PARENT-US only)
	# B640 Reissue of (PARENT-US only)
	# B641US Divisional resissue information of a related US document (PARENT-US, SIBLING+)
	# B645 Reexamination requested by the  applicant, assignee, or commissioner (PARENT-US only)
	# B646US Reexamination requested by a 3rd party (PARENT-US only)
	# B650 Previously-published document concerning the same application (DOC only)
	# B660 Document for which this is a substitute (PARENT-US only)
	# B680US - US provisional information (doc only)
	relationKind 		=Column(String(30))	

	# for related-publication, us-provisional-application, division (child), continuation (child), continuation-in-part (child), reissue (child)
	docCountry 			= Column(String(2))		# ???/DOC/CTRY/PDAT
	docNumber 			= Column(String(8))		# ???/DOC/DNUM/PDAT
	docKind 			= Column(String(2))		# ???/DOC/KIND/PDAT
	docDate 			= Column(String(8))		# ???/DOC/DATE/PDAT

	# child-doc
	childCountry		= Column(String(2))		# ???/PARENT-DOC/CDOC/DOC/CTRY/PDAT
	childNumber 		= Column(String(8))		# ???/PARENT-DOC/CDOC/DOC/DNUM/PDAT - child doc number
	childKind 			= Column(String(2))		# ???/PARENT-DOC/CDOC/DOC/KIND/PDAT
	childDate 			= Column(String(8))		# ???/PARENT-DOC/CDOC/DOC/DATE/PDAT

	# SDOBI/B600/B630 - 
	# for division, continuation, continuation-in-part, reissue
	# parentStatus options = ['ABANDONED', 'GRANTED', 'PENDING']
	parentCountry 		= Column(String(2))		# ???/PARENT-DOC/PDOC/DOC/CTRY/PDAT - parent doc country
	parentNumber 		= Column(String(8))		# ???/PARENT-DOC/PDOC/DOC/DNUM/PDAT - parent doc number
	parentKind 			= Column(String(2))		# ???/PARENT-DOC/PDOC/DOC/KIND/PDAT - parent doc kind
	parentDate 			= Column(String(8))		# ???/PARENT-DOC/PDOC/DOC/DATE/PDAT - parent doc date
	parentGrantCountry	= Column(String(2))		# ???/PARENT-DOC/PPUB/DOC/CTRY/PDAT - granted parent doc country
	parentGrantNumber	= Column(String(8))		# ???/PARENT-DOC/PPUB/DOC/DNUM/PDAT - granted parent doc number
	parentGrantKind		= Column(String(2))		# ???/PARENT-DOC/PPUB/DOC/KIND/PDAT - granted parent doc kind
	parentGrantDate		= Column(String(8))		# ???/PARENT-DOC/PPUB/DOC/DATE/PDAT - granted parent doc date



# B700/B720/B721
class Inventor(Base):
	__tablename__ = 'XML25_Inventor'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("inventors", cascade="delete"))

	sequence			= Column(String(5))		# Count
	# addressbook
	lastName			= Column(String(50))	# SDOBI/B700/B720/B721/PARTY-US/NAM/SNM/STEXT/PDAT
	firstName			= Column(String(50))	# SDOBI/B700/B720/B721/PARTY-US/NAM/FNM/PDAT
	city 				= Column(String(50))	# SDOBI/B700/B720/B721/PARTY-US/ADR/CITY/PDAT
	country 			= Column(String(2))		# SDOBI/B700/B720/B721/PARTY-US/ADR/CTRY/PDAT


# B700/B740/B741 - Attorney, agent, or representative. 
class Agent(Base):
	__tablename__ = 'XML25_Agent'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("agents", cascade="delete"))

	sequence 			= Column(String(3))		# count

	orgName 			= Column(String(50))	# SDOBI/B700/B740/B741/PARTY-US/NAM/ONM/STEXT/PDAT
	lastName 			= Column(String(50))	# SDOBI/B700/B740/B741/PARTY-US/NAM/SNM/STEXT/PDAT
	firstName 			= Column(String(50))	# SDOBI/B700/B740/B741/PARTY-US/NAM/FNM/PDAT



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
# B700/B730 Assignee
class Assignee(Base):
	__tablename__ = 'XML25_Assignee'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("assignees", cascade="delete"))

	# addressbook
	orgName	 			= Column(String(50))	# SDOBI/B700/B730/B731/PARTY-US/NAM/ONM/STEXT/PDAT
	city 				= Column(String(30))	# SDOBI/B700/B730/B731/PARTY-US/ADR/CITY/PDAT
	state 				= Column(String(5))		# SDOBI/B700/B730/B731/PARTY-US/????
	country 			= Column(String(5))		# SDOBI/B700/B730/B731/PARTY-US/ADR/CTRY/PDAT
	role 				= Column(String(5))		# SDOBI/B700/B730/B732US/PDAT


# B700/B745/(B746|B747)
class Examiner(Base):
	__tablename__ = 'XML25_Examiner'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("examiners", cascade="delete"))

	# examinerType options = ['primary-examiner', 'assistant-examiner']
	examinerType		= Column(String(20))	# Primary = B746, Assistant = B747
	firstName 			= Column(String(50))	# SDOBI/B700/(B745|B746)/PARTY-US/NAM/FNM/PDAT
	lastName 			= Column(String(50))	# SDOBI/B700/(B745|B746)/PARTY-US/NAM/SNM/STEXT/PDAT
	department			= Column(String(4))		# SDOBI/B700/B748US/PDAT



# B800/B860 - PCT or regional authority filing information
class PCTOrRegionalFiling(Base):
	__tablename__ = 'XML25_PCTOrRegionalFiling'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PCTOrRegionalFilings", cascade="delete"))

	docCountry 			= Column(String(2))		# SDOBI/B800/B860/B861/DOC/CTRY/PDAT
	docNumber 			= Column(String(20))	# SDOBI/B800/B860/B861/DOC/DNUM/PDAT
	docKind 			= Column(String(2))		# SDOBI/B800/B860/B861/DOC/KIND/PDAT
	docDate 			= Column(String(8)) 	# SDOBI/B800/B860/B861/DOC/DATE/PDAT
	date371 			= Column(String(8)) 	# SDOBI/B800/B860/B864US/DATE/PDAT

# B800/B870 - PCT or regional authority publication information
class PCTOrRegionalPublishing(Base):
	__tablename__ = 'XML25_PCTOrRegionalPublishing'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PCROrRegionalPublishings", cascade="delete"))

	docCountry 			= Column(String(2))		# SDOBI/B800/B870/B871/DOC/CTRY/PDAT
	docNumber 			= Column(String(20))	# SDOBI/B800/B870/B871/DOC/DNUM/PDAT
	docKind 			= Column(String(2))		# SDOBI/B800/B870/B871/DOC/KIND/PDAT
	docDate 			= Column(String(8)) 	# SDOBI/B800/B870/B871/DOC/DATE/PDAT






# SDOAB/BTEXT/PARA
class AbstractP(Base):
	__tablename__ = 'XML25_AbstractP'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("abstractPs", cascade="delete"))

	abId 				= Column(String(15))
	lvl 				= Column(String(15))
	# using ElementTree -> for t in node.itertext(): content += t
	content 			= Column(Text)			# SDOAB/BTEXT/PARA/PTEXT/PDAT
	asString 			= Column(Text)

	@property 
	def hasChemistry(self):
		return len(self.chemistries) > 0



	
# figures
# note that these appear under the drawings heading, not the figures
# class Figure(Base):
# 	__tablename__ = 'ICE42_Figure'

# 	id 					= Column(Integer, primary_key=True)
# 	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
# 	patentGrant			= relation("UsPatentGrant", backref=backref("figures", cascade="delete"))

# 	figureId			= Column(String(50))
# 	num 				= Column(String(5))

# 	imgId 				= Column(String(50))
# 	# orientation options = ['portrait', 'landscape'] default to 'portrait'
# 	# img-content options = ['drawing', 'photograph', 'character', 'dna', 'undefined', 'chem', 'table', 'math', 'program-listing', 'flowchart'] default to 'drawing'
# 	# img-format options = ['jpg', 'tif', 'st33', 'st35'] 
# 	imgHe 				= Column(String(15))
# 	imgWi 				= Column(String(15))
# 	imgOrientation 		= Column(String(15))
# 	imgFile 			= Column(String(50))
# 	imgAlt 				= Column(String(255))
# 	imgContent 			= Column(String(15))
# 	imgFormat 			= Column(String(5))


