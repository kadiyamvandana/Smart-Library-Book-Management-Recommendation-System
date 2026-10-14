from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for
from library_system.database import LibraryRepository
from library_system.models import Book, EBook
from library_system.algorithms import recommend_books
ROOT=Path(__file__).resolve().parent
app=Flask(__name__); app.config.update(SECRET_KEY='dev-only-change-me', DATABASE=str(ROOT/'library.db'))
def repo(): return LibraryRepository(app.config['DATABASE'])
@app.get('/')
def index():
 q=request.args.get('q','').strip(); category=request.args.get('category','').strip()
 r=repo()
 return render_template('index.html',books=r.list_books(q,category),categories=r.categories(),stats=r.stats(),q=q,category=category)
@app.route('/add',methods=['GET','POST'])
def add_book():
 if request.method=='POST':
  try:
   title=request.form['title'].strip(); author=request.form['author'].strip(); category=request.form['category'].strip(); copies=int(request.form['copies']); kind=request.form.get('kind','print')
   if not all((title,author,category)) or copies<0: raise ValueError
   item=EBook(title,author,category,copies) if kind=='ebook' else Book(title,author,category,copies)
   repo().add_book(item); flash('Book added successfully.','success'); return redirect(url_for('index'))
  except (KeyError,ValueError): flash('Enter valid details. Copies must be zero or more.','error')
 return render_template('add_book.html')
@app.post('/borrow/<int:book_id>')
def borrow(book_id):
 borrower=request.form.get('borrower','').strip()
 if not borrower: flash("Enter the borrower's name.",'error')
 elif repo().borrow_book(book_id,borrower): flash('Book borrowed successfully.','success')
 else: flash('No copies are available.','error')
 return redirect(url_for('index'))
@app.post('/return/<int:book_id>')
def return_book(book_id):
 ok=repo().return_book(book_id)
 flash('Book returned successfully.' if ok else 'No outstanding loan found.','success' if ok else 'error')
 return redirect(url_for('index'))
@app.get('/recommendations')
def recommendations():
 category=request.args.get('category','').strip(); books=[b for b in repo().list_books() if b['copies']>0]
 return render_template('recommendations.html',books=recommend_books(books,category or None),categories=repo().categories(),category=category)
@app.get('/admin')
def admin():
 r=repo(); return render_template('admin.html',books=r.list_books(),loans=r.list_loans(),stats=r.stats())
if __name__=='__main__':
 repo().initialize(); app.run(debug=True)
