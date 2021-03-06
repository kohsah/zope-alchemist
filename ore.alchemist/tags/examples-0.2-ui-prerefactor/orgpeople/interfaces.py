"""
defines schema annotations for ui information

transforms sqlalchemy table definitions into zope 3 schemas
using the annotation.

modifies the domain classes to attach the schema interface 

$Id$
"""

from zope.interface import Interface, directlyProvides
from ore.alchemist.annotation import TableAnnotation
from ore.alchemist.sa2zs import transmute
from zope import schema as zschema
from zope.schema.interfaces import IContextSourceBinder

import schema

PersonAnnotation = TableAnnotation(
    "Person",
    columns = [
         dict( name="first_name", label = "First Name", table_column=True ),
         dict( name="middle_initial", label = "Middle Initial", table_column=True ),         
         dict( name="last_name", label = "Last Name",  table_column=True ),
         dict( name="email", label = "Email Address", table_column=True ),
         dict( name="phone_number", label = "Home Phone Number"),
         ]
    )

AddressAnnotation = TableAnnotation(
    "Address",
    columns = [
        dict( name="address_id", omit = True ),
        dict( name="address_1", label = "address line 1"),
        dict( name="address_2", label = "address line 2"),
        ]
    )


from vocabulary import StateVocabulary
                  
IAddressTable = transmute( schema.AddressTable,
                           AddressAnnotation,
                           properties = {'state':zschema.Choice( title=u"state", vocabulary=StateVocabulary() ) },
                           __module__="Products.orgperson.interfaces" )

IPersonTable = transmute( schema.PersonTable,
                          PersonAnnotation,
                          properties = {'address':zschema.Object( IAddressTable, required=False ) },
                          __module__="Products.orgperson.interfaces" )


class IPersonContainer( Interface ):
    """ marker interface for adding app specific views and adapters to generic containers """
