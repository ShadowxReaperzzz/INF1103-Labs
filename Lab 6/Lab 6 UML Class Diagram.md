**Inventory**

\- \_\_products: list\[Product]

\- \_\_transactions: list\[int]

\- \_\_total\_transaction\_amount: int



\+ add\_product(product:Product): void

\+ search\_product(query: str): Product

\+ update\_stock(query:str, new\_quantity: int): Product

\+ display\_all(): void

\+ validate\_new\_product\_id(product\_id: str): str

\+ to\_dict(): dict



\+ from dict(data: dict): Inventory

\- \_record\_transaction(amount: int): void



**Product**

\- \_\_product\_id: str

\- \_\_name: str

\- \_\_price: float

\- \_\_stock: int

\+ product\_id, name, price, stock (read-only)

\+ update\_stock(quantity: int): int

\+ matches(query: str): bool

\+ display\_information(): void

\+ to\_dict(): dict

\+ validate\_product\_id(product\_id: str):str

\+ validate\_name(name: str):str

\+ validate\_price(price: float):float

\+ from dict(data: dict, default\_id: str):Product

