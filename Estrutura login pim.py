import json

admin = False
ACCOUNTS_FILE = "JSONN.jsonl"

def loadAccounts():
    try:
        with open(ACCOUNTS_FILE, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Arquivo '{ACCOUNTS_FILE}' não encontrado. Criando um novo.")
        return []
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON '{ACCOUNTS_FILE}'. Verifique a formatação.")
        return []

def saveAccounts(accounts):
    try:
        with open(ACCOUNTS_FILE, 'w') as file:
            json.dump(accounts, file, indent=4)
        print("Contas salvas com sucesso.")
    except IOError:
        print(f"Erro ao escrever no arquivo '{ACCOUNTS_FILE}'.")

def userFileExists(username):
    accounts = loadAccounts()
    for account in accounts:
        if account.get("username") == username:
            return True
    return False

def authenticate(username, password):
    accounts = loadAccounts()
    for account in accounts:
        if account.get("username") == username and account.get("password") == password:
            print(f"Login bem-sucedido para o usuário: {username}")
            return True
    print("Nome de usuário ou senha incorretos.")
    return False

def login():
    print("\n--- Login ---")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")
    authenticate(username, password)

def listAccounts():
    print("\n--- Lista de Contas ---")
    accounts = loadAccounts()
    if not accounts:
        print("Nenhuma conta registrada.")
        return
    for account in accounts:
        print(f"Nome de Usuário: {account.get('username')}")

def addAccount():
    print("\n--- Adicionar Nova Conta ---")
    username = input("Digite o novo nome de usuário: ")
    if userFileExists(username):
        print("Este nome de usuário já existe. Escolha outro.")
        return
    password = input("Digite a senha para o novo usuário: ")
    accounts = loadAccounts()
    accounts.append({"username": username, "password": password})
    saveAccounts(accounts)
    print(f"Conta para o usuário '{username}' criada com sucesso.")

def firstMenu():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Login")
        print("2. Listar Contas")
        print("3. Adicionar Conta")
        print("4. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            login()
        elif choice == '2':
            listAccounts()
        elif choice == '3':
            addAccount()
        elif choice == '4':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    firstMenu()

if __name__ == "__main__":
    main()
