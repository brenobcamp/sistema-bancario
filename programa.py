from time import sleep
from datetime import datetime
from traceback import print_tb
from textwrap import dedent

def menu_inicial():
    print(f'''
======= Banco Batista Campos =======
    [1] Saque
    [2] Depósito
    [3] Extrato
    [4] Novo Usuário
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair
====================================
''')
    return int(input("Digite a operação que deseja realizar: ").strip())
def saque(*, saldo, valor, extrato, numero_saques, tempo):
    if numero_saques<=3:
        if valor < 0:
            print("\nDigite um valor positivo")
            sleep(1)
        elif valor <= saldo:
            if valor > 500:
                print("\nNão foi possivel realizar a operação. Limite de saque: R$500.00")
                sleep(1)
                input("\nAperte Enter para voltar ao menu")
            else:
                print("\nSaque realizado com sucesso. Retire o dinheiro no caixa")
                extrato += f"\n{tempo} SAQUE    R$ {valor:.2f}"
                saldo -= valor
                numero_saques += 1
                sleep(1)
                input("\nAperte Enter para voltar ao menu")
                return saldo, extrato, numero_saques
        else:
            print(f"\nSaldo insuficiente para o saque desejado. Seu saldo é R$ {saldo:.2f}")
            sleep(1)
            input("\nAperte Enter para voltar ao menu")
    else:
        print("\nNúmero de saques diários excedido. Limite de saques: 3")
        sleep(1)
def deposito(saldo, valor, extrato, tempo, /):
    extrato += f"\n{tempo} DEPÓSITO R$ {valor:.2f}"
    saldo += valor
    sleep(1)
    print(f"\nDepósito de R${valor:.2f} realizado com sucesso")
    sleep(1)
    input("\nAperte Enter para voltar ao menu")
    return saldo, extrato
def exibir_extrato(saldo, /, *, extrato):
    sleep(1)
    print(f"\nExtrato:")
    print("Não foram realizadas operações" if not extrato else extrato)
    print(f"\n                   SALDO: R$ {saldo:.2f}")
    sleep(1)
    input("\nAperte Enter para voltar ao menu")
def criar_usuario(usuarios):
    cpf = input("\nDigite seu CPF (Somente números): ").replace(".","").replace("-","").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\nCPF já cadastrado!")
        sleep(1)
        input("Aperte Enter para voltar ao menu")
        return
    
    print("Cadastro de novo usuário. Digite as informações necessárias:")
    nome = input("\nNome completo: ").strip().capitalize()
    data_nascimento = input("\nData de nascimento (formato DD-MM-AAAA): ").strip()
    endereco =input("\nEndereço (Logradouro, NR, Bairro, Cidade/Sigla Estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Criando usuário ........ ")
    sleep(2)
    print(" Usuário criado com sucesso!")
    input("Aperte Enter para voltar ao menu")
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return  usuarios_filtrados[0] if usuarios_filtrados else None
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    sleep(1)
    if usuario:
        print("\nConta criada com sucesso!")
        input("Aperte Enter para voltar ao menu")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\nUsuário não encontrado. Conta não pode ser criada.")
    input("Aperte Enter para voltar ao menu")
def listar_contas(contas):
    if contas:
        for conta in contas:
            linha = f"""\
                Agência:\t{conta["agencia"]}
                CC:\t\t{conta["numero_conta"]}
                Titular:\t{conta["usuario"]["nome"]}
                """
            print("="*100)
            print(dedent(linha))
            input("Aperte Enter para voltar ao menu")
    else:
        print("\nNão há contas para listar. Crie uma nova conta no nosso banco!")
        input("Aperte Enter para voltar ao menu")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    AGENCIA = "0001"
    tempo = datetime.now().strftime("%d-%m-%Y %H:%M")
    usuarios = []
    contas = []

    while True:
        opcao = menu_inicial()
        if opcao == 1:
            valor_saque = float(input("\nQuanto deseja sacar?"))
            saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor_saque, extrato=extrato,numero_saques=numero_saques, tempo=tempo)
        elif opcao == 2:
            valor_deposito = float(input("\nQuanto deseja depositar?"))
            saldo, extrato = deposito(saldo, valor_deposito, extrato, tempo)
        elif opcao == 3:
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == 4:
            criar_usuario(usuarios)
        elif opcao == 5:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == 6:
            listar_contas(contas)
        elif opcao == 7:
            print("\nObrigado por utilizar nosso banco!")
            sleep(1)
            break
        else:
            print("\nDigite uma opção válida")
            sleep(1)

main()