

class Conta:

    def __init__(self, id):
        self.id = id
        self.saldo = 0

    def movimenta(self, quantia):
        self.saldo += quantia


if __name__ == '__main__':
    bb = Conta(100.007)
    bb.movimenta(99)
    bb.movimenta(0)
    bb.movimenta(-7)
    print(bb.saldo)


