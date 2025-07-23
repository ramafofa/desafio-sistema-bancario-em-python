from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
class Cliente:
     def __init__(self,endereco):
          self.endereco = endereco
          self.contas = []

     def realizar_transacao(self,conta,transacao):
          transacao.registrar(conta)

     def adicionar_conta(self,conta):
          self.contas.append(conta)

class PessoaFisica(Cliente):
     def __init__(self, nome, data_nascimento, cpf, endereco):
          super().__init__(endereco)
          self.nome = nome
          self.data_nascimento = data_nascimento
          self.cpf = cpf

class Conta:
        def __init__(self, numero, cliente):
            self.saldo = 0
            self.numero = numero
            self.cliente = cliente
            self.agencia = "12345"
            self.historico = Historico()

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
             saldo = self.saldo
             sem_saldo_suficiente = valor > saldo

             if sem_saldo_suficiente:
                  print("Saldo insuficiente.")    
            
             elif valor > 0:
                  self.saldo -= valor
                  print(f"Saque no valor de {valor} realizado com sucesso")
                  return True

             else:
                  print("ERRO:Valor inválido.")
                  return False


        def depositar(self, valor):
            if valor > 0 :
                self.saldo += valor
                print(f"Depósito no valor de R${valor:.2f} realizado com sucesso.")
                return True
            else:
                print("ERRO:Valor inválido.")
                return False
            
          
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
         super().__init__(numero, cliente)
         self.limit = limite
         self.limite_saques = limite_saques

    def sacar(self,valor):
         numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

         sem_limite = valor > self.limite
         sem_limite_saques = numero_saques > self.limite_saques

         if sem_limite:
              print("Limite insufisciente--Nao autorizado.")

         elif sem_limite_saques:
              print("Limite de saque excedido--Nao autorizado.")
        
         else:
            return super().sacar(valor)
         
         return False
    
    def __str__(self):
         return f"""\
            Agencia:{self.agencia}
            CC:{self.numero}
            Titular:{self.cliente.nome}
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
                    "tipo": transacao.__class__.__name__,
                    "valor": transacao.valor,
                    "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
               }
            )
    
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass   
     
class Saque(Transacao):
     def __init__(self,valor):
          self._valor =  valor

     @property
     def valor(self):
          return self._valor
     def registrar(self, conta):
          transacao_aprovada = conta.sacar(self.valor)

          if transacao_aprovada:
               conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
     def __init__(self, valor):
          self._valor = valor
     
     @property
     def valor(self):
          return self._valor
     
     def registrar(self, conta):
         transacao_aprovada = conta.depositar(self.valor)

         if transacao_aprovada:
               conta.historico.adicionar_transacao(self)


def menu():
     menu = """\n
    =============MENU=============
    [1]DEPOSITAR
    [2]SACAR
    [3]EXTRATO
    [4]NOVA CONTA
    [5]LISTAR CONTAS
    [6]NOVO USUÁRIO
    [7]SAIR
    DIGITE SUA OPÇAO =>"""
     return input((menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("SALDO INSUFICIENTE.")

    elif excedeu_limite:
        print("LIMITE INSUFICIENTE")

    elif excedeu_saques:
        print("LIMITE DE SAQUE EXCEDIDO")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"SAQUE NO VALOR DE R${valor:.2f} REALIZADO COM SUCESSO.")

    else:
        print("ERRO:VALOR INVÁLIDO.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuário já existe.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Usuário não encontrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()