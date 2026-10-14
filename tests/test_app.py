import pytest
from app import app
from library_system.database import LibraryRepository
@pytest.fixture
def client(tmp_path,monkeypatch):
 path=str(tmp_path/'test.db'); monkeypatch.setitem(app.config,'DATABASE',path); LibraryRepository(path).initialize(); app.config['TESTING']=True
 with app.test_client() as c:yield c
def test_home(client):assert client.get('/').status_code==200
def test_add_book(client):
 r=client.post('/add',data={'title':'Python','author':'A Student','category':'Computing','copies':'2','kind':'print'},follow_redirects=True)
 assert r.status_code==200 and b'Python' in r.data
def test_invalid_form(client):assert b'Enter valid details' in client.post('/add',data={},follow_redirects=True).data
def test_library_pages_and_loan_lifecycle(client):
 for path in ('/','/add','/recommendations','/admin'):
  assert client.get(path).status_code==200

 client.post('/borrow/1',data={'borrower':'Maya Reader'})
 loans=client.get('/admin')
 assert b'Maya Reader' in loans.data and b'On loan' in loans.data

 returned=client.post('/return/1',follow_redirects=True)
 assert returned.status_code==200 and b'Returned' in client.get('/admin').data
