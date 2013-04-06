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
        phy = 'Phyics',
        hss = "HSS"
        )

hostels = ['Barak', 'Brahmaputra', 'Dibang', 'Dihing', 'Kameng', 'Kapili', 'Manas', 'Siang', 'Subansiri', 'Umiam']

if db(db.hostels.id > 0).count() == 0:
    for hostel in hostels:
        db.hostels.insert(name = hostel)

if db(db.departments.id > 0).count() == 0:
  for dept in depts:
    db.departments.insert (short=dept, name=depts[dept])

moduledir = os.path.dirname(os.path.abspath('__file__'))
dbFiles = os.path.join(request.folder, 'models', 'students')

drepGid = 0
grepGid = 0
if db(db.auth_group.id > 0).count() == 0:
    # Create a group for representatives.
    dRepGid = db.auth_group.insert(role='drep', description='Department representative.')
    gRepGid = db.auth_group.insert(role='grep', description='Global representative.')

dReps = open(os.path.join(dbFiles, "dreps")).readlines()
gReps = open(os.path.join(dbFiles, "greps")).readlines()


if db(db.auth_user.id > 0).count() == 0:
  # Insert users
    for dept in depts:
        userInfo = open(os.path.join(dbFiles, dept)).readlines()
        deptId   = db(db.departments.short == dept).select().first()['id']
        for user in userInfo:
            user = user.strip().split(',')
            first_name = user[0].split()[0]
            last_name  = user[0].split()[-1]

            first_name = first_name[0].upper() + first_name[1:].lower()
            last_name  = last_name[0].upper() + last_name[1:].lower()
            #raise Exception (user)
            userId = db.auth_user.insert(
                        password = db.auth_user.password.validate(user[2])[0],
                        email = user[1] + "@iitg.ac.in",
                        first_name = first_name,
                        last_name = last_name,
                     )
            db.department_student.insert (userid = userId, deptid = deptId, btech = (int(user[3]) == 1))
            if user[1] + "\n" in dReps:
                db.auth_membership.insert(user_id = userId, group_id = dRepGid)
            if user[1] + "\n" in gReps:
                db.auth_membership.insert(user_id = userId, group_id = gRepGid)
