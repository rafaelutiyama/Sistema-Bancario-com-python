from datetime import date, timedelta, datetime
import json
import os

# === Configurações e constantes ===
PASTA_USUARIOS = "usuarios_json"
os.makedirs(PASTA_USUARIOS, exist_ok=True)

LIMITE_SAQUE = 500.0
LIMITE_SAQUES_DIARIOS = 3
LIMITE_TRANSACAO_DIARIO = 10

# Variáveis globais
conta = None
nome_usuario = None

# === Funções auxiliares ===
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

def salvar_usuario():
    global conta, nome_usuario
    if conta and nome_usuario:
        caminho = os.path.join(PASTA_USUARIOS, f"usuario_{nome_usuario}.json")
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(conta, f, ensure_ascii=False, indent=4)

# === Funções principais ===
def deposito():
    if conta["transacoes"] >= LIMITE_TRANSACAO_DIARIO:
        print("❌ Limite de transações diárias atingido.\n")
        return

    valor = ler_float("💰 Quanto deseja depositar? R$ ", minimo=1)
    conta["saldo"] += valor
    conta["transacoes"] += 1
    conta["extrato"].append(f"Depósito: +R${valor:.2f},  {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    salvar_usuario()
    print(f"✅ Depósito de R${valor:.2f} realizado com sucesso!\n")

def saque():
    if conta["saques"] >= LIMITE_SAQUES_DIARIOS:
        print("❌ Limite diário de saques atingido.\n")
        return

    if conta["transacoes"] >= LIMITE_TRANSACAO_DIARIO:
        print("❌ Limite de transações diárias atingido.\n")
        return

    valor = ler_float("💸 Quanto deseja sacar? R$ ", minimo=1, maximo=LIMITE_SAQUE)

    if valor > conta["saldo"]:
        print("❌ Saldo insuficiente.\n")
        return

    conta["saldo"] -= valor
    conta["saques"] += 1
    conta["transacoes"] += 1
    conta["extrato"].append(f"Saque:    -R${valor:.2f},  {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    salvar_usuario()
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

# === Cadastro e login ===
def criar_conta():
    nome = input("Digite o nome do novo usuário: ").strip().lower()
    caminho = os.path.join(PASTA_USUARIOS, f"usuario_{nome}.json")


    cpf = input("Digite seu CPF: ").strip().lower()

    if os.path.exists(caminho):
        print(f"⚠️ O usuário '{nome}' já existe!\n")
        return

    # Verifica se CPF já está cadastrado em qualquer arquivo na pasta
    for arquivo in os.listdir(PASTA_USUARIOS):
        if arquivo.endswith(".json"):
            caminho_arquivo = os.path.join(PASTA_USUARIOS, arquivo)
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if dados.get("cpf") == cpf:
                    print(f"⚠️ O CPF '{cpf}' já está cadastrado!\n")
                    return

    senha = input("Crie uma senha para sua conta: ").strip()
    conta_nova = {
        "nome": nome,
        "senha": senha,
        "cpf": cpf,
        "saldo": 0.0,
        "saques": 0,
        "transacoes": 0,
        "extrato": [],
        "data_ultimo_reset": datetime.today().strftime("%Y-%m-%d")
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(conta_nova, f, ensure_ascii=False, indent=4)
    print(f"✅ Usuário '{nome}' criado com sucesso!\n")


def login():
    global conta, nome_usuario
    nome = input("Digite o nome do usuário: ").strip().lower()
    caminho = os.path.join(PASTA_USUARIOS, f"usuario_{nome}.json")

    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        senha_digitada = input("Digite sua senha: ").strip()

        if senha_digitada == dados.get("senha"):
            conta = dados
            nome_usuario = nome
            print(f"✅ Login realizado! Bem-vindo(a), {nome}!\n")
            verificar_reset_diario()
            lista()
        else:
            print("❌ Senha incorreta.\n")
    else:
        print("❌ Usuário não encontrado. Crie uma conta primeiro.\n")


def verificar_reset_diario():
    global conta
    if conta is None:
        return

    data_salva = conta.get("data_ultimo_reset")
    data_hoje = datetime.today().strftime("%Y-%m-%d")

    if data_salva != data_hoje:
        conta["saques"] = 0
        conta["transacoes"] = 0
        conta["data_ultimo_reset"] = data_hoje
        salvar_usuario()


def lista():
    while True:
        try:
            opcao = int(input('''
=============================
🏦 BANCO DIGITAL - MENU
1️⃣  Despositar
2️⃣  Sacar
3️⃣  Extrato
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


# === Menu principal ===
def menu():
    while True:
        try:
            opcao = int(input('''
=============================
🏦 BANCO DIGITAL - MENU
1️⃣  Login
2️⃣  Criar conta
3️⃣  Sair
Escolha uma opção: '''))
            print()
            if opcao == 1:
                login()
            elif opcao == 2:
                criar_conta()
            elif opcao == 3:
                print("👋 Programa encerrado. Obrigado por usar nosso sistema!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.\n")
        except ValueError:
            print("❌ Entrada inválida. Digite um número.\n")

# === Iniciar o programa ===
menu()
