from flask import Blueprint,render_template,request,url_for,redirect,request,abort
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
from os import path
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from datetime import datetime

from src.config import Config
from src.models.book import Book
from src.views.book.forms import BookForm
from src.ext import db

book_bp=Blueprint('boo',__name__)


def img_upload_path(img_upl,img_input=None,img_ext=None):
    if img_upl and getattr(img_upl,'filename',None):
        filename  = secure_filename(img_upl.filename)
        upload_path = path.join(Config.UPLOAD_PATH,filename)
        img_upl.save(upload_path)
        return filename
    if img_input and hasattr(img_input,'img'):
        return img_input.img
    return 'default.jpg'


@book_bp.route("/books")
def book_by_category():
    query = Book.query
    selected_cat = request.args.get('category', 'all')
    all_categories = {
        'buy': ['buy', 'შეძენა'],
        'sell': ['sell', 'გაყიდვა'],
        'gifting': ['gifting', 'ჩუქება'],
        'giveaway': ['giveaway', 'გაჩუქება'],
        'exchange': ['exchange', 'გაცვლა'],
        'donation': ['donation', 'ქველმოქმედება'],
        'completed': ['completed', 'completed']
    }

    if selected_cat == 'all' or not selected_cat:
        query = query.filter(Book.category != 'completed')
    else:

        if selected_cat in all_categories:
            query = query.filter(Book.category.in_(all_categories[selected_cat]))

    books = query.all()
    return render_template(
        "book/books.html",
        books=books,
        selected_cat=selected_cat,
        # title='წიგნების კატალოგი'
    )

@book_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = BookForm()
    if form.validate_on_submit():
        filename = img_upload_path(form.img.data)
        book = Book(
            location=form.location.data,
            title=form.title.data,
            quantity=form.quantity.data,
            status=form.status.data,
            category = form.category.data,
            img=filename,
            user_id=current_user.id,
            
        )

        book.create()
        if book.category=='exchange':   
            return redirect(url_for('boo.exchange', id=book.id))

        return redirect(url_for('boo.book_by_category'))  

    else:
        if form.is_submitted():
            print("ფორმის შეცდომები:", form.errors)

    return render_template("book/create.html", form=form)

@book_bp.route('/detail/<int:id>')
def book_detail(id):
    book = Book.query.get(id)
    return render_template('book/book.html',book=book)
    

@book_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    book = Book.query.get_or_404(id)
    if book.user_id !=current_user.id:
        abort(403)

    form = BookForm()
    if form.validate_on_submit():
        
        changes =  (form.location.data!=book.location or
            form.title.data!=book.title or 
            form.quantity.data!=book.quantity or 
            form.status.data!=book.status or 
            form.category.data != book.category or
            form.img.data is not None and form.img.data.filename !='')
        if form.is_submitted():
          print(request.form)
          print(changes)
          print(request.form.get('confirm'))
         
        if not changes and request.form.get('confirm') is None:
            return render_template('book/check_update.html',
                                form = form,
                                book=book)

    
        book.img = img_upload_path(form.img.data,img_input=book)
        book.location = form.location.data
        book.title = form.title.data
        book.quantity = form.quantity.data
        book.status = form.status.data
        book.category = form.category.data
        book.save()
        return redirect(url_for('boo.book_by_category'))

    else:
            form.location.data=book.location
            form.title.data=book.title
            form.quantity.data= book.quantity
            form.status.data=book.status
            form.category.data = book.category
           
            return render_template("book/create.html", form=form, book=book)
    

@book_bp.route("/exchange/<int:id>", methods=["GET", "POST"])
@login_required
def exchange(id):
    book = Book.query.get_or_404(id)

    if book.user_id != current_user.id:
        abort(403)

    form = BookForm(obj=book)

    if form.validate_on_submit():

        book.title = form.title.data
        book.quantity = form.quantity.data
        book.status = form.status.data
        book.location = form.location.data

        book.exchange_with = form.exchange_with.data
        book.category = "გაცვლა"

        db.session.commit()
        return redirect(url_for("boo.book_by_category"))

    return render_template("book/exchange.html", form=form, book=book)

@book_bp.route('/complete/<int:id>')
@login_required
def complete(id):
    book = Book.query.get_or_404(id)
    if book.user_id != current_user.id:
        abort(403)
    book.category = 'completed'
    db.session.commit()
    return redirect(url_for('boo.book_by_category'))


@book_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    book = Book.query.get_or_404(id)
    if book.user_id!=current_user.id:
        abort(403)
    book.delete()

    return redirect(url_for('boo.book_by_category'))







