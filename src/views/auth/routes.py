from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.security import check_password_hash
from flask import request
from flask import Blueprint,render_template,redirect,url_for, flash
from src.views.auth.forms import RegisterForm,LoginForm
from src.models.user import User

auth_bp=Blueprint('auth',__name__)
clinic_stuff = []



@auth_bp.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(name=form.name.data).first()
        if user_exists:
            flash ('ამ სახელით მომხმარებელი უკვე არსებობს')
            return render_template('auth/register.html',form=form)
        user = User(name = form.name.data,password = form.password1.data)
        user.create()
        new_stuff={
        "name": form.name.data }
        clinic_stuff.append(new_stuff)

        flash("პერსონალი დარეგისტრირებულია")
        return  redirect(url_for('main.index'))
    
    else:
        print(form.errors)
    return render_template("auth/register.html",form=form)

# @auth_bp.route("/personal_users",methods=["GET","POST"])
# def personals_list():

#     return render_template("auth/all_persons.html",stuff=clinic_stuff)


@auth_bp.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    print(current_user)
    if form.validate_on_submit():
        user=User.query.filter_by(name=form.name.data).first()
        if user and check_password_hash(user.password, form.password1.data):
            login_user(user)    
            if request.args.get('next'):
                return redirect(request.args.get('next'))

            new_person = {'name':user.name}
            if new_person not in clinic_stuff:
                clinic_stuff.append(new_person)         
            return redirect(url_for('main.index'))
        else:
            return  redirect(url_for('main.index'))
    
    else:
        print(form.errors)
    return render_template("auth/login.html",form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return  redirect(url_for('main.index'))