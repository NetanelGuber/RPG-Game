import random
import os
from time import sleep
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
from tkinter import StringVar, OptionMenu, Button

# --- Constants and Configuration ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(CURRENT_DIR, "RPG Images")

# Using a dictionary for easier lookup by tier
ALL_ENEMIES = {
    1: {
        "level_cap": 5, "enemies": {
            "Grove Prowler": {"health": 15, "attack": 5},
            "Cave Stalker": {"health": 25, "attack": 10},
            "Mountain Scout": {"health": 40, "attack": 15},
        }
    },
    2: {
        "level_cap": 10, "enemies": {
            "Marsh Harrier": {"health": 40, "attack": 15},
            "Desert Nomad": {"health": 60, "attack": 20},
            "Tundra Vanguard": {"health": 80, "attack": 25},
        }
    },
    3: {
        "level_cap": 15, "enemies": {
            "Flame Specter": {"health": 120, "attack": 30},
            "Thunder Wraith": {"health": 150, "attack": 35},
            "Frost Phantom": {"health": 180, "attack": 40},
        }
    },
    4: {
        "level_cap": 20, "enemies": {
            "Abyssal Knight": {"health": 220, "attack": 45},
            "Celestial Guard": {"health": 260, "attack": 50},
            "Ethereal Templar": {"health": 300, "attack": 55},
        }
    },
    5: {
        "level_cap": 25, "enemies": {
            "Primeval Behemoth": {"health": 350, "attack": 60},
            "Arcane Colossus": {"health": 400, "attack": 65},
            "Cosmic Leviathan": {"health": 450, "attack": 70},
        }
    }
}

UPGRADE_TIERS = {
    1: {
        "level_cap": 5,
        "upgrades": {
            "1": {"text": "Increase attack damage by 5", "action": lambda p: setattr(p, 'attack', p.attack + 5)},
            "2": {"text": "Increase healing amount by 10", "action": lambda g: setattr(g, 'heal_amount', g.heal_amount + 10)}
        }
    },
    2: {
        "level_cap": 10,
        "upgrades": {
            "1": {"text": "Increase attack damage by 7.5", "action": lambda p: setattr(p, 'attack', p.attack + 7.5)},
            "2": {"text": "Increase healing amount by 20", "action": lambda g: setattr(g, 'heal_amount', g.heal_amount + 20)},
            "3": {"text": "Increase critical chance by 1%", "action": lambda p: setattr(p, 'critical_chance', p.critical_chance + 1)}
        }
    },
    3: {
        "level_cap": 15,
        "upgrades": {
            "1": {"text": "Increase attack damage by 10", "action": lambda p: setattr(p, 'attack', p.attack + 10)},
            "2": {"text": "Increase healing amount by 25", "action": lambda g: setattr(g, 'heal_amount', g.heal_amount + 25)},
            "3": {"text": "Increase critical chance by 2%", "action": lambda p: setattr(p, 'critical_chance', p.critical_chance + 2)}
        }
    },
    4: {
        "level_cap": 20,
        "upgrades": {
            "1": {"text": "Increase attack damage by 12.5", "action": lambda p: setattr(p, 'attack', p.attack + 12.5)},
            "2": {"text": "Increase healing amount by 30", "action": lambda g: setattr(g, 'heal_amount', g.heal_amount + 30)},
            "3": {"text": "Increase critical chance by 2%", "action": lambda p: setattr(p, 'critical_chance', p.critical_chance + 2)}
        }
    },
    5: {
        "level_cap": 25,
        "upgrades": {
            "1": {"text": "Increase attack damage by 15", "action": lambda p: setattr(p, 'attack', p.attack + 15)},
            "2": {"text": "Increase healing amount by 35", "action": lambda g: setattr(g, 'heal_amount', g.heal_amount + 35)},
            "3": {"text": "Increase critical chance by 3%", "action": lambda p: setattr(p, 'critical_chance', p.critical_chance + 3)}
        }
    }
}


# --- Helper Functions ---
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_and_resize_image(path, size_divisor):
    try:
        image = Image.open(path)
        new_width = image.size[0] // size_divisor
        new_height = image.size[1] // size_divisor
        return ImageTk.PhotoImage(image.resize((new_width, new_height)))
    except FileNotFoundError:
        print(f"Error: Image not found at {path}")
        return None

# --- Game Classes ---
class Player:
    def __init__(self):
        self.health = 100
        self.attack = 10
        self.level = 1
        self.critical_chance = 1

class Game:
    def __init__(self, root_window):
        self.root = root_window
        self.player = Player()
        self.enemies_defeated = 0
        self.heal_amount = 10
        self.running = False
        self.ui_widgets = {}

        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack(fill="both", expand=True)

        self.ui_widgets['player_health_label'] = self.canvas.create_text(
            55, 210, text=f"Your Health: {self.player.health}", fill="black", font=("Arial", 12), anchor="w"
        )
        self.ui_widgets['info_label'] = self.canvas.create_text(
            20, 55, text="", fill="black", font=("Arial", 12), anchor="w"
        )

        self.photo1 = load_and_resize_image(os.path.join(IMAGE_PATH, "man.png"), 14)
        self.photo3 = load_and_resize_image(os.path.join(IMAGE_PATH, "sword.png"), 8)
        self.ui_widgets['player_image'] = self.canvas.create_image(75, 300, anchor="w", image=self.photo1)
        self.ui_widgets['sword_image'] = self.canvas.create_image(125, 300, anchor="w", image=self.photo3)

        start_button = Button(self.root, text="Begin Game", command=self.start_game_thread, height=2, width=10, font=('Arial', '20'))
        self.canvas.create_window(250, 450, window=start_button)
        self.ui_widgets['start_button'] = start_button

    def update_info_label(self, text, duration=2):
        self.canvas.itemconfig(self.ui_widgets['info_label'], text=text)
        self.root.update()
        if duration:
            sleep(duration)

    def update_player_health_label(self):
        self.canvas.itemconfig(self.ui_widgets['player_health_label'], text=f"Your Health: {self.player.health}")

    def get_current_tier_data(self, data_map):
        for tier_num in sorted(data_map.keys()):
            tier = data_map[tier_num]
            if self.player.level <= tier["level_cap"]:
                return tier
        return data_map[max(data_map.keys())]

    def select_enemy(self):
        current_tier = self.get_current_tier_data(ALL_ENEMIES)
        return random.choice(list(current_tier["enemies"].keys()))

    def fight_enemy(self, enemy_name):
        current_tier_enemies = self.get_current_tier_data(ALL_ENEMIES)["enemies"]
        enemy_stats = current_tier_enemies[enemy_name]
        enemy_health = enemy_stats["health"]
        enemy_attack = enemy_stats["attack"]

        print(f"A wild {enemy_name} appears!\n")
        self.update_info_label(f"A wild {enemy_name} appears!", 1)

        enemy_photo = load_and_resize_image(os.path.join(IMAGE_PATH, "slime.png"), 24)
        enemy_image = self.canvas.create_image(425, 300, anchor="e", image=enemy_photo)
        enemy_health_label = self.canvas.create_text(450, 230, text=f"Enemy Health: {enemy_health}", fill="black", font=("Arial", 12), anchor="e")

        while enemy_health > 0 and self.player.health > 0:
            # Player attacks
            damage = self.player.attack
            is_crit = random.random() <= self.player.critical_chance / 100
            if is_crit:
                damage *= 2
            
            enemy_health -= damage
            print(f"You attack the {enemy_name} for {damage} damage.")
            self.update_info_label(f"You attack the {enemy_name} for {damage} damage.", 0)
            self.canvas.itemconfig(enemy_health_label, text=f"Enemy Health: {max(0, enemy_health)}")

            # Simple attack animation
            self.canvas.move(self.ui_widgets['player_image'], 225, 0)
            self.canvas.move(self.ui_widgets['sword_image'], 225, 0)
            self.root.update()
            sleep(0.5)
            self.canvas.move(self.ui_widgets['player_image'], -225, 0)
            self.canvas.move(self.ui_widgets['sword_image'], -225, 0)
            self.root.update()
            sleep(1)

            if enemy_health <= 0:
                print(f"The {enemy_name} is defeated!\n")
                self.update_info_label(f"The {enemy_name} is defeated!", 2)
                self.enemies_defeated += 1
                self.player.level += 1
                print(f"You leveled up to level {self.player.level}")
                self.update_info_label(f"You leveled up to level {self.player.level}", 2)
                break

            # Enemy attacks
            self.player.health -= enemy_attack
            print(f"The {enemy_name} attacks you for {enemy_attack} damage.")
            self.update_info_label(f"The {enemy_name} attacks you for {enemy_attack} damage.", 0)
            self.update_player_health_label()

            # Simple enemy attack animation
            self.canvas.move(enemy_image, -275, 0)
            self.root.update()
            sleep(0.5)
            self.canvas.move(enemy_image, 275, 0)
            self.root.update()
            sleep(1)

            if self.player.health <= 0:
                self.handle_game_over()
                return

        self.canvas.delete(enemy_image)
        self.canvas.delete(enemy_health_label)
        if self.player.health > 0:
            print("You survived the encounter.")
            self.update_info_label("You survived the encounter.", 2)
        
        clear_console()

    def handle_upgrade(self):
        clear_console()
        sleep(1)
        
        current_tier = self.get_current_tier_data(UPGRADE_TIERS)
        upgrades = current_tier["upgrades"]
        
        upgrade_texts = [f"{key}. {val['text']}" for key, val in upgrades.items()]
        print(f"Tier {self.player.level} upgrades\n")
        print("\n".join(upgrade_texts))
        self.update_info_label(f"Tier {self.player.level} upgrades\n\n" + "\n".join(upgrade_texts), 0)

        options = ["Choose an option"] + list(upgrades.keys())
        option_var = StringVar(self.root)
        option_var.set(options[0])

        def on_submit(choice):
            self.cleanup_ui_widgets(['upgrade_menu', 'upgrade_button'])
            if choice in upgrades:
                upgrade_info = upgrades[choice]
                print(f"Applying upgrade: {upgrade_info['text']}")
                if "attack" in upgrade_info["text"] or "critical" in upgrade_info["text"]:
                    upgrade_info["action"](self.player)
                else:
                    upgrade_info["action"](self)
                self.update_info_label(f"Upgraded: {upgrade_info['text']}", 3)
            else:
                print("No upgrade was added")
                self.update_info_label("No upgrade was added", 2)
            clear_console()
            self.game_loop()

        option_menu = OptionMenu(self.root, option_var, *options)
        submit_button = Button(self.root, text="Submit", command=lambda: on_submit(option_var.get()), height=1, width=5, font=('Arial', '10'))

        self.ui_widgets['upgrade_menu'] = self.canvas.create_window(80, 125, window=option_menu)
        self.ui_widgets['upgrade_button'] = self.canvas.create_window(80, 155, window=submit_button)

    def handle_heal(self):
        clear_console()
        sleep(1)
        print("Healing...\n")
        self.update_info_label("Healing...", 2)
        self.player.health += self.heal_amount
        print(f"Your health is now at {self.player.health}")
        self.update_info_label(f"Your health is now at {self.player.health}", 2)
        self.update_player_health_label()
        clear_console()
        self.game_loop()

    def handle_exit(self):
        clear_console()
        print("Thanks for playing!")
        self.update_info_label("Thanks for playing!", 3)
        self.root.quit()

    def handle_game_over(self):
        sleep(2)
        clear_console()
        print("You have been defeated. Game Over.")
        sleep(1)
        print(f"\nYou killed a total of {self.enemies_defeated} enemies")
        print(f"You died with {self.player.level} levels")
        self.update_info_label(f"You have been defeated. Game Over.\n\nYou killed {self.enemies_defeated} enemies\nYou died at level {self.player.level}", 5)
        self.root.quit()

    def game_loop(self):
        enemy = self.select_enemy()
        self.fight_enemy(enemy)

        if self.player.health <= 0:
            return

        print(f"You healed by {self.heal_amount} health\n")
        self.player.health += self.heal_amount
        self.update_info_label(f"You healed by {self.heal_amount} health", 2)
        self.update_player_health_label()
        
        stats_text = (
            f"You are level {self.player.level}, have {self.player.health} health left, "
            f"{self.player.attack} attack damage, heal {self.heal_amount} health per battle, "
            f"and have a {self.player.critical_chance}% chance to crit\n"
        )
        print(stats_text)
        self.update_info_label(stats_text.replace(", ", "\n"), 7.5)

        self.prompt_next_action()

    def prompt_next_action(self):
        self.cleanup_ui_widgets(['option_menu', 'submit_button'])
        print("Here are your options:\n")
        options_text = f"1. Continue fighting\n2. Upgrade\n3. Heal again (Heal by {self.heal_amount})\n4. Leave"
        print(options_text)
        self.update_info_label("Here are your options:\n\n" + options_text.replace("\n", "\n"), 0)

        options = ["Choose an option", "1", "2", "3", "4"]
        option_var = StringVar(self.root)
        option_var.set(options[0])

        def on_submit(choice):
            self.cleanup_ui_widgets(['option_menu', 'submit_button'])
            if choice == "1":
                self.game_loop()
            elif choice == "2":
                self.handle_upgrade()
            elif choice == "3":
                self.handle_heal()
            elif choice == "4":
                self.handle_exit()

        option_menu = OptionMenu(self.root, option_var, *options)
        submit_button = Button(self.root, text="Submit", command=lambda: on_submit(option_var.get()), height=1, width=5, font=('Arial', '10'))

        self.ui_widgets['option_menu'] = self.canvas.create_window(80, 125, window=option_menu)
        self.ui_widgets['submit_button'] = self.canvas.create_window(80, 155, window=submit_button)

    def cleanup_ui_widgets(self, widget_keys):
        for key in widget_keys:
            if key in self.ui_widgets:
                widget_id = self.ui_widgets.pop(key)
                # Check if it's a canvas item or a widget
                if isinstance(widget_id, int):
                    self.canvas.delete(widget_id)
                else:
                    widget_id.destroy()

    def start_game_thread(self):
        self.cleanup_ui_widgets(['start_button'])
        if not self.running:
            self.running = True
            # Run the game loop in a separate thread to keep the UI responsive
            game_thread = Thread(target=self.game_loop, daemon=True)
            game_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.title("RPG Game")
    game_instance = Game(root)
    root.mainloop()
