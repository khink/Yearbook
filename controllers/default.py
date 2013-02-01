# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to web2py!")
    redirect(URL('default','profile'))

@auth.requires_login()
def profile():                
    rows = db(db.basic_information.userid == auth.user_id).select()
    record_id = None
    action = 'editProfile'
    if len(rows) == 1:
        record_id = rows[0].id        
    retVal = dict()
    retVal['name'] = auth.user.first_name + " " + auth.user.last_name
    form1 = SQLFORM(db.basic_information, record_id,                     
               fields = ['email', 'nicknames', 'favourite_quotation'], 
               labels = {'name':'Full Name', 'nicknames':'Nicknames', 'email':'Alternate Email'},
               col3 = {'nicknames':'What do friends call you?'}, submit_button = 'Submit',                                                
               comments = False, keepopts = [], showid = False,
               ignore_rw = True, record_id = None,                        
               buttons = ['submit'], separator = ': ', _method = 'POST', 
               _action = action)
    if form1.process().accepted:
       response.flash = 'Form Accepted'
    elif form1.errors:
       response.flash = 'Form has Errors'                               
    
    retVal['form1'] = form1        
    return retVal

def editProfile():
    requestVars = request.post_vars
    if 'email' in requestVars and 'nicknames' in requestVars and 'favourite_quotation' in requestVars:
        rows = db(db.basic_information.userid == auth.user_id).select()        
        if len(rows) == 1:
            record_id = rows[0].id 
            db(db.basic_information.id == record_id).update(email=requestVars['email'], nicknames = requestVars['nicknames'],
                                                   favourite_quotation = requestVars['favourite_quotation'])
        elif len(rows) == 0:
            db.basic_information.insert(userid = auth.user_id, email = requestVars['email'],
                                        nicknames = requestVars['nicknames'], 
                                        favourite_quotation = requestVars['favourite_quotation']
                                    )
                                    
    redirect(URL('default','profile'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
