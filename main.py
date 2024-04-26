import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.ttk import Treeview
import csv


# Global dictionary to store shopping items (which will be updated by the user)
shopping_list = {}

def update_display():
    # clears Treeview to update list
    list_display.delete(*list_display.get_children())
    # iteration over the items in shopping list
    for item, details in shopping_list.items():
        list_display.insert("", "end", values=(item, details['quantity'], details['price']))

def add_update_item():
    # gets item, quantity, and price from the user
    item_name = item_name_var.get()
    try:
        quantity = int(quantity_var.get())
        price = float(price_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for quantity and price.")
        return
    
    if item_name in shopping_list:
        shopping_list[item_name]['quantity'] += quantity
    else:
        shopping_list[item_name] = {'quantity': quantity, 'price': price}
    update_display()

# used to delete item from the shopping list (if one exists of course)
def remove_item():
    item_name = item_name_var.get()
    if item_name in shopping_list:
        confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to remove {item_name}?")
        if confirm:
            del shopping_list[item_name]
            update_display()
    else:
        messagebox.showerror("Error", "Item not found in the list.")

def calculate_total_cost():
    # gets tax rate and discount from the user (as a percentage also without percentage sign)
    tax_rate = simpledialog.askfloat("Tax Rate", "Enter the tax rate (as a percentage excluding percent sign):", minvalue=0.0, maxvalue=100.0)
    if tax_rate is None:
        return
    discount = simpledialog.askfloat("Discount", "Enter discount if you have any (as a percentage excluding percent sign):", minvalue=0.0, maxvalue=100.0)
    if discount is None:
        return
    total_cost = 0
    for details in shopping_list.values():
        cost = details['quantity'] * details['price']
        total_cost += cost
    total_cost += total_cost * (tax_rate / 100)
    total_cost -= total_cost * (discount / 100)
    # now displays the total cost with tax + discount
    messagebox.showinfo("Total Cost", f"The total cost including tax and discount is: ${total_cost:.2f}")

def save_to_csv():
    # added CSV feature for saving the shopping list and functionality overall
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not filename:
        return
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Item', 'Quantity', 'Price'])
            for item, details in shopping_list.items():
                writer.writerow([item, details['quantity'], details['price']])
        messagebox.showinfo("Success", "Shopping list saved to CSV file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving to CSV file:\n{str(e)}")

# user can also import their own CSV file to load the shopping list
def load_from_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filename:
        return
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                item_name, quantity, price = row
                shopping_list[item_name] = {'quantity': int(quantity), 'price': float(price)}
        messagebox.showinfo("Success", "Shopping list loaded from CSV file.")
        update_display()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading from CSV file:\n{str(e)}")

# main windows of an application
root = tk.Tk()
root.title("Shopping List Manager with CSV Support")

# Configure grid so application can be responsive for resizing
root.grid_rowconfigure(7, weight=1)  # Make the Treeview row expandable
root.grid_columnconfigure(1, weight=1)  # Make the second column expandable

# Input fields and labels
item_name_var = tk.StringVar()
quantity_var = tk.StringVar()
price_var = tk.StringVar()

tk.Label(root, text="Item Name:").grid(row=0, column=0, sticky='ew')
tk.Entry(root, textvariable=item_name_var).grid(row=0, column=1, sticky='ew')

tk.Label(root, text="Quantity:").grid(row=1, column=0, sticky='ew')
tk.Entry(root, textvariable=quantity_var).grid(row=1, column=1, sticky='ew')

tk.Label(root, text="Price:").grid(row=2, column=0, sticky='ew')
tk.Entry(root, textvariable=price_var).grid(row=2, column=1, sticky='ew')

# buttons
tk.Button(root, text="Add/Update Item", command=add_update_item).grid(row=3, column=0, columnspan=2, sticky='ew')
tk.Button(root, text="Remove Item", command=remove_item).grid(row=4, column=0, columnspan=2, sticky='ew')
tk.Button(root, text="Calculate Total Cost", command=calculate_total_cost).grid(row=5, column=0, columnspan=2, sticky='ew')
tk.Button(root, text="Save to CSV", command=save_to_csv).grid(row=6, column=0, sticky='ew')
tk.Button(root, text="Load from CSV", command=load_from_csv).grid(row=6, column=1, sticky='ew')

# Treeview for displaying items
list_display = Treeview(root, columns=("Item", "Quantity", "Price"), show="headings")
list_display.heading("Item", text="Item")
list_display.heading("Quantity", text="Quantity")
list_display.heading("Price", text="Price")
list_display.grid(row=7, column=0, columnspan=2, sticky='nsew')  # Make the Treeview expandable

root.mainloop()
