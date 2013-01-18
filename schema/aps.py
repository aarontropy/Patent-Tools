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

	# remember to ignore trailing spaces in the APS doc
	# PATN
	docNumber			= Column(String(8))		# WKU
	seriesCode			= Column(String(1))		# SRC
	appNumber			= Column(String(6))		# APN
	appType				= Column(String(1))		# APT
	pubLevel 			= Column(String(2))		# PBL
	artUnit				= Column(String(3))		# ART
	filingDate 			= Column(String(8))		# APD
	title 				= Column(String(255))	# TTL
	issueDate			= Column(String(8))		# ISD
	numberOfClaims		= Column(String(4))		# NCL
	exemplaryClaims		= Column(String(14))	# ECL - Comma separated list, terminated by space
	assistantExaminer 	= Column(String(255))	# EXA - Last; First M.
	primaryExaminer 	= Column(String(255))	# EXP
	numberDrawingSheets = Column(String(4))		# NDR
	numberFigures		= Column(String(4))		# NFG
	disclaimerDate 		= Column(String(8))		# DCD



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




class PriorityClaim(Base):
	__tablename__ = 'XML25_PriorityClaim'

	id 					= Column(Integer, primary_key=True)
	patentGrant_id 		= Column(Integer, ForeignKey(UsPatentGrant.id))
	patentGrant			= relation("UsPatentGrant", backref=backref("PriorityClaims", cascade="delete"))

	docNumber 			= Column(String(25))	# SDOBI/B300/B310/DNUM/PDAT
	docDate 			= Column(String(8))		# SDOBI/B300/B320/DATE/PDAT
	docCountry 			= Column(String(2))		# SDOBI/B300/B330/CTRY/PDAT



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
