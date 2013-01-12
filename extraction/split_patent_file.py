import re
import codecs
import htmlentitydefs
from PatentTools.extraction import uspto_sgml_entities

codecs.register_error('spacer', lambda ex: (u' ', ex.start + 1))

# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

preunescape_re = re.compile('&.+?;')
def _preunescape_sub(m):
	"""
	Callback for the preunescape function below
	"""
	keepers = ['&quot;', '&amp;', '&apos;', '&lt;', '&gt;']
	content = m.group(0)
	if content not in keepers:
		return re.sub('&', '&amp;', content)
	else:
		return content

def preunescape(text):
	"""
	USPTO's SGML definition has almost 2000 SGML entities which map to various characters
	needing UTF16 representation.  For this application, the mapping is kept in the dictionary
	PatentTools.extraction.uspto_sgml_entities 
	Rather than do the conversion in this application we prep the text so that it can be parsed
	with an ordinary XML parser by changing all '&' that appear at the begining of a chunk of 
	characters to '&amp;'
	HOWEVER, we SKIP the 5 entities defined by xml: ['&quot;', '&amp;', '&apos;', '&lt;', '&gt;']
	"""
	return preunescape_re.sub(_preunescape_sub, text)





def identify_zip(filename):
	"""
	takes the filename of a zip file and identifies the encoding type
	# Patent Grant Data / XML ST. 36 (ICE) v4.2 (a.k.a. Red Book) (2007 - present)
	# Patent Grant Data / XML ST. 36 (ICE) v4.1 (a.k.a. Red Book) (2006)
	# Patent Grant Data / XML ST. 36 (ICE) v4.0 (a.k.a. Red Book) (2005)
	# Patent Grant Data / XML ST. 32 v2.5 (a.k.a. Red Book) (2002-2004)
	# Patent Grant Data / SGML ST. 32 v2.4 (2001)
	# Patent Grant Data / APS - ASCII (1976-2001)
	"""


	ice = re.compile('ipgb(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_wk\d{2}')
	xml = re.compile('pgb(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_wk\d{2}')
	aps = re.compile('pba(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_wk\d{2}')
	yr 	= re.compile('(?P<year>\d{4})')

	mice = ice.match(filename)
	mxml = xml.match(filename)
	maps = aps.match(filename)
	myr  = yr.match(filename)

	if mice:
		y = int(mice.group('year'))
		if y >= 2007:
			return 'ice42'
		elif y >= 2006:
			return 'ice41'
		elif y >= 2005:
			return 'ice40'
		else:
			return None
	elif mxml:
		y = int(mxml.group('year'))
		if y >= 2002:
			return 'xml25'
		else:
			return 'sgml'
	elif maps:
		return 'aps'
	elif myr:
		return 'aps'

	else:
		return None




def split_ice(xmlfile):
	try:
		f = open(xmlfile, 'r')
	except:
		return

	xmlout = '<top>'
	for line in f:
		line = line.decode('utf8', 'spacer')
		if (line.find('<?xml') == -1 and line.find('<!DOCTYPE') == -1):
			xmlout = xmlout + line
		if line.find('</us-patent-grant>') > -1:
			xmlout = xmlout + '</top>'
			yield xmlout
			xmlout = '<top>'
	f.close()


def split_xml25(xmlfile):
	"""
	the sgml files are encoded as utf8, but contain html entities
	which must be represented in utf16. eg. &ldquo; -> \u201c

	preunescape will transform the ampersand in entities to '&amp;'
	We can process the entities at a later time
	"""
	try:
		f = open(xmlfile, 'r')
	except:
		return

	xmlout = ''
	for line in f:
		line = line.decode('utf8', 'spacer')
		line = preunescape(line)
		if (line.find('<?xml') == -1 and line.find('<!') == -1 and line.find('<') == 0):
			xmlout = xmlout + line
		if line.find('</PATDOC>') > -1:
			yield xmlout
			xmlout = ''
	f.close()


def split_aps(apsfile):
	try:
		f = open(apsfile, 'r')
	except:
		return

	apsout = ''
	for line in f:
		line = line.decode('utf8')
		if (line.find('PATN') == 0 and len(apsout) > 0):
			yield apsout
			apsout = line
		elif line.find('H') != 0:
			apsout = apsout + line

	f.close()


def validate_xml_string(xmlstring):
	"""
	Raises an error when the xmlstring does not parse
	"""
	from xml.dom import minidom
	minidom.parseString(xmlstring)





#-------------------------------------------------------------------------------
# NOT USED, BUT KEEP ANYWAY
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1].lower()])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

if __name__ == '__main__':
	import os
	f = open('xml25.txt', 'w')

	i = 0
	for t in split_xml25(os.path.join(os.getcwd(), 'SampleData', 'Bibliographic', 'pgb20040601.xml')):
		i += 1
		if i == 500:
			f.write(t)
			break

	f.close()
	# import os
	# xmlfile = os.path.join(os.getcwd(), 'SampleData', 'Bibliographic', 'pgb20040601.xml')
	# find_funny_characters(xmlfile)	
