menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


while True:

    opcoes = input(menu)
    
    match opcoes:
        case "1":  #Depositar
            valor = float(input("informe o valor do depósito: "))
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                print("Deposito realizado com sucesso")
            else:
                print("Valor inválido")
        case "2":  #Saque
            valor = float(input("informe o valor do saque: "))
            if valor > 0 and valor <= saldo and numero_saques < LIMITE_SAQUES and valor <= limite:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print("Saque realizado com sucesso")
            else:
                print("Saldo indisponivel")
                  
        case "3":  #Extrato
            print("\n========== EXTRATO BANCARIO ==========")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("===============================")
        case "4": #Sair
            break

    
    
    

    

