from helpers import (
    exit_program,
    list_categories,
    find_category_by_name,
    list_suppliers,
    find_supplier_by_name,
    create_supplier,
    update_supplier,
    delete_supplier,
    list_products,
    find_product_by_name,
    find_product_by_id,
    create_product,
    update_product,
    delete_product,
    list_orders,
    find_order_by_id,
    create_order,
    list_order_details,
    find_order_details_by_id,
    list_inventories,
    find_inventory_by_id,
    list_customers
)


def main():
    while True:
        menu()
        option = int(input("Enter an option:> "))
        if  option == 0:
            exit_program()
        elif option == 1:
            list_categories()
        elif option == 2:
            find_category_by_name()
        elif option == 3:
            list_suppliers()
        elif option == 4:
            find_supplier_by_name()
        elif option == 5:
            create_supplier()
        elif option == 6:
            update_supplier()
        elif option == 7:
            delete_supplier()
        elif option == 8:
            list_products()
        elif option == 9:
            find_product_by_name()
        elif option == 10:
            find_product_by_id()
        elif option == 11:
            create_product()
        elif option == 12:
            update_product()
        elif option == 13:
            delete_product()
        elif option == 14:
            list_orders()
        elif option == 15:
            find_order_by_id()
        elif option == 16:
            create_order()
        elif option == 17:
            list_order_details()
        elif option == 18:
            find_order_details_by_id()
        elif option == 19:
            list_inventories()
        elif option == 20:
            find_inventory_by_id()
        else:
             print("Invalid choice")


def menu():
    print("Please select an option:")
    print("1. List categories")
    print("2. Find category by name")
    print("3. List suppliers")
    print("4. Find supplier by name")
    print("5. Create supplier")
    print("6. Update supplier")
    print("7. Delete supplier")
    print("8. List products")
    print("9. Find product by name")
    print("10. Find product by ID")
    print("11. Create product")
    print("12. Update product")
    print("13. Delete product")
    print("14. List orders")
    print("15. Find order by ID")
    print("16. Create order")
    print("17. List order details")
    print("18. Find order details by ID")
    print("19. List inventories")
    print("20. Find inventory by ID")
    
    
if __name__ == "__main__":
    main()