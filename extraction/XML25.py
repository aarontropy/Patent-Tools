# populate()
# by Allan Niemerg
# Populates a Mysql database with patent data from files found on 
# http://www.google.com/googlebooks/uspto.html
# This file works with Patent files from 2006 onwards

# populate will parse the following dtd versions:
#   4.2

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
import MySQLdb as mdb
import codecs

import sqlalchemy as sa
import PatentTools.schema as sc
import PatentTools.schema.xml25 as x25

def convertToHTMLView(x):
	num = 0
	des = ''
	for i in x:
		if (i == '<'):
			num = num + 1
			continue
		if (i == '>'):
			num = num - 1
			continue
		if num == 0:
			des = des + i
	return des

def nodeText(n):
	try:
		return n.text
	except:
		return None






def parse_xml25(filename):

	#start parsing
	doc = ElementTree()
	doc.parse(filename)
	root = doc.getroot()


	#loop for main patent
	
	patObjects = []

	patentGrant = ice.UsPatentGrant()
	patentGrant.docCountry 			= nodeText(root.find('SDOBI/B100/B190/PDAT'))
	patentGrant.docNumber 			= nodeText(root.find('SDOBI/B100/B110/DNUM/PDAT'))
	patentGrant.docKind 			= nodeText(root.find('SDOBI/B100/B130/PDAT'))
	patentGrant.docDate 			= nodeText(root.find('SDOBI/B100/B140/DATE/PDAT'))
	patentGrant.appNumber 			= nodeText(root.find('SDOBI/B200/B210/DNUM/PDAT'))
	patentGrant.appSeriesCode		= nodeText(root.find('SDOBI/B200/B211US/PDAT'))
	patentGrant.appDate 			= nodeText(root.find('SDOBI/B200/B220/DATE/PDAT'))
	patentGrant.disclaimerDate 		= nodeText(root.find('SDOBI/B400/B472/B473'))
	patentGrant.termDisclaimer		= root.find('SDOBI/B400/B472/B473US') is not None	# (present or not?)
	patentGrant.grantLength			= nodeText(root.find('SDOBI/B400/B472/B474/PDAT'))
	patentGrant.termExtension		= nodeText(root.find('SDOBI/B400/B472/B474US/PDAT'))
	patentGrant.inventionTitle 		= nodeText(root.find('SDOBI/B500/B540/STEXT/PDAT'))
	patentGrant.numberOfClaims		= nodeText(root.find('SDOBI/B500/B570/B577/PDAT'))
	patentGrant.numberOfSheets		= nodeText(root.find('SDOBI/B500/B590/B595/PDAT'))
	patentGrant.numberOfColorSheets = nodeText(root.find('SDOBI/B500/B590/B595US/PDAT'))
	patentGrant.numberOfFigures		= nodeText(root.find('SDOBI/B500/B590/B596/PDAT'))

	patObjects.append(patentGrant)

	#---------------------------------------------------------------
	# IPC Classification
	ipcVersion = nodeText(root.find('SDOBI/B500/B510/B516/PDAT'))
	for c in root.iterfind('SDOBI/B500/B510/*'):	# Classifications can be either B511 or B512, ignore B516
		if c.tag != 'B516':
			ic = x25.ClassificationIPCR()

			ic.patentGrant 			= patentGrant

			ic.classification 		= nodeText(root.find('PDAT'))
			ic.ipcVersion			= ipcVersion
			ic.firstPosition		= c.tag == 'B511'
			patObjects.append(ic)
	
	#---------------------------------------------------------------
	# National Classification
	natClass = bib.find('classification-national')
	for c in root.iterfind('SDOBI/B500/B520/*'):	# Classifications can be either B521 or B522, ignore B522US
		if c.tag != 'B522US':
			nc = x25.ClassificationNational()

			nc.patentGrant = patentGrant

			classification 		= nodeText(c.find('PDAT'))
			main 				= c.tag == 'B521'
			patObjects.append(nc)

	#---------------------------------------------------------------
	# References Cited
	for c in root.iterfind('SDOBI/B500/B560/*'):		# citations are either B561 or B562
		ci = x25.ReferenceCited()
		ci.patentGrant = patentGrant

		ci.refType		= 'PCIT' if c.tag == 'B561' else 'NCIT'
		if c.find('CITED-BY-EXAMINER') is not None:
			ci.category = 'CITED-BY-EXAMINER'
		elif c.find('CITED-BY-OTHER') is not None:
			ci.category = 'CITED-BY-OTHER'

		innerc = c.find(ci.refType)
		ci.docCountry		= noteText(innerc.find('DOC/CTRY/PDAT'))
		ci.docNumber		= noteText(innerc.find('DOC/DNUM/PDAT'))
		ci.docKind			= noteText(innerc.find('DOC/KIND/PDAT'))
		ci.docDate			= noteText(innerc.find('DOC/DATE/PDAT'))
		ci.docName			= noteText(innerc.find('PARTY-US/NAM/SNM/STEXT/PDAT'))
		ci.otherCit			= noteText(innerc.find('STEXT/PDAT'))
		patObjects.append(ci)


	#---------------------------------------------------------------
	# Field of Search Classes
	for fos in root.iterfind('SDOBI/B500/B580/*'):
		fc = x25.FieldOfSearch()
		fc.patentGrant = patentGrant

		if foc.tag == 'B582':
			fc.classification = noteText(foc.find('PDAT'))
		elif foc.tag == 'B581':
			IPCRClassification = nodeText(foc.find('PDAT'))
		elif foc.tag == 'B583US':
			unstructuredClass = noteText(foc.find('PDAT'))
		patObjects.append(fc)


	#---------------------------------------------------------------
	# Applicants
	applicants = bib.find('parties/applicants')
	if applicants is not None:
		for a in applicants.iter('applicant'):
			ap = ice.Applicant()
			ap.patentGrant		  = patentGrant
			ap.sequence			 = a.attrib.get('sequence', None) 
			ap.appType			  = a.attrib.get('app-type', None)
			ap.designation		  = a.attrib.get('designation', None)
			ap.lastName			 = nodeText(a.find('addressbook/last-name'))
			ap.firstName			= nodeText(a.find('addressbook/first-name')) 
			ap.city				 = nodeText(a.find('addressbook/address/city'))
			ap.state				= nodeText(a.find('addressbook/address/state'))
			ap.country			  = nodeText(a.find('addressbook/address/country'))
			ap.nationality		  = nodeText(a.find('nationality/country'))
			ap.residenceCountry	 = nodeText(a.find('residence/country'))
			patObjects.append(ap)


	#---------------------------------------------------------------
	# Agents
	agCount = 0
	for a in root.iter('SDOBI/B700/B740/B741'):
		ag = x25.Agent()
		ag.patentGrant = patentGrant
		agCount += 1

		ag.sequence		= agCount
		ag.orgName		= nodeText(a.find('PARTY-US/NAM/ONM/STEXT/PDAT'))
		ag.lastName		= nodeText(a.find('PARTY-US/NAM/SNM/STEXT/PDAT'))
		ag.firstName	= nodeText(a.find('PARTY-US/NAM/FNM/PDAT'))
		patObjects.append(ag)


	#---------------------------------------------------------------
	# Assignees
	assigneeRole = nodeText(root.find('SDOBI/B700/B730/B732US/PDAT'))
	for a in root.iter('SDOBI/B700/B730/B731'):
		ass = x25.Assignee()
		ass.patentGrant = patentGrant

		orgName		= nodeText(a.find('PARTY-US/NAM/ONM/STEXT/PDAT'))
		city		= nodeText(a.find('PARTY-US/ADR/CITY/PDAT'))
		country		= nodeText(a.find('PARTY-US/ADR/CTRY/PDAT'))
		role 		= assigneeRole
		patObjects.append(ass)



	#---------------------------------------------------------------------------
	# Inventors
	invCount = 0
	for i in root.iter('SDOBI/B700/B720/B721'):
		inv = x25.Inventor()
		invCount +=1
		inv.patentGrant = patentGrant

		inv.sequence		= invCount
		inv.lastName		= nodeText(inv.find('PARTY-US/NAM/SNM/STEXT/PDAT'))
		inv.firstName		= nodeText(inv.find('PARTY-US/NAM/FNM/PDAT'))
		inv.city			= nodeText(inv.find('PARTY-US/ADR/CITY/PDAT'))
		inv.country			= nodeText(inv.find('PARTY-US/ADR/CTRY/PDAT'))
		patObjects.append(inv)

	#---------------------------------------------------------------
	# Abstract
	abstract = root.find('SDOAB/BTEXT')
	if abstract is not None:
		for p in abstract.iter('PARA'):
			ap = x25.AbstractP()
			ap.patentGrant = patentGrant

			ap.abId 			= p.attrib.get('ID', None)
			ap.lvl 				= p.attrib.get('LVL', None)
			ap.asString 		= ElementTree.tostring(p)
			ap.content = ''
			for t in p.itertext(): 
				ap.content += t

			patObjects.append('ap')


	#---------------------------------------------------------------
	# Priority Claims
	for c in root.iter('SDOBI/B300'):
		cl = x25.PriorityClaim()
		cl.patentGrant = patentGrant
		cl.docNumber 		= nodeText(c.find('B310/DNUM/PDAT'))
		cl.docDate 			= nodeText(c.find('B320/DATE/PDAT'))
		cl.docCountry 		= nodeText(c.find('B330/CTRY/PDAT'))
		
		patObjects.append(cl)

	#---------------------------------------------------------------
	# Related Documents
	relationKind = {
		'B610':		'Addition',
		'B620':		'Division',
		'B630':		'Continuation',
		'B631':		'Continuation',
		'B632':		'Continue-in-part',
		'B633':		'Continue-Reissue',
		'B640':		'Reissue',
		'B641US':	'Divisional-Reissue',
		'B645':		'ReexamReq-applicant',
		'B646US':	'ReexamReq-other',
		'B650':		'PrevPub',
		'B660':		'SubbedDoc',
		'B680US':	'Provisional',
	}
	elementList = root.findall('SDOBI/B600/*') + root.findall('SDOBI/B600/B630/*')
	for doc in elementList:
		if doc.tag != 'B630':
			rd = x25.RelatedDocument()
			rd.patentGrant = patentGrant
			
			rd.relationKind = relationKind[doc.tag]
			rd.docCountry				= nodeText(doc.find('DOC/CTRY/PDAT'))
			rd.docNumber				= nodeText(doc.find('DOC/DNUM/PDAT'))
			rd.docKind					= nodeText(doc.find('DOC/KIND/PDAT'))
			rd.docDate					= nodeText(doc.find('DOC/DATE/PDAT'))
			rd.childCountry				= nodeText(doc.find('PARENT-DOC/CDOC/DOC/CTRY/PDAT'))
			rd.childNumber				= nodeText(doc.find('PARENT-DOC/CDOC/DOC/DNUM/PDAT'))
			rd.childKind				= nodeText(doc.find('PARENT-DOC/CDOC/DOC/KIND/PDAT'))
			rd.childDate				= nodeText(doc.find('PARENT-DOC/CDOC/DOC/DATE/PDAT'))
			rd.parentCountry			= nodeText(doc.find('PARENT-DOC/PDOC/DOC/CTRY/PDAT'))
			rd.parentNumber				= nodeText(doc.find('PARENT-DOC/PDOC/DOC/DNUM/PDAT'))
			rd.parentKind				= nodeText(doc.find('PARENT-DOC/PDOC/DOC/KIND/PDAT'))
			rd.parentDate				= nodeText(doc.find('PARENT-DOC/PDOC/DOC/DATE/PDAT'))
			rd.parentGrantCountry		= nodeText(doc.find('PARENT-DOC/PPUB/DOC/CTRY/PDAT'))
			rd.parentGrantNumber		= nodeText(doc.find('PARENT-DOC/PPUB/DOC/DNUM/PDAT'))
			rd.parentGrantKind			= nodeText(doc.find('PARENT-DOC/PPUB/DOC/KIND/PDAT'))
			rd.parentGrantDate			= nodeText(doc.find('PARENT-DOC/PPUB/DOC/DATE/PDAT'))
			patObjects.append(rd)

	#---------------------------------------------------------------------------
	# Examiners
	examinerDepartment = nodeText(root.find('SDOBI/B700/B748US/PDAT'))
	for e in root.iterfind('B700/B745/*/[PARTY-US]'): # gets child nodes of B700/B745/ that have PARTY-US child node
		em = x25.Examiner()
		em.patentGrant = patentGrant

		em.examinerType 	= 'Primary' if e.tag == 'B746' else 'Assistant'
		em.firstName		= nodeText(e.find('PARTY-US/NAM/FNM/PDAT'))
		em.lastName			= nodeText(e.find('PARTY-US/NAM/SNM/STEXT/PDAT'))
		em.department 		= examinerDepartment
		patObjects.append(em)


	#---------------------------------------------------------------------------
	# PCT or Regional Filings
	for f in root.iter('SDOBI/B800/B860'):
		fi = x25.PCTOrRegionalFiling()
		fi.patentGrant = patentGrant
		fi.docCountry   = nodeText(f.find('B861/DOC/CTRY/PDAT'))
		fi.docNumber	= nodeText(f.find('B861/DOC/DNUM/PDAT'))
		fi.docKind	  = nodeText(f.find('B861/DOC/KIND/PDAT'))
		fi.docDate	  = nodeText(f.find('B861/DOC/DATE/PDAT'))
		fi.date371	  = nodeText(f.find('B864US/DATE/PDAT'))
		patObjects.append(fi)

	#---------------------------------------------------------------------------
	# PCT or Regional Publishing
	for f in root.iter('SDOBI/B800/B870'):
		fi = x25.PCTOrRegionalPublishing()
		fi.patentGrant = patentGrant
		fi.docCountry   = nodeText(f.find('B871/DOC/CTRY/PDAT'))
		fi.docNumber	= nodeText(f.find('B871/DOC/DNUM/PDAT'))
		fi.docKind	  = nodeText(f.find('B871/DOC/KIND/PDAT'))
		fi.docDate	  = nodeText(f.find('B871/DOC/DATE/PDAT'))
		patObjects.append(fi)

	#---------------------------------------------------------------------------
	# Exemplary Claims
	for e in root.iter('SDOBI/B500/B570/B578US'):
		ex = x25.ExemplaryClaim()
		ex.patentGrant = patentGrant
		ex.claim = nodeText(e.find('PDAT'))
		patObjects.append(ex)


#-------------------------------------------------------------------------------
# FULLTEXT
#-------------------------------------------------------------------------------


	#---------------------------------------------------------------------------
	# Drawings 
	# drawings = grant.find('drawings')
	# if drawings is not None:
	# 	for fig in drawings.iter('figure')
	# 		fi = ice.Figure()
	# 		fi.patentGrant = patentGrant
	# 		fi.figureId		 = fig.attrib.get('id', None)
	# 		fi.num			  = fig.attrib.get('num', None)
	# 		img = fig.find('img')
	# 		fi.imgId			= img.attrib.get('id', None)
	# 		fi.imgHe			= img.attrib.get('he', None)
	# 		fi.imgWi			= img.attrib.get('wi', None)
	# 		fi.imgOrientation   = img.attrib.get('orientation', 'portrait')
	# 		fi.imgFile		  = img.attrib.get('file', None)
	# 		fi.imgAlt		   = img.attrib.get('alt', None)
	# 		fi.imgContent	   = img.attrib.get('img-content', 'drawing')
	# 		fi.imgFormat		= img.attrib.get('img-format', None)
	# 		patObjects.append(fi)

	#---------------------------------------------------------------------------
	# Description
	# description = grant.find('description')

	#---------------------------------------------------------------------------
	# Claims 
	# claims = grant.find('claims')
	
