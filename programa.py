from calendar import c
from time import sleep
from datetime import datetime
from traceback import print_tb
from textwrap import dedent
from abc import ABC, abstractmethod, abstractproperty

class Cliente():
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    @property
    def cpf(self):
        return self._cpf
    @property
    def nome(self):
        return self._nome
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):  
        saldo = self._saldo
        if valor < 0:
            print("\nDigite um valor positivo")
            sleep(1)
            return False
        elif valor <= saldo:
            if valor > 500:
                print("\nNão foi possivel realizar a operação. Limite de saque: R$500.00")
                sleep(1)
                input("\nAperte Enter para voltar ao menu")
                return False
            else:
                print("\nSaque realizado com sucesso. Retire o dinheiro no caixa")
                self._saldo -= valor
                sleep(1)
                input("\nAperte Enter para voltar ao menu")
                return True
        else:
            print(f"\nSaldo insuficiente para o saque desejado. Seu saldo é R$ {saldo:.2f}")
            sleep(1)
            input("\nAperte Enter para voltar ao menu")
            return False

    def depositar(self, valor):
        if valor > 0:    
            self._saldo += valor
            print("\nDeposito realizado com sucesso!")
            sleep(1)
            input("\nAperte Enter para voltar ao menu")
            return True
        else:
            print("\nOperação falhou. Informe um número positivo")
            sleep(1)
            return False

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saques=3, limite=500):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques = 0
    @property
    def limite_por_saque(self):
        return self._limite
    @property
    def limite_diario_saques(self):
        return self._limite_saques
    @property
    def nr_saques(self):
        return self._saques
    @property
    @nr_saques.setter
    def nr_saques(self, valor):
        self._saques += valor
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excedeu o limite")
        elif excedeu_saques:
            print("\nOperação falhou! Número de saques diário excedido")
        else: 
            return super().sacar(valor)
        return False
    def __str__(self):
        return f"""
                Agência: {self.agencia}
                Conta: {self.numero}
                Titular: {self.cliente.nome}
                """

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
       
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now(),
            }
        )
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


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
def main():
    clientes = []
    contas = []
    while True:
        opcao = menu_inicial()
        if opcao == 1:
            saque(clientes)
        elif opcao == 2:
            deposito(clientes)
        elif opcao == 3:
            exibir_extrato(clientes)
        elif opcao == 4:
            criar_cliente(clientes)
        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == 6:
            listar_contas(contas)
        elif opcao == 7:
            print("\nObrigado por utilizar nosso banco!")
            sleep(1)
            break
        else:
            print("\nDigite uma opção válida")
            sleep(1)




def saque(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return
    valor = float(input("\nInforme o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def deposito(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return
    valor = float(input("\nInforme o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui contas")
        return
    return cliente.contas[0]
def exibir_extrato(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print(f"\nExtrato:")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas transações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo: \n\tR$ {conta.saldo:.2f}")
    input("\nAperte Enter para voltar ao menu")

def criar_cliente(clientes):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    print("Cadastro de novo usuário. Digite as informações necessárias:")
    nome = input("\nNome completo: ").strip().capitalize()
    data_nascimento = input("\nData de nascimento (formato DD-MM-AAAA): ").strip()
    endereco =input("\nEndereço (Logradouro, NR, Bairro, Cidade/Sigla Estado): ")
    
    cliente = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nascimento=data_nascimento)
    clientes.append(cliente)

    print("Criando usuário ........ ")
    sleep(2)
    print(" Usuário criado com sucesso!")
    input("Aperte Enter para voltar ao menu")
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente._cpf == cpf]
    return  clientes_filtrados[0] if clientes_filtrados else None
def criar_conta(numero_conta, clientes, contas):
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\nConta criada com sucesso!")
    input("Aperte Enter para voltar ao menu")

def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(dedent(str(conta)))
        input("Aperte Enter para voltar ao menu")

main()