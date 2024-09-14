# Password-Manager
The source code is above but the actual exe with required files are in the release section. 

The compressed file in release contains 9 files that are used in the process of decrypting and encrypting data, and a folder with python files containing modules used and what not.

When you open the program, you will be prompted to create a password. This is the password that you will be using to log into the program. After creating a password, you will be given two codes.

The first code is a recovery code. You will be asked to save this somewhere safe. This is basically your back up password, so do not lose it.

The second code is a key. This key is the key that you will need to input in order to decrypt the information you save into the program. You will be asked to save this somewhere safe. DO NOT LOSE THIS.

When it came to creating this program, I came across a few obstacles, one being key storing. When the program reads in your password, it opens up a file that has your password saved as encrypted.
It will decrypt it and see if they match. Now, in the process of this, it also grabs the key to decrypt your password from another file (one of the nine files). Now this creates a slight issue.
Your key and encrypted password are saved in a file, which could pose as a threat. Now it would mean that someone would have to somehow gain access to your computer, look for the files, decrypt it,
and then find your password. Though, it is still an issue and its in return for convenience so that you dont have to manually input a key everytime, just to login for your login password.

So if this is a possibility, then where is the security? This is where the key that is given comes in. All the usernames and passwords you save into your password manager are encrypted and decrypted
with said key. This key must be manually inputted into the program to correctly view and edit your passwords. "Isn't this what you just said you didnt want to do?" you might be asking. Yes, but no.
It would not seem worth it to input a key for the password login because at that point, I should just make the user input a key instead of a password. By making it that you have to input a key for your
actual collection of passwords would seem more worth it. In a way, this is a two factor authenication. Someone *could* gain access to your login info, but without that key to access your actual passwords,
it is pointless to try to break in. The only place this key can be found is where you hide it. So hide it carefully.

Another note on the key, make sure you input the correct key or nothing will be displayed.

The rest is pretty self-explanatory. You can add passwords, view passwords, or delete them.

As 9/13/24, I have not added sufficient comments to the source code so for now, do what you will.

