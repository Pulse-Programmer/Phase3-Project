from models.__init__ import CONN, CURSOR
from models.category import Category
from models.supplier import Supplier

class Product:
    
    all = {}
    
    def __init__(self, name, description, price, category_id, supplier_id, id=None) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.id = id
        
        
    def __repr__(self) -> str:
        return (f"<Product {self.id}: {self.name}, {self.description}, {self.price}, " +
               f"Category ID: {self.category_id}, " + 
               f"Supplier ID: {self.supplier_id}>")
        

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name  
        else:
            raise ValueError("Name must be a non-empty string")
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        if isinstance(description, str) and len(description):
            self._description = description
        else:
            raise ValueError("Description must be a non-empty string")
        
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        if isinstance(price, float):
            self._price = price
        else:
            raise ValueError("Price must be a non-empty float")
        
    @property
    def category_id(self):
        return self._category_id
    
    @category_id.setter
    def category_id(self, category_id):
        if isinstance(category_id, int) and Category.find_by_id(category_id):
            self._category_id = category_id
        else:
            raise ValueError("Category ID must reference an existing category")
        
    @property
    def supplier_id(self):
        return self._supplier_id
    
    @supplier_id.setter
    def supplier_id(self, supplier_id):
        if isinstance(supplier_id, int) and Supplier.find_by_id(supplier_id):
            self._supplier_id = supplier_id
        else:
            raise ValueError("Supplier ID must reference an existing supplier")
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Product instances """
        sql = """
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            price REAL,
            category_id INTEGER,
            supplier_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """ Drop the products table if it exists """
        sql = "DROP TABLE IF EXISTS products"
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """ Save the Product instance to the database """
        sql = "INSERT INTO products (name, description, price, category_id, supplier_id) VALUES(?,?,?,?,?)"
        CURSOR.execute(sql, (self.name, self.description, self.price, self.category_id, self.supplier_id))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
        
    def update(self):
        """ Update the Product instance in the database """
        sql = "UPDATE products SET name = ?, description = ?, price = ?, category_id = ?, supplier_id = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.description, self.price, self.category_id, self.supplier_id, self.id))
        CONN.commit()
        
        type(self).all[self.id] = self
        
    def delete(self):
        """ Delete the Product instance from the database """
        sql = "DELETE FROM products WHERE id = ?"
        CURSOR.execute(sql, (self.id, ))
        CONN.commit()
        
        del type(self).all[self.id]
        self.id = None
        
    
    @classmethod
    def create(cls, name, description, price, category_id, supplier_id):
        """ Create a new Product instance and save it to the database """
        product = Product(name, description, price, category_id, supplier_id)
        product.save()
        return product
    
    @classmethod
    def instance_from_db(cls, row):
        """ Create a Product instance from a database row """
        
         # Check the dictionary for an existing instance using the row's primary key
        product = cls.all.get(row[0])
        if product:
            # ensure attributes match row values in case local instance was modified
            product.name = row[1]
            product.description = row[2]
            product.price = row[3]
            product.category_id = row[4]
            product.supplier_id = row[5]
        else:
            product = cls(row[1], row[2], row[3], row[4], row[5], row[0])
            cls.all[product.id] = product
        return product
    
    @classmethod
    def get_all(cls):
        """ Get all Product instances from the database """
        sql = "SELECT * FROM products"
        CURSOR.execute(sql)
        return [cls.instance_from_db(row) for row in CURSOR.fetchall()]
    
    @classmethod
    def find_by_id(cls, id):
        """ Find a Product instance by its ID """
        sql = "SELECT * FROM products WHERE id = ?"
        CURSOR.execute(sql, (id, ))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """ Find a Product instance by its name """
        sql = "SELECT * FROM products WHERE name = ?"
        CURSOR.execute(sql, (name, ))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
            