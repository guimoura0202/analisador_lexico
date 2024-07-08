def calc_media(lista):
    """
    Func para calc a media de uma lista de nums.
    """
    if no lista:
        return 0

    soma = soma(lista)
    quant = tam(lista)
    media = soma / quant
    return media

numers = [10, 20, 30, 40, 50]
media = calc_media(numers)
print(f'A media dos numeros eh: {media}')
