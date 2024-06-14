from models.__init__ import CONN, CURSOR
from models.customer import Customer


class Order:

    all = {}
    
    def __init__(self, customer_id, order_date, total_amount, id=None) -> None:
        self.customer_id = customer_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.id = id

    def __repr__(self) -> str:
        return (f"<Order {self.id}: {self.order_date}, {self.total_amount}" + 
                f"Customer ID: {self.customer_id}>")

    

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        if isinstance(customer_id, int) and Customer.find_by_id(customer_id):
            self._customer_id = customer_id
        else:
            raise ValueError("Customer ID must reference an existing customer in the database")

    @property
    def order_date(self):
        return self._order_date

    @order_date.setter
    def order_date(self, order_date):
        if isinstance(order_date, str) and len(order_date):
            self._order_date = order_date
        else:
            raise ValueError("Order date must be a non-empty string")

    @property
    def total_amount(self):
        return self._total_amount

    @total_amount.setter
    def total_amount(self, total_amount):
        if isinstance(total_amount, float) and len(total_amount):
            self._total_amount = total_amount
        else:
            raise ValueError("Total amount must be a non-empty float")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Order instances """
        CURSOR.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, total_amount REAL, FOREIGN KEY (customer_id) REFERENCES customers(id))")
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the orders table if it exists """
        CURSOR.execute("DROP TABLE IF EXISTS orders")
        CONN.commit()
    
    
    def save(self):
        """ Save the Order instance to the database """
        CURSOR.execute("INSERT INTO orders (customer_id, order_date, total_amount) VALUES(?,?,?)", (self.customer_id, self.order_date, self.total_amount))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    def update(self):
        """ Update the Order instance in the database """
        CURSOR.execute("UPDATE orders SET customer_id=?, order_date=?, total_amount=? WHERE id=?", (self.customer_id, self.order_date, self.total_amount, self.id))
        CONN.commit()
        
        type(self).all[self.id] = self
        
    def delete(self):
        """ Delete the Order instance from the database """
        CURSOR.execute("DELETE FROM orders WHERE id=?", (self.id,))
        CONN.commit()
        type(self).all.pop(self.id)
        
        self.id = None
        
    @classmethod
    def create(cls, customer_id, order_date, total_amount):
        """ Create a new Order instance and save it to the database """
        order = Order(customer_id, order_date, total_amount)
        order.save()
        return order
    
    @classmethod
    def instance_from_db(cls, row):
        """ Create an Order instance from a database row """
        order = cls.all.get(row[0])
        if order:
            # ensure attributes match row values in case local instance was modified
            order.customer_id = row[1]
            order.order_date = row[2]
            order.total_amount = row[3]
        else:
            order = cls(row[1], row[2], row[3], row[0])
            cls.all[row[0]] = order
        return order
    
    @classmethod
    def get_all(cls):
        """ Get all Order instances from the database """
        CURSOR.execute("SELECT * FROM orders")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return order object corresponding to the table row matching the specified primary key"""
        CURSOR.execute("SELECT * FROM orders WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Return order object corresponding to the table row matching the specified customer_id"""
        CURSOR.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
            