from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship, backref, relation
from sqlalchemy.schema import ForeignKey

from PatentTools.schema import Base


class RetrievedFile(Base):
	__tablename__ = "files_retrieved"

	id				= Column(Integer, primary_key=True)
	filename		= Column(String(255))
	url				= Column(String(255))
	downloadDate 	= Column(DateTime)
	loadDate 		= Column(DateTime)

class FileDownloadRecord(Base):
	__tablename__ = "FileDownloadRecord"

	id = Column(Integer, primary_key=True)
	url 			= Column(String(255))
	tmpFilename 	= Column(String(255))
	downloadDate 	= Column(DateTime)	
	imported 		= Column(Boolean)

class PatentImportRecord(Base):
	__tablename__ = "PatentImportRecord"

	id 				= Column(Integer, primary_key=True)
	docNumber 		= Column(String(10))
	url 			= Column(String(255))

	fileDownloadRecord_id 	= Column(Integer, ForeignKey(FileDownloadRecord.id))
	fileDownloadRecord 		= relation("FileDownloadRecord", backref=backref("patentImports", cascade=None))

