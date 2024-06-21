# Sip and Store

## CLI Application Project

### Description

This CLI application project is designed to manage a simple inventory system for a liquor store business. It utilizes various helper methods and models to perform various tasks such as managing categories, suppliers, products, orders, order details, inventory, and customers.

## Installation

1. Clone the repository using `git clone git@github.com:Pulse-Programmer/Phase3-Project-Sip-and-Store.git`

2. Navigate to the project directory.

3. Install the required dependencies by running pipenv install

## Usage

To run the CLI application, execute the following command: python lib/cli.py

The application will provide a menu with various options to perform different tasks.

## Helper Methods

The CLI application project utilizes the following helper methods:

1. Category:
   -list_categories: Lists all categories.
   -find_category_by_name: Finds a category by name.
   -create_category: Creates a new category.
   -update_category: Updates an existing category.
   -delete_category: Deletes a category.

2. Supplier:
   -list_suppliers: Lists all suppliers.
   -find_supplier_by_name: Finds a supplier by name.
   -create_supplier: Creates a new supplier.
   -update_supplier: Updates an existing supplier.
   -delete_supplier: Deletes a supplier.

3. Product:
   -list_products: Lists all products.
   -find_product_by_name: Finds a product by name.
   -find_product_by_id: Finds a product by ID.
   -create_product: Creates a new product.
   -update_product: Updates an existing product.
   -delete_product: Deletes a product.

4. Order:
   list_orders: Lists all orders.
   find_order_by_id: Finds an order by ID.
   create_order: Creates a new order.
   update_order: Updates an existing order.
   delete_order: Deletes an order.

5. Order Details:
   list_order_details: Lists all order details.
   find_order_details_by_id: Finds order details by ID.
   create_order_details: Creates new order details.
   update_order_details: Updates existing order details.
   delete_order_details: Deletes order details.

6. Inventory:
   list_inventory: Lists all inventory items.
   find_inventory_by_id: Finds inventory by ID.
   update_inventory: Updates the quantity of an inventory item.

7. Customer:
   list_customers: Lists all customers.
   find_customer_by_id: Finds a customer by ID.
   create_customer: Creates a new customer.
   update_customer: Updates an existing customer.
   delete_customer: Deletes a customer.

### Models

The CLI application project utilizes the following models:

1. Category
2. Supplier
3. Product
4. Order
5. OrderDetails
6. Inventory
7. Customer

Each model represents a table in the database and provides methods to interact with the data.

License
This project is licensed under the MIT License.
