def calcular_media(lista_numeros):
    """
    Função para calcular a média de uma lista de números.
    """
    if not lista_numeros:
        return 0

    soma = sum(lista_numeros)
    quantidade = len(lista_numeros)
    media = soma / quantidade
    return media

numeros = [10, 20, 30, 40, 50]
media = calcular_media(numeros)
print(f'A média dos números é: {media}')
