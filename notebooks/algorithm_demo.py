from time import perf_counter
from library_system.algorithms import select_books_dp,select_books_backtracking,select_books_branch_bound
books=[{'title':'Python','weight':2,'value':6},{'title':'Data Structures','weight':3,'value':8},{'title':'Algorithms','weight':4,'value':9},{'title':'Databases','weight':5,'value':10},{'title':'Networks','weight':1,'value':3}]
for name,fn in [('Dynamic programming',select_books_dp),('Backtracking',select_books_backtracking),('Branch and bound',select_books_branch_bound)]:
 start=perf_counter(); value,chosen=fn(books,7); elapsed=perf_counter()-start
 print(f'{name}: value={value}, selected={[b["title"] for b in chosen]}, time={elapsed:.8f}s')
print('Timing depends on your computer; record your own measurements.')
