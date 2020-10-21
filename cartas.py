""" Adaptado a partir de 
Think Python, 2nd Edition by Allen Downey http://thinkpython2.com
Copyright 2015 Allen Downey 
License: http://creativecommons.org/licenses/by/4.0/
"""

import random


class Carta:
    """Represents a standard playing carta.
    Attributes:
      naipe: integer 0-3
      rank: integer 1-13
    """

    naipe_names = ["Paus", "Ouros", "Copas", "Espadas"]
    rank_names = [None, "As", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Valete", "Rainha", "Rei"]

    def __init__(self, naipe=0, rank=2):
        self.naipe = naipe
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation."""
        return '{} de {}'.format(Carta.rank_names[self.rank],
                                Carta.naipe_names[self.naipe])

    def __eq__(self, other):
        # Eu estou informando para o objeto, para a classe, como fazer comparação dessas coisas
        """Checks whether self and other have the same rank and naipe.

        returns: boolean
        """
        return self.naipe == other.naipe and self.rank == other.rank

    def __lt__(self, other):
        # lt = larger than = maior que
        """Compares this carta to other, first by naipe, then rank.

        returns: boolean
        """
        t1 = self.naipe, self.rank
        t2 = other.naipe, other.rank
        return t1 < t2


class Baralho:
    """Represents a deck of cartas.

    Attributes:
      cartas: list of Carta objects.
    """

    def __init__(self):
        """Initializes the Baralho with 52 cartas.
        """
        self.cartas = []
        for naipe in range(4):
            for rank in range(1, 14):
                carta = Carta(naipe, rank)
                self.cartas.append(carta)

    def __str__(self):
        """Returns a string representation of the deck.
        """
        res = []
        for carta in self.cartas:
            res.append(str(carta))
        return '\n'.join(res)

    def add_carta(self, carta):
        """Adds a carta to the deck.

        carta: Carta
        """
        self.cartas.append(carta)

    def remove_carta(self, carta):
        """Removes a carta from the deck or raises exception if it is not there.

        carta: Carta
        """
        self.cartas.remove(carta)

    def pop_carta(self, i=-1):
        """Removes and returns a carta from the deck.

        i: index of the carta to pop; by default, pops the last carta.
        """
        return self.cartas.pop(i)

    def shuffle(self):
        """Shuffles the cartas in this deck."""
        random.shuffle(self.cartas)

    def sort(self):
        """Sorts the cartas in ascending order."""
        self.cartas.sort()

    def move_cartas(self, hand, num):
        """Moves the given number of cartas from the deck into the Mao.

        hand: destination Mao object
        num: integer number of cartas to move
        """
        for i in range(num):
            hand.add_carta(self.pop_carta())


class Mao(Baralho):
    """Represents a hand of playing cartas."""

    def __init__(self, label=''):
        self.cartas = []
        self.label = label


if __name__ == '__main__':
    deck = Baralho()
    deck.shuffle()
    #
    claudio = Mao('Claudio')
    bernardo = Mao('Bernardo')
    #
    deck.move_cartas(claudio, 3)
    deck.move_cartas(bernardo, 3)
    # hand.sort()
    # print(hand)
