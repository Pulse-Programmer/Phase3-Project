from models.__init__ import CONN, CURSOR
from models.order import Order
from models.product import Product

class OrderDetails:

    all = {}
    
    def __init__(self, order_id, product_id, quantity, price, id=None) -> None:
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.id = id
        
    def __repr__(self) -> str:
        return (f"<OrderDetails {self.id}: {self.quantity}, {self.price}, " + 
                f"Order ID: {self.order_id}" + 
                f"Product ID: {self.product_id}>")
    

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        if isinstance(order_id, int) and Order.find_by_id(order_id):
            self._order_id = order_id
        else:
            raise ValueError("Order ID must reference an existing order in the database")

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        if isinstance(product_id, int) and Product.find_by_id(product_id):
            self._product_id = product_id
        else:
            raise ValueError("Product ID must reference an existing product in the database")

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        if isinstance(quantity, int):
            self._quantity = quantity
        else:
            raise ValueError("Quantity must be a non-empty integer")
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if isinstance(price, float):
            self._price = price
        else:
            raise ValueError("Price must be a non-empty float")
        
    
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of OrderDetails instances """
        sql = """

        CREATE TABLE IF NOT EXISTS order_details(
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
         """

        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """ Drop the table to persist the attributes of OrderDetails instances """
        sql = """
        DROP TABLE IF EXISTS order_details
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    
    def save(self):
        """ Save the OrderDetails instance to the database """
        sql = """
        INSERT INTO order_details(order_id, product_id, quantity, price)
        VALUES(?,?,?,?)
        """
        CURSOR.execute(sql, (self.order_id, self.product_id, self.quantity, self.price))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    
    def update(self):
        """Update the table row corresponding to the current OrderDetails instance."""
        sql = """
        UPDATE order_details
        SET order_id=?, product_id=?, quantity=?, price=?
        WHERE id=?
        """
        CURSOR.execute(sql, (self.order_id, self.product_id, self.quantity, self.price, self.id))
        CONN.commit()
        type(self).all[self.id] = self
        
    
    def delete(self):
        """ Delete the OrderDetails instance from the database """
        sql = """
        DELETE FROM order_details
        WHERE id=?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        type(self).all.pop(self.id)
        
        self.id = None
        
    
    @classmethod
    def instance_from_db(cls, row):
        """ Create an OrderDetails instance from a database row """
        
         # Check the dictionary for an existing instance using the row's primary key
        order_details = cls.all.get(row[0])
        if order_details:
            # ensure attributes match row values in case local instance was modified
            order_details.order_id = row[1]
            order_details.product_id = row[2]
            order_details.quantity = row[3]
            order_details.price = row[4]
        else:
            order_details = cls(row[1], row[2], row[3], row[4], row[0])
            cls.all[order_details.id] = order_details
        return order_details
        
    @classmethod
    def create(cls, order_id, product_id, quantity, price):
        """ Create a new OrderDetails instance and save it to the database """
        order_details = OrderDetails(order_id, product_id, quantity, price)
        order_details.save()
        return order_details
    
    @classmethod
    def get_all(cls):
        """ Get all OrderDetails instances from the database """
        sql = "SELECT * FROM order_details"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """ return an OrderDetails object corresponding to the table row matching its primary key """
        sql = "SELECT * FROM order_details WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_order_id(cls, order_id):
        """ return a list of OrderDetails objects corresponding to the table rows matching the order_id """
        sql = "SELECT * FROM order_details WHERE order_id = ?"
        CURSOR.execute(sql, (order_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_product_id(cls, product_id):
        """ return a list of OrderDetails objects corresponding to the table rows matching the product_id """
        sql = "SELECT * FROM order_details WHERE product_id = ?"
        CURSOR.execute(sql, (product_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]