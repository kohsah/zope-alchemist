##################################################################
#
# (C) Copyright 2006-2007 Kapil Thangavelu <kapilt at gmail.com>    
# All Rights Reserved
#
# This file is part of Alchemist.
#
# Alchemist is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alchemist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################
"""
Annotations for Table objects, to annotate as needed, the notion
is that the annotation keys correspond to column, and values correspond
to application specific column metadata.

$Id$
"""

from zope.interface import implements
from sqlalchemy.util import OrderedDict

class TableAnnotation( object ):

    def __init__(self, table_name, columns=(), properties=(), schema_order=(), table_columns=(), order_by=()):
        self.table_name = table_name
        self._options = {}
        self._annot = OrderedDict()

        for info in columns:
            self._annot[ info['name'] ] = info

        self.properties = properties
        self.schema_order = schema_order        
        self.table_columns = table_columns
        self.order_by = order_by

    def setOption( self, name, value ):
        self._options[ name ] = value
        
    def getOption( self, name, default=None ):
        return self._options.get( name, default )
    
    def __call__( self, context ):
        return ModelAnnotation( context, self )

    def __setitem__(self, name, value ):
        self._annot[name] = value

    def get( self, name, default=None ):
        return self._annot.get( name, default )

    def __getitem__(self, anme):
        return self.get( name )

    def values( self ):
        return self._annot.values()

    def __contains__(self, name ):
        marker = object()
        return not marker == self.get( name, marker )
