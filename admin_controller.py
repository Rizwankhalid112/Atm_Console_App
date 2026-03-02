import datetime
from auth import Auth

class AdminDashboard:
    def __init__(self, data_manager):
        self.db = data_manager

    def show_menu(self, current_admin):
        while True:
            is_master = (current_admin.name == "System Admin")
            print(f"\n--- Admin Panel (Logged in as: {current_admin.name}) ---")
            
            menu_options = ["1. Manage Users"]
            if is_master:
                menu_options.append("2. Manage Admins")
            
            offset = 0 if is_master else -1
            print("\n".join(menu_options))
            print(f"{3+offset}. View Transactions\n{4+offset}. Delete History\n{5+offset}. Change Passwords\n{6+offset}. Logout")
            
            choice = input("Select (or 0 to Go Back): ").strip()

            if choice == "1": 
                self.manage_users_menu()
            elif is_master and choice == "2": 
                self.manage_admins_menu(current_admin)
            elif choice == str(3 + offset): 
                self.view_transactions_menu() 
            elif choice == str(4 + offset): 
                self.delete_transactions_logic()
            elif choice == str(5 + offset): 
                self.change_password_logic(current_admin)
            elif choice in [str(6 + offset), "0"]: 
                break

    def manage_users_menu(self):
        users = self.db.load_data(self.db.users_file)
        print("\n1. Create\n2. Update\n3. Delete\n4. View All\n5. Search\n6. Set Limits\n0. Back")
        sub = input("Selection: ").strip()
        if sub == "0": return

        if sub == "1":
            try:
                val = input("New ID (Numeric, or 0 to Cancel): ").strip()
                if val == "0": return
                u_id = int(val) 
                if str(u_id) in users:
                    print("Error: ID exists.")
                    return
                name = input("Name: ")
                raw_pass = input("Password: ")
                users[u_id] = {
                    "name": name, "password": Auth.hash_password(raw_pass), 
                    "balance": 0.0, "transactions": [],
                    "withdrawal_limit": 50000.0, "transfer_limit": 100000.0
                }
                print(f"User {name} created successfully.")
            except ValueError:
                print("Error: ID must be a numeric integer.")
        elif sub == "2":
            u_id = input("ID to Update: ").strip()
            if u_id in users:
                users[u_id]["name"] = input("New Name: ")
                users[u_id]["password"] = Auth.hash_password(input("New Pass: "))
        elif sub == "3":
            u_id = input("ID to Delete: ").strip()
            users.pop(u_id, None)
        elif sub == "4":
            for uid, info in users.items():
                print(f"ID: {uid} | Name: {info['name']} | Bal: {info['balance']}")
        elif sub == "5":
            search = input("Search: ").strip().lower()
            for uid, info in users.items():
                if search in uid or search in info['name'].lower():
                    print(f"Match Found -> ID: {uid} | Name: {info['name']} | Balance: {info['balance']}")
        elif sub == "6":
            u_id = input("ID: ").strip()
            if u_id in users:
                try:
                    users[u_id]["withdrawal_limit"] = float(input("New Withdraw-Limit: "))
                    users[u_id]["transfer_limit"] = float(input("New Transfer-Limit: "))
                except ValueError: print("Numeric values only.")
        
        self.db.save_data(users, self.db.users_file)

    def manage_admins_menu(self, current_admin):
        admins = self.db.load_data(self.db.admins_file)
        print("\n1. Create Admin\n2. View All Admins\n3. Delete Admin\n0. Back")
        sub = input("Selection: ").strip()
        if sub == "0": return

        if sub == "1":
            try:
                a_id = int(input("New ID: ").strip())
                if str(a_id) in admins or a_id == "A01":
                    print("Error: ID exists.")
                    return
                name = input("Name: ")
                raw_pass = input("Password: ")
                admins[a_id] = {"name": name, "password": Auth.hash_password(raw_pass)}
                print(f"Admin {name} created.")
            except ValueError: print("Numeric ID required.")
        elif sub == "2":
            print("ID: A01 | Name: System Admin")
            for aid, info in admins.items():
                print(f"ID: {aid} | Name: {info['name']}")
        elif sub == "3":
            if current_admin.name != "System Admin":
                print("Permission Denied.")
                return
            a_id = input("ID to delete: ").strip()
            if a_id != "A01": admins.pop(a_id, None)
            
        self.db.save_data(admins, self.db.admins_file)

    def view_transactions_menu(self):
        users = self.db.load_data(self.db.users_file)
        print("\n1. All Transactions\n2. Specific User Transactions\n0. Back")
        choice = input("Selection: ")
        if choice == "1":
            for uid, data in users.items():
                for tx in data.get('transactions', []):
                    print(f"User ID: {uid} | {tx['date']} | {tx['type']} | {tx['amount']}")
        elif choice == "2":
            uid = input("User ID: ").strip()
            if uid in users:
                for tx in users[uid].get('transactions', []):
                    print(tx)
            else:
                print("User not found.")

    def delete_transactions_logic(self):
        uid = input("User ID to clear: ").strip()
        users = self.db.load_data(self.db.users_file)
        if uid in users:
            users[uid]['transactions'] = []
            self.db.save_data(users, self.db.users_file)
            print("History cleared.")

    def change_password_logic(self, current_admin):
        print("\n1. Change My Password\n2. Change Others (System Admin Only)\n0. Back")
        choice = input("Choice: ").strip()
        if choice == "0": return

        if choice == "1":
            new_p = input("New Password: ").strip()
            admins = self.db.load_data(self.db.admins_file)
            if current_admin.name == "System Admin":
                print("Update via .env file.")
            elif current_admin.account_id in admins:
                admins[current_admin.account_id]["password"] = Auth.hash_password(new_p)
                self.db.save_data(admins, self.db.admins_file)
                print("Password updated.")

        elif choice == "2":
            if current_admin.name != "System Admin":
                print("ACCESS DENIED.") 
                return
            target = input("Target (1. User / 2. Admin): ").strip()
            t_id = input("Enter ID: ").strip()
            new_p = Auth.hash_password(input("Enter New Password: "))
            if target == "1":
                data = self.db.load_data(self.db.users_file)
                if t_id in data: 
                    data[t_id]["password"] = new_p
                    self.db.save_data(data, self.db.users_file)
            else:
                data = self.db.load_data(self.db.admins_file)
                if t_id in data: 
                    data[t_id]["password"] = new_p
                    self.db.save_data(data, self.db.admins_file)