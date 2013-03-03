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
    form1 = SQLFORM(db.basic_information, record_id, showid = False,
                   labels = {'nicknames': 'Nicknames', 'email' : 'Alternate email', 'permanent_addr':'Permanent Address',
                             'btp_title':'BTP Title', 'btp_guide' : 'BTP Guide', 'dob' : 'Date of birth (YYYY-MM-DD)',
                             'best_memory':'Best memory at IIT Guwahati (<200 chars)', 
                             'wanted_to_do':'One thing that you wanted to but couldn\'t do at IITG (<200 chars)',
                             'people_dont_know':'One thing people don\'t know about you (<200 chars)', 'what_next':'What next?(<200 chars)', 
                             'after_15_years' : 'Where do you see yourself in 15 years?(<200 chars)', 
                             'claim_to_fame':'Your claim to fame at IITG(<200 chas)', 'song_describes_you':'One song title that describes your life'
                            }
                   )    
    
    if form1.process().accepted:
       response.flash = 'Form Accepted'
    elif form1.errors:
       response.flash = 'Form has Errors'

    retVal['form1'] = form1
    return retVal

@auth.requires_membership('drep')
def viewProfile():
    '''
    Displays profile of a student to the department representative.
    '''
    userid = int(request.args[0])
    profile = db(db.basic_information.userid == userid).select()
    profileExists = True
    data = []
    if len(profile) == 0:
        profileExists = False
    else:
        data.append(('Nicknames', profile[0]['nicknames']))
        data.append(('Date of birth',profile[0]['dob']))
        data.append(('Alternate email', profile[0]['email']))
        data.append(('Best memory', profile[0]['best_memory']))
        data.append(('BTP Guide', profile[0]['btp_guide']))
        data.append(('BTP Title', profile[0]['btp_title']))
        data.append(('Claim to fame', profile[0]['claim_to_fame']))
        data.append(('Favourite Quotation', profile[0]['favourite_quotation']))
        data.append(('Hostel', profile[0]['hostel']))
        data.append(('Phone', profile[0]['phone']))
        data.append(('Permanent Address', profile[0]['permanent_addr']))
        data.append(('One thing you couldn\'t do', profile[0]['wanted_to_do']))
        data.append(('One thing people don\'t know', profile[0]['people_dont_know']))
        data.append(('What next?', profile[0]['what_next']))
        data.append(('After 15 years', profile[0]['after_15_years']))
        data.append(('Song', profile[0]['song_describes_you']))
                    
    return dict(exists = profileExists, data = data)
    

@auth.requires_membership('drep')
def viewDeptProfiles():
    '''
    This displays the content of the profiles of all the students in the department. Only viewable for the department reps.
    '''
    row = db(db.department_student.userid == auth.user_id).select()[0]
    deptid = row['deptid']
    btech  = row['btech']

    basic_info = db((db.department_student.deptid == deptid) & (db.department_student.btech == btech) &
                    (db.basic_information.userid == db.department_student.userid) &
                    (db.auth_user.id == db.department_student.userid)).select('auth_user.id')
    info_filled = list()                    
    for i in basic_info: 
        info_filled.append(i['auth_user.id'])
        
    testimonials = db((db.department_student.deptid == deptid) & (db.department_student.btech == btech) &
                      (db.testimonials.receiver == db.department_student.userid) & 
                      (db.auth_user.id == db.department_student.userid)).select('auth_user.id')
    testimonial_received = list()                    
    for i in testimonials: 
        testimonial_received.append(i['auth_user.id'])    

    students = db((db.department_student.deptid == deptid) &(db.department_student.btech == btech) & 
                  (db.auth_user.id == db.department_student.userid)).select('auth_user.id', 'auth_user.first_name', 'auth_user.last_name')            
    
    studentsList = []
    for s in students:
        info = (s['auth_user.id'] in info_filled)                    
        if s['auth_user.id'] in testimonial_received:
            testimonial = 'Yes'
        else:
            testimonial = 'No'
        studentsList.append((s['auth_user.id'], s['auth_user.first_name'] + " " + s['auth_user.last_name'], info, testimonial))
        
    return dict(u = auth.user_id, deptid = deptid, btech = btech, studentsList = studentsList)


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
