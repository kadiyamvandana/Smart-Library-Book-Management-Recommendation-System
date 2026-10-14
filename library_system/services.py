from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from time import perf_counter,sleep
from typing import Callable,TypeVar
F=TypeVar('F',bound=Callable)
def timed(function:F)->F:
 @wraps(function)
 def wrapper(*args,**kwargs):
  start=perf_counter()
  try:return function(*args,**kwargs)
  finally:print(f'{function.__name__}: {perf_counter()-start:.6f}s')
 return wrapper # type: ignore[return-value]
def simulated_catalog_lookup(source:str)->dict[str,str]:
 sleep(.05); return {'source':source,'status':'ok'}
def fetch_catalog_sources(sources:list[str])->list[dict[str,str]]:
 """Threads overlap simulated I/O waits; they do not generally speed up CPU-bound Python."""
 with ThreadPoolExecutor(max_workers=min(4,max(1,len(sources)))) as pool:return list(pool.map(simulated_catalog_lookup,sources))
def iter_batches(items:list,batch_size:int):
 if batch_size<=0:raise ValueError('batch_size must be positive')
 for i in range(0,len(items),batch_size):yield items[i:i+batch_size]
