import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet
import random
import string
import ast
import logging


def remember_pass(entry_box):

    global enc_key

    enc_key = entry_box.get()

def derive_key(input_string):
    # Create a SHA-256 hash of the user input and truncate to 32 bytes
    key = input_string.encode()

    return key


def encrypt_key_box(binary):

    check = ""

    with open('loginkey.key', 'rb') as mykey:
        key = mykey.read()

    f = Fernet(key)

    with open('enc_login.txt', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open('pass_temp.txt', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

    with open('pass_temp.txt', 'r') as decrypted_file:
        dec_password = decrypted_file.read()  # cut off

    encrypted_file.close()
    open("pass_temp.txt", "w").close()

    with open('enc_recovery.txt', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open('recovery_temp.txt', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

    with open('recovery_temp.txt', 'r') as decrypted_file:
        dec_recovery = decrypted_file.read()  # cut off

    encrypted_file.close()
    open("recovery_temp.txt", "w").close()
    mykey.close()

    if binary == '0':

        failed = ttk.Label(window, text='Wrong password. Try again')
        failed.place(x=230, y=200)

        if (entry.get() == dec_password):
            check = "pass"

    elif binary == '1':

        failed = ttk.Label(program2, text='Wrong recovery code. Try again')
        failed.place(x=220, y=200)

        if (entry2.get() == dec_recovery):
            check = "pass"

    if check == "pass":

        if binary == '1':
            program2.destroy()

        window.withdraw()

        global enc_key_input

        key_box = tk.Toplevel()
        key_box.protocol("WM_DELETE_WINDOW", on_close)
        key_box.title('Password Manager')
        sizer(key_box, 600, 300)

        enc_key_input = ttk.Entry(key_box)

        requestLabel = ttk.Label(key_box,
                                 text='                    Please enter your encryption key:\nInformation will not be displayed if key is input wrongly.')


        submitButton = ttk.Button(key_box, text='Submit', command=lambda: [remember_pass(enc_key_input), key_box.destroy(), frame1()])

        requestLabel.place(x=155, y=40)
        submitButton.place(x=265, y=175)
        enc_key_input.place(x=150, y=125, width=310)



def both_codes():
    codes_file = tk.Toplevel()
    codes_file.protocol("WM_DELETE_WINDOW", on_close)
    codes_file.title('Password Manager')
    sizer(codes_file, 600, 400)

    characters = string.ascii_letters + string.digits

    random_string = ''.join(random.choice(characters) for _ in range(10))

    with open('recovery_temp.txt', 'w') as original_file: #store recovery code in text
        original_file.write(random_string)

    with open('recovery_temp.txt', 'rb') as original_file: #read that code as bytes into recovery_temp
        recovery_temp = original_file.read()

    with open('loginkey.key', 'rb') as mykey: # grab that same key used to encrypt the password
        key = mykey.read()

    f = Fernet(key)

    encrypted_recovery = f.encrypt(recovery_temp)

    with open('enc_recovery.txt', 'wb') as encrypted_file: #encrypt recovery code with the key and save it
        encrypted_file.write(encrypted_recovery)

    with open('Key Receipt.txt', 'w') as pinNumber: # to tell program that password and recovery have already been set
        pinNumber.write('1')

    pinNumber.close()

    open("pass_temp.txt", "w").close()

    mykey.close()

    encrypted_file.close()

    program_key = Fernet.generate_key() # key that will be used to encrypt and decrypted stored passwords and usernames

    disclaimer1 = ttk.Label(codes_file, text='This is your recovery key. DO NOT LOSE IT.')

    code1 = ttk.Label(codes_file, text=random_string)

    disclaimer2 = ttk.Label(codes_file, text='This is your decrypting key. DO NOT LOSE IT.')

    code2 = ttk.Label(codes_file, text=str(program_key))

    disclaimer1.place(x=185, y=50)
    code1.place(x=270, y=125)
    disclaimer2.place(x=185, y=250)
    code2.place(x=150, y=325)


def save_login():
    key = Fernet.generate_key()

    with open('pass_temp.txt', 'w') as original_file: # temporarily store password in text to be read
        original_file.write(login.get())

    with open('pass_temp.txt', 'rb') as original_file: # read that password as bytes into pass_temp
        pass_temp = original_file.read()

    with open('loginkey.key', 'wb') as mykey: # key that will be used for decrypting/encrypting password and recovery code
        mykey.write(key)

    f = Fernet(key)

    encrypted_login = f.encrypt(pass_temp)

    with open('enc_login.txt', 'wb') as encrypted_file: # write encrypted password into enc login file
        encrypted_file.write(encrypted_login)

    open("pass_temp.txt", "w").close()

    mykey.close()
    encrypted_file.close()


def intro_box():
    intro_file = tk.Toplevel()
    intro_file.protocol("WM_DELETE_WINDOW", on_close)
    intro_file.title('Password Manager')
    sizer(intro_file, 600, 300)

    global login

    requestLabel = ttk.Label(intro_file, text='Please create a password for login:')

    submitButton = ttk.Button(intro_file, text='Submit',
                              command=lambda: [save_login(), intro_file.destroy(), both_codes()])

    login = ttk.Entry(intro_file)

    requestLabel.place(x=210, y=75)
    submitButton.place(x=261, y=175)
    login.place(x=236, y=125)


def treeview_password_box():
    try:
        file_viewer = tk.Toplevel()
        file_viewer.protocol("WM_DELETE_WINDOW", on_close)
        sizer(file_viewer, 600, 300)
        file_viewer.title('Password Manager')

        file_viewer.columnconfigure(0, weight=1)
        file_viewer.columnconfigure(1, weight=1)
        file_viewer.columnconfigure(2, weight=1)
        file_viewer.rowconfigure(0, weight=1)
        file_viewer.rowconfigure(1, weight=0)

        table = ttk.Treeview(file_viewer, columns=('Site/Email/App:', 'Password'), show='headings')
        table.heading('Site/Email/App:', text='Site/Email/App:')
        table.heading('Password', text='Password')
        table.grid(row=0, column=0, columnspan=3, sticky="ew")

        # Add a button directly below the Treeview
        button1 = ttk.Button(file_viewer, text='Back', command=lambda: [file_viewer.destroy(), frame1()])
        button1.grid(row=1, column=1)

        index_num = 0

        base64_key = derive_key(enc_key)

        f = Fernet(base64_key)

        with open('enc_registry.txt', 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        if len(encrypted) != 0:
            # Decrypt file and handle exceptions
            try:
                decrypted = f.decrypt(encrypted)
            except Exception as e:
                logging.error(f"Decryption failed: {e}")
                return  # Stop execution if decryption fails

            with open('dec_registry.txt', 'wb') as decrypted_file:
                decrypted_file.write(decrypted)

            with open('dec_registry.txt', 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        # Skip empty lines
                        continue

                    try:
                        # Ensure the line is a valid Python literal
                        tuple_data = ast.literal_eval(line)
                        if isinstance(tuple_data, tuple) and len(tuple_data) == 2:
                            user, password = tuple_data
                            table.insert(parent='', index=index_num, values=(user, password))
                            index_num += 1
                        else:
                            logging.error(f"Invalid data format: {line}")
                    except (SyntaxError, ValueError) as e:
                        logging.error(f"Failed to process line: {e}, line: {line}")
                        continue

            # Re-encrypt the file after processing
            try:
                with open('dec_registry.txt', 'rb') as original_file:
                    original = original_file.read()

                encrypted = f.encrypt(original)

                with open('enc_registry.txt', 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)

                open("dec_registry.txt", "w").close()
            except Exception as e:
                logging.error(f"Re-encryption failed: {e}")

    except Exception as general_exception:
        logging.error(f"An unexpected error occurred: {general_exception}")


def delete_password(box_name):
    username = user_box.get()
    password = password_box.get()

    password_tuple = (username, password)

    base64_key = derive_key(enc_key)
    f = Fernet(base64_key)

    with open('enc_registry.txt', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    if len(encrypted) != 0:
        decrypted = f.decrypt(encrypted)

        with open('dec_registry.txt', 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        remaining_tuples = []

        with open('dec_registry.txt', 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace or newline characters

                # Skip empty lines
                if not line:
                    continue

                # Convert the line to a tuple using ast.literal_eval
                try:
                    tuple_item = ast.literal_eval(line)

                    # Check if the current tuple matches the one we want to remove
                    if tuple_item != password_tuple:
                        # If it doesn't match, keep the tuple
                        remaining_tuples.append(tuple_item)

                except Exception as e:
                    print(f"Error parsing line '{line}': {e}")

        # Write the remaining tuples back to the file
        with open('dec_registry.txt', 'w') as file:
            for remaining_tuple in remaining_tuples:
                file.write(str(remaining_tuple) + '\n')

        # Encrypt the updated file
        with open('dec_registry.txt', 'rb') as original_file:
            original = original_file.read()

        encrypted = f.encrypt(original)

        with open('enc_registry.txt', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        # Clear the decrypted file
        open("dec_registry.txt", "wb").close()

    # Notify the user the deletion is complete
    done = ttk.Label(box_name, text='Done!')
    done.place(x=280, y=250)
    box_name.after(3000, done.destroy)


def delete_password_box():
    delete_file = tk.Toplevel()
    delete_file.protocol("WM_DELETE_WINDOW", on_close)
    delete_file.title('Password Manager')
    sizer(delete_file, 600, 300)

    global user_box
    global password_box

    user_box = ttk.Entry(delete_file)
    password_box = ttk.Entry(delete_file)

    label = ttk.Label(delete_file, text='Site/Email/App:')
    label1 = ttk.Label(delete_file, text='Password:')

    button = ttk.Button(delete_file, text='Delete', command=lambda: [delete_password(delete_file)])
    button1 = ttk.Button(delete_file, text='Back', command=lambda: [delete_file.destroy(), frame1()])

    label.place(x=78, y=90)
    user_box.place(x=78, y=115, width=200)
    password_box.place(x=320, y=115, width=200)
    label1.place(x=320, y=90)
    button.place(x=260, y=155)
    button1.place(x=260, y=205)


def add_password(box_name):
    username = user_box.get()

    password = password_box.get()

    password_tuple = (username, password)

    base64_key = derive_key(enc_key)

    f = Fernet(base64_key)

    with open('enc_registry.txt', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    if len(encrypted) == 0:

        with open('dec_registry.txt', 'a') as decrypted_file:
            decrypted_file.write(str(password_tuple))

        with open('dec_registry.txt', 'rb') as original_file:
            original = original_file.read()

        encrypted = f.encrypt(original)

        with open('enc_registry.txt', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        open("dec_registry.txt", "wb").close()

        encrypted_file.close()

    else:

        decrypted = f.decrypt(encrypted)

        with open('dec_registry.txt', 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        with open('dec_registry.txt', 'a') as decrypted_file:
            decrypted_file.write("\n" + str(password_tuple))

        with open('dec_registry.txt', 'rb') as original_file:
            original = original_file.read()

        encrypted = f.encrypt(original)

        with open('enc_registry.txt', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        open("dec_registry.txt", "wb").close()

        encrypted_file.close()

    done = ttk.Label(box_name, text='Done!')
    done.place(x=280, y=250)
    box_name.after(3000, done.destroy)


def add_password_box():
    add_file = tk.Toplevel()
    add_file.protocol("WM_DELETE_WINDOW", on_close)
    add_file.title('Password Manager')
    sizer(add_file, 600, 300)

    global user_box
    global password_box

    user_box = ttk.Entry(add_file)
    password_box = ttk.Entry(add_file)

    label = ttk.Label(add_file, text='Site/Email/App:')
    label1 = ttk.Label(add_file, text='Password:')

    button = ttk.Button(add_file, text='Add', command=lambda: [add_password(add_file)])
    button1 = ttk.Button(add_file, text='Back', command=lambda: [add_file.destroy(), frame1()])

    label.place(x=78, y=90)
    user_box.place(x=78, y=115, width=200)
    password_box.place(x=320, y=115, width=200)
    label1.place(x=320, y=90)
    button.place(x=260, y=155)
    button1.place(x=260, y=205)


def view_password_box():
    view_files = tk.Toplevel()
    view_files.protocol("WM_DELETE_WINDOW", on_close)
    view_files.title('Password Manager')
    global table
    table = ttk.Treeview(view_files, columns=('username', 'password'), show='headings')
    table.heading('username', text='Site/Email/App:')
    table.heading('password', text='Password:')
    table.pack()


def on_close():
    window.destroy()


def sizer(frame, width, height):
    frame.minsize(width, height)
    frame.maxsize(width, height)

    display_width = frame.winfo_screenwidth()
    display_height = frame.winfo_screenheight()

    left = int(display_width / 2 - width / 2)
    top = int(display_height / 2 - height / 2)

    frame.geometry(f'{width}x{height}+{left}+{top}')


def frame1():
    global program

    program = tk.Toplevel()
    program.protocol("WM_DELETE_WINDOW", on_close)
    sizer(program, 800, 500)

    program.columnconfigure(0, weight=1)
    program.columnconfigure(1, weight=1)
    program.rowconfigure(0, weight=1)
    program.rowconfigure(1, weight=1)

    style = ttk.Style()
    style.configure('new.TButton', font=('Arial', 20))

    make_password = ttk.Button(program, text='Make password', style='new.TButton',
                               command=lambda: [program.destroy(), add_password_box()])
    view_passwords = ttk.Button(program, text='View all passwords', style='new.TButton',
                                command=lambda: [program.destroy(), treeview_password_box()])
    del_password = ttk.Button(program, text='Delete password', style='new.TButton',
                              command=lambda: [program.destroy(), delete_password_box()])

    make_password.grid(row=0, column=0, sticky='nsew')
    del_password.grid(row=0, column=1, sticky='nsew')
    view_passwords.place(x=0, y=270, height=230, width=800)


def frame2():
    global program2
    global entry2
    window.withdraw()
    program2 = tk.Toplevel()
    program2.protocol("WM_DELETE_WINDOW", on_close)
    program2.title('Password Manager')

    sizer(program2, 600, 300)

    label = ttk.Label(program2, text='Recovery key:')

    entry2 = ttk.Entry(program2)

    button = ttk.Button(program2, text='Back to password', command=lambda: [program2.destroy(), window.deiconify()])
    button2 = ttk.Button(program2, text='Login', command=lambda: [encrypt_key_box('1')])

    label.place(x=268, y=90)
    entry2.place(x=205, y=115, width=200)
    button.place(x=204, y=145)
    button2.place(x=309, y=145, width=97)


def mainframe():
    global window
    global entry
    window = tk.Tk()
    window.title('Password Manager')

    with open('Key Receipt.txt', 'r') as pinNumber:
        pinnum = pinNumber.read()

    if pinnum == '0':
        window.withdraw()
        intro_box()


    sizer(window, 600, 300)

    label = ttk.Label(window, text='Password:')

    entry = ttk.Entry(window)

    button = ttk.Button(window, text='Use recovery key', command=frame2)
    button2 = ttk.Button(window, text='Login', command=lambda: [encrypt_key_box('0')])

    label.place(x=274, y=90)
    entry.place(x=205, y=115, width=200)
    button.place(x=204, y=145)
    button2.place(x=305, y=145, width=100)

    window.mainloop()

mainframe()
