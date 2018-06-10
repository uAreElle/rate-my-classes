# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if auth.is_logged_in():
        if auth.user.school is not None:
            redirect(URL('default', 'school_profile'))
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def class_search():
    # Value from class search bar is in request.vars.search
    return dict(search_var=request.vars.search)


def school_search():
    # Value from school search bar is in request.vars.schoolsearch
    return dict(search_var=request.vars.schoolsearch)


def school_profile():
    # Displays the school profile.

    toprated = []
    easy_a = ''
    gpakillers = ''
    schoolname = ''
    schoolid = ''

    r = request.vars.schoolsearch                   # Retrieve search bar input
    if r is not None:
        q = db((db.school.name == r)).select().first()  # Match search input to school in db
    else:
        q = db((db.school.name == auth.user.school)).select().first()

    # Store all the classes associated with the school id
    if q is not None:
        schoolname = q.name
        schoolid = q.id

        # code for toprated
        review_sum = db.reviews.overall_rate.sum()
        review_count = db.reviews.overall_rate.count()

        rows = db().select(db.reviews.class_id, review_sum, review_count, groupby=db.reviews.class_id)

        for r in rows:
            c = db((db.myclass.id == r.reviews.class_id)).select().first()
            t = dict(
                id=c.id,
                department=c.department,
                course_num=c.course_num,
                course_name=c.course_name,
                avgrate=r._extra[review_sum] / r._extra[review_count]
            )
            toprated.append(t)

        # code for easy_as
        rows = db((db.reviews.grade.belongs('A+', 'A', 'A-'))).select(db.reviews.id,
                                                                      orderby=db.reviews.class_id,
                                                                      groupby=db.reviews.class_id)
        if db.myclass is not None:
            easy_a = db(db.myclass.id.belongs(rows)).select()

        # code for gpakillers
        rows = db((db.reviews.grade.belongs('D+', 'D', 'D-', 'F'))).select(db.reviews.id,
                                                                           orderby=db.reviews.class_id,
                                                                           groupby=db.reviews.class_id)
        if db.myclass is not None:
            gpakillers = db(db.myclass.id.belongs(rows)).select()

    return dict(
        school_name=schoolname,
        school_id=schoolid,
        toprated=easy_a,
        easy_as=easy_a,
        gpakillers=gpakillers
    )


def class_profile():
    # Displays the class profile.

    # Get query associated with class from myclass table
    q = db((db.myclass.id == request.vars.classid)).select().first()

    # Get all reviews associated with class
    rows = db((db.reviews.class_id == request.vars.classid)).select(orderby=~db.reviews.created_on)

    reviews = ' '
    overallrating = 0
    recommendclass = 0.0
    counter = 0

    if rows is not None:
        reviews = rows

        for r in rows:
            counter = counter + 1
            if r.overall_rate is not None:
                overallrating = overallrating + r.overall_rate
            if r.recommend is True:
                recommendclass = recommendclass + 1

        if counter is not 0:
            overallrating = overallrating / counter  # computes average rating
            recommendclass = (recommendclass/counter)*100  # computes recommendclass percentage

        overallrating = round(overallrating, 1)
        recommendclass = round(recommendclass, 1)

    return dict(
        class_id=request.vars.classid,
        school_name=request.vars.schoolname,
        class_name=q.course_name,
        department=q.department,
        course_number=q.course_num,
        general_ed=q.genEd,
        class_info=q.info,
        reviews=reviews,
        overallrating=overallrating,
        recommendclass=recommendclass
    )

@auth.requires_login()
def add_school():
    form = SQLFORM(db.school)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

@auth.requires_login()
def add_class():
    form = SQLFORM(db.myclass)
    form.vars.school_id = request.vars.schoolid
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

@auth.requires_login()
def add_review():
    form = SQLFORM(db.reviews)
    # lowers size of mainreview textbox
    form.element('textarea[name=main_review]')['_style'] = 'width:500px;height:150px;'
    form.vars.class_id = request.vars.classid
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)


def class_directory():
    r = request.vars.schoolname  #retrieve from school_profile html passing
    q = db((db.school.name == r)).select().first()
    
    if q is not None:
        if db.myclass is not None:
            c = db((db.myclass.school_id == q.school_id)).select()
            return dict(school_name=q.name, school_id=q.school_id, my_classes=c)
        else:
            return dict(school_name=q.name, school_id=q.school_id, my_classes="")
   
    


    


