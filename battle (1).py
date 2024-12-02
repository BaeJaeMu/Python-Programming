class Equipment:
    def __init__(self, name, grade, attack_bonus=0, defense_bonus=0):
        self.name = name
        self.grade = grade
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus

    def __str__(self):
        return f"{self.grade} {self.name} (Attack: {self.attack_bonus}, Defense: {self.defense_bonus})"

class Character:
    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.level = 1

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        effective_damage = max(0, damage - self.defense)
        self.hp -= effective_damage
        return effective_damage

    def level_up(self):
        self.hp += 20
        self.attack += 5
        self.defense += 5
        self.speed += 2

class Hero(Character):
    def __init__(self, name, hp, attack, defense, speed):
        super().__init__(name, hp, attack, defense, speed)
        self.weapon = None
        self.armor = None
        self.exp = 0

    def equip(self, equipment):
        if isinstance(equipment, Equipment):
            if equipment.attack_bonus > 0:
                self.weapon = equipment
            elif equipment.defense_bonus > 0:
                self.armor = equipment

    def calculate_attack(self):
        return self.attack + (self.weapon.attack_bonus if self.weapon else 0)

    def calculate_defense(self):
        return self.defense + (self.armor.defense_bonus if self.armor else 0)

    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= self.level * 50:
            self.level += 1
            self.level_up()
            print(f"{self.name} 레벨 업! Lv.{self.level}")

    def level_up(self):
        super().level_up()
        print(f"{self.name}의 능력치가 향상되었습니다!")

class Monster(Character):
    def __init__(self, name, hp, attack, defense, speed, level):
        super().__init__(name, hp, attack, defense, speed)
        self.level = level

    def exp_reward(self):
        return self.level * 20

    def drop_loot(self):
        if random.random() > 0.5:
            grade = random.choices(["Common", "Rare", "Legendary"], weights=[50, 30, 20])[0]
            if random.random() > 0.5:
                return Equipment("Weapon", grade, attack_bonus=random.randint(5, 15))
            else:
                return Equipment("Armor", grade, defense_bonus=random.randint(5, 15))
        return None

class Battle:
    def fight(self, hero, monster):
        print(f"전투 시작 {hero.name} vs {monster.name}")
        turn = 1

        while hero.is_alive() and monster.is_alive():
            print(f"==턴 {turn}==")

            if hero.speed >= monster.speed:
                first, second = hero, monster
            else:
                first, second = monster, hero

            damage = second.take_damage(first.calculate_attack())
            print(f"{first.name}가 {second.name}에게 {damage}의 데미지를 입힘")
            if not second.is_alive():
                print(f"{second.name}가 쓰러짐")
                if isinstance(second, Monster):
                    hero.gain_exp(second.exp_reward())
                    loot = second.drop_loot()
                    if loot:
                        print(f"{second.name}가 {loot} 드롭")
                return

            # Second attacks
            damage = first.take_damage(second.attack)
            print(f"{second.name}가 {first.name}에게 {damage}의 데미지를 입힘")
            if not first.is_alive():
                print(f"{first.name}가 쓰러짐")
                return

            turn += 1

        print("전투 종료")
