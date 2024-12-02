class Character:
    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return (f"{self.name} - HP: {self.hp}, 공격력: {self.attack}, "
                f"방어력: {self.defense}, 속도: {self.speed}")


class Equipment:
    def __init__(self, name, grade, attack_bonus, defense_bonus):
        self.name = name
        self.grade = grade
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus

    def __str__(self):
        return f"{self.name} [{self.grade}] - 공격력 보너스: {self.attack_bonus}, 방어력 보너스: {self.defense_bonus}"


class Hero(Character):
    def __init__(self, name, hp, attack, defense, speed, role):
        super().__init__(name, hp, attack, defense, speed)
        self.role = role
        self.exp = 0
        self.level = 1
        self.weapon = None
        self.armor = None

    def equip(self, equipment):
        if equipment.attack_bonus > 0:
            self.weapon = equipment
        elif equipment.defense_bonus > 0:
            self.armor = equipment

    def calculate_attack(self):
        return self.attack + (self.weapon.attack_bonus if self.weapon else 0)

    def calculate_defense(self):
        return self.defense + (self.armor.defense_bonus if self.armor else 0)

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        if self.role == "전사":
            self.hp += 20
            self.attack += 5
            self.defense += 3
        elif self.role == "마법사":
            self.hp += 15
            self.attack += 7
            self.defense += 2
        elif self.role == "궁수":
            self.hp += 18
            self.attack += 4
            self.defense += 2
        self.speed += 2

    def special_attack(self):
        if self.role == "전사":
            return self.calculate_attack() + 4
        elif self.role == "마법사":
            return self.calculate_attack() + 3
        elif self.role == "궁수":
            return self.calculate_attack() + 2
        else:
            return self.calculate_attack()

    def __str__(self):
        weapon = str(self.weapon) if self.weapon else "None"
        armor = str(self.armor) if self.armor else "None"
        return (f"{self.name}[{self.role}] - 레벨: {self.level}, HP: {self.hp}, 공격력: {self.calculate_attack()}, "
                f"방어력: {self.calculate_defense()}, 속도: {self.speed}, 경험치: {self.exp}, "
                f"무기: {weapon}, 갑옷: {armor}")


class Monster(Character):
    def __init__(self, name, hp, attack, defense, speed, level):
        super().__init__(name, hp, attack, defense, speed)
        self.level = level

    def drop_loot(self):
        if random.random() < 0.5:  # 50% chance to drop loot
            is_weapon = random.random() < 0.5  # 50% chance for weapon or armor
            grade_chance = random.random()
            if grade_chance < 0.5:
                grade = "일반"
                bonus = 5
            elif grade_chance < 0.8:
                grade = "레어"
                bonus = 10
            else:
                grade = "전설"
                bonus = 20
            if is_weapon:
                return Equipment("무기", grade, bonus, 0)
            else:
                return Equipment("갑옷", grade, 0, bonus)
        return None

    def exp_reward(self):
        return self.level * 20

    def level_up(self):
        self.level += 1
        self.hp += 15
        self.attack += 3
        self.defense += 2
        self.speed += 1

    def __str__(self):
        return (f"{self.name} - 레벨: {self.level}, HP: {self.hp}, 공격력: {self.attack}, "
                f"방어력: {self.defense}, 속도: {self.speed}")


class Battle:
    def fight(hero, monster):
        print(f"전투 시작! {hero.name} vs {monster.name}")
        while hero.is_alive() and monster.is_alive():
            if hero.speed >= monster.speed:
                damage = hero.calculate_attack()
                actual_damage = monster.take_damage(damage)
                print(f"{hero.name}이(가) {monster.name}에게 {actual_damage}의 피해를 입혔습니다.")
                if not monster.is_alive():
                    print(f"{monster.name}이(가) 쓰러졌습니다!")
                    hero.gain_exp(monster.exp_reward())
                    loot = monster.drop_loot()
                    if loot:
                        print(f"{monster.name}이(가) {loot}를 드롭했습니다.")
                    return
            damage = monster.attack
            actual_damage = hero.take_damage(damage)
            print(f"{monster.name}이(가) {hero.name}에게 {actual_damage}의 피해를 입혔습니다.")
            if not hero.is_alive():
                print(f"{hero.name}이(가) 쓰러졌습니다! 게임 오버!")
                return

