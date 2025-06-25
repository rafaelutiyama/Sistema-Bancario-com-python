saldo = 0.0;
contador = 0

def deposito():

  global saldo
  dep = float(input("Quanto deseja deporsitar: "))
  if dep < 1:
    while dep < 1:
      dep = float(input("Digite um valor valido."))
  saldo += dep
  print(f"Deposito de R${dep: .2f} feito com sucesso.\n")
  print("-----------------------------------------")

def saque():

  global saldo
  global contador

  if contador >=3:
    print("Limite de saques diarios atingidos.")
    return

  saq = float(input("Quanto deseja sacar: "))

  if saq > 500:
    while saq > 500:
      saq = float(input("Digite um valor de no max R$500,00."))
  if saq < 1:
    while saq < 1:
      saq = float(input("Digite um valor de no positiva (maior que R$1,00)."))

  if(saq > saldo):
    print("Saldo insuficiente.")
    return
  else:
    print(f"Saque de {saq: .2f} realizado com sucesso.")
    saldo -= saq
    contador += 1
  print("\n-----------------------------------------")


def extrato():

  print(f"Seu saaldo atual é de R${saldo: .2f}.")
  print("\n-----------------------------------------")


while True:

  opcao = int(input('''
---------------------------------------
Digite o que deseja fazer:
1 para deposito:
2 para saque:
3 para ver extrato
0 para interromper
Escolha:
  '''))

  if opcao == 1:
    deposito()
  elif opcao ==2:
    saque()
  elif opcao == 3:
    extrato()
  elif opcao == 0:
    print("Programa encerrado.")
    break
  else:
    print("Opcao invalida.")

