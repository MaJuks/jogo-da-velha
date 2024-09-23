velha = [["a1", "a2", "a3"], ["b1", "b2", "b3"], ["c1", "c2", "c3"]]
wins = [
    ["a1", "a2", "a3"],
    ["b1", "b2", "b3"],
    ["c1", "c2", "c3"],
    ["a1", "b1", "c1"],
    ["a2", "b2", "c2"],
    ["a3", "b3", "c3"],
    ["a1", "b2", "c3"],
    ["a3", "b2", "c1"],
]


def setando_game(velha, wins):
    velha_jogo = [linha[:] for linha in velha]
    wins_robo = wins[:]
    wins_user = []
    jogadas = []
    return velha_jogo, wins_robo, wins_user, jogadas


velha_jogo, wins_robo, wins_user, jogadas = setando_game(velha, wins)


def mostrar_jogo():
    for linha in velha_jogo:
        print(" | ".join(linha))
        print()
    print("Posições ocupadas: ", jogadas)


def computar_jogada(jogada):
    for linha in range(3):
        for coluna in range(3):
            if velha[linha][coluna] == jogada:
                velha_jogo[linha][coluna] = usuario
                jogadas.append(jogada)
                return


def computador():
    global jogada_robo

    def melhor_jogada(posicoes, jogador):
        contador = 0
        jogada_possivel = None
        for pos in posicoes:
            for linha in range(3):
                for coluna in range(3):
                    if velha[linha][coluna] == pos:
                        if velha_jogo[linha][coluna] == jogador:
                            contador += 1
                        elif velha_jogo[linha][coluna] not in [usuario, robo]:
                            jogada_possivel = (linha, coluna)
        return contador, jogada_possivel

    # Priorizar a vitória do robô
    for opcao in wins_robo:
        contador_robo, jogada_possivel = melhor_jogada(opcao, robo)
        if contador_robo == 2 and jogada_possivel:
            jogada_robo = jogada_possivel
            break
    else:
        # Impedir a vitória do usuário
        for opcao in wins:
            contador_usuario, jogada_possivel = melhor_jogada(opcao, usuario)
            if contador_usuario == 2 and jogada_possivel:
                jogada_robo = jogada_possivel
                break
        else:
            # Fazer a melhor jogada disponível
            for opcao in wins_robo:
                _, jogada_possivel = melhor_jogada(opcao, robo)
                if jogada_possivel and velha_jogo[jogada_possivel[0]][jogada_possivel[1]] not in [usuario, robo]:
                    jogada_robo = jogada_possivel
                    break

    # Realizar a jogada do robô
    if jogada_robo:
        velha_jogo[jogada_robo[0]][jogada_robo[1]] = robo
        jogadas.append(velha[jogada_robo[0]][jogada_robo[1]])


def ganhador():
    # Verificar se há um vencedor
    for win in wins:
        contador_usuario = 0
        contador_robo = 0
        for pos in win:
            for linha in range(3):
                for coluna in range(3):
                    if velha[linha][coluna] == pos and velha_jogo[linha][coluna] == usuario:
                        contador_usuario += 1
                    elif velha[linha][coluna] == pos and velha_jogo[linha][coluna] == robo:
                        contador_robo += 1
        if contador_usuario == 3:
            print("GANHADOR DO USUÁRIO")
            return True
        elif contador_robo == 3:
            print("GANHADOR DO ROBO")
            return True

    # Verificar se deu velha (empate)
    if all(velha_jogo[linha][coluna] in [usuario, robo] for linha in range(3) for coluna in range(3)):
        print("DEU VELHA! O jogo empatou.")
        return True

    return False


# Loop principal do jogo
print("ESCOLHA X ou O")
usuario = input().upper()
robo = "O" if usuario == "X" else "X"

while True:
    mostrar_jogo()
    jogada = input("Digite a posição: ").strip().lower()
    if jogada in jogadas:
        print("Posição já ocupada. Tente novamente.")
        continue
    computar_jogada(jogada)
    if ganhador():
        break
    computador()
    if ganhador():
        break
