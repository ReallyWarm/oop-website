from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discount import Wholesale
    from review import Review

class Tool:
    def __init__(self, code:str, name:str, description:str, brand:str, \
                 amount:int, image, price:float, type_of_tool:str) -> None:
          self._code = code
          self._name = name
          self._description = description
          self._brand = brand
          self._amount = amount
          self._price = price
          self._category = type_of_tool
          self._reviews = [ ]
          self._image = [image]
          self._wholesale = [ ]
          self._rating = 0.00
          self.__n_review = 0.00
          self.__rated_review = 0.00

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def wholesales(self) -> list:
        return self._wholesale
    
    def add_wholesale(self, wholesale:'Wholesale') -> None:
        self._wholesale.append(wholesale)

    @property
    def price(self) -> float:
        return self._price
    
    @property
    def review_list(self) -> list:
        return self._reviews
    
    @property
    def code(self):
        return self._code
    
    @property
    def description(self):
        return self._description
    
    @property
    def brand(self):
        return self._brand
    
    def add_review(self, review:'Review') -> None:
        self._reviews.append(review)
        self.__n_review += 1
        self.__rated_review += review._rating
        self._rating = self.__rated_review / self.__n_review

    @property
    def rating(self) -> float:
        return self._rating
    
    @property
    def type_of_tool(self):
        return self._category
    
    def change_name(self,new_name:str):
        self._name = new_name
            
    def change_description(self,new_description:str):
        self._description = new_description
            
    def change_brand(self,new_brand:str):
        self._brand = new_brand
            
    def change_price(self,new_price:float):
        self._price = new_price

    def change_code(self,new_code):
        self._code = new_code

    def change_type_of_tool(self, new_type_of_tool):
        self._category = new_type_of_tool

    def __str__(self) -> str:
        return str(self.__class__)+'\n'+', '.join(f'{key} : {value}' for key, value in self.__dict__.items())

class Item:
    def __init__(self, tool:'Tool', buy_amount:int) -> None: 
        self._tool = tool
        self._buy_amount = buy_amount
        self._items_price = tool.price * buy_amount

    @property
    def tool(self) -> 'Tool':
        return self._tool
    
    @property
    def buy_amount(self) -> int:
        return self._buy_amount
    
    @property
    def items_price(self) -> float:
        return self._items_price
    
    def set_buy_amount(self, amount:int) -> None:
        self._buy_amount = amount
        self.update_item()

    def update_item(self) -> None:
        self._items_price = self.tool.price * self.buy_amount

    def __str__(self) -> str:
        return str(self.__class__)+'\n'+', '.join(f'{key} : {value}' for key, value in self.__dict__.items())

    def __repr__(self) -> str:
        return f'\"{self.__str__()}\"'