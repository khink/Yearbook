# coding: utf8

# testimonials
db.define_table('testimonials',
    Field('author', db.auth_user, required = True, notnull = True),
    Field('receiver', db.auth_user, required = True, notnull = True),
    Field('testimony', 'text', required = True, notnull = True),
    format = '%(name)s')

# Department
db.define_table('departments',
    Field('name', 'string', length = 100, notnull = True, unique=True),
    Field('short', 'string', length=5, notnull = True, unique=True),
    format = '%(name)s')       
    
# basic_information table
db.define_table('basic_information',
    Field('name', 'string', length = 100, required = True, notnull = True),
    Field('email', 'string', length = 100, required = True, notnull = True, unique = True),
    Field('favourite_quotation', 'text'),
    Field('nicknames', 'string', length = 100),
    Field('userid', db.auth_user, required = True, notnull = True, unique = True),
    Field('department_id', db.departments, required = True, notnull = True),
    format = ' %(name)s')
