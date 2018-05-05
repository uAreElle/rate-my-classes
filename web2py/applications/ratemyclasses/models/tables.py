# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
import datetime
from random import *

def get_user_email():
    return auth.user.email if auth.user is not None else None

def get_user_school():
    return auth.user.school if auth.user is not None else None

def make_random_id():
    return randint(4,9000)


db.define_table('myclass',
                Field('course_name'),   #Full course name ex. Web Applications
                Field('department', readable=False, writable=False),    #Can be full department name(i.e. Computer Science) or shorthand (i.e CMPS)
                Field('course_num', readable=False, writable=False),    #Course number ex. 101
                #Field('university'),    #To know which university this class belongs to
                Field('genEd', readable=False, writable=False),         #General education requirement it satisfies
                Field('info', readable=False, writable=False),          #The course details go here(a brief synopsis)
                Field('bookmark', 'boolean', default=False, readable=False, writable=False), #If the student wants to bookmark it it's true else false
                #Field('professor_name'), not sure how we want professor to be(input by the student or pre-approved, etc.)
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow(), readable=False, writable=False),
                Field('school_id', readable=True, writable=False)
)

db.define_table('university',
                Field('name'),          #Name of the university
                Field('state_name'),    #State that the university is in
                Field('city_name'),     #City the university is in
                Field('zipcode'),       #Zipcode
                Field('uni_bookmark', 'boolean', default=False) #A way to keep track if it's the student's school
)

db.define_table('reviews',
                Field('overall_rate'),
                Field('difficulty_rate'),
                Field('rec_professor')
)

#Dummy table testing
db.define_table('school',
                Field('name', default=get_user_school()),
                Field('school_id', default=make_random_id(), readable=False,    writable=False)
                )


# Pre-populate db with schools if none
if db(db.school.id>0).count() == 0:
    SCHOOLS = ['University of CA Santa Cruz', 'University of CA Berkeley', 'University of CA Merced']
    for i,s in enumerate(SCHOOLS):
        db.school.insert(name = s, school_id=i)
    db.commit()
# Test classes
if db(db.myclass.id>0).count() == 0:
    CLASSES = ['UCSC 101', 'UCB 102', 'UCM 103']
    for i,c in enumerate(CLASSES):
        db.myclass.insert(course_name = c, school_id=i)
    db.commit()



# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
