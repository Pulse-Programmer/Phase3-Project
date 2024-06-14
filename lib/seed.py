from models.__init__ import CONN, CURSOR
from models.product import Product
from models.category import Category
from models.supplier import Supplier
from models.order import Order
from models.order_details import OrderDetails
from models.inventory import Inventory
from models.customer import Customer

def seed_database():
    Product.drop_table()
    Category.drop_table()
    Supplier.drop_table()
    Order.drop_table()
    OrderDetails.drop_table()
    Inventory.drop_table()
    Customer.drop_table()

    Product.create_table()
    Category.create_table()
    Supplier.create_table()
    Order.create_table()
    OrderDetails.create_table()
    Inventory.create_table()
    Customer.create_table()
    
    
    # Create seed data
    eabl = Supplier.create("EABL", "Garden City, 348")
    kwal = Supplier.create("Kwal", "Industrial Park, 128")
    
    beer = Category.create("Beer", "Malt")
    wine = Category.create("Wine", "Red Wine, White Wine")
    whisky = Category.create("Whisky", "Scotch whisky")
    
    beer1 = Product.create("Heineken", "Coca Cola", 2.5, beer.id, eabl.id)
    beer2 = Product.create("Corona", "Coca Cola", 2.5, beer.id, eabl.id)
    wine1 = Product.create("Chateau d'Yquem", "Champagne", 10.0, wine.id, kwal.id)
    wine2 = Product.create("4 Cousins", "white", 10.0, wine.id, kwal.id)
    whisky1 = Product.create("Balantines", "Scottish whisky", 25.5, whisky.id, kwal.id)
    whisky2 = Product.create("Tullamore", "Rye", 45.5, whisky.id, kwal.id)

    customer1 = Customer.create("Smith","smith@example.com",7452666374, "Membley")
    customer2 = Customer.create("John","john@example.com",7452635374, "Roysambu")
    customer3 = Customer.create("Jane","jane@example.com",4552635374, "Westlands")

    order1 = Order.create(customer1.id, "12/2/2024", 50.5)
    order2 = Order.create(customer2.id, "10/1/2024", 30.8)
    order3 = Order.create(customer3.id, "1/1/2024", 20.4)
    
    #generate instances of OrderDetails
    OrderDetails.create(order1.id, beer1.id, 24, 8000.0)
    OrderDetails.create(order1.id, beer2.id, 20, 700.0)
    OrderDetails.create(order2.id, wine1.id, 12, 1200.0)
    OrderDetails.create(order2.id, wine2.id, 42, 5000.0)
    OrderDetails.create(order3.id, whisky1.id, 22, 3000.0)
    
    #generate instances of inventory
    Inventory.create(beer1.id, 100)
    Inventory.create(beer2.id, 200)
    Inventory.create(wine1.id, 300)
    Inventory.create(wine2.id, 400)
    Inventory.create(whisky1.id, 500)
    Inventory.create(whisky2.id, 600)
    

seed_database()
print("Seeded database")
    