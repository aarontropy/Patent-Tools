from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types

Base = declarative_base()

DATABASE = 'Patent_Test'
USERNAME = 'sqlalchemy'
PASSWORD = 'sqlalchemy'


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]

def engine():
	return create_engine('mysql://%(username)s:%(password)s@127.0.0.1/%(database)s' % {
		'username': USERNAME,
		'password': PASSWORD,
		'database': DATABASE
		} )

def create_schema():
	db = engine()
	Base.metadata.create_all(db)


from patent import *
from entity import *
from litigation import *

