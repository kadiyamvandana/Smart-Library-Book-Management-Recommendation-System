import pytest
from hypothesis import given, strategies as st
from library_system.algorithms import recommend_books,select_books_dp,select_books_backtracking,select_books_branch_bound,merge_sort,available_book_stream

def test_recommendations_prioritize_category():
 books=[{'title':'Zoo','category':'Science','copies':1},{'title':'Python','category':'Computing','copies':1}]
 assert recommend_books(books,'Computing')[0]['title']=='Python'
def test_optimization_algorithms_agree():
 books=[{'title':'A','weight':2,'value':3},{'title':'B','weight':3,'value':4},{'title':'C','weight':4,'value':5}]
 assert select_books_dp(books,5)[0]==select_books_backtracking(books,5)[0]==select_books_branch_bound(books,5)[0]==7
def test_negative_capacity():
 with pytest.raises(ValueError):select_books_dp([], -1)
def test_generator_only_available():
 assert len(list(available_book_stream([{'copies':1},{'copies':0}])))==1
@given(st.lists(st.integers(min_value=-100,max_value=100),max_size=30))
def test_merge_sort_matches_builtin(values):assert merge_sort(values,lambda x:x)==sorted(values)
