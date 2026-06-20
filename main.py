import json
import os
import getpass
from cryptography.fernet import Fernet

KEY_FILE = "key.key"

MASTER_PASSWORD = "admin123"
FILE = "password.json"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return f.read()

def get_fernet():
    key = load_key()
    return Fernet(key)

def check_master_password():
    print("<*=*> Password Manager <*=*>")
    attempts = 3

    while attempts > 0:
        password = getpass.getpass("Enter Master Password: ")

        if password == MASTER_PASSWORD:
            print("Access Granted!")
            return True
        else:
            attempts -= 1
            print(f"Wrong Password! {attempts} attempts left")

    print("Too many wrong attempts! Exiting...")
    return False

def load_password():
    if not os.path.exists(FILE):
        return []
    f = get_fernet()
    with open(FILE, "rb") as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    return json.loads(decrypted.decode())
    
def save_password(passwords):
    f = get_fernet()
    data = json.dumps(passwords, indent=4).encode()
    encrypted = f.encrypt(data)
    with open(FILE, "wb") as file:
        file.write(encrypted)

def add_password():
    print("<*=*> Add Password <*=*>")
    site = input("Enter site/App name: ")
    username = input("Enter Username/Email: ")
    password = input("Enter Password: ")

    passwords = load_password()
    passwords.append({
        "site": site,
        "username": username,
        "password": password
    })

    save_password(passwords)
    print("Password saved successfully!")

def view_passwords():
    passwords = load_password()

    if not passwords:
        print("\nNo passwords saved yet!")
        return
    
    print("<*=*> All Password <*=*>")
    for i, entry in enumerate(passwords, start=1):
        print(f"\n{i}.")
        print(f"   Site     : {entry['site']}")
        print(f"   Username : {entry['username']}")
        print(f"   Password : {entry['password']}")
        print("  --------------------------")

def search_password():
    passwords = load_password()

    if not passwords:
        print("\nNo passwords saved yet!")
        return
    
    print("<*=*> Search Password <*=*>")
    keyword = input("Enter site/app name to search: ").lower()

    results = [(i, entry) for i, entry in enumerate(passwords) if keyword in entry['site'].lower()]

    if not results:
        print(f"\nNo results found for '{keyword}'")
        return
    
    print(f"Found {len(results)} result(s)")
    for i, (index, entry) in enumerate(results, start=1):
        print(f"\n{i}.")
        print(f"   Site     : {entry['site']}")
        print(f"   Username : {entry['username']}")
        print(f"   Password : {entry['password']}")
        print("  --------------------------")

def delete_password():
    passwords = load_password()

    if not passwords:
        print("\nNo passwords saved yet!")
        return
    
    print("<*=*> Delete Password <*=*>")
    keyword = input("Enter site/app name to search: ").lower()

    results = [(i, entry) for i, entry in enumerate(passwords) if keyword in entry['site'].lower()]

    if not results:
        print(f"\nNo results found for '{keyword}'")
        return
    
    print(f"Found {len(results)} result(s)")
    for i, (index, entry) in enumerate(results, start=1):
        print(f"{i}. {entry['site']} - {entry['username']}")

    try:
        choice = int(input("\nEnter number to delete (0 to cancel): "))

        if choice == 0:
            print("Deletion cancelled")
            return
        
        if choice < 1 or choice > len(results):
            print("Invalid number!")
            return
        
        original_index, entry = results[choice - 1]

        print(f"\nYou are about to delete:")
        print(f"   Site     : {entry['site']}")
        print(f"   Username : {entry['username']}")

        confirm = input("\nAre you sure? (yes/no):").lower()

        if confirm == "yes":
            passwords.pop(original_index)
            save_password(passwords)
            print(f"Password for '{entry['site']}' deleted successfully!")
        else:
            print("Deletion cancelled")

    except ValueError:
        print("Please enter a valid number!")

def menu():
    print("<*=*> Password Manager <*=*>")
    print("1. Add Password")
    print("2. View All Passwords")
    print("3. Search Password")
    print("4. Delete Password")
    print("5. Exit")
    print("=============================")

def main():

    if not check_master_password():
        return

    while True:
        menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            search_password()
        elif choice == "4":
            delete_password()
        elif choice == "5":
            print("Goodbye!")
            break
        else: 
            print("Invalid choice! please enter 1-5")

main()