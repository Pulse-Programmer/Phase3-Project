from models.__init__ import CONN, CURSOR


class Category:
    all = {}

    def __init__(self, name, description, id=None) -> None:
        self.name = name
        self.description = description
        self.id = id

    def __repr__(self) -> str:
        return (f"<Category {self.id}: {self.name}, {self.description}>")
    
    
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
    
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Category instances """
        CURSOR.execute("CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY, name TEXT, description TEXT)")
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the categories table if it exists """
        CURSOR.execute("DROP TABLE IF EXISTS categories")
        CONN.commit()
    
    
    def save(self):
        """ Save the Category instance to the database """
        CURSOR.execute("INSERT INTO categories (name, description) VALUES(?,?)", (self.name, self.description))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, name, description):
        """ Create a new Category instance and save it to the database """
        category = Category(name, description)
        category.save()
        return category
    
    def update(self):
        """ Update the Category instance in the database """
        CURSOR.execute("UPDATE categories SET name = ?, description = ? WHERE id = ?", (self.name, self.description, self.id))
        CONN.commit()
        
        type(self).all[self.id] = self
        
    def delete(self):
        """ Delete the Category instance from the database """
        CURSOR.execute("DELETE FROM categories WHERE id =?", (self.id,))
        CONN.commit()
        
        del type(self).all[self.id]

        self.id = None
        
    
    @classmethod
    def instance_from_db(cls, row):
        """ Create a Category instance from a database row """
        
         # Check the dictionary for an existing instance using the row's primary key
        category = cls.all.get(row[0])
        if category:
            # ensure attributes match row values in case local instance was modified
            category.name = row[1]
            category.description = row[2]
        else:
            category = cls(row[1], row[2], row[0])
            cls.all[category.id] = category
        return category
            
        
    @classmethod
    def get_all(cls):
        """ Get all Category instances from the database """
        CURSOR.execute("SELECT * FROM categories")
        return [cls.instance_from_db(row) for row in CURSOR.fetchall()]
    
    
    @classmethod
    def find_by_id(cls, id):
        """ return a Category object corresponding to the table row matching its primary key """
        CURSOR.execute("SELECT * FROM categories WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """ return a Category object corresponding to the table row matching its name """
        CURSOR.execute("SELECT * FROM categories WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    def products(self):
        """ return all Product instances belonging to this Category """
        
        

    