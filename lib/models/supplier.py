from models.__init__ import CONN, CURSOR


class Supplier:
    all = {}

    def __init__(self, name, contact_info, id=None) -> None:
        self.name = name
        self.contact_info = contact_info
        self.id = id

    def __repr__(self) -> str:
        return (f"<Supplier {self.id}: {self.name}, {self.contact_info}>")
    

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
    def contact_info(self):
        return self._contact_info
    
    @contact_info.setter
    def contact_info(self, contact_info):
        if isinstance(contact_info, str) and len(contact_info):
            self._contact_info = contact_info
        else:
            raise ValueError("Contact info must be a non-empty string")
        

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Supplier instances """
        CURSOR.execute("CREATE TABLE IF NOT EXISTS suppliers(id INTEGER PRIMARY KEY, name TEXT, contact_info TEXT)")
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the suppliers table if it exists """
        CURSOR.execute("DROP TABLE IF EXISTS suppliers")
        CONN.commit()
    
    
    def save(self):
        """ Save the Supplier instance to the database """
        CURSOR.execute("INSERT INTO suppliers (name, contact_info) VALUES(?,?)", (self.name, self.contact_info))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, contact_info):
        new_supplier = cls(name, contact_info)
        new_supplier.save()
        return new_supplier
    
    def update(self):
        """ Update the Supplier instance in the database """
        CURSOR.execute("UPDATE suppliers SET name = ?, contact_info = ? WHERE id = ?", (self.name, self.contact_info, self.id))
        CONN.commit()
        
        type(self).all[self.id] = self
        
    def delete(self):
        """ Delete the Supplier instance from the database """
        CURSOR.execute("DELETE FROM suppliers WHERE id =?", (self.id,))
        CONN.commit()
        
        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def instance_from_db(cls, row):
        """Return a supplier object having the attribute values from the table row."""
        
        supplier = cls.all.get(row[0])
        if supplier:
            supplier.name = row[1]
            supplier.contact_info = row[2]
        else:
            supplier = cls(row[1], row[2])
            supplier.id = row[0]
            cls.all[supplier.id] = supplier
        return supplier
    
    @classmethod
    def get_all(cls):
        sql = """
        SELECT * FROM suppliers
        """
        CURSOR.execute(sql)
        return [cls.instance_from_db(row) for row in CURSOR.fetchall()]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
        SELECT * FROM suppliers
        WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
        SELECT * FROM suppliers
        WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None