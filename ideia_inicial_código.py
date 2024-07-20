def calcular_media(vetor):
    """Função para calcular a média dos valores em um vetor."""
    return sum(vetor) / len(vetor) if vetor else 0

def girar_esquerda():
    """Função para simular a ação de girar à esquerda."""
    print("Girando à esquerda")

def girar_direita():
    """Função para simular a ação de girar à direita."""
    print("Girando à direita")

def analisar_vetor(vetor, limite_inferior, limite_lateral):
    """Função para analisar as médias das partes do vetor."""
    tamanho = len(vetor)
    if tamanho < 3:
        print("Vetor muito pequeno para análise")
        return

    tercio = tamanho // 3

    while True:
        parte_esquerda = vetor[:tercio]
        parte_central = vetor[tercio:2*tercio]
        parte_direita = vetor[2*tercio:]

        media_esquerda = calcular_media(parte_esquerda)
        media_central = calcular_media(parte_central)
        media_direita = calcular_media(parte_direita)

        print(f"Média Esquerda: {media_esquerda}, Média Central: {media_central}, Média Direita: {media_direita}")

        if media_central <= limite_inferior:
            break

        if media_direita > limite_lateral:
            girar_esquerda()

        if media_esquerda > limite_lateral:
            girar_direita()
