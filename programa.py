from time import sleep
from datetime import datetime
def menu_inicial():
    print(f'''
======= Banco Batista Campos =======
    [1] Saque
    [2] Depósito
    [3] Extrato
    [4] Sair
====================================
''')

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
tempo = datetime.now().strftime("%d-%m-%Y %H:%M")

while True:
    menu_inicial()
    opcao = int(input("Digite a operação que deseja realizar: ").strip())
    
    if opcao == 1:
        saque = float(input("\nQuanto deseja sacar?"))
        sleep(1)
        if numero_saques<=3:
            if saque < 0:
                print("\nDigite um valor positivo")
                sleep(1)
            elif saque <= saldo:
                if saque > 500 and saque > 0:
                    print("\nNão foi possivel realizar a operação. Limite de saque: R$500.00")
                    sleep(1)
                    input("\nAperte Enter para voltar ao menu")
                else:
                    print("\nSaque realizado com sucesso. Retire o dinheiro no caixa")
                    extrato += f"\n{tempo} SAQUE    R$ {saque:.2f}"
                    saldo -= saque
                    numero_saques += 1
                    sleep(1)
                    input("\nAperte Enter para voltar ao menu")
            else:
                print(f"\nSaldo insuficiente para o saque desejado. Seu saldo é R$ {saldo:.2f}")
                sleep(1)
                input("\nAperte Enter para voltar ao menu")
        else:
            print("\nNúmero de saques diários excedido. Limite de saques: 3")
            sleep(1)
    elif opcao == 2:
        deposito = float(input("\nQuanto deseja depositar?"))
        extrato += f"\n{tempo} DEPÓSITO R$ {deposito:.2f}"
        saldo += deposito
        sleep(1)
        print(f"\nDepósito de R${deposito:.2f} realizado com sucesso")
        sleep(1)
        input("\nAperte Enter para voltar ao menu")
    elif opcao == 3:
        sleep(1)
        print(f"\nExtrato do mês:{extrato}")
        print(f"\n                   SALDO: R$ {saldo:.2f}")
        sleep(1)
        input("\nAperte Enter para voltar ao menu")
    elif opcao == 4:
        print("\nObrigado por utilizar nosso banco!")
        sleep(1)
        break
    else:
        print("\nDigite uma opção válida")
        sleep(1)
