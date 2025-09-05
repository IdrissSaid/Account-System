import os
import json

class AccountManager:
    def __init__(self, data_file="account_data.json"):
        self.data_file = data_file
        self.balance = self._load_balance()
    
    def _load_balance(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    return data.get('balance', 1000.0)
            except (json.JSONDecodeError, IOError):
                pass
        return 1000.0  # Default initial balance
    
    def _save_balance(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump({'balance': self.balance}, file)
            return True
        except IOError:
            return False
    
    def get_balance(self):
        return self.balance
    
    def credit_account(self, amount):
        if amount <= 0:
            return False, "Le montant doit être supérieur à zéro."
        
        self.balance += amount
        self._save_balance()
        return True, f"Compte crédité de {amount:.2f}. Nouveau solde: {self.balance:.2f}"
    
    def debit_account(self, amount):
        if amount <= 0:
            return False, "Le montant doit être supérieur à zéro."
        
        if amount > self.balance:
            return False, "Fonds insuffisants."
        
        self.balance -= amount
        self._save_balance()
        return True, f"Compte débité de {amount:.2f}. Nouveau solde: {self.balance:.2f}"
