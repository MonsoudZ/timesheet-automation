from config_manager import ConfigManager
import getpass

def main():
    print("Please enter your credentials to save them securely.")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    master_password = getpass.getpass("Enter a master password to encrypt your credentials: ")
    confirm_master = getpass.getpass("Confirm master password: ")
    
    if master_password != confirm_master:
        print("Master passwords do not match!")
        return
    
    config = ConfigManager()
    config.save_credentials(username, password, master_password)
    print("\nCredentials saved successfully!")
    print("Keep your master password safe - you'll need it to run the automation script.")

if __name__ == "__main__":
    main() 