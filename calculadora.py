import os, sqlite3, time
from tabulate import tabulate

db = sqlite3.connect("precoTeto.db")
db.execute('''
    CREATE TABLE IF NOT EXISTS precoTeto(
           id INTEGER PRIMARY KEY AUTOINCREMENT, nm_acao TEXT, vl_acao DECIMAL, qt_papeis INTEGER, vl_yieldMinimo DECIMAL,
           vl_payout DECIMAL, vl_lucroProjetivo DECIMAL, vl_lpa DECIMAL, vl_precoTeto DECIMAL, vl_margemSeguranca REAL
           )
           ''')

def exibe_relatorio(dados):
    cabecalho = ["Ticker", "Cotação", "Qtde de Papéis", "Yield Min", "Payout", "Lucro Proj.", "LPA", "Preço-Teto", "Margem de Segurança"]

    if isinstance(dados, tuple):
        dados = [dados]

    print(tabulate(dados, headers=cabecalho, floatfmt=".2f", tablefmt="fancy_grid"))
    print("\n")
    input("Aperte qualquer tecla para voltar para o menu inicial")
    return


def calcular():
    os.system('cls')
    print("Você escolheu Calcular Novo Preço-Teto\n")

    ticker = input("Digite o ticker da ação: ").upper()
    precoAtual = float(input("Digite o valor da cotação atual da ação: R$"))
    qtdePapeis = int(input("Entre com a sua quantidade de papéis emitidos: "))
    lucroProjetivo = float(input("Digite o lucro projetivo anual da empresa: R$"))
    payout = float(input("Digite o payout da empresa (não digite em porcentagem): ")) / 100
    yieldMinimo = float(input("Digite o yield mínimo desejado (não digite em porcentagem): ")) / 100

    lpa = lucroProjetivo / qtdePapeis
    dpa = lpa * payout
    precoTeto = dpa / yieldMinimo
    margemSeguranca = ((precoTeto - precoAtual) / precoTeto) * 100

    db.execute("INSERT INTO precoTeto VALUES(NULL,?,?,?,?,?,?,?,?,?)",(ticker, precoAtual, qtdePapeis, yieldMinimo, payout, lucroProjetivo, lpa, precoTeto, margemSeguranca))
    db.commit()
    print("\nPreço-teto adicionado \n")

    input("Aperte qualquer tecla para continuar")
    time.sleep(2)

def relatorio():
    os.system('cls')
    cursor = db.cursor()
    escolha = input("Deseja ver o relátorio de uma ação específica? [s]im ou [n]ão: ").lower().startswith('s')
    if escolha:
        acao = input("Digite o ticker da ação desejada: ").upper()
        cursor.execute("SELECT * FROM precoTeto WHERE nm_acao = ?",(acao,))
        resultado = cursor.fetchone()

        if resultado:
            print("Exibindo as informações da ação escolhida...")
            exibe_relatorio(resultado)
            return
        else:
            print("Nenhum registro encontrado!!! Retornando para o menu principal...")
            time.sleep(5)
            return
        
    else:
        cursor.execute("SELECT * FROM precoTeto")
        dados = cursor.fetchall()
        if len(dados) == 0:
            print("Nenhum registro encontrado!!! Retornando para o menu principal...")
            time.sleep(5)
            return
        else:
            exibe_relatorio(dados)
            return
    

while True:
    os.system("cls")
    print("--- MENU DE OPÇÕES ---")
    print("1 - Calcular Novo Preço-Teto")
    print("2 - Relátorio")
    print("3 - Atualizar Preço-Teto")
    print("4 - Excluir Preço-Teto")
    print("5 - Encerrar Programa")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        calcular()
    elif opcao == 2:
        relatorio()
    else:
        db.close()
        break