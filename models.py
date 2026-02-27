import datetime


class Account:
    """Base class to demonstrate Inheritance."""

    def __init__(self, account_id, name, password):
        self.account_id = account_id
        self.name = name
        self.password = password


class Admin(Account):
    """Fulfills Admin capabilities."""

    def __init__(self, account_id, name, password):
        super().__init__(account_id, name, password)


class User(Account):
    """Fulfills User capabilities."""

    def __init__(self, user_id, name, password, balance=0.0, w_limit=50000, t_limit=100000):
        super().__init__(user_id, name, password)
        self.balance = balance
        self.withdrawal_limit = w_limit
        self.transfer_limit = t_limit
        self.transactions = []  #

    def add_transaction(self, tx_type, amount, note=""):
        entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "type": tx_type,
            "amount": amount,
            "note": note
        }
        self.transactions.append(entry)

    def withdraw(self, amount):
        """Logic for withdrawal with edge cases and limits."""
        if amount <= 0:
            print("Error: Invalid amount.")
            return False
        if amount > self.withdrawal_limit:
            print(f"Error: Amount exceeds your withdrawal limit of {self.withdrawal_limit}.")
            return False
        if amount > self.balance:
            print("Error: Insufficient balance.")
            return False

        self.balance -= amount
        self.add_transaction("Withdrawal", amount)
        print(f"Success! New balance: {self.balance}")
        return True

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction("Deposit", amount)
            print(f"Success! {amount} deposited. New balance: {self.balance}")
            return True
        print("Error: Deposit amount must be positive.")
        return False

    def view_history(self, days):
        """List comprehension for selective history."""
        today = datetime.datetime.now()
        filtered = [
            t for t in self.transactions
            if (today - datetime.datetime.strptime(t['date'], "%Y-%m-%d")).days <= days
        ]
        if not filtered:
            print(f"No transactions found in the last {days} days.")
        else:
            print(f"\n--- History (Last {days} Days) ---")
            for t in filtered:
                print(f"{t['date']} | {t['type']}: {t['amount']} {t['note']}")