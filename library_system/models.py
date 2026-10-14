from abc import ABC, abstractmethod
from dataclasses import dataclass
@dataclass
class LibraryItem(ABC):
 title:str; author:str; category:str; copies:int
 @abstractmethod
 def item_type(self)->str: ...
@dataclass
class Book(LibraryItem):
 def item_type(self)->str: return 'Printed book'
@dataclass
class EBook(LibraryItem):
 def item_type(self)->str: return 'E-book'
