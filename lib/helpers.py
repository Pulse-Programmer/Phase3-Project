from models.category import Category
from models.supplier import Supplier
from models.product import Product
from models.order import Order
from models.order_details import OrderDetails
from models.inventory import Inventory
from models.customer import Customer


def exit_program():
    print("Goodbye!")
    exit()
    


#category methods
def list_categories():
    categories = Category.get_all()
    for category in categories:
        print(f"    {category.id}: {category.name}")
        
def find_category_by_name():
    name = input("Enter category name:> ")
    category = Category.find_by_name(name)
    print(f"    {category.id}: {category.name}") if category else print(
        "No category found with that name"
    )


#supplier methods      
def list_suppliers():
    suppliers = Supplier.get_all()
    for supplier in suppliers:
        print(f"    {supplier.id}: {supplier.name}")
        
def find_supplier_by_name():
    name = input("Enter supplier name:> ")
    supplier = Supplier.find_by_name(name)
    print(f"    {supplier.id}: {supplier.name}") if supplier else print(
        "No supplier found with that name"
    )

def create_supplier():
    name = input("Enter supplier name:> ")
    contact = input("Enter supplier contact:> ")
    try:
        supplier = Supplier(name, contact).create()
        print(f'    Success: {supplier}')
    except Exception as e:
        print('Error saving supplier:', e)
        

def update_supplier():
    id_ = int(input("Enter supplier ID:> "))
    supplier = Supplier.find_by_id(id_)
    if supplier:
        try:
            name = input("Enter supplier name:> ")
            supplier.name = name
            contact = input("Enter supplier contact:> ")
            supplier.contact_info = contact
        
            supplier = Supplier.update()
            print(f"    Success: {supplier}")
        except Exception as exc:
            print("Error updating supplier:", exc)
    else:
        print("No supplier found with that ID")
        
        
def delete_supplier():
    id_ = int(input("Enter supplier ID:> "))
    supplier = Supplier.find_by_id(id_)
    if supplier:
        supplier.delete()
        print(f'    Supplier {id_} deleted')
        
    else:
        print("No supplier found with that ID")


#product methods
def list_products():
    products = Product.get_all()
    for product in products:
        print(f"    {product.id}: {product.name}")
        
def find_product_by_name():
    name = input("Enter product name:> ")
    product = Product.find_by_name(name)
    print(f"    {product.id}: {product.name}") if product else print(
        "No product found with that name"
    )
    
def find_product_by_id():
    id_ = int(input("Enter product ID:> "))
    product = Product.find_by_id(id_)
    print(f"    {product.id}: {product.name}") if product else print(
        "No product found with that ID"
    )
    
def create_product():
    name = input("Enter product name:> ")
    description = input("Enter product description:> ")
    price = float(input("Enter product price:> "))
    category_id = int(input("Enter product category ID:> "))
    supplier_id = int(input("Enter product supplier ID:> "))
    try:
        product = Product(name, description, price, category_id, supplier_id)
        print(f"    Success: {product}")
    except Exception as exc:
        print("Error creating product: ", exc)
           
def update_product():
    id_ = int(input("Enter product ID:> "))
    product = Product.find_by_id(id_)
    if product:
        try:
            name = input("Enter new product name:> ")
            product.name = name
            description = input("Enter new product description:> ")
            product.description = description
            price = float(input("Enter new product price:> "))
            product.price = price
            category_id = int(input("Enter new product category ID:> "))
            product.category_id = category_id
            supplier_id = int(input("Enter new product supplier ID:> "))
            product.supplier_id = supplier_id
        
            product.update()
            print(f"    Success: {product}")
        except Exception as exc:
            print("Error updating product: ", exc)
    else:
        print("No product found with that ID")

def delete_product():
    id_ = int(input("Enter product ID:> "))
    product = Product.find_by_id(id_)
    if product:
        product.delete()
        print(f"    Success: {product}")
    else:
        print("No product found with that ID")



#order methods     
def list_orders():
    orders = Order.get_all()
    for order in orders:
        print(f"    {order.id}: {order.customer_id}")
        
def find_order_by_id():
    id_ = int(input("Enter order ID:> "))
    order = Order.find_by_id(id_)
    print(order) if order else print(
        "No order found with that ID"
    )
 
def create_order():
    customer_id = int(input("Enter customer ID:> "))
    order_date = input("Enter date of order:> ")
    amount = input("Enter amount:> ")
    
    try:
        order = Order.create(customer_id, order_date, amount)
        print(f'    Success: {order}')
    except Exception as e:
        print('Error saving order:', e)
 
        
#orderdetails methods
def list_order_details():
    orderdetails = OrderDetails.get_all()
    for orderdetail in orderdetails:
        print(f"    {orderdetail.id}: {orderdetail}")
        
def find_order_details_by_id():
    id_ = int(input("Enter order details ID:> "))
    orderdetails = OrderDetails.find_by_id(id_)
    print(orderdetails) if orderdetails else print(
        "No order details found with that ID"
    )


def create_order_details():
    order_id = int(input("Enter order ID:> "))
    product_id = int(input("Enter product ID:> "))
    quantity = int(input("Enter quantity:> "))
    price = float(input("Enter price:> "))
    try:
        orderdetails = OrderDetails.create(order_id, product_id, quantity, price)
        print(f'    Success: {orderdetails}')
    except Exception as exc:
        print('Error saving order details:', exc)       
    
#inventory methods
def list_inventories():
    inventory = Inventory.get_all()
    for inv in inventory:
        print(f"    {inv}")


def find_inventory_by_id():
    id_ = int(input("Enter inventory ID:> "))
    inventory = Inventory.find_by_id(id_)
    print(inventory) if inventory else print(
        "No inventory found with that ID"
    )

#customer methods      
def list_customers():
    customers = Customer.get_all()
    for customer in customers:
        print(f"    {customer.id}: {customer.name}")
        
def create_customer():
    name = input("Enter customer name:> ")
    email = input("Enter customer email:> ")
    phone = input("Enter customer phone:> ")
    address = input("Enter customer address:> ")
    try:
        customer = Customer.create(name, email, phone, address)
        print(f'    Success: {customer}')
    except Exception as e:
        print('Error saving customer:', e)
        
def find_customer_by_id():
    id_ = int(input("Enter customer ID:> "))
    customer = Customer.get_by_id(id_)
    print(customer) if customer else print(
        "No customer found with that ID"
    )

def update_customer():
    id_ = int(input("Enter customer ID:> "))
    
    if customer:= Customer.get_by_id(id_):
        try:
            name = input("Enter new customer name:> ")
            customer.name = name
            email = input("Enter new customer email:> ")
            customer.email = email
            phone = input("Enter new customer phone:> ")
            customer.phone = phone
            address = input("Enter new customer address:> ")
            customer.address = address
       
            customer.update()
            print(f"    Success: {customer}")
        except Exception as exc:
            print("Error updating customer: ", exc)
    else:
        print("No customer found with that ID")


def delete_customer():
    id_ = int(input("Enter customer ID:> "))
    customer = Customer.get_by_id(id_)
    if customer:
        customer.delete()
        print(f"    Deleted: {customer}")
    else:
        print("No customer found with that ID")






        
