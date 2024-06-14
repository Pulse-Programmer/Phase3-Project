from models.__init__ import CONN, CURSOR
from models.product import Product


class Inventory:

    all = {}
    
    def __init__(self, product_id, quantity, id=None) -> None:
        self.product_id = product_id
        self.quantity = quantity
        self.id = id
        
    def __repr__(self) -> str:
        return (f"<Inventory {self.id}: {self.quantity}, " + 
                f"Product ID: {self.product_id}>")
        

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

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Inventory instances """
        sql = """

        CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY,
            product_id INTEGER UNIQUE,
            quantity INTEGER,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
         """

        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """ Drop the table to persist the attributes of Inventory instances """
        sql = """
        DROP TABLE IF EXISTS inventory
        """
        CURSOR.execute(sql)
        CONN.commit()
        

    def save(self):
        """ Save an instance of Inventory to the database """
        sql = "INSERT INTO inventory(product_id, quantity) VALUES(?, ?)"
        CURSOR.execute(sql, (self.product_id, self.quantity))
        CONN.commit()

        self.id = CURSOR.lastrowid

        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, product_id, quantity):
        """ Initialize a new inventory instance and save the object to the database """
        inventory = cls(product_id, quantity)
        inventory.save()
        return inventory
    
    def update(self):
        """ Update an existing inventory instance in the database """
        sql = "UPDATE inventory SET product_id=?, quantity = ? WHERE id = ?"
        CURSOR.execute(sql, (self.product_id, self.quantity, self.id))
        CONN.commit()
        
        type(self).all[self.id] = self
        
    def delete(self):
        """ Delete an existing inventory instance from the database """
        CURSOR.execute('DELETE FROM inventory WHERE id =?', (self.id,))
        CONN.commit()
        
        del type(self).all[self.id]

        self.id = None
        
    @classmethod
    def instance_from_db(cls, row):
        """ Create an Inventory instance from a database row """
        inventory = cls.all.get(row[0])
        if inventory:
            inventory.product_id = row[1]
            inventory.quantity = row[2]
        else:
            inventory = cls(row[1], row[2], row[0])
            cls.all[inventory.id] = inventory
        return inventory
        
    @classmethod
    def get_all(cls):
        """ Get all Inventory instances from the database """
        sql = """
        SELECT * FROM inventory
        """
        CURSOR.execute(sql)
        return [cls.instance_from_db(row) for row in CURSOR.fetchall()]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
        SELECT * FROM inventory
        WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None