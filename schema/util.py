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
