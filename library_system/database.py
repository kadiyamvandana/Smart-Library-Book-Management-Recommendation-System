import sqlite3
from pathlib import Path
from typing import Any
from library_system.models import LibraryItem
class LibraryRepository:
 'Repository pattern isolates database operations from routes.'
 def __init__(self,path:str)->None: self.path=path
 def connect(self)->sqlite3.Connection:
  db=sqlite3.connect(self.path); db.row_factory=sqlite3.Row; db.execute('PRAGMA foreign_keys=ON'); return db
 def initialize(self)->None:
  Path(self.path).parent.mkdir(parents=True,exist_ok=True)
  with self.connect() as db:
   db.executescript('''CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY,title TEXT NOT NULL,author TEXT NOT NULL,category TEXT NOT NULL,copies INTEGER NOT NULL CHECK(copies>=0),item_type TEXT NOT NULL); CREATE TABLE IF NOT EXISTS loans(id INTEGER PRIMARY KEY,book_id INTEGER NOT NULL REFERENCES books(id),borrower TEXT NOT NULL,borrowed_at TEXT DEFAULT CURRENT_TIMESTAMP,returned_at TEXT);''')
   sample_books = [
    ('The Pragmatic Programmer','Andrew Hunt','Technology',3,'print'),
    ('Clean Code','Robert C. Martin','Technology',2,'print'),
    ('Atomic Habits','James Clear','Self Development',4,'print'),
    ('Deep Work','Cal Newport','Productivity',2,'ebook'),
    ('The Alchemist','Paulo Coelho','Fiction',5,'print'),
    ('Python Crash Course','Eric Matthes','Computing',3,'ebook'),
    ('The Lean Startup','Eric Ries','Business',2,'print'),
   ]
   db.executemany('INSERT OR IGNORE INTO books(title,author,category,copies,item_type) VALUES(?,?,?,?,?)', sample_books)
 def add_book(self,item:LibraryItem)->int:
  with self.connect() as db:
   cur=db.execute('INSERT INTO books(title,author,category,copies,item_type) VALUES(?,?,?,?,?)',(item.title,item.author,item.category,item.copies,item.item_type())); return int(cur.lastrowid)
 def list_books(self,search:str='',category:str='')->list[dict[str,Any]]:
  sql='SELECT * FROM books WHERE 1=1'; args=[]
  if search: sql+=' AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ?)'; args += [f'%{search.lower()}%',f'%{search.lower()}%']
  if category: sql+=' AND category=?'; args.append(category)
  sql+=' ORDER BY title COLLATE NOCASE'
  with self.connect() as db: return [dict(x) for x in db.execute(sql,args).fetchall()]
 def categories(self)->list[str]:
  with self.connect() as db: return [r[0] for r in db.execute('SELECT DISTINCT category FROM books ORDER BY category')]
 def borrow_book(self,book_id:int,borrower:str)->bool:
  with self.connect() as db:
   cur=db.execute('UPDATE books SET copies=copies-1 WHERE id=? AND copies>0',(book_id,))
   if cur.rowcount!=1: return False
   db.execute('INSERT INTO loans(book_id,borrower) VALUES(?,?)',(book_id,borrower)); return True
 def return_book(self,book_id:int)->bool:
  with self.connect() as db:
   loan=db.execute('SELECT id FROM loans WHERE book_id=? AND returned_at IS NULL ORDER BY id LIMIT 1',(book_id,)).fetchone()
   if loan is None: return False
   db.execute('UPDATE loans SET returned_at=CURRENT_TIMESTAMP WHERE id=?',(loan['id'],)); db.execute('UPDATE books SET copies=copies+1 WHERE id=?',(book_id,)); return True
 def list_loans(self)->list[dict[str,Any]]:
  with self.connect() as db: return [dict(x) for x in db.execute('SELECT loans.*,books.title FROM loans JOIN books ON books.id=loans.book_id ORDER BY loans.id DESC')]
 def stats(self)->dict[str,int]:
  with self.connect() as db:
   b=db.execute('SELECT COUNT(*) titles,COALESCE(SUM(copies),0) copies FROM books').fetchone(); l=db.execute('SELECT COUNT(*) total,SUM(CASE WHEN returned_at IS NULL THEN 1 ELSE 0 END) active FROM loans').fetchone()
  return {'titles':b['titles'],'copies':b['copies'],'loans':l['total'],'active_loans':l['active'] or 0}
