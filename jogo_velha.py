import tkinter as tk
from tkinter import messagebox

velha = [["a1", "a2", "a3"], ["b1", "b2", "b3"], ["c1", "c2", "c3"]]  ## TABULEIRO

wins = [
    ["a1", "a2", "a3"],
    ["b1", "b2", "b3"],
    ["c1", "c2", "c3"],
    ["a1", "b1", "c1"],
    ["a2", "b2", "c2"],
    ["a3", "b3", "c3"],
    ["a1", "b2", "c3"],
    ["a3", "b2", "c1"],
]  ## CONJUNTO DE JOGADAS QUE LEVEM A VITÓRIA


def setando_game(velha, wins):  ## FUNÇÃO PARA CONFIGURAR VARIÁVEIS DO JOGO
    velha_jogo = [linha[:] for linha in velha]
    wins_robo = wins[:]
    wins_user = []
    jogadas = []
    return velha_jogo, wins_robo, wins_user, jogadas


velha_jogo, wins_robo, wins_user, jogadas = setando_game(velha, wins)  ## CONFIGURANDO VARIÁVEIS QUE SERÃO USADAS


def mostrar_jogo():  ## FUNÇÃO PARA MOSTRAR JOGO
    for linha in range(3):
        for coluna in range(3):
            buttons[linha][coluna].config(text=velha_jogo[linha][coluna], state="normal")


def computar_jogada(jogada, linha, coluna):  ## FUNÇÃO PARA MARCAR JOGADA DO USUÁRIO
    if velha_jogo[linha][coluna] not in [usuario, robo]:
        velha_jogo[linha][coluna] = usuario
        jogadas.append(jogada)
        buttons[linha][coluna].config(text=usuario, state="disabled")  ## INTEGRAÇÃO COM INTERFACE GRÁFICA
        if ganhador():
            return
        computador()


def computador():  ## FUNCÃO PARA SIMULAR PENSAMENTO COMPUTACIONAL
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

    for opcao in wins_robo:
        contador_robo, jogada_possivel = melhor_jogada(opcao, robo)
        if contador_robo == 2 and jogada_possivel:
            jogada_robo = jogada_possivel
            break
    else:
        for opcao in wins:
            contador_usuario, jogada_possivel = melhor_jogada(opcao, usuario)
            if contador_usuario == 2 and jogada_possivel:
                jogada_robo = jogada_possivel
                break
        else:
            for opcao in wins_robo:
                _, jogada_possivel = melhor_jogada(opcao, robo)
                if jogada_possivel:
                    jogada_robo = jogada_possivel
                    break

    if jogada_robo:
        velha_jogo[jogada_robo[0]][jogada_robo[1]] = robo
        jogadas.append(velha[jogada_robo[0]][jogada_robo[1]])
        buttons[jogada_robo[0]][jogada_robo[1]].config(text=robo, state="disabled")
        ganhador()


def ganhador():
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
            messagebox.showinfo("Resultado", "Você venceu!")
            reset_jogo()
            return True
        elif contador_robo == 3:
            messagebox.showinfo("Resultado", "O robô venceu!")
            reset_jogo()
            return True

    if all(velha_jogo[linha][coluna] in [usuario, robo] for linha in range(3) for coluna in range(3)):
        messagebox.showinfo("Resultado", "Empate! Deu velha.")
        reset_jogo()
        return True

    return False


def reset_jogo():
    global velha_jogo, wins_robo, wins_user, jogadas
    velha_jogo, wins_robo, wins_user, jogadas = setando_game(velha, wins)
    mostrar_jogo()


# Interface gráfica
root = tk.Tk()
root.title("Jogo da Velha")

# Variável global para usuário e robô
usuario = None
robo = None

# Criação do tabuleiro com botões (inicialmente desativados)
buttons = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        button = tk.Button(root, text="", width=10, height=3, state="disabled", command=lambda i=i, j=j: computar_jogada(velha[i][j], i, j))
        button.grid(row=i, column=j)
        buttons[i][j] = button


# Função para escolher o jogador e iniciar o jogo
def escolhe_jogador():
    global usuario, robo
    usuario = escolha.get().upper()
    robo = "O" if usuario == "X" else "X"

    # Habilita os botões para começar o jogo
    mostrar_jogo()
    label.config(text=f"Você escolheu {usuario}. Boa sorte!")
    start_button.config(state="disabled")


# Escolha de X ou O
escolha = tk.StringVar(value="X")  # Define um valor padrão

label = tk.Label(root, text="Escolha X ou O:")
label.grid(row=3, column=0, columnspan=2)

x_button = tk.Radiobutton(root, text="X", variable=escolha, value="X")
x_button.grid(row=3, column=2)

o_button = tk.Radiobutton(root, text="O", variable=escolha, value="O")
o_button.grid(row=3, column=3)

start_button = tk.Button(root, text="Iniciar Jogo", command=escolhe_jogador)
start_button.grid(row=4, column=0, columnspan=4)

# Inicia o loop da interface gráfica
root.mainloop()
