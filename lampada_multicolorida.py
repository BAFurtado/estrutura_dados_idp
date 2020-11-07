class Lampada:
    def __init__(self):
        self.status = 0
        self.cores = ['Verde', 'Vermelho', 'Azul', 'Amarelo']

    def acende(self):
        resposta = self.cores[self.status % 4]
        self.status += 1
        print(resposta)
        return resposta


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    lampada_1 = Lampada()
    lampada_2 = Lampada()

    lampada_1.acende()  # Verde
    lampada_1.acende()  # Vermelho
    lampada_2.acende()  # Verde
