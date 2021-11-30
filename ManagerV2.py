
import json

manage_on = True

while manage_on:

    prompt = "\nIf you want to make a new password, type 'Make password'."
    prompt += "\nIf you want to look for a password, type 'Look for password'.\n"
    prompt += "If you want to view all your passwords, type 'View all passwords'.\n"
    prompt += "if you want to delete a password, type 'Delete password'.\n"
    answer = input(prompt)

    answer = answer.upper()
    # ^ asks user whether they want to make a password or look for one


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
    # ^ function checks whether password dictionary is empty or not. If not then it will read dictionary
    def delete_password(account_name):
        passwords = load_passwords()
        del passwords[account_name]
        return passwords

    def password_list(account_name, password_name):
        passwords = load_passwords()
        passwords[account_name] = password_name
        return passwords
    # ^ load_password function gets passed into this function. account name and password get added

    if answer == "MAKE PASSWORD":
        account_name = input("What use is this password for? ").upper()
        password_name = input("What is the password? ")
        passwords = password_list(account_name, password_name)
        with open("passwords.txt", "w+") as f:
            f.write(json.dumps(passwords))
        print("Your password was saved!")


    elif answer == "LOOK FOR PASSWORD":
        passwords = load_passwords()

        if passwords:
            search_account = input("What account is this password for? ").upper()

            if search_account in passwords:
                print(f"The password is '{(passwords.get(search_account))}'.")
            else:
                print("Sorry, we can't find such name.")

    elif answer == "VIEW ALL PASSWORDS":
        passwords = load_passwords()

        try:
            for keys, values in passwords.items():
                print(f"Account: {keys}")
                print(f"Password: {values}")
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

