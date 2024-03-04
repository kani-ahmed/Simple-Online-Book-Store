# class to manage the whole collection of books
class BookInventory:
    def __init__(self):
        # dictionary to store all books
        self.books_dict = {}

    # store a book
    def add_book(self, book):
        if book.book_id in self.books_dict:
            print(f"Book ID {book.book_id} already exists. Update the book instead of adding a new one.")
        else:
            if book.price > 0 and book.quantity >= 0:
                self.books_dict[book.book_id] = {
                    'title': book.title,
                    'author': book.author,
                    'price': book.price,
                    'quantity': book.quantity
                }
            else:
                print("Book price must be positive and quantity non-negative.")

    # another method to remove books from the books_dict
    def remove_book(self, book_id):
        if book_id in self.books_dict:
            del self.books_dict[book_id]
        else:
            print("Can't delete a book that don't exist")

    # decrease the quantity of a book (-1 if no quantity is passed)
    def decrease_quantity(self, book_id, quantity=1):
        if book_id in self.books_dict and quantity <= self.books_dict[book_id]['quantity']:
            self.books_dict[book_id]['quantity'] -= quantity
        else:
            print(
                f"Cannot decrease quantity for Book ID {book_id}. "
                f"Check if the book exists and has sufficient quantity.")

    # print all books in the inventory
    def print_all_books_in_inventory(self):
        for book_id, book_details in self.books_dict.items():
            print(f"Book ID: {book_id}, Title: {book_details['title']}, "
                  f"Author: {book_details['author']}, Price: {book_details['price']}, "
                  f"Quantity: {book_details['quantity']}")


class Book:
    def __init__(self, book_id, title, author, price, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return (f"Book ID: {self.book_id}, Title: {self.title}, "
                f"Author: {self.author}, Price: {self.price}, "
                f"Quantity: {self.quantity}")


class ShoppingCart:

    def __init__(self, inventory):
        self.inventory = inventory
        # dict to store all shopping cart items
        self.shopping_cart_dict = {}

    def add_book_to_shopping_cart(self, book_id, quantity):
        if quantity > 0:  # quantity must be > 0
            if (book_id in self.inventory.books_dict and  # if the book is in store
                    self.inventory.books_dict[book_id]['quantity'] > 0):  # and it has positive quantity
                # and the user is not ordering more than the available quantity for that book
                if quantity <= self.inventory.books_dict[book_id]['quantity']:
                    # either add newly purchased book to the shopping cart dict
                    # or just increase its quantity if existing
                    self.shopping_cart_dict[book_id] = (self.shopping_cart_dict.get(book_id, 0) +
                                                        quantity)
                else:
                    print("Can't purchase. Quantity too high for in-stock quantity")
                    print(f"Available number of books for book {book_id}: "
                          f"{self.inventory.books_dict[book_id]['quantity']}")
            else:
                print("Book not available. We will notify you when back in stock")
        else:
            print("Quantity must be greater than 0.")

    def remove_book_from_shopping_chart(self, book_id):
        if book_id in self.shopping_cart_dict:
            del self.shopping_cart_dict[book_id]
        else:
            print("Cart does not contain a book with his id")

    def decrease_quantity(self, book_id):
        # if we have the book in the shopping cart
        if book_id in self.shopping_cart_dict:
            # if the quantity book is 1 or more
            if self.shopping_cart_dict[book_id] > 1:
                # decrease it
                self.shopping_cart_dict[book_id] -= 1
            else:
                # just delete it
                self.remove_book_from_shopping_chart(book_id)

    def print_shopping_cart(self):
        for book_id, quantity in self.shopping_cart_dict.items():
            if book_id in self.inventory.books_dict:  # in case a book has been removed from inventory
                book_details = self.inventory.books_dict[book_id]
                print(f"Book ID: {book_id}, Title: {book_details['title']}, "
                      f"Author: {book_details['author']}, "
                      f"Price: {book_details['price']}, Quantity: {quantity}")
            else:
                print(f"Book ID {book_id} not found in inventory.")

    def total_cost_all_items_in_chart(self):
        total_all_items = 0
        for book_id, quantity in self.shopping_cart_dict.items():
            total_all_items += self.inventory.books_dict[book_id][
                                   'price'] * quantity  # self.shopping_cart_dict[self.book_id]
        return total_all_items


class Order:
    # keeps track of all ordered items
    ordered_items_dict = {}

    def __init__(self, order_id, shopping_cart, inventory):
        self.inventory = inventory
        self.order_id = order_id
        self.books = shopping_cart.shopping_cart_dict  # Dictionary of book_id to quantity
        self.total_cost_of_orders = self.calculate_total_cost(shopping_cart)
        self.status = 'New'
        # self.process_order()  # Automatically process the order upon initialization

    def calculate_total_cost(self, shopping_cart):
        total_cost = 0
        for book_id, quantity in shopping_cart.shopping_cart_dict.items():
            book_price = self.inventory.books_dict[book_id]['price']
            total_cost += book_price * quantity
        return total_cost

    def complete_checkout(self):
        valid = True
        for book_id, quantity in self.books.items():
            if book_id not in self.inventory.books_dict or self.inventory.books_dict[book_id]['quantity'] < quantity:
                valid = False
                print(f"Checkout failed for Book ID {book_id}. Insufficient stock.")
                break
        if valid:
            for book_id, quantity in self.books.items():
                self.inventory.decrease_quantity(book_id, quantity)  # update inventory
            Order.ordered_items_dict[self.order_id] = {
                'books': self.books,
                'total_cost_of_order': self.total_cost_of_orders,
                'status': self.status
            }
        else:
            print("Checkout failed due to stock issues.")

    def check_orders_status(self):
        print("Order Status:")
        for order_id, order_details in Order.ordered_items_dict.items():
            print(f"\nOrder ID: {order_id}")
            total_cost = order_details['total_cost_of_order']
            status = order_details['status']
            for book_id, quantity in order_details['books'].items():
                # Fetch book details from the inventory to print
                book = self.inventory.books_dict.get(book_id, {})
                title = book.get('title', 'Unknown Title')
                author = book.get('author', 'Unknown Author')
                price = book.get('price', 0)
                # Print details for each book in the order
                print(f"  - Title: {title}, Author: {author}, Price: ${price}, Quantity: {quantity}")
            # Print total cost and status at the end of each order's details
            print(f"Total Cost of Order: ${total_cost}, Status: {status}")

    def update_order_status(self, new_status):
        valid_statuses = ["New", "Processed", "Shipped", "Cancelled"]
        allowed_transitions = {
            "New": ["Processed"],
            "Processed": ["Shipped", "Cancelled"],
            "Shipped": [],
            "Cancelled": []
        }

        if new_status in valid_statuses:
            if new_status not in allowed_transitions[self.status]:
                print(f"Invalid status transition from {self.status} to {new_status}.")
                return
            else:
                if new_status == "Cancelled" and self.status != "Cancelled":
                    for book_id, quantity in self.books.items():
                        self.inventory.books_dict[book_id]['quantity'] += quantity
                Order.ordered_items_dict[self.order_id]['status'] = new_status
        else:
            print(f"{new_status} is not a valid status.")


def main():
    inventory = BookInventory()
    # Adding books to inventory
    book1 = Book(1, "first book", "Ali", 100, 5)
    book2 = Book(2, "second book", "Abdikani", 100, 3)
    inventory.add_book(book1)
    inventory.add_book(book2)

    print("----------------------------------------------------------------------------------------")
    print("Show book details in the inventory")
    print("----------------------------------------------------------------------------------------")
    inventory.print_all_books_in_inventory()

    # Initializing a ShoppingCart with reference to the inventory
    shopping_cart = ShoppingCart(inventory)
    # Adding books to the shopping cart (takes book_id, quantity) for simplicity
    shopping_cart.add_book_to_shopping_cart(1, 2)  # Adding 2 copies of book1
    shopping_cart.add_book_to_shopping_cart(2, 1)  # Adding 1 copy of book2

    # Displaying shopping cart contents
    print("----------------------------------------------------------------------------------------")
    print("Show shopping cart contents")
    print("----------------------------------------------------------------------------------------")
    shopping_cart.print_shopping_cart()
    print(f"Total cost: {shopping_cart.total_cost_all_items_in_chart()}")

    # Processing an order based on the shopping cart
    order1 = Order(1, shopping_cart, inventory)
    order1.complete_checkout()
    print("----------------------------------------------------------------------------------------")
    print("Show order details")
    print("----------------------------------------------------------------------------------------")
    order1.check_orders_status()
    order1.update_order_status("Processed")
    print("----------------------------------------------------------------------------------------")
    print("Show order details after status changed to processed")
    print("----------------------------------------------------------------------------------------")
    order1.check_orders_status()

    order1.update_order_status("Shipped")
    print("----------------------------------------------------------------------------------------")
    print("Show order details after status changed to shipped")
    print("----------------------------------------------------------------------------------------")
    order1.check_orders_status()


main()
