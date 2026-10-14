from typing import Callable, Iterable, TypeVar
T=TypeVar('T')
def recommend_books(books:Iterable[dict],category:str|None=None,limit:int=10)->list[dict]:
 """Greedy rule-based recommendation; O(n log n) time, O(n) space."""
 if limit<0: raise ValueError('limit cannot be negative')
 items=[b for b in books if int(b['copies'])>0]
 items.sort(key=lambda b:(0 if category and b['category'].casefold()==category.casefold() else 1,b['title'].casefold()))
 return items[:limit]
def select_books_dp(books:list[dict],capacity:int)->tuple[int,list[dict]]:
 """0/1 knapsack dynamic programming; O(nW) time and space."""
 if capacity<0: raise ValueError('capacity cannot be negative')
 n=len(books); dp=[[0]*(capacity+1) for _ in range(n+1)]
 for i,b in enumerate(books,1):
  w,v=int(b['weight']),int(b['value'])
  if w<0 or v<0: raise ValueError('weight/value must be non-negative')
  for c in range(capacity+1): dp[i][c]=max(dp[i-1][c],dp[i-1][c-w]+v if w<=c else 0)
 chosen=[]; c=capacity
 for i in range(n,0,-1):
  if dp[i][c]!=dp[i-1][c]: chosen.append(books[i-1]); c-=int(books[i-1]['weight'])
 chosen.reverse(); return dp[n][capacity],chosen
def select_books_backtracking(books:list[dict],capacity:int)->tuple[int,list[dict]]:
 """Explore include/exclude choices; worst-case O(2^n)."""
 if capacity<0: raise ValueError('capacity cannot be negative')
 best=[0,[]]
 def visit(i,w,v,chosen):
  if w>capacity:return
  if i==len(books):
   if v>best[0]: best[:]=[v,chosen.copy()]
   return
  visit(i+1,w,v,chosen); b=books[i]; bw,bv=int(b['weight']),int(b['value'])
  if bw<0 or bv<0: raise ValueError('weight/value must be non-negative')
  chosen.append(b); visit(i+1,w+bw,v+bv,chosen); chosen.pop()
 visit(0,0,0,[]); return best[0],best[1]
def select_books_branch_bound(books:list[dict],capacity:int)->tuple[int,list[dict]]:
 """Branch-and-bound knapsack with optimistic fractional upper bound; exponential worst case."""
 if capacity<0: raise ValueError('capacity cannot be negative')
 items=sorted(books,key=lambda b:int(b['value'])/max(1,int(b['weight'])),reverse=True)
 if any(int(b['weight'])<0 or int(b['value'])<0 for b in items): raise ValueError('weight/value must be non-negative')
 best=[0,[]]
 def bound(i,w,v):
  room=capacity-w; total=float(v)
  for b in items[i:]:
   bw,bv=int(b['weight']),int(b['value'])
   if room<=0: break
   if bw==0: total+=bv
   elif bw<=room: total+=bv; room-=bw
   else: total+=bv*room/bw; break
  return total
 def visit(i,w,v,chosen):
  if w>capacity or bound(i,w,v)<=best[0]:return
  if i==len(items): best[:]=[v,chosen.copy()]; return
  b=items[i]; chosen.append(b); visit(i+1,w+int(b['weight']),v+int(b['value']),chosen); chosen.pop(); visit(i+1,w,v,chosen)
 visit(0,0,0,[]); return best[0],best[1]
def merge_sort(values:list[T],key:Callable[[T],object])->list[T]:
 """Divide-and-conquer merge sort: O(n log n) time, O(n) auxiliary space."""
 if len(values)<=1:return values.copy()
 m=len(values)//2; left=merge_sort(values[:m],key); right=merge_sort(values[m:],key); out=[]; i=j=0
 while i<len(left) and j<len(right):
  if key(left[i])<=key(right[j]):out.append(left[i]);i+=1
  else:out.append(right[j]);j+=1
 return out+left[i:]+right[j:]
def apply_filter(items:Iterable[T],predicate:Callable[[T],bool])->list[T]: return [x for x in items if predicate(x)]
def available_book_stream(books:Iterable[dict]):
 for book in books:
  if int(book.get('copies',0))>0: yield book
