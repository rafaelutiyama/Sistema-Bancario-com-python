from datetime import date, timedelta
from datetime import datetime

# Constantes
LIMITE_SAQUE = 500.0
LIMITE_SAQUES_DIARIOS = 3
LIMITE_TRANSACAO_DIARIO = 10

# Estado da conta
conta = {
    "saldo": 0.0,
    "saques": 0,
    "transacoes": 0,
    "extrato": []
}

# Função auxiliar para ler número com validação
def ler_float(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = float(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"⚠️ Valor mínimo permitido: R${minimo:.2f}")
            elif maximo is not None and valor > maximo:
                print(f"⚠️ Valor máximo permitido: R${maximo:.2f}")
            else:
                return valor
        except ValueError:
            print("❌ Entrada inválida. Digite um número válido.")

# Funções principais
def deposito():
    if conta["transacoes"] >= LIMITE_TRANSACAO_DIARIO:
        print("❌ Limite de transações diárias atingido.\n")
        print(f"Próximo saque disponível em: {date.today() + timedelta(days=1)}")
        return

    valor = ler_float("💰 Quanto deseja depositar? R$ ", minimo=1)
    conta["saldo"] += valor
    conta["transacoes"] += 1
    conta["extrato"].append(f"Depósito: +R${valor:.2f},  {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✅ Depósito de R${valor:.2f} realizado com sucesso!\n")

def saque():
    if conta["saques"] >= LIMITE_SAQUES_DIARIOS:
        print("❌ Limite diário de saques atingido.\n")
        return

    if conta["transacoes"] >= LIMITE_TRANSACAO_DIARIO:
        print("❌ Limite de transações diárias atingido.\n")
        print(f"Próximo saque disponível em: {date.today() + timedelta(days=1)}")
        return

    valor = ler_float("💸 Quanto deseja sacar? R$ ", minimo=1, maximo=LIMITE_SAQUE)

    if valor > conta["saldo"]:
        print("❌ Saldo insuficiente.\n")
        return

    conta["saldo"] -= valor
    conta["saques"] += 1
    conta["transacoes"] += 1
    conta["extrato"].append(f"Saque:    -R${valor:.2f},  {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✅ Saque de R${valor:.2f} realizado com sucesso!\n")

def extrato():
    print("\n📄 === EXTRATO ===")
    if not conta["extrato"]:
        print("Nenhuma movimentação realizada.")
    else:
        for transacao in conta["extrato"]:
            print(transacao)
    print(f"\nSaldo atual: R${conta['saldo']:.2f}")
    print(f"Saques feitos hoje: {conta['saques']}/{LIMITE_SAQUES_DIARIOS}")
    print(f"Transações feitas hoje: {conta['transacoes']}/{LIMITE_TRANSACAO_DIARIO}")
    print("=========================\n")

# Loop principal
def menu():
    while True:
        try:
            opcao = int(input('''
=============================
🏦 BANCO DIGITAL - MENU
1️⃣  Depositar
2️⃣  Sacar
3️⃣  Ver Extrato
0️⃣  Sair
Escolha uma opção: '''))
            print()
            if opcao == 1:
                deposito()
            elif opcao == 2:
                saque()
            elif opcao == 3:
                extrato()
            elif opcao == 0:
                print("👋 Programa encerrado. Obrigado por usar nosso sistema!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.\n")
        except ValueError:
            print("❌ Entrada inválida. Digite um número.\n")

# Executar o programa
menu()
