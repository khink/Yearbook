# coding: utf8

# testimonials
db.define_table('testimonials',
    Field('author', db.auth_user, required = True, notnull = True),
    Field('receiver', db.auth_user, required = True, notnull = True),
    Field('testimonial', 'text', required = True, notnull = True),
    Field('approved', 'boolean', required = True, default = 'false'),
    Field('created_on', 'datetime', required = True, default = request.now),
    format = '%(name)s')

# Department
db.define_table('departments',
    Field('name', 'string', length = 100, notnull = True, unique=True),
    Field('short', 'string', length=5, notnull = True, unique=True),
    format = '%(name)s')


# Department-student mapping
db.define_table('department_student',
    Field('userid', db.auth_user, required = True),
    Field('deptid', db.departments, required = True),
    format = '%(name)s')
# basic_information table
db.define_table('basic_information',
    Field('email', 'string', length = 100, required = True, notnull = True, unique = True),
    Field('favourite_quotation', 'text'),
    Field('nicknames', 'string', length = 100),
    Field('userid', db.auth_user, required = True, notnull = True, unique = True),
    format = ' %(name)s')
