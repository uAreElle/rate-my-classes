# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
import datetime
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

<<<<<<< HEAD
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
=======
import datetime
>>>>>>> 54eac1e180fe1dc36c0375e1664ea4b03485e5be

def get_user_email():
    return auth.user.email if auth.user is not None else None

'''
db.define_table('user_profile',
                Field('user_email', default=get_user_email()),
                Field('school')
               )
'''
# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
