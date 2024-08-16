
import json

manage_on = True

while manage_on:

    prompt = "\nIf you want to make a new password, type 'Make password'."
    prompt += "\nIf you want to look for a password, type 'Look for password'.\n"
    prompt += "If you want to view all your passwords, type 'View all passwords'.\n"
    prompt += "if you want to delete a password, type 'Delete password'.\n"
    answer = input(prompt)

    answer = answer.upper()
    


    def load_passwords():
        try:
            with open("passwords.txt", "r") as f:
                passwords = json.loads(f.read())
            return passwords
        except FileNotFoundError:
            if answer == "MAKE PASSWORD":
                return {}
            elif answer == "LOOK FOR PASSWORD":
                print("Sorry but there are no passwords available. Make a new one!")
                return {}
    # ^ function that loads up the password dictionary from text file and returns all the account and passwords saved.
    
    def delete_password(account_name):
        passwords = load_passwords()
        del passwords[account_name]
        return passwords
    # ^ function for deleting password
    
    def password_list(account_name, password_name):
        passwords = load_passwords()
        passwords[account_name] = password_name
        return passwords
    # ^ function for adding password

    if answer == "MAKE PASSWORD":
        account_name = input("What use is this password for? ").upper() # < account_name is for subject associated with password
        password_name = input("What is the password? ")
        passwords = password_list(account_name, password_name) # < passwords is a dictionary containing account and password names. After this line, passwords has all the updated passwords.
        with open("passwords.txt", "w+") as f:
            f.write(json.dumps(passwords))
        print("Your password was saved!")


    elif answer == "LOOK FOR PASSWORD":
        passwords = load_passwords()

        if passwords: # < if passwords is not empty...
            search_account = input("What account is this password for? ").upper()

            if search_account in passwords:
                print(f"The password is '{(passwords.get(search_account))}'.") # < Retrieves password in dictionary associated with account name
            else:
                print("Sorry, we can't find such name.")

    elif answer == "VIEW ALL PASSWORDS":
        passwords = load_passwords()

        try:
            for keys, values in passwords.items(): # < For all account names and passwords in the dictionary (string form?)
                print(f"Account: {keys}") # < account_name
                print(f"Password: {values}") # < passwords
                print("\n")
        except AttributeError:
            print("There are no passwords made yet. Make one!")

    elif answer == "DELETE PASSWORD":
        print("\n")
        account_name = input("What account or purpose is this password for? ").upper()
        passwords = delete_password(account_name)
        with open("passwords.txt", "w+") as f:
            f.write(json.dumps(passwords))
        print("\nThe password has been deleted")

    continue_or_leave = input("\nDo you wish to exit? 'no' or 'yes'. ").upper()

    if continue_or_leave == "YES":
        manage_on = False

