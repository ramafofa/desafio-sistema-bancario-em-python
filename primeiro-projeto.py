menu = """
                Bem vindo(a)!
[1] = deposito
[2] = saque
[3] = extrato
[4] = sair
Digite aqui sua opção=>
"""
saldo = 0
limite = 500
LIMITE_DE_SAQUE = 3
saques = 0
extrato = ""

while True :
    opcao = input(menu)
    if opcao == "1" :
        valor = float(input("Digite o valor do depósito =>"))
        if valor > 0 :
            saldo += valor
            extrato += f"Deposito no valor de R${valor:.2f} realizado com sucesson.\n"
        else:
            print("Erro:Valor inválido.")
    elif opcao == "2" :
        valor = float(input("Digite o valor do saque =>"))
        sem_saldo = valor > saldo
        sem_limite = valor > limite
        sem_limite_de_saque = saques > LIMITE_DE_SAQUE
        if sem_saldo:
            print ("Saldo insuficienete.\n")
        elif sem_limite:
            print("Limite insuficiente.\n")
        elif sem_limite_de_saque:
            print("Voce excedeu seu limite de saque diário.\n")
        elif valor > 0:
            saldo -= valor
            limite -= valor
            saques += 1
            print(f"Saque no valor de R${valor:.2f} realizado com sucesso.\n")
        else:
            print("Erro:Valor inválido.")
    elif opcao == "3":
        print("EXTRATO\n")
        print(extrato if extrato else "Não foram realizadas movimentações.")
        print(f"Saldo disponível: R${saldo:.2f}. Limite disponível: R${limite:.2f}")
    elif opcao == "4":
        break
    else:
        print("Opção inválida.Tente novamente.")
    
        
        