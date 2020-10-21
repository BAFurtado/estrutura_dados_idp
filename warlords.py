"""

In this mission you should add a new class Warlord(), which should be the subclass of the Warrior class and have
the next characteristics:
health = 100
attack = 4
defense = 2

Also, when the Warlord is included in any of the armies, that particular army gets the new move_units() method which
allows to rearrange the units of that army for the better battle result. The rearrangement is done not only before
the battle, but during the battle too, each time the allied units die. The rules for the rearrangement are as follow:

    If there are Lancers in the army, they should be placed in front of everyone else.
    If there is a Healer in the army, he should be placed right after the first soldier to heal him during the fight.
    If the number of Healers is > 1, all of them should be placed right behind the first Healer.
    If there are no more Lancers in the army, but there are other soldiers who can deal damage,
    they also should be placed in first position, and the Healer should stay in the 2nd row (if army still has Healers).
    Warlord should always stay way in the back to look over the battle and rearrange the soldiers when it's needed.
    Every army can have no more than 1 Warlord.
    If the army doesn’t have a Warlord, it can’t use the move_units() method.
"""


class Warrior:
    def __init__(self, health=50, attack=5):
        self.health = health
        self.attack = attack

    @property
    def is_alive(self):
        return self.health > 0

    def hit(self, other):
        other.loss(self.attack)

    def damage(self, attack):
        return attack

    def loss(self, attack):
        self.health -= self.damage(attack)

    def equip_weapon(self, weapon):
        self.health += weapon.health
        self.attack += weapon.attack
        try:
            self.defense += weapon.defense
        except AttributeError:
            pass
        try:
            self.vampirism += weapon.vampirism
            self.vampirism = int(self.vampirism)
        except AttributeError:
            pass
        try:
            self.heal_power += weapon.heal_power
        except AttributeError:
            pass


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3)
        self.defense = 2

    def damage(self, attack):
        return max(0, attack - self.defense)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self.vampirism = 50

    def hit(self, other):
        super().hit(other)
        self.health += other.damage(self.attack) * self.vampirism // 100


class Healer(Warrior):
    def __init__(self, heal_power=2):
        super().__init__(health=60, attack=0)
        self.heal_power = heal_power

    def heal(self, other):
        other.health += self.heal_power
        if other.health > type(other)().health:
            other.health = type(other)().health


class Lancer(Warrior):
    def __init__(self):
        super().__init__(attack=6)


class Warlord(Warrior):
    def __init__(self):
        super().__init__(health=100, attack=4)
        self.defense = 2

    def damage(self, attack):
        return max(0, attack - self.defense)


def fight(unit_1, unit_2):
    while 1:
        unit_1.hit(unit_2)
        if unit_2.health <= 0:
            return True
        unit_2.hit(unit_1)
        if unit_1.health <= 0:
            return False


class Army:
    def __init__(self):
        self.units = []

    def add_units(self, unit_class, count):
        for _ in range(count):
            self.units.append(unit_class())

    def move_units(self):
        warlord = [w for w in self.units if isinstance(w, Warlord) and w.is_alive is True]
        if warlord:
            lancers = [l for l in self.units if isinstance(l, Lancer) and l.is_alive is True]
            healers = [h for h in self.units if isinstance(h, Healer) and h.is_alive is True]
            others = [o for o in self.units if o not in lancers and
                      o not in healers
                      and o not in warlord
                      and o.is_alive is True]
            new = list()
            if lancers:
                new.append(lancers.pop(0))
            elif others:
                new.append(others.pop(0))
            if healers:
                new += healers
            if lancers:
                new += lancers
            if others:
                new += others
            new.append(warlord.pop(0))
            self.units = new
        else:
            return

    @property
    def first_alive_unit(self):
        for unit in self.units:
            if unit.is_alive:
                return unit

    def alive_units(self):
        return [u for u in self.units if u.is_alive]

    def next_unit(self, unit):
        i = self.units.index(unit)
        if i + 1 < len(self.units):
            return self.units[i + 1]

    @property
    def is_alive(self):
        return self.first_alive_unit is not None


class Weapon:
    def __init__(self, health=0, attack=0, defense=0, vampirism=0, heal_power=0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.vampirism = vampirism
        self.heal_power = heal_power


class Sword(Weapon):
    def __init__(self):
        super().__init__(health=5, attack=2)


class Shield(Weapon):
    def __init__(self):
        super().__init__(health=20, attack=-1, defense=2)


class GreatAxe(Weapon):
    def __init__(self):
        super().__init__(health=-15, attack=5, defense=-2, vampirism=10)


class Katana(Weapon):
    def __init__(self):
        super().__init__(health=-20, attack=6, defense=-5, vampirism=50)


class MagicWand(Weapon):
    def __init__(self):
        super().__init__(health=30, attack=3, heal_power=3)


class Battle:
    @staticmethod
    def hit(unit_1, unit_2, army_2, army_1):
        unit_4 = army_1.next_unit(unit_1)
        unit_3 = army_2.next_unit(unit_2)
        unit_1.hit(unit_2)
        if isinstance(unit_1, Lancer):
            if unit_3:
                unit_3.loss(unit_1.attack // 2)
        if unit_4:
            if isinstance(unit_4, Healer):
                unit_4.heal(unit_1)

    @classmethod
    def fight(cls, army_1, army_2):
        while army_1.is_alive and army_2.is_alive:
            army_1.move_units()
            army_2.move_units()
            unit_1 = army_1.first_alive_unit
            unit_2 = army_2.first_alive_unit
            while 1:
                cls.hit(unit_1, unit_2, army_2, army_1)
                if unit_2.health <= 0:
                    break
                cls.hit(unit_2, unit_1, army_1, army_2)
                if unit_1.health <= 0:
                    break
        return army_1.is_alive

    @classmethod
    def straight_fight(cls, army_1, army_2):
        while army_1.is_alive and army_2.is_alive:
            duels = list(zip(army_1.alive_units(), army_2.alive_units()))
            if not duels:
                break
            for duel in duels:
                fight(duel[0], duel[1])
        return army_1.is_alive


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Warrior, 2)
    army_1.add_units(Lancer, 2)
    army_1.add_units(Defender, 1)
    army_1.add_units(Warlord, 3)
    army_2.add_units(Warlord, 2)
    army_2.add_units(Vampire, 1)
    army_2.add_units(Healer, 5)
    army_2.add_units(Knight, 2)
    army_1.move_units()
    army_2.move_units()
    battle = Battle()
    assert battle.fight(army_1, army_2) == False

    ronald = Warlord()
    heimdall = Knight()

    assert fight(heimdall, ronald) == False

    my_army = Army()
    my_army.add_units(Warlord, 1)
    my_army.add_units(Warrior, 2)
    my_army.add_units(Lancer, 2)
    my_army.add_units(Healer, 2)

    enemy_army = Army()
    enemy_army.add_units(Warlord, 3)
    enemy_army.add_units(Vampire, 1)
    enemy_army.add_units(Healer, 2)
    enemy_army.add_units(Knight, 2)

    my_army.move_units()
    enemy_army.move_units()

    assert type(my_army.units[0]) == Lancer
    assert type(my_army.units[1]) == Healer
    assert type(my_army.units[-1]) == Warlord

    assert type(enemy_army.units[0]) == Vampire
    assert type(enemy_army.units[-1]) == Warlord
    assert type(enemy_army.units[-2]) == Knight

    # 6, not 8, because only 1 Warlord per army could be
    assert len(enemy_army.units) == 6

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == True
print("Coding complete? Let's try tests!")
