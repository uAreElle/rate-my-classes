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

def get_user_firstname():
    return auth.user.first_name if auth.user is not None else None


def make_random_id():
    return randint(4,9000)


#Dummy table testing
db.define_table('school',
                Field('name', default=get_user_school()),
                Field('school_id', default=make_random_id(), readable=False, writable=False)
                )

db.define_table('myclass',
                Field('department'),    #Can be full department name(i.e. Computer Science) or shorthand (i.e CMPS)
                Field('course_num', label='Course Number'),    #Course number ex. 101
                Field('course_name', label='Course Name'),   #Full course name ex. Web Applications
                Field('genEd', label='General Education Code'),         #General education requirement it satisfies
                Field('info', label='Course Details'),          #The course details go here(a brief synopsis)
                #Field('bookmark', 'boolean', default=False), #If the student wants to bookmark it it's true else false
                # (will uncomment above if we get time to implement this)
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow(), readable=False, writable=False),
                Field('school_id', readable=False, writable=False)
                #Field('class_id', default=make_random_id(), readable=False, writable=False)
)

db.myclass.id.writable = db.myclass.id.readable = False

db.define_table('reviews',
                #Field('class_id', 'reference myclass'),
                #Field('class_id', readable=True, writable=False),
                Field('class_id', 'reference myclass', readable=False, writable=False),
                Field('overall_rate', 'float', label='Overall Rating (1-5)'),
                Field('difficulty_rate', 'float', label='Difficulty Rating (1-5)'),
                #Field('rec_professor'),
                Field('grade', label='Grade Earned'),
                Field('teacher'),
                Field('recommend', 'boolean', default=False, label='Would you recommend this class?'),
                Field('main_review', 'text', label='Enter your review here.'),
                Field('created_on', 'datetime', update=datetime.datetime.utcnow(), readable=False, writable=False),
                Field('first_name', default=get_user_firstname(), readable=False, writable=False)
)

db.reviews.id.writable = db.reviews.id.readable = False

# Pre-populate db with schools if none
if db(db.school.id>0).count() == 0:
    SCHOOLS = ['University of CA Santa Cruz', 'University of CA Berkeley', 'University of CA Merced']
    for i,s in enumerate(SCHOOLS):
        db.school.insert(name = s, school_id=i)
    db.commit()
# Add test classes
if db(db.myclass.id>0).count() == 0:
    CLASSES = ['UCSC 101', 'UCB 102', 'UCM 103']
    for i,c in enumerate(CLASSES):
        db.myclass.insert(course_name = c, school_id=i)
    db.commit()  # classes stored in myclass table



# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
