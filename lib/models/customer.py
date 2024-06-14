from models.__init__ import CONN, CURSOR

class Customer:
    all = {}

    def __init__(self, name, email, phone, address, id=None) -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.id = id

    def __repr__(self) -> str:
        return (f"<Customer {self.id}: {self.name}, {self.email}, {self.phone}, {self.address}>")
    
    
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
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if isinstance(email, str) and len(email):
            self._email = email
        else:
            raise ValueError("Email must be a non-empty string")
        
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone):
        phone = int(phone)
        if isinstance(phone, int) and len(phone)==10:
            self._phone = phone  
        else:
            raise ValueError("Phone number must be a 10-digit integer")
        
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address):
        if isinstance(address, str) and len(address):
            self._address = address
        else:
            raise ValueError("Address must be a non-empty string")
        
    @classmethod
    def create_table(cls):
         """ Create a new table to persist the attributes of Customer instances """
        
         CURSOR.execute('CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone INTEGER, address TEXT)')
         CONN.commit()
         
    @classmethod
    def drop_table(cls):
        """ Drop the customers table if it exists """
        
        CURSOR.execute('DROP TABLE IF EXISTS customers')
        CONN.commit()
        
    def save(self):
        """ Save the Customer instance to the database """ 

        CURSOR.execute('INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)', (self.name, self.email, self.phone, self.address))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
        type(self).all[self.id] = self
        
        
    @classmethod
    def create(cls, name, email, phone, address):
        """ Create a new Customer instance and save it to the database """
        
        customer = Customer(name, email, phone, address)
        customer.save()
        return customer
    
    def update(self):
        """ Update the Customer instance in the database """
        
        CURSOR.execute('UPDATE customers SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?', (self.name, self.email, self.phone, self.address, self.id))
        CONN.commit()
        
        type(self).all[self.id] = self
        
    def delete(self):
        """ Delete the Customer instance from the database """
        
        CURSOR.execute('DELETE FROM customers WHERE id =?', (self.id,))
        CONN.commit()
        
        del type(self).all[self.id]

        self.id = None
        
    @classmethod
    def instance_from_db(cls, row):
        """ Create a Customer instance from a row of the database """
        
        # Check the dictionary for an existing instance using the row's primary key
        customer = cls.all.get(row[0])
        if customer:
            #ensure attributes match row values in case of modification on the local class instance
            customer.name = row[1]
            customer.email = row[2]
            customer.phone = row[3]
            customer.address = row[4]
        else:
            customer = Customer(row[1], row[2], row[3], row[4], row[0])
            cls.all[row[0]] = customer
            
        return customer
    
    @classmethod
    def get_all(cls):
        """ Get all Customer instances from the database """
        
        CURSOR.execute('SELECT * FROM customers')
        rows = CURSOR.fetchall()
        customers = [cls.instance_from_db(row) for row in rows]
        return customers
        
    @classmethod
    def get_by_id(cls, id):
        """ Get a Customer instance from the database by id """
        
        CURSOR.execute('SELECT * FROM customers WHERE id = ?', (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
        
        
    @classmethod
    def get_by_name(cls, name):
        """ Get a Customer instance from the database by name """
        
        CURSOR.execute('SELECT * FROM customers WHERE name = ?', (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    def orders(self):
        """ Get all orders associated with this customer """
        from models.order import Order
        
        return Order.get_by_customer_id(self.id)
        