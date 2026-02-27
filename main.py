import sys
import datetime
from data_manager import DataManager
from admin_controller import AdminDashboard
from models import User, Admin


class ATMSystem:
    def __init__(self):
        self.db = DataManager()
        self.admin_panel = AdminDashboard(self.db)

    def run(self):
        while True:
            print("\n" + "=" * 30 + "\n  ATM CONSOLE APPLICATION  \n" + "=" * 30)
            print("1. Admin Login\n2. User Login\n3. Exit")
            choice = input("Select: ").strip()
            if choice == "1":
                self.handle_admin_login()
            elif choice == "2":
                self.handle_user_login()
            elif choice == "3":
                sys.exit()

    def handle_admin_login(self):
        """
        Handles Admin authentication from both hardcoded and file data.
        Ensures the code does not break if a user is not found.
        """
        username = input("Admin Username: ")
        password = input("Admin Password: ")

        # 1. First, check the Master Admin (Source 15)
        if username == "admin" and password == "1234":
            admin_obj = Admin("A01", "System Admin", "1234")
            self.admin_panel.show_menu(admin_obj)
            return

        # 2. Check for other Admins in the storage file (Source 18, 33)
        admins_data = self.db.load_data(self.db.admins_file)

        # We loop through the dictionary to find a match (Source 3)
        admin_found = False
        for a_id, info in admins_data.items():
            if info.get('name') == username and info.get('password') == password:
                admin_obj = Admin(a_id, info['name'], info['password'])
                admin_found = True
                self.admin_panel.show_menu(admin_obj)
                break

        if not admin_found:
            # Source 32: Well prompted error message for security
            print("Access Denied: Incorrect Admin credentials.")

    def handle_user_login(self):
        u_id, pin = input("User ID: "), input("Password: ")
        users_data = self.db.load_data(self.db.users_file)

        if u_id in users_data and users_data[u_id]['password'] == pin:
            data = users_data[u_id]
            # FIX: Load limits from JSON instead of defaults
            user_obj = User(
                u_id, data['name'], data['password'], data['balance'],
                data.get('withdrawal_limit', 50000),
                data.get('transfer_limit', 100000)
            )
            user_obj.transactions = data.get('transactions', [])
            self.show_user_dashboard(user_obj)
        else:
            print("Login Failed.")

    def show_user_dashboard(self, user):
        while True:
            print(
                f"\n--- Welcome, {user.name} ---\n1. Profile\n2. Withdraw\n3. Deposit\n4. Transfer\n5. History\n6. Logout")
            choice = input("Choice: ").strip()

            if choice == "1":
                print(f"ID: {user.account_id} | Bal: {user.balance} | Transfer Limit: {user.transfer_limit}")
            elif choice == "2":
                try:
                    if user.withdraw(float(input("Amount: "))): self.update_user_file(user)
                except ValueError:
                    print("Invalid amount.")
            elif choice == "3":
                try:
                    if user.deposit(float(input("Amount: "))): self.update_user_file(user)
                except ValueError:
                    print("Invalid amount.")
            elif choice == "4":
                self.handle_transfer(user)
            elif choice == "5":
                m = {"1": 7, "2": 30, "3": 90}
                p = input("1. 7 Days\n2. 30 Days\n3. 90 Days\nSelect: ")
                if p in m: user.view_history(m[p])
            elif choice == "6":
                break

    # Part of handle_transfer in main.py
    def handle_transfer(self, user):
        """
        Handles funds transfer with specific error messages for
        limit violations, invalid recipients, and low balance.
        """
        try:
            target_id = input("Recipient ID: ")
            amt = float(input("Amount to Transfer: "))

            # 1. Check against the limit set by Admin (Source 30)
            if amt > user.transfer_limit:
                print(f"Error: Transfer denied. Your limit is {user.transfer_limit}.")
                return

            # Load the most recent data to check recipient
            users_data = self.db.load_data(self.db.users_file)

            # 2. Check if Recipient exists (Requirement: Search User)
            if target_id not in users_data:
                print(f"Error: Receiver ID '{target_id}' not found. Please check the ID.")
                return

            # 3. Check if Sender has enough money (Requirement: Edge Cases)
            if amt > user.balance:
                print(f"Error: Insufficient balance. Your current balance is {user.balance}.")
                return

            # If all checks pass, proceed with the transfer logic (Source 23)
            if user.withdraw(amt):
                # Update recipient's balance and transaction history
                users_data[target_id]['balance'] += amt
                users_data[target_id]['transactions'].append({
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "type": "Transfer Received",
                    "amount": amt,
                    "note": f"From {user.name}"
                })

                # Sync both accounts to the file storage (Source 33)
                self.update_user_file(user)
                self.db.save_data(users_data, self.db.users_file)
                print(f"Transfer Successful! {amt} sent to {users_data[target_id]['name']}.")

        except ValueError:
            # Source 32: Well prompted error message for invalid data types
            print("Error: Invalid input. Please enter a numeric value for the amount.")

    def update_user_file(self, user):
        all_users = self.db.load_data(self.db.users_file)
        all_users[user.account_id] = {
            "name": user.name, "password": user.password, "balance": user.balance,
            "transactions": user.transactions,
            "withdrawal_limit": user.withdrawal_limit,
            "transfer_limit": user.transfer_limit
        }
        self.db.save_data(all_users, self.db.users_file)


if __name__ == "__main__":
    ATMSystem().run()