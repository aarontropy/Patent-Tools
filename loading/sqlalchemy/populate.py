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
import PatentTools.schema.ICE42 as ice

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


# def populate(inputFile):
# 	db = schema.engine()
# 	db.echo = False

# 	Session = sessionmaker(bind=db)
# 	session = Session()



def parse_ICE(filename):

	#start parsing
	doc = ElementTree()
	doc.parse(filename)
	root = doc.getroot()


	#loop for main patent
	grant = root.find("us-patent-grant")
	bib = root.find('us-patent-grant/us-bibliographic-data-grant')
	if not bib or not grant:
		# give up now
		return

	patObjects = []

	patentGrant = ice.UsPatentGrant()
	patentGrant.lang			   = grant.attrib.get('lang', None)
	patentGrant.dtdVersion		 = grant.attrib.get('dtd-version', None)
	patentGrant.singleFile		 = grant.attrib.get('file', None)
	patentGrant.groupFile		  = "WHAT AM I?"
	patentGrant.status			 = grant.attrib.get('status', None)
	patentGrant.dateProduced	   = grant.attrib.get('date-produced', None)
	patentGrant.datePublished	  = grant.attrib.get('date-publ', None)

	patentGrant.docCountry		   = nodeText(bib.find('publication-reference/document-id/country'))
	patentGrant.docNumber		  = nodeText(bib.find('publication-reference/document-id/doc-number'))
	patentGrant.docKind			= nodeText(bib.find('publication-reference/document-id/kind'))
	patentGrant.docDate			= nodeText(bib.find('publication-reference/document-id/date'))

	patentGrant.appType			= bib.find('application-reference').attrib.get('appl-type', None)
	patentGrant.appCountry		 = nodeText(bib.find('application-reference/document-id/country'))
	patentGrant.appNumber		  = nodeText(bib.find('application-reference/document-id/doc-number'))
	patentGrant.appDate			= nodeText(bib.find('application-reference/document-id/date'))

	patentGrant.grantLength		= '?'
	patentGrant.termExtension	  = nodeText(bib.find('us-term-of-grant/us-term-extension'))

	patentGrant.appSeriesCode	  = nodeText(bib.find('us-application-series-code'))
	patentGrant.inventionTitle	 = nodeText(bib.find('invention-title'))
	patentGrant.inventionTitleId   = bib.find('invention-title').attrib.get('id', None)
	patentGrant.numberOfClaims	   = nodeText(bib.find('number-of-claims'))
	patentGrant.usExemplaryClaims  = nodeText(bib.find('us-exemplary-claim'))
    patentGrant.numberOfSheets      = nodeText(bib.find('figures/number-of-drawing-sheets'))
    patentGrant.numberOfFigures     = nodeText(bib.find('figures/number-of-figures'))

	patObjects.append(patentGrant)

	#---------------------------------------------------------------
	# IPC Classification
	ipcClass = bib.find('classifications-ipcr')
	if ipcClass is not None:
		for c in ipcClass.iter('classification-ipcr'):
			ic = ice.ClassificationIPCR()
			ic.patentGrant		= patentGrant
			ic.ipcVersion		 = nodeText(c.find('ipc-version-indicator/date'))
			ic.klassLevel		 = nodeText(c.find('classification-level'))
			ic.section			= nodeText(c.find('section'))
			ic.klass			  = nodeText(c.find('class'))
			ic.subKlass		   = nodeText(c.find('subclass'))
			ic.mainGroup		  = nodeText(c.find('main-group'))
			ic.subGroup		   = nodeText(c.find('subgroup'))
			ic.symbolPosition	 = nodeText(c.find('symbol-position'))
			ic.value			  = nodeText(c.find('classification-value')) 
			ic.actionDate		 = nodeText(c.find('action-date/date'))
			ic.genOfficeCountry	 = nodeText(c.find('generating-office/country'))
			ic.klassStatus		  = nodeText(c.find('classification-status'))
			ic.klassDataSource	  = nodeText(c.find('classification-data-source')) 
			patObjects.append(ic)
	
	#---------------------------------------------------------------
	# National Classification
	natClass = bib.find('classification-national')
	if natClass is not None:
		natClassCountry = nodeText(natClass.find('country'))
		for c in natClass.getchildren():
			if c.tag.find('classification') != -1:
				nc = ice.ClassificationNational()
				nc.patentGrant   = patentGrant
				nc.country	   = natClassCountry
				nc.text		  = nodeText(c)
				if c.tag == 'main-classification':
					nc.main = True
				elif c.tag == 'further-classification':
					nc.main = False
				patObjects.append(nc)


	#---------------------------------------------------------------
	# References Cited
	refCited = bib.find('references-cited')
	if refCited is not None:
		for c in refCited.iter('citation'):
			ci = ice.ReferenceCited()
			ci.patentGrant	  = patentGrant
			if c.find('patcit'):
				ci.refType = 'patcit'
                ci.klassCountry = nodeText(c.find('classification-national/country'))
                ci.klassMain = nodeText(c.find('classification-national/main-classification'))
				cir = c.find('patcit/document-id')
			elif c.find('nplcit'):
				ci.refType = 'nplcit'
				cir = c.find('nplcit/document-id')
			ci.num			= cir.attrib.get('num', None)
			ci.category	   = nodeText(c.find('category'))
			ci.otherCit	   = nodeText(cir.find('othercit'))

			ci.docCountry	 = nodeText(cir.find('country'))
			ci.docNumber	  = nodeText(cir.find('doc-number'))
			ci.docName		= nodeText(cir.find('name'))
			ci.docKind		= nodeText(cir.find('kind'))
			ci.docDate		= nodeText(cir.find('date'))
			patObjects.append(ci)

	#---------------------------------------------------------------
	# Field of Search Classes
	fos = bib.find('us-field-of-classification-search')
	if fos is not None:
		for c in fos.iter('classification-national'):
			fc = ice.FieldOfSearch()
			fc.patentGrant  = patentGrant
			fc.country	  = nodeText(c.find('country'))
			fc.mainKlass	= nodeText(c.find('main-classification'))
            fc.additionalInfo   = nodeText(c.find('additional-info'))
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
	agents = bib.find('parties/agents')
	if agents is not None:
		for a in agents.iter(''):
			ag = ice.Agent()
			ag.patentGrant = patentGrant
			ag.sequence	 = a.attrib.get('sequence', None)
			ag.repType	  = a.attrib.get('rep-type', None)
			ag.orgName	  = nodeText(a.find('addressbook/orgname'))
			ag.lastName	 = nodeText(a.find('addressbook/last-name'))
			ag.firstName	= nodeText(a.find('addressbook/first-name'))
			ag.country	  = nodeText(a.find('country'))
			patObjects.append(ag)
	
	#---------------------------------------------------------------
	# Assignees
	assignees = bib.find('assignees')
	if assignees is not None:
		for a in assignees.iter(''):
			ae = ice.Assignee()
			ae.patentGrant  = patentGrant
			ae.orgName	  = nodeText(a.find('addressbook/orgname'))
			ae.role		 = nodeText(a.find('addressbook/role'))
			ae.city		 = nodeText(a.find('addressbook/address/city'))
			ae.state		= nodeText(a.find('addressbook/address/state'))
			ae.country	  = nodeText(a.find('addressbook/address/country'))
			patObjects.append(ae)

	#---------------------------------------------------------------
	# Abstract
	abstract = grant.find('abstract')
	if abstract is not None:
		for p in abstract.iter('p'):
			# create abstract p items
			ap = ice.AbstractP()
			ap.patentGrant = patentGrant
			ap.abId		 = p.attrib.get('id', None)
			ap.num		  = p.attrib.get('num', None)
			ap.content	  = nodeText(p)
			for c in p.iter('chemistry'):
				ch = ice.AbstractChemistry()
				ch.abstractP = ap

				ch.chemId	   = ch.attrib.get('id', None)
				ch.num		  = ch.attrib.get('num', None)
				img = ch.find('img')
				if img is not None:
					ch.imgId		= img.attrib.get('id', None)
					ch.imgHe		= img.attrib.get('he', None)
					ch.imgWi		= img.attrib.get('wi', None)
					ch.imgFile	  = img.attrib.get('file', None)
					ch.imgAlt	   = img.attrib.get('alt', None)
					ch.imgContent   = img.attrib.get('img-content', None)
					ch.imgFormat	= img.attrib.get('img-format', None)
				patObjects.append(ch)
			patObjects.append('ap')


	#---------------------------------------------------------------
	# Priority Claims
	pclaims = bib.find('priority-claims')
	if pclaims is not None:
		for c in pclaims.iter('priority-claim'):
			cl = ice.PriorityClaim()
			cl.patentGrant = patentGrant
			cl.sequence	 = c.attrib.get('sequence', None)
			cl.kind		 = c.attrib.get('kind', None)
			cl.country	  = nodeText(c.find('country'))
			cl.docNumber	= nodeText(c.find('doc-number'))
			cl.date		 = nodeText(c.find('date'))
			patObjects.append(cl)

	#---------------------------------------------------------------
	# Related Documents
	related = bib.find('us-related-documents')
	if related is not None:
		for r in related.getchildren():
			if r.tag in ['continuation', 'continuation-in-part', 'division']:
				pass
			elif r.tag in ['us-provisional-application', 'related-publication']:
				pass

	#---------------------------------------------------------------------------
	# Examiners
	exam = bib.find('examiners')
	if exam is not None:
		for e in exam.getchildren():
			em = ice.Examiner()
			em.patentGrant  = patentGrant
			em.examinerType = e.tag
			em.firstName	= nodeText(e.find('first-name'))
			em.lastName	 = nodeText(e.find('last-name'))
			em.department   = nodeText(e.find('department'))
			patObjects.append(em)

    #---------------------------------------------------------------------------
    # Foreign Filings
    for f in bib.iter('pct-or-regional-filing-data'):
        fi = ice.ForeignFiling()
        fi.patentGrant = patentGrant
        fi.docCountry   = nodeText(f.find('document-id/country'))
        fi.docNumber    = nodeText(f.find('document-id/doc-number'))
        fi.docKind      = nodeText(f.find('document-id/kind'))
        fi.docDate      = nodeText(f.find('document-id/date'))
        fi.date371      = nodeText(f.find('us-371c124-date/date'))
        patObjects.append(fi)

    #---------------------------------------------------------------------------
    # Foreign Publishing
    for f in bib.iter('pct-or-regional-publishing-data'):
        fi = ice.ForeignPublishing()
        fi.patentGrant = patentGrant
        fi.docCountry   = nodeText(f.find('document-id/country'))
        fi.docNumber    = nodeText(f.find('document-id/doc-number'))
        fi.docKind      = nodeText(f.find('document-id/kind'))
        fi.docDate      = nodeText(f.find('document-id/date'))
        patObjects.append(fi)
