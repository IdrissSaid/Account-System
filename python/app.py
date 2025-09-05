from account_manager import AccountManager

def display_menu():
    print("\n=== Application de Gestion de Compte ===")
    print("1. Afficher le solde")
    print("2. Créditer le compte")
    print("3. Débiter le compte")
    print("4. Quitter")
    return input("Choisissez une option (1-4): ")

def get_amount():
    while True:
        try:
            amount = float(input("Entrez le montant: "))
            if amount < 0:
                print("Le montant ne peut pas être négatif.")
                continue
            return amount
        except ValueError:
            print("Veuillez entrer un montant valide.")

def main():
    account = AccountManager()

    while True:
        choice = display_menu()

        match choice:
            case "1":
                balance = account.get_balance()
                print(f"Solde actuel: {balance:.2f}")
            case "2":
                amount = get_amount()
                success, message = account.credit_account(amount)
                print(message)
            case "3":
                amount = get_amount()
                success, message = account.debit_account(amount)
                print(message)
            case "4":
                print("Merci d'avoir utilisé l'application. Au revoir!")
                break
            case _:
                print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
