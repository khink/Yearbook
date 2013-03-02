# Values for Deparment table
import os 

depts = dict(
        bt  = 'Biotechnology',
        cle = 'Chemical Engineering',
        cst = 'Chemical Science and Technology',
        ce  = 'Civil Engineering',
        cse = 'Computer Science and Engineering',
        dod = 'Department of Design',
        ece = 'Electronics and Communications Engineering',
        eee = 'Electronics and Electrical Engineering',
        mnc = 'Mathematics and Computing',
        me  = 'Mechanical Engineering',
        phy = 'Phyics'
        )

if db(db.departments.id > 0).count() == 0:
  for dept in depts:
    db.departments.insert (short=dept, name=depts[dept])

if db(db.auth_user.id > 0).count() == 0:
  # Insert users    
    moduledir = os.path.dirname(os.path.abspath('__file__'))
    try:
        for dept in depts:           
            userInfo = open(os.path.join(moduledir, 'applications', 'yearbook2013', 'models', 'students', dept)).readlines()
            deptId   = db(db.departments.short == dept).select().first()['id']
            for user in userInfo:
                user = user.strip().split(',')
                #raise Exception (user)
                userId = db.auth_user.insert(                
                            password = db.auth_user.password.validate(user[2])[0],
                            email = user[1] + "@iitg.ac.in",
                            first_name = user[0].split()[0],
                            last_name = user[0].split()[-1],                
                         )
                db.department_student.insert (userid = userId, deptid = deptId, btech = (int(user[3]) == 1))
    except Exception as e:
        raise e
