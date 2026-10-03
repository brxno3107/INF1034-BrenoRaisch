OPERADORES = ["+", "-", "*", "/"]
def lerEntrada(mensagem):
    return input(mensagem).strip()

def converterNumero(texto):
    try:
        return float(texto)
    except ValueError:
        return None

def calcular(valorA, operador, valorB):
    if operador == "+":
        return valorA + valorB
    if operador == "-":
        return valorA - valorB
    if operador == "*":
        return valorA * valorB
    if valorB == 0:
        return None
    return valorA / valorB

def formatarResultado(valor):
    if valor == int(valor):
        return str(int(valor))
    return str(valor)
##########################################################
def main():
    memoria = None
    operadorPendente = None
    print("Calculadora (digite 'sair' para encerrar)")
    while 1==1:
        if memoria is None or operadorPendente is not None:
            mensagem = "Insira o número: "
        else:
            mensagem = "Insira a operação: "
        entrada = lerEntrada(mensagem)
        if entrada.lower() == "sair":
            break

        if entrada in OPERADORES:
            if memoria is None:
                print("Digite um número antes do operador.")
                continue
            operadorPendente = entrada
            continue

        numero = converterNumero(entrada)
        if numero is None:
            print("Entrada inválida. Use números ou +, -, *, /.")
            continue

        if memoria is None or operadorPendente is None:
            memoria = numero
            print(f"RESULTADO: {formatarResultado(memoria)}")
            continue

        resultado = calcular(memoria, operadorPendente, numero)
        operadorPendente = None
        if resultado is None:
            print("Erro: Eh impossivel dividir por zero")
            continue
        print(f"RESULTADO: {formatarResultado(resultado)}")
        print("################################################")
        memoria = resultado


if __name__ == "__main__":
    main()
