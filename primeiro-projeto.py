def depositar(valor, saldo, extrato):
            if valor > 0 :
                saldo += valor
                extrato += f"Depósito: R${valor:.2f}\n"
                print(f"Depósito no valor de R${valor:.2f} realizado com sucesso.\n")
            else:
                print("Erro:Valor inválido.")
            
            return saldo, extrato

def sacar(saldo, valor, limite, extrato, saques, LIMITE_DE_SAQUE):
        sem_saldo = valor > saldo
        sem_limite = valor > limite
        sem_limite_de_saque = saques >= LIMITE_DE_SAQUE
        if sem_saldo:
            print ("Saldo insuficiente.\n")
        elif sem_limite:
            print("Limite insuficiente.\n")
        elif sem_limite_de_saque:
            print("Voce excedeu seu limite de saque diário.\n")
        elif valor > 0:
            saldo -= valor
            limite -= valor
            saques += 1
            extrato += f"Saque: R${valor:.2f}\n"
            print(f"Saque no valor de R${valor:.2f} realizado com sucesso.\n")
        else:
            print("Erro: Valor inválido.")


        return saldo, limite, saques , extrato


def exibir_extrato(saldo, limite, extrato):
    print("EXTRATO\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo disponível: R${saldo:.2f}. Limite disponível: R${limite:.2f}")


def lin():
     print("-"*30)



menu = """
                Bem vindo(a)!
[1] = deposito
[2] = saque
[3] = extrato
[4] = sair
Digite aqui sua opção => 
"""

saldo = 0
limite = 500
LIMITE_DE_SAQUE = 3
saques = 0
extrato = ""

while True :
    opcao = input(menu)

    if opcao == "1":
        lin()
        valor =  float(input("Digite o valor do depósito =>"))
        saldo, extrato = depositar(valor, saldo, extrato)
        lin()

    elif opcao == "2":
        lin()
        valor = float(input("Digite o valor do saque => "))
        saldo, limite, saques, extrato = sacar(saldo, valor, limite, extrato, saques, LIMITE_DE_SAQUE)
        lin()

    elif opcao == "3":
        lin()
        exibir_extrato(saldo, limite, extrato)
        lin()
    elif opcao == "4":
        break

    else:
        lin()
        print("Opção inválida.Tente novamente.")
        lin()
    
        
        