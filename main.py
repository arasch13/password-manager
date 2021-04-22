from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate random password"""
    # define usable characters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # create random password
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    # insert password into password field
    password_box.delete(0, END)
    password_box.insert(END, password)

    # copy password to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    """Save Website, User and Password to password database file"""
    website = website_box.get()
    account = account_box.get()
    password = password_box.get()

    if not website or not account or not password:
        messagebox.showerror(title="Error", message="Please provide all details!")
    else:
        is_ok = messagebox.askokcancel(title=f"{website}", message=f"Add the following user and password?\n\n"
                                                                   f"Username/Email: {account}\nPassword: {password}")
        if is_ok:
            # save new data in dict
            new_entry = {
                website: {
                    "User": account,
                    "Password": password
                }
            }

            # open existing database (if available) and update json file
            try:
                with open("password_database.json", mode="r") as password_database:
                    all_data = json.load(password_database)
                    all_data.update(new_entry)
            except FileNotFoundError: # create new data base and only add new entry
                with open("password_database.json", mode="w") as password_database:
                    json.dump(new_entry, password_database, indent=4)
            else:
                with open("password_database.json", mode="w") as password_database:
                    json.dump(all_data, password_database, indent=4)
            finally: # reset GUI and show confirmation window
                website_box.delete(0, END)
                password_box.delete(0, END)
                website_box.focus()
                messagebox.showinfo(title="Success", message="User and password have been added to password database.")


WHITE = "#ffffff"
FONT_NAME = "Tahoma"


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def show_data():
    website = website_box.get()
    if website:
        try:
            with open("password_database.json", mode="r") as password_database:
                all_data = json.load(password_database)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message=f"No database created yet.")
        else:
            if website in all_data:
                messagebox.showinfo(title=website, message=f"User/Email: {all_data[website]['User']}\n"
                                                           f"Password: {all_data[website]['Password']}")
            else:
                messagebox.showerror(title="Error", message=f"No data for {website} available.")
    else:
        messagebox.showerror(title="Error", message=f"Please enter website first!")


# ---------------------------- UI SETUP ------------------------------- #
# create window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)

# show logo
canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# create text boxes
website_text = Label(text="Website:", bg=WHITE, font=(FONT_NAME, 11, "normal"))
website_text.grid(column=0, row=1)
account_text = Label(text="Email/Username:", bg=WHITE, font=(FONT_NAME, 11, "normal"))
account_text.grid(column=0, row=2)
password_text = Label(text="Password:", bg=WHITE, font=(FONT_NAME, 11, "normal"))
password_text.grid(column=0, row=3)

# create edit boxes
website_box = Entry(width=35)
website_box.focus()
website_box.grid(column=1, row=1)
account_box = Entry(width=54)
account_box.insert(END, "username@provider.com")
account_box.grid(column=1, row=2, columnspan=2)
password_box = Entry(width=35)
password_box.grid(column=1, row=3)

# create buttons
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)
search_button = Button(text="Search", width=14, command=show_data)
search_button.grid(column=2, row=1)
add_button = Button(text="Add", width=45, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)

# hold window
window.mainloop()
