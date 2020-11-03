class Lampada:
    def __init__(self):
        self.status = 0
        self.cores = ['Green', 'Red', 'Blue', 'Yellow']

    def acende(self):
        resposta = self.cores[self.status % 4]
        self.status += 1
        print(resposta)
        return resposta


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    lampada_1 = Lampada()
    lampada_2 = Lampada()

    lampada_1.acende()  # Green
    lampada_1.acende()  # Red
    lampada_2.acende()  # Green

    assert lampada_1.acende() == "Blue"
    assert lampada_1.acende() == "Yellow"
    assert lampada_1.acende() == "Green"
    assert lampada_2.acende() == "Red"
    assert lampada_2.acende() == "Blue"
