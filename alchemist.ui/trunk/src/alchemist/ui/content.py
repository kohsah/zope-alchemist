"""

This module gets populated with generic add/edit/view forms for
domain objects.

"""

from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.formlib import form
from zope.formlib.namedtemplate import NamedTemplate
from zope.traversing.browser import absoluteURL
    
class AddForm( form.AddForm ):
    """
    generic add form for piston
    """
     
    def createAndAdd( self, data ):
        # create the object
        ob = createInstance( self.context.domain_model, data )

        # apply extra form values
        form.applyChanges( ob, self.form_fields, data )
        
        # fire an object created event
        notify(ObjectCreatedEvent(ob))
        
        # save the object, id is generated by db
        self.context[''] = ob

        # signal to add form machinery to go to next url
        self._finished_add = True
        
    def nextURL( self ):
        return absoluteURL( self.context, self.request )
        
class EditForm( form.EditForm ):
    """
    generic edit form for piston
    """
    
    
class View( form.DisplayForm ):
    """
    generic view form for piston
    """

