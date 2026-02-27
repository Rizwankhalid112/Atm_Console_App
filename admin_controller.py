import datetime


class AdminDashboard:
    def __init__(self, data_manager):
        self.db = data_manager

    def show_menu(self, current_admin):
        """Interactable menu for admin interaction (Source 34)."""
        while True:
            print(f"\n--- Admin Panel (Logged in as: {current_admin.name}) ---")
            print("1. Manage Users ")
            print("2. Manage Admins ")
            print("3. View All/User Transactions")
            print("4. Delete Transactions")
            print("5. Change Passwords (Admin/User)")
            print("6. Logout")

            choice = input("Select action: ").strip()

            if choice == "1":
                self.manage_users_menu()
            elif choice == "2":
                self.manage_admins_menu()
            elif choice == "3":
                self.view_transactions_menu()
            elif choice == "4":
                self.delete_transactions_logic()
            elif choice == "5":
                self.change_password_logic(current_admin)
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again (Source 32).")

    def manage_users_menu(self):
        """Fulfills Source 16 & 30: User CRUD and Limits."""
        users = self.db.load_data(self.db.users_file)
        print("\n1. Create User\n2. Update User\n3. Delete User\n4. View All Users\n5. Search User\n6. Set Limits")
        sub_choice = input("Selection: ")

        if sub_choice == "1":
            u_id = input("New ID: ")
            users[u_id] = {
                "name": input("Name: "), "password": input("Pass: "),
                "balance": 0.0, "transactions": [],
                "withdrawal_limit": 50000.0, "transfer_limit": 100000.0
            }
        elif sub_choice == "2":
            u_id = input("User ID to update: ")
            if u_id in users:
                users[u_id]["name"] = input(f"New Name ({users[u_id]['name']}): ")
                users[u_id]["password"] = input("New Password: ")
        elif sub_choice == "3":
            u_id = input("User ID to delete: ")
            users.pop(u_id, None)
        elif sub_choice == "4":
            print("\n--- All Users ---")
            for uid, info in users.items():
                print(f"ID: {uid} | Name: {info['name']} | Bal: {info['balance']}")
        elif sub_choice == "5":
            search = input("Search by ID or Name: ")
            for uid, info in users.items():
                if search in uid or search in info['name']:
                    print(f"Match Found -> ID: {uid}, Name: {info['name']}")
        elif sub_choice == "6":
            u_id = input("User ID: ")
            if u_id in users:
                try:
                    users[u_id]["withdrawal_limit"] = float(input("New Withdrawal Limit: "))
                    users[u_id]["transfer_limit"] = float(input("New Transfer Limit: "))
                    print("Limits updated (Source 30).")
                except ValueError:
                    print("Error: Numeric values only (Source 32).")

        self.db.save_data(users, self.db.users_file)

    def manage_admins_menu(self):
        """Fulfills Source 18: Admin CRUD and viewing."""
        admins = self.db.load_data(self.db.admins_file)
        print("\n1. Create Admin\n2. View All Admins\n3. Delete Admin")
        sub_choice = input("Selection: ")

        if sub_choice == "1":
            a_id = input("New Admin ID: ")
            admins[a_id] = {"name": input("Name: "), "password": input("Password: ")}
        elif sub_choice == "2":
            print("\n--- Registered Admins ---")
            print("ID: A01 | Name: System Admin")  # Master Admin
            for a_id, info in admins.items():
                if a_id != "A01":
                    print(f"ID: {a_id} | Name: {info['name']}")
        elif sub_choice == "3":
            a_id = input("Admin ID to delete: ")
            if a_id != "A01":
                admins.pop(a_id, None)

        self.db.save_data(admins, self.db.admins_file)

    def view_transactions_menu(self):
        """Fulfills Source 17: View all transactions."""
        users = self.db.load_data(self.db.users_file)
        print("\n1. View All\n2. View Specific User")
        choice = input("Choice: ")
        if choice == "1":
            for uid, data in users.items():
                for tx in data.get('transactions', []):
                    print(f"User: {uid} | {tx['date']} | {tx['type']} | {tx['amount']}")
        elif choice == "2":
            uid = input("User ID: ")
            if uid in users:
                for tx in users[uid].get('transactions', []):
                    print(tx)

    def delete_transactions_logic(self):
        """Fulfills Source 19: Delete transitions."""
        uid = input("User ID to clear: ")
        users = self.db.load_data(self.db.users_file)
        if uid in users:
            users[uid]['transactions'] = []
            self.db.save_data(users, self.db.users_file)
            print("History cleared.")

    def change_password_logic(self, current_admin):
        """
        Security Rule: Only 'System Admin' can change others' passwords (Source 20).
        Others can only change their own.
        """
        print("\n1. Change My Password\n2. Change Others (System Admin Only)")
        choice = input("Choice: ")

        if choice == "1":
            new_p = input("New Password: ")
            admins = self.db.load_data(self.db.admins_file)
            # Update current session and storage
            if current_admin.account_id in admins:
                admins[current_admin.account_id]["password"] = new_p
                self.db.save_data(admins, self.db.admins_file)
            print("Password updated.")

        elif choice == "2":
            # Strict name check for the Master Admin
            if current_admin.name == "System Admin":
                target_type = input("Target (1. User / 2. Admin): ")
                t_id = input("Enter ID: ")
                new_p = input("Enter New Password: ")

                if target_type == "1":
                    data = self.db.load_data(self.db.users_file)
                    if t_id in data:
                        data[t_id]["password"] = new_p
                        self.db.save_data(data, self.db.users_file)
                        print("User password updated.")
                else:
                    data = self.db.load_data(self.db.admins_file)
                    if t_id in data:
                        data[t_id]["password"] = new_p
                        self.db.save_data(data, self.db.admins_file)
                        print("Admin password updated.")
            else:
                print("Permission Denied: Only System Admin can change other passwords.")