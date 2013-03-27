# coding: utf8
# try something like
def index(): 
    redirect('view')

@auth.requires_login()
def approve():
    if len(request.args) >= 0:
        t = 0
        try:
            post_id = int(request.args[0])
            t = 1
            row = db(db.testimonials.id == post_id).select()[0]
            t = 2
            if auth.user_id == int(row['receiver']):
                t = 3
                db(db.testimonials.id == post_id).update(approved = 'True')
                t = 4
            #return dict(vars=request.vars, args=request.args)
        except Exception as e:
#            return dict(message="Failed", t = t, e = e)
            pass  # Add logging here
    
    redirect(URL('testimonials','view'))
    
@auth.requires_login()    
def disapprove():
    if len(request.args) >= 0:
        t = 0
        try:
            post_id = int(request.args[0])
            t = 1
            row = db(db.testimonials.id == post_id).select()[0]
            t = 2
            if auth.user_id == int(row['receiver']):
                t = 3
                db(db.testimonials.id == post_id).update(approved = 'False')
                t = 4
            #return dict(vars=request.vars, args=request.args)
        except Exception as e:
#            return dict(message="Failed", t = t, e = e)
            pass  # Add logging here
    
    redirect(URL('testimonials','view'))

@auth.requires_login()
def view():
    # Fetch testimonials for the logged in user.
    rows = db(db.testimonials.receiver == auth.user_id).select()
    testimonials = []
    for row in rows:
        author = db(db.auth_user.id == row['author']).select()[0]
        name = author['first_name'] + " " + author['last_name']
        if row['approved']: actionURL = URL('testimonials', 'disapprove', args=[str(row['id'])])        
        else : actionURL = URL('testimonials', 'approve', args=[str(row['id'])])    
        testimonials.append(dict(id = row['id'], name = name, content = row['testimonial'], approved = row['approved'], url = actionURL, time = row['created_on']))
        
    return dict(testimonials = testimonials)

@auth.requires_login()
def edit():
    receiver = int(request.args[0])
    rows = db((db.testimonials.receiver == receiver) & (db.testimonials.author == auth.user_id)).select()
    receiverDetails = db(db.auth_user.id == receiver).select().first()
    receiverName = receiverDetails['first_name'] + " " + receiverDetails['last_name']
    form1 = None
    if len(rows) == 1:
        record_id = int(rows[0]['id'])
        form1 = SQLFORM(db.testimonials, record_id,                     
               fields = ['testimonial'], 
               labels = {'testimonial':'Testimonial'}, submit_button = 'Update',                                                
               comments = False, keepopts = [], showid = False,
               ignore_rw = True, buttons = ['submit'], separator = ': ', _method = 'POST')
        if form1.process().accepted:
           response.flash = 'Changes Accepted'
        elif form1.errors:
           response.flash = 'Form has Errors' 
    else:
        form1 = SQLFORM(db.testimonials, fields = ['testimonial'], 
               labels = {'testimonial':'Testimonial'}, submit_button = 'Submit',                                                
               comments = False, keepopts = [], showid = False,
               ignore_rw = True, buttons = ['submit'], separator = ': ', _method = 'POST',
               _action = URL('testimonials', 'editSubmit', args=[receiver]))
    
    return dict(form=form1, receiver = receiverName)       
    
@auth.requires_login()
def editSubmit():
    receiver = int(request.args[0])    
    author = auth.user_id
    if 'testimonial' not in request.vars or receiver == author:
        redirect(URL('testimonials', 'post'))
    
    
    # First make sure that a record doesn't already exist
    rows = db((db.testimonials.receiver == receiver) & (db.testimonials.author == author)).select()
    if len(rows) > 0:
        if rows[0]['approved']:
            raise Exception("Cannot change existing entry")
        else:
            rows[0].update(testimonial=request.vars['testimonial'])
    else:
         db.testimonials.insert(author = author, receiver = receiver, testimonial = request.vars['testimonial'])
         
    redirect (URL('testimonials', 'edit', args=[receiver]))    
    

@auth.requires_login()
def view_sent():
    '''
    Function to see all the sent testimonials
    '''
    rows = db(db.testimonials.author == auth.user_id).select()
    testimonials = []
    for row in rows:
        receiver = db(db.auth_user.id == row['receiver']).select()[0]
        name = receiver['first_name'] + " " + receiver['last_name']
        editURL = URL('testimonials', 'edit', args=[str(row['receiver'])])                
        testimonials.append(dict(id = row['id'], name = name, content = row['testimonial'], approved = row['approved'], url = editURL, time = row['created_on']))
    return dict(testimonials=testimonials)

@auth.requires_login()
def post():     
    vars = request.vars    
    
    if 'student' in vars:
        fields = ['testimonials.receiver', 'testimonials.created_on', 'testimonials.approved', 'testimonials.testimonial', 'auth_user.first_name', 'auth_user.last_name']
        earlierTestimonial = db( (db.testimonials.author == auth.user_id) & (db.testimonials.receiver == int(vars['student']))).select(*fields, 
                                join = db.auth_user.on(db.auth_user.id == db.testimonials.receiver))        
        testimonialExists = (len(earlierTestimonial) == 1)
        editURL = URL('testimonials', 'edit', args=[vars['student']])
        if testimonialExists:
            earlierTestimonial[0]['url'] = editURL
        else:
            redirect(editURL)
        return dict(state = 3, testimonialExists = testimonialExists, table=earlierTestimonial[0])
    elif 'dept' in vars:
        # Give a list of students in that department        
        rows = db(db.department_student.deptid == int(vars['dept'])).select(
                    join=db.auth_user.on( (db.department_student.userid == db.auth_user.id) & (db.auth_user.id != auth.user_id)) )        
        #join=db.thing.on(db.person.id==db.thing.owner))
        tableBtech = []
        tableMtech = []
        for row in rows:
            if row['department_student.btech']:
                table = tableBtech
            else:
                table = tableMtech
            table.append(dict(name = row['auth_user.first_name'] + " " + row['auth_user.last_name'], 
                              url  = URL('testimonials', 'post', vars=dict(student=row['auth_user.id']))))            
        return dict(state = 2, tableBtech=tableBtech, tableMtech = tableMtech)            
    else:
        # Give a list of departments
        rows = db(db.departments).select()        
        for row in rows:
            row['url'] = URL('testimonials', 'post', vars=dict(dept=row['id']))
        return dict(state = 1, table = rows)
