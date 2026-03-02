import datetime
from auth import Auth

class AdminDashboard:
    def __init__(self, data_manager):
        self.db = data_manager

    def show_menu(self, current_admin):
        while True:
            print(f"\n--- Admin Panel (Logged in as: {current_admin.name}) ---")
            print("1. Manage Users\n2. Manage Admins\n3. View Transactions\n4. Delete History\n5. Change Passwords\n6. Logout")
            choice = input("Select (or 0 to Go Back): ").strip()
            if choice == "1": self.manage_users_menu()
            elif choice == "2": self.manage_admins_menu()
            elif choice == "3": self.view_transactions_menu()
            elif choice == "4": self.delete_transactions_logic()
            elif choice == "5": self.change_password_logic(current_admin)
            elif choice in ["6", "0"]: break

    def manage_users_menu(self):
        users = self.db.load_data(self.db.users_file)
        print("\n1. Create\n2. Update\n3. Delete\n4. View All\n5. Search\n6. Set Limits\n0. Back")
        sub = input("Selection: ").strip()
        if sub == "0": return

        if sub == "1":
            u_id = input("New ID (or 0 to Cancel): ").strip()
            if u_id == "0": return
            if u_id in users:
                print(f"Error: User ID '{u_id}' already exists.")
                return
            name = input("Name: ")
            raw_pass = input("Password: ")
            users[u_id] = {
                "name": name, "password": Auth.hash_password(raw_pass), 
                "balance": 0.0, "transactions": [],
                "withdrawal_limit": 50000.0, "transfer_limit": 100000.0
            }
            print(f"User {name} created successfully.")
            
        elif sub == "4": 
            print("\n--- Registered Users ---")
            for uid, info in users.items():
                print(f"ID: {uid} | Name: {info['name']} | Balance: {info['balance']}")

        elif sub == "5": 
            search = input("Enter ID or Name to Search: ").strip()
            found = False
            for uid, info in users.items():
                if search.lower() in uid.lower() or search.lower() in info['name'].lower():
                    print(f"Match Found -> ID: {uid} | Name: {info['name']} | Bal: {info['balance']}")
                    found = True
            if not found: print("No matching user found.")

        elif sub == "6":
            u_id = input("User ID (or 0 to Cancel): ").strip()
            if u_id in users:
                try:
                    users[u_id]["withdrawal_limit"] = float(input("New Withdrawal Limit: "))
                    users[u_id]["transfer_limit"] = float(input("New Transfer Limit: "))
                except ValueError: print("Numeric values only.")
        
        self.db.save_data(users, self.db.users_file)

    def manage_admins_menu(self):
        admins = self.db.load_data(self.db.admins_file)
        print("\n1. Create Admin\n2. View All Admins\n3. Delete Admin\n0. Back")
        sub = input("Selection: ").strip()
        if sub == "0": return

        if sub == "1":
            a_id = input("New Admin ID (or 0 to Cancel): ").strip()
            if a_id in admins or a_id == "A01":
                print("Error: Admin ID already exists.")
                return
            name = input("Name: ")
            raw_pass = input("Password: ")
            admins[a_id] = {"name": name, "password": Auth.hash_password(raw_pass)}
            print(f"Admin {name} created successfully.")

        elif sub == "2": 
            print("\n--- Registered Admins ---")
            print("ID: A01 | Name: System Admin") 
            for aid, info in admins.items():
                print(f"ID: {aid} | Name: {info['name']}")
            
        elif sub == "3":
            a_id = input("ID to delete (or 0 to Cancel): ").strip()
            if a_id != "A01": admins.pop(a_id, None)
            
        self.db.save_data(admins, self.db.admins_file)

    def view_transactions_menu(self): 
        users = self.db.load_data(self.db.users_file)
        print("\n1. View All Transactions\n2. View Specific User Transactions\n0. Back")
        choice = input("Selection: ").strip()
        
        if choice == "1":
            for uid, data in users.items():
                for tx in data.get('transactions', []):
                    print(f"User: {uid} | {tx['date']} | {tx['type']} | {tx['amount']} | {tx.get('note', '')}")
        elif choice == "2":
            uid = input("Enter User ID: ").strip()
            if uid in users:
                for tx in users[uid].get('transactions', []):
                    print(f"{tx['date']} | {tx['type']} | {tx['amount']} | {tx.get('note', '')}")
            else: print("User not found.")

    def delete_transactions_logic(self): 
        uid = input("User ID to clear history (or 0 to Cancel): ").strip()
        if uid == "0": return
        users = self.db.load_data(self.db.users_file)
        if uid in users:
            users[uid]['transactions'] = []
            self.db.save_data(users, self.db.users_file)
            print(f"Transaction history for ID {uid} has been cleared.")

    def change_password_logic(self, current_admin): 
        print("\n1. Change My Password\n2. Change Others (System Admin Only)\n0. Back")
        choice = input("Choice: ").strip()
        if choice == "0": return

        if choice == "1":
            new_p = input("New Password: ").strip()
            admins = self.db.load_data(self.db.admins_file)
            if current_admin.account_id in admins:
                admins[current_admin.account_id]["password"] = Auth.hash_password(new_p)
                self.db.save_data(admins, self.db.admins_file)
                print("Your password has been updated.")
            elif current_admin.account_id == "A01":
                print("Note: Master Admin password is controlled via .env file.")

        elif choice == "2" and current_admin.name == "System Admin":
            target = input("Target (1. User / 2. Admin / 0. Back): ").strip()
            if target == "0": return
            t_id = input("Enter ID: ").strip()
            new_p = input("Enter New Password: ").strip()
            hashed_p = Auth.hash_password(new_p)

            if target == "1":
                data = self.db.load_data(self.db.users_file)
                if t_id in data: 
                    data[t_id]["password"] = hashed_p
                    self.db.save_data(data, self.db.users_file)
                    print("User password updated.")
            elif target == "2":
                data = self.db.load_data(self.db.admins_file)
                if t_id in data: 
                    data[t_id]["password"] = hashed_p
                    self.db.save_data(data, self.db.admins_file)
                    print("Admin password updated.")