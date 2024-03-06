import tkinter as tk
import webbrowser
from tkinter import messagebox, PhotoImage, Tk, Label, Radiobutton, StringVar
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk


"""
    Author:  Shalom Ayalkibet
    Date written: 03/07/24
    Assignment:  module 8  Final Project Submission
    Short Desc:  Titus Palace Pizza Order Manager" is to provide an easy-to-use interface for customers to
 place pizza orders online.
"""
""" Name of the GUI Application:
"Titus Palace Pizza Order Manager"
Purpose of the Application:
The primary purpose of " Titus Palace Pizza Order Manager" is to provide an easy-to-use interface for customers to
 place pizza orders online. It aims to streamline the ordering process, making it efficient, user-friendly, and
 accessible for many customers.
"""


# Dictionary to define the prices of different types of pizzas.
pizza_prices = {
    "Chicken": 12.99,  # Price for chicken pizza
    "Beef": 14.99,  # Price for beef pizza
    "Pepperoni": 11.99  # Price for pepperoni pizza
}


# Function to validate user inputs like pizza selection and quantity.
def validate_input(input_str, data_type):
    """
    Validates user input to ensure it meets the required criteria.

    Args:
    input_str (str): The input value from the user.
    data_type (str): The type of data expected, currently supports "string".

    Returns:
    bool: True if input is valid, False otherwise.
    """
    if data_type == "string":
        if not input_str.strip():  # Check if the input string is empty.
            messagebox.showerror("Error", "Input cannot be empty")
            return False
    return True


# Function to add a selected pizza to the order list.
def add_pizza():
    """
    Adds the selected pizza along with its size, quantity, and toppings to the order summary.
    Validates the selection before addition.
    """
    pizza = pizza_var.get()  # Get the selected pizza type.
    size = size_var.get()  # Get the selected pizza size.
    quantity = quantity_var.get()  # Get the selected pizza quantity.
    # List comprehension to get selected toppings based on the BooleanVar states.
    selected_toppings = [topping for topping, is_selected in toppings_var.items() if is_selected.get()]

    # Validate pizza and size selections before proceeding.
    if validate_input(pizza, "string") and validate_input(size, "string"):
        image_path = pizza_images[pizza]  # Path to the image of the selected pizza.
        pizza_price = pizza_prices[pizza]  # Price of the selected pizza.
        total_price = pizza_price * quantity  # Total price calculation.
        # Append the order details to the order summary list.
        order_summary.append({
            "size": size, "pizza": pizza, "toppings": selected_toppings, "quantity": quantity,
            "total_price": total_price, "image": image_path
        })
        messagebox.showinfo("Success", "Pizza added to your order!")
    else:
        messagebox.showerror("Error", "Please complete your selection.")


# Function to view the current order summary in a new window.
def view_order():
    """
    Opens a new window to display the current order summary with details.
    """
    OrderWindow()  # Instantiate and display the order summary window.


# Function to exit the application with a confirmation dialog.
def exit_app():
    """
    Exits the application after confirming with the user.
    """
    if messagebox.askyesno("Exit", "Do you want to exit the application?"):
        root.destroy()


# Class to create a new window for displaying the order summary.
class OrderWindow:
    def __init__(self):
        """
        Initializes and displays the order summary window with order details.
        """
        self.window = tk.Toplevel()  # Create a new top-level window.
        self.window.title("Order Summary")
        tk.Label(self.window, text="Your Order:").pack()

        # Loop through each item in the order summary to display its details.
        for item in order_summary:
            toppings_text = ", ".join(item.get("toppings", []))  # Get a string of toppings.
            text = f"{item['size']} {item['pizza']} Pizza with {toppings_text}" if toppings_text else (f"{item['size']}"
            f" {item['pizza']} Pizza")
            text += f" - Total: ${item['total_price']:.2f}"
            tk.Label(self.window, text=text).pack()

            # Load and display the image for each pizza in the order.
            img = Image.open(item['image'])
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.window, image=photo)
            img_label.image = photo
            img_label.pack()

        # Buttons to confirm the order, modify the order, or exit.
        tk.Button(self.window, text="Confirm Order", command=self.confirm_order).pack()
        tk.Button(self.window, text="Modify Order", command=self.modify_order).pack()
        tk.Button(self.window, text="Exit", command=exit_app).pack()

    # Function called when confirming the order.
    def confirm_order(self):
        """
        Confirms the current order and closes the application.
        """
        messagebox.showinfo("Confirmed", "Your order has been confirmed!")
        self.window.destroy()  # Close the order summary window.
        root.destroy()  # Exit the application.

    # Function to close the order summary window for order modification.
    def modify_order(self):
        """
        Closes the order summary window, allowing the user to modify their order.
        """
        self.window.destroy()


# Paths to pizza images for display in the GUI.
pizza_images = {
    "Chicken": "chicken.png",
    "Beef": "beef.png",
    "Pepperoni": "pepperoni.png"
}


# Function to load and return a resized PhotoImage for display in the GUI.
def load_resized_image(image_path, new_width, new_height):
    """
    Loads an image from the specified path and resizes it.

    Args:
    image_path (str): Path to the image file.
    new_width (int): New width for the resized image.
    new_height (int): New height for the resized image.

    Returns:
    PhotoImage: The resized image as a PhotoImage object for use in Tkinter.
    """
    img = Image.open(image_path)  # Load the image from the file.
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize the image.
    return ImageTk.PhotoImage(resized_img)  # Return the resized image as a PhotoImage.


# Function to open the default mail client with a pre-addressed email
def open_mail_client():
    support_email = "sayalkibet@gmail.com"
    subject = "Support Request"
    body = "Please describe your issue or feedback."
    # Properly encode the URL to handle spaces and special characters in the subject and body
    mailto_url = f"mailto:{support_email}?subject={subject}&body={body}"
    encoded_mailto_url = mailto_url.replace(" ", "%20").replace("\n", "%0A")
    webbrowser.open(encoded_mailto_url)


# Main application setup and layout configuration.
root = Tk()
root.title("Titus Palace Pizza Order Manager")

# Set the background color and pack the welcome label at the top.
root.configure(bg='light blue')
welcome_label = tk.Label(root, text="Welcome to Titus Palace Pizza!", bg='green')

# Variables to store user selections for pizza type, size, and quantity.
pizza_var = StringVar()
size_var = StringVar()
quantity_var = tk.IntVar(value=1)  # Default quantity is 1.
order_summary = []  # List to hold the order summary.

# Spinbox for quantity selection.
tk.Label(root, text="Select Quantity:").pack()
quantity_spinbox = tk.Spinbox(root, from_=1, to=10, textvariable=quantity_var)
quantity_spinbox.pack()

# Toppings selection setup.
toppings_options = ["Olives", "Tomatoes", "Mushrooms", "Peppers"]
toppings_var = {topping: tk.BooleanVar(value=False) for topping in toppings_options}
tk.Label(root, text="Select Toppings:").pack()
for topping in toppings_options:
    tk.Checkbutton(root, text=topping, variable=toppings_var[topping]).pack()

# Load and display pizza images with selection options.
image_width, image_height = 100, 100
beef_image = load_resized_image('beef.png', image_width, image_height)
chicken_image = load_resized_image('chicken.png', image_width, image_height)
pepperoni_image = load_resized_image('pepperoni.png', image_width, image_height)

# Display each pizza option with its image and selection radio button.
Label(root, image=beef_image).pack()
Radiobutton(root, text="Beef", variable=pizza_var, value="Beef").pack()
Label(root, image=chicken_image).pack()
Radiobutton(root, text="Chicken", variable=pizza_var, value="Chicken").pack()
Label(root, image=pepperoni_image).pack()
Radiobutton(root, text="Pepperoni", variable=pizza_var, value="Pepperoni").pack()

# Size selection radio buttons.
tk.Label(root, text="Select Size:").pack()
tk.Radiobutton(root, text="Small", variable=size_var, value="Small").pack()
tk.Radiobutton(root, text="Medium", variable=size_var, value="Medium").pack()
tk.Radiobutton(root, text="Large", variable=size_var, value="Large").pack()

# Buttons for adding to order, viewing order, and exiting
tk.Button(root, text="Add to Order", command=add_pizza).pack()
tk.Button(root, text="View Order", command=view_order).pack()
tk.Button(root, text="Exit", command=exit_app).pack()
# Add the support label here
tk.Label(root, text="For assistance or to provide feedback, contact our support team ",
         bg='light blue').pack(side=tk.BOTTOM)

# Button to contact support which opens the default mail client
tk.Button(root, text="Contact Support", command=open_mail_client).pack(side=tk.BOTTOM)

root.mainloop()  # Start the GUI event loop.
