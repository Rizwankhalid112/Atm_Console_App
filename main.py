import sys
import os
import datetime
from data_manager import DataManager
from admin_controller import AdminDashboard
from models import User, Admin
from auth import Auth
from dotenv import load_dotenv

load_dotenv()

class ATMSystem:
    def __init__(self):
        self.db = DataManager()
        self.admin_panel = AdminDashboard(self.db)
        
        self.master_user = os.getenv("MASTER_ADMIN_USER")
        self.master_pass = os.getenv("MASTER_ADMIN_PASS")

    def run(self):
        while True:
            print("\n" + "=" * 30 + "\n  ATM CONSOLE APPLICATION  \n" + "=" * 30)
            print("1. Admin Login\n2. User Login\n3. Exit")
            choice = input("Select: ").strip()
            if choice == "1": self.handle_admin_login()
            elif choice == "2": self.handle_user_login()
            elif choice == "3": sys.exit()

    def handle_admin_login(self):
        """
        Handles Admin authentication.
        Checks against Master credentials (from .env) first, then JSON database.
        """
        user = input("Admin Username (or 0 to Back): ").strip()
        if user == "0": return
        pwd = input("Admin Password: ")

        if user == self.master_user and pwd == self.master_pass:
            admin_obj = Admin("A01", "System Admin", self.master_pass)
            self.admin_panel.show_menu(admin_obj)
            return

     
        admins_data = self.db.load_data(self.db.admins_file)
        hashed_input = Auth.hash_password(pwd)
        
        for a_id, info in admins_data.items():
            if info.get('name') == user and info.get('password') == hashed_input:
                admin_obj = Admin(a_id, info['name'], info['password'])
                self.admin_panel.show_menu(admin_obj)
                return
        
        print("Access Denied: Incorrect Admin credentials.")

    def handle_user_login(self):
        u_id = input("User ID (or 0 to Back): ").strip()
        if u_id == "0": return
        pin = input("Password: ")
        users_data = self.db.load_data(self.db.users_file)

        
        if u_id in users_data and users_data[u_id]['password'] == Auth.hash_password(pin):
            data = users_data[u_id]
            user_obj = User(u_id, data['name'], data['password'], data['balance'],
                            data.get('withdrawal_limit', 50000), data.get('transfer_limit', 100000))
            user_obj.transactions = data.get('transactions', [])
            self.show_user_dashboard(user_obj)
        else:
            print("Login Failed.")

    def show_user_dashboard(self, user):
        while True:
            print(f"\n--- Welcome, {user.name} ---\n1. Profile\n2. Withdraw\n3. Deposit\n4. Transfer\n5. History\n6. Logout")
            choice = input("Choice: ").strip()
            if choice == "1": 
                print(f"ID: {user.account_id} | Bal: {user.balance} | Transfer Limit: {user.transfer_limit}")
            elif choice == "2":
                try:
                    if user.withdraw(float(input("Amount: "))): self.update_user_file(user)
                except ValueError: print("Invalid amount.")
            elif choice == "3":
                try:
                    if user.deposit(float(input("Amount: "))): self.update_user_file(user)
                except ValueError: print("Invalid amount.")
            elif choice == "4": self.handle_transfer(user)
            elif choice == "5":
                m = {"1": 7, "2": 30, "3": 90}
                p = input("1. 7 Days\n2. 30 Days\n3. 90 Days\nSelect: ")
                if p in m: user.view_history(m[p])
            elif choice == "6": break

    def handle_transfer(self, user):
        """Logic for funds transfer between users with limit and ID validation."""
        try:
            target_id = input("Recipient ID (or 0 to Cancel): ").strip()
            if target_id == "0": return
            amt = float(input("Amount to Transfer: "))
            
            if amt > user.transfer_limit:
                print(f"Error: Your transfer limit is {user.transfer_limit}."); return
            
            users_data = self.db.load_data(self.db.users_file)
            
            if target_id in users_data and user.withdraw(amt):
              
                users_data[target_id]['balance'] += amt
                users_data[target_id]['transactions'].append({
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "type": "Transfer Received", "amount": amt, "note": f"From {user.name}"
                })
              
                self.update_user_file(user)
                self.db.save_data(users_data, self.db.users_file)
                print(f"Transfer Successful! {amt} sent to {users_data[target_id]['name']}.")
            else: 
                print("Error: Target ID not found or insufficient balance.")
        except ValueError: 
            print("Error: Please enter a valid numeric value for the amount.")

    def update_user_file(self, user):
        """Syncs the current user object state back to the JSON database."""
        all_users = self.db.load_data(self.db.users_file)
        all_users[user.account_id] = {
            "name": user.name, "password": user.password, "balance": user.balance,
            "transactions": user.transactions,
            "withdrawal_limit": user.withdrawal_limit, "transfer_limit": user.transfer_limit
        }
        self.db.save_data(all_users, self.db.users_file)

if __name__ == "__main__":
    
    ATMSystem().run()