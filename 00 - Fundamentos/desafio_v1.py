from abc import ABC, abstractmethod
from datetime import datetime, date

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta) -> None:
        ...


    @property
    @abstractmethod
    def valor(self) -> float:
        ...


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        conta.saldo = conta.saldo + self._valor
        conta.historico.adicionar_transacao(self)
        print(f"Depósito de {self._valor} realizado com sucesso")

    @property
    def valor(self):
        return self._valor

  # Saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if conta.saldo >= self._valor:
            conta.saldo = conta.saldo - self._valor
            conta.historico.adicionar_transacao(self)
            print(f"Saque de {self._valor} realizado com sucesso")
        else:
            print("Saldo Insuficiente!")

    @property
    def valor(self):
        return self._valor

# Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

# Conta
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(cliente=cliente, numero=numero)
    
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Valor de saque inválido.")
            return False
        if self.saldo >= valor:
            saque = Saque(valor)
            saque.registrar(self)
            return True
        print("Saldo Insuficiente!")
        return False

    def depositar(self, valor:float) -> bool:
        if valor <= 0:
            print("Valor de depósito inválido.")
            return False
        deposito = Deposito(valor)
        deposito.registrar(self)
        return True

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        self._saldo = valor

    @property
    def historico(self) -> "Historico":
        return self._historico


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=1000.0, limite_saques=3, agencia="0001"):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Valor de saque inválido.")
            return False
        if valor > self.limite:
            print("Valor excede o limite por saque.")
            return False
        numero_saques = sum(1 for t in self.historico.transacoes if isinstance(t, Saque))
        if numero_saques >= self.limite_saques:
            print("Limite de saques atingido.")
            return False
        return super().sacar(valor)

class Cliente:
    def __init__ (self, endereco):
        self._endereco = endereco
        self._contas = []

    def adicionar_conta(self, conta:Conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    @property
    def contas(self):
        return self._contas

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        if isinstance(data_nascimento, date):
            self._data_nascimento = data_nascimento
        else:
            try:
                self._data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
            except Exception:
                self._data_nascimento = None
        
        
        