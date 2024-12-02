from character import Hero, Monster
from battle import Battle

def main():
    print("=== RPG 게임 ===")
    name = input("영웅의 이름을 입력하세요: ")
    role = input("직업을 선택하세요 (전사/마법사/궁수): ")
    hero = Hero(name="아서", hp=100, attack=20, defense=10, speed=12, role="전사")
    print(hero)
    monster = Monster(name="고블린", hp=50, attack=15, defense=5, speed=10, level=1)
    print(monster)
    battle = Battle()
    for i in range(5):
        print(f"\n===== {i+1}번째 전투 =====")
        Battle.fight(hero, monster)
        monster.level_up()
if __name__ == "__main__":
    main()
