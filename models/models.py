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
    Field('btech', 'boolean'),
    format = '%(name)s')

db.define_table('hostels',
    Field('name', 'string', length = 20, notnull = True, unique = True),
    format = '%(name)s')

lengthForText = 200
# basic_information table
db.define_table('basic_information',
    Field('rollno', 'string', length = 10, required = True, notnull = True),
    Field('email', 'string', length = 100, required = True, notnull = True),
    Field('favourite_quotation', 'text', length = lengthForText),
    Field('nicknames', 'string', length = 100),
    Field('userid', db.auth_user, required = True, notnull = True, unique = True, readable = False, writable = False, default = auth.user_id),
    Field('hostel', db.hostels, required = True),
    Field('permanent_addr', 'string', length=100, required = True, notnull = True),
    Field('dob', 'date', required = True, notnull = True),
    Field('phone', 'string', required = True, notnull = True),
    Field('btp_title', 'string', length = 100, required = True),
    Field('btp_guide', 'string', length = 40, required = True),
    Field('best_memory', 'text', length = lengthForText, required = True),
    Field('wanted_to_do', 'text', length = lengthForText, required = True),
    Field('people_dont_know', 'text', length = lengthForText, required = True),
    Field('what_next', 'text', length = lengthForText, required = True),
    Field('after_15_years', 'text', length = lengthForText, required = True),
    Field('claim_to_fame', 'text', length = lengthForText, required = True),
    Field('song_describes_you', 'string', length = 100, required = True),
    format = ' %(name)s')
