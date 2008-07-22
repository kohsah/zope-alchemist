"""
Generic Content Views

"""

from zope import interface
from zope.event import notify
from zope.formlib import form
from zope.lifecycleevent import ObjectCreatedEvent
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zope.publisher.browser import BrowserView

from zope.app.pagetemplate import ViewPageTemplateFile

from ore.alchemist import Session
from sqlalchemy import orm

from i18n import _
import generic, core


class AddFormBase( object ):

    _next_url = None
    adapters = None

    def createAndAdd( self, data ):

        domain_model = removeSecurityProxy( self.context.domain_model )
        # create the object, inspect data for constructor args      
        try:  
            ob = generic.createInstance( domain_model, data )
        except TypeError:
            ob = domain_model()
        
        # apply any context values
        self.finishConstruction( ob )
        
        # apply extra form values
        form.applyChanges( ob, self.form_fields, data, self.adapters )
        
        # save the object, id is generated by db on flush
        self.context[''] = ob
        
        # flush so we have database id
        session = Session()
        session.flush()
        
        # fire an object created event
        notify(ObjectCreatedEvent(ob))
        
        # signal to add form machinery to go to next url
        self._finished_add = True
        
        mapper = orm.object_mapper( ob )
        
        # TODO single primary key ( need changes to base container)
        oid = mapper.primary_key_from_instance( ob )
        
        # retrieve the object with location and security information
        return self.context[ oid ]
        
    def finishConstruction(self, ob ):
        """ no op, subclass to provide additional initialization behavior"""
        return 
        
    def nextURL( self ):
        if not self._next_url:
            return absoluteURL( self.context, self.request )
        return self._next_url
        
    def update( self ):
        self.status = self.request.get('portal_status_message','')
        super( AddFormBase, self).update()

    def validateAdd(self, action, data ):
        errors = self.validateUnique(action, data )
        return errors
        
    @form.action(_(u"Cancel"), validator=core.null_validator )
    def handle_cancel( self, action, data ):
        url = self.nextURL()
        return self.request.response.redirect( url )
        
    @form.action(_(u"Save and continue editing"), condition=form.haveInputWidgets, validator='validateAdd')
    def handle_add_edit( self, action, data ):
        ob = self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( ob, self.request ) + "/@@edit?portal_status_message=%s Added"%name
        
    @form.action(_(u"Save and add another"), condition=form.haveInputWidgets)
    def handle_add_and_another(self, action, data ):
        self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( self.context, self.request ) + '/@@add?portal_status_message=%s Added'%name
        
    def invariantErrors( self ):        
        errors = []
        for error in self.errors:
            if isinstance( error, interface.Invalid ):
                errors.append( error )
        return errors

class Add( AddFormBase, form.AddForm ):
    """
    static add form for db content
    """

class DynamicAdd( core.DynamicFields, Add):
    """
    generic add form ( dynamic fields ) for db content
    """
    mode = "add"

ContentAddForm = DynamicAdd

class Display( BrowserView ):
    """
    Content Display
    """
    template = ViewPageTemplateFile('templates/content-view.pt')
    form_name = _("View")    
    
    def __call__( self ):
        return self.template()

ContentDisplayForm = Display
        
class ContentEditForm( BrowserView ):
    """
    Content Edit View
    """
    template = ViewPageTemplateFile('templates/content-edit.pt')
    form_name = _("Edit")
    
    def __call__( self ):
        return self.template()

class EditForm( form.EditForm ):

    adapters = None

    def setUpWidgets( self, ignore_request=False):
        self.adapters = self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
            
    @form.action(_(u"Cancel"), condition=form.haveInputWidgets, validator=core.null_validator)
    def handle_cancel_action( self, action, data ):
        return core.handle_edit_action( self, action, data )            
        
    @form.action(_(u"Save"), condition=form.haveInputWidgets)
    def handle_edit_action( self, action, data ):
        return core.handle_edit_action( self, action, data )
    
    def invariantErrors( self ):        
        errors = []
        for error in self.errors:
            if isinstance( error, interface.Invalid ):
                errors.append( error )
        return errors
