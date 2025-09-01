import textwrap  # Importa o módulo textwrap para manipulação de strings

# Função para exibir o menu de opções e capturar a escolha do usuário
def menu():
    # Define o menu de opções
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    # Exibe o menu e retorna a opção escolhida pelo usuário
    return input(textwrap.dedent(menu))


# Função para realizar depósito
def depositar(saldo, valor, extrato, /):
    # Verifica se o valor do depósito é positivo
    if valor > 0:
        saldo += valor  # Adiciona o valor ao saldo
        extrato += f"Depósito:\tR$ {valor:.2f}\n"  # Registra o depósito no extrato
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retorna o saldo e extrato atualizados
    return saldo, extrato


# Função para realizar saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # Verifica se o valor do saque excede o saldo
    excedeu_saldo = valor > saldo
    # Verifica se o valor do saque excede o limite permitido
    excedeu_limite = valor > limite
    # Verifica se o número de saques excedeu o limite diário
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor  # Subtrai o valor do saldo
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"  # Registra o saque no extrato
        numero_saques += 1  # Incrementa o número de saques
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retorna o saldo e extrato atualizados
    return saldo, extrato


# Função para exibir o extrato bancário
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    # Exibe mensagem caso não haja movimentações
    print("Não foram realizadas movimentações." if not extrato else extrato)
    # Exibe o saldo atual
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    # Verifica se já existe usuário com o CPF informado
    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Adiciona o novo usuário à lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


# Função para filtrar usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    # Retorna o primeiro usuário encontrado com o CPF informado ou None
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


# Função para criar uma nova conta bancária
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    # Verifica se o usuário existe
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        # Retorna o dicionário da conta criada
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


# Função para listar todas as contas cadastradas
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


# Função principal do programa
def main():
    LIMITE_SAQUES = 3  # Limite diário de saques
    AGENCIA = "0001"   # Número da agência

    saldo = 0  # Saldo inicial
    limite = 500  # Limite de saque
    extrato = ""  # Extrato inicial
    numero_saques = 0  # Contador de saques
    usuarios = []  # Lista de usuários
    contas = []  # Lista de contas

    # Loop principal do programa
    while True:
        opcao = menu()  # Exibe o menu e captura a opção

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1  # Gera o número da conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break  # Encerra o programa

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()  # Executa a função principal