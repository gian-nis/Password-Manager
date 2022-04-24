import json
from cryptography.fernet import Fernet

manage_on = True

while manage_on:

    def load_key():

        return open("secret.key", "rb").read()
    # ^ loads into file containing keys used to decrypt messages

    def encrypt_message(message, key):
        c = Fernet(key)
        encrypted_message = c.encrypt(message)
        return encrypted_message
    # ^ takes in a password/message and a key to then encrypt the password/message with the key
    # and return the encrypted message

    def make_password(usage, password):
        key = Fernet.generate_key()
        enc_password = encrypt_message(password, key)
        key = key.decode("utf-8")
        key_dict = {usage: key}
        enc_password = enc_password.decode("utf-8")
        pass_dict = {usage: enc_password}
        with open('passwords.json', 'w') as f:
            json.dump(pass_dict, f)
        with open("secret.key", 'w') as f:
            json.dump(key_dict, f)
    # ^ a usage for password and the password are taken in. a key is generated and is then taken
    # to encrypt a password. This is where the root problem is because i cant dump a byte into a json
    # so i decode it to remove the byte tag and hope to dump it


    def check_file():
        try:
            with open('passwords.json', "r") as f:
                pass_dict = json.loads(f.read())
            return pass_dict
        except FileNotFoundError:
            return {}
    # checks if there is a password file containing the dict of the usage: password

    def assignment():
        pass_dict = check_file()
        if pass_dict:
            if answer == 'MAKE PASSWORD':
                usage = input("What is this password for? ").upper()
                password = input("what would that password be? ")
                make_password(usage, password)
            # ^ saves usage, password and then generates key to encrypt password
            elif answer == 'LOOK FOR PASSWORD':
                pass_dict = check_file()
                search_account = input("What account is this password for? ").upper()
                if search_account in pass_dict:
                    enc_password = pass_dict.get(search_account)
                    with open('secret.key', "r") as f:
                        key_dict = json.loads(f.read())
                    key = key_dict.get(search_account)
                    key = key.encode("utf-8")
                    enc_password = enc_password.encode("utf-8")
                    c = Fernet(key)
                    password = c.decrypt(enc_password)
                    print(f"The password for {search_account} is {password}")
                else:
                    print("Sorry, we can't find such name.")
            # ^ checks if usage is in the dict inside the password saved file. if it is then grab
            # password. Does the same for the file containing keys. encodes both password and key and
            # decrypt ( also the problem)
            elif answer == 'VIEW ALL PASSWORDS':
                pass_dict = check_file()
                for keys in pass_dict:
                    enc_password = pass_dict[keys]
                    with open('secret.key', "r") as f:
                        key_dict = json.loads(f.read())
                    key = key_dict[keys]
                    f = Fernet(key)
                    password = f.decrypt(enc_password)
                    print(f"{keys}: {password}")
                    print("\n")
            # ^ decrypts passwords with keys and displays all passwords with their usage
            elif answer == 'DELETE PASSWORD':
                pass_dict = check_file()
                with open('secret.key', "r") as f:
                    key_dict = json.loads(f.read())
                usage = input("What account or purpose is this password for? ").upper()
                if usage in pass_dict:
                    del pass_dict[usage]
                    with open('passwords.json', 'w') as f:
                        json.dump(pass_dict, f)
                    del key_dict[usage]
                    with open('secret.key', 'w') as f:
                        json.dump(key_dict, f)
                    print("\nThe password has been deleted")
            # deletes section in dictionaries for passwords and keys
        else:
            usage = input("What is this password for? ").upper()
            password = input("what would that password be? ")
            make_password(usage, password)
        # if there is no file detected then forces a new password to be made


    prompt = "\nIf you want to make another new password, type 'Make password'."
    prompt += "\nIf you want to look for a password, type 'Look for password'.\n"
    prompt += "If you want to view all your passwords, type 'View all passwords'.\n"
    prompt += "if you want to delete a password, type 'Delete password'.\n\n"
    answer = input(prompt).upper()

    assignment()

    continue_or_leave = input("\nDo you wish to exit? 'no' or 'yes'. ").upper()

    if continue_or_leave == "YES":
        manage_on = False