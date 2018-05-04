# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
import datetime

def get_user_email():
    return auth.user.email if auth.user is not None else None

def get_user_school():
    return auth.user.school if auth.user is not None else None

db.define_table('myclass',
                Field('course_name'),   #Full course name ex. Web Applications
                Field('department'),    #Can be full department name(i.e. Computer Science) or shorthand (i.e CMPS)
                Field('course_num'),    #Course number ex. 101
                Field('university'),    #To know which university this class belongs to
                Field('genEd'),         #General education requirement it satisfies
                Field('info'),          #The course details go here(a brief synopsis)
                Field('bookmark', 'boolean', default=False), #If the student wants to bookmark it it's true else false
                #Field('professor_name'), not sure how we want professor to be(input by the student or pre-approved, etc.)
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow())
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
                Field('name', default=get_user_school())
                )

# Pre-populate db with schools
if db(db.school.id>0).count() == 0:
    SCHOOLS = ['UC Santa Cruz', 'UC Berkeley', 'UC Merced']
    for s in SCHOOLS:
        db.school.insert(name = s)
    db.commit()

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
