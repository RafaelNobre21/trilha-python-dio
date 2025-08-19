menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo usuário
[5] Nova conta
[6] Listar contas
[7] Sair

=> """

AGENCIA = "0001"

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso.")
    else:
        print("Valor de depósito inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if valor <= 0:
        print("Valor de saque inválido.")
    elif excedeu_saldo:
        print("Saldo insuficiente.")
    elif excedeu_limite:
        print("Valor do saque excede o limite por operação.")
    elif excedeu_saques:
        print("Número máximo de saques diários atingido.")
    else:
        saldo -= valor
        extrato += f"Saque:    R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO BANCARIO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato, end="")
    print(f"\nSaldo:   R$ {saldo:.2f}")
    print("======================================")

def filtrar_usuario(cpf, usuarios):
    cpf = "".join(filter(str.isdigit, cpf or ""))
    usuarios_filtrados = [u for u in usuarios if u["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números ou com máscara): ")
    cpf = "".join(filter(str.isdigit, cpf or ""))
    if not cpf:
        print("CPF inválido.")
        return

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Já existe usuário cadastrado com esse CPF.")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    print("Informe o endereço no formato: logradouro, nro - bairro - cidade/UF")
    endereco = input("Endereço: ").strip()

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
    })
    print("Usuário cadastrado com sucesso.")

def cadastrar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado. Cadastre o usuário antes de criar a conta.")
        return None

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
    }
    print(f"Conta criada com sucesso. Agência: {agencia} | Nº Conta: {numero_conta} | Titular: {usuario['nome']}")
    return conta

def listar_contas(contas):
    if not contas:
        print("Não há contas cadastradas.")
        return
    print("\n========== CONTAS ==========")
    for conta in contas:
        titular = conta["usuario"]["nome"]
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {titular}")
    print("============================")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    usuarios = []
    contas = []

    while True:
        opcoes = input(menu)

        match opcoes:
            case "1":  # Depositar
                try:
                    valor = float(input("Informe o valor do depósito: "))
                except ValueError:
                    print("Valor inválido.")
                    continue
                saldo, extrato = depositar(saldo, valor, extrato)

            case "2":  # Sacar
                try:
                    valor = float(input("Informe o valor do saque: "))
                except ValueError:
                    print("Valor inválido.")
                    continue
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )

            case "3":  # Extrato
                exibir_extrato(saldo, extrato=extrato)

            case "4":  # Novo usuário
                cadastrar_usuario(usuarios)

            case "5":  # Nova conta
                conta = cadastrar_conta(AGENCIA, len(contas) + 1, usuarios)
                if conta:
                    contas.append(conta)

            case "6":  # Listar contas
                listar_contas(contas)

            case "7":  # Sair
                break

            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

    
    
    

    

