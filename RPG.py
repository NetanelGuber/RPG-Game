import random
import os
from time import sleep
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
from tkinter import Tk, OptionMenu, StringVar

current_dir = os.path.dirname(os.path.abspath(__file__))

clear = lambda: os.system('cls')

running = False
option_chosen = False

option_var = None
option_menu = None
submit_button = None

button_pressed = False

upgrade_button_pressed1 = False
upgrade_button_pressed2 = False
upgrade_button_pressed3 = False
upgrade_button_pressed4 = False
upgrade_button_pressed5 = False

root = tk.Tk()

# enemy stats
tier1_enemies = {
    "Grove Prowler": {"health": 15, "attack": 5},
    "Cave Stalker": {"health": 25, "attack": 10},
    "Mountain Scout": {"health": 40, "attack": 15},
}

tier2_enemies = {
    "Marsh Harrier": {"health": 40, "attack": 15},
    "Desert Nomad": {"health": 60, "attack": 20},
    "Tundra Vanguard": {"health": 80, "attack": 25},
}

tier3_enemies = {
    "Flame Specter": {"health": 120, "attack": 30},
    "Thunder Wraith": {"health": 150, "attack": 35},
    "Frost Phantom": {"health": 180, "attack": 40},
}

tier4_enemies = {
    "Abyssal Knight": {"health": 220, "attack": 45},
    "Celestial Guard": {"health": 260, "attack": 50},
    "Ethereal Templar": {"health": 300, "attack": 55},
}

tier5_enemies = {
    "Primeval Behemoth": {"health": 350, "attack": 60},
    "Arcane Colossus": {"health": 400, "attack": 65},
    "Cosmic Leviathan": {"health": 450, "attack": 70},
}

# player stats
player = {
    "health": 100, 
    "attack": 10, 
    "level": 1,
    "critical_chance": 1
}

enemies_defeated = 0
heal_amount = 10

root.geometry("500x500")

root.title("RPG Game")

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack(fill="both", expand=True)

left = "w"
up = "n"

playerHealth_label = canvas.create_text(55, 210, text=f"Your Health: {player['health']}", fill="black", font=("Arial", 12), anchor=left)
info_label = canvas.create_text(20, 55, text=f"", fill="black", font=("Arial", 12), anchor=left)

image_path1 = os.path.join(current_dir, "RPG Images", "man.png")
imageOpen1 = Image.open(image_path1)
new_width1 = imageOpen1.size[0] // 14
new_height1 = imageOpen1.size[1] // 14
resized_image1 = imageOpen1.resize((new_width1, new_height1))
photo1 = ImageTk.PhotoImage(resized_image1)
image1 = canvas.create_image(75, 300, anchor=left, image=photo1)

image_path3 = os.path.join(current_dir, "RPG Images", "sword.png")
imageOpen3 = Image.open(image_path3)
new_width3 = imageOpen3.size[0] // 8
new_height3 = imageOpen3.size[1] // 8
resized_image3 = imageOpen3.resize((new_width3, new_height3))
photo3 = ImageTk.PhotoImage(resized_image3)
image3 = canvas.create_image(125, 300, anchor=left, image=photo3)

def fight_enemy(enemy):
    global enemies_defeated, playerHealth_label, info_label, image1, image3

    left = "w"
    right = "e"
    up = "n"
    down = "s"
    bottom_left = "sw"
    bottom_right = "se"
    top_left = "nw"
    top_right = "ne"

    if player["level"] <= 5:
        enemy_name = enemy
        enemy_health = tier1_enemies[enemy]["health"]
        enemy_attack = tier1_enemies[enemy]["attack"]

        print(f"A wild {enemy_name} appears!\n")

        image_path2 = os.path.join(current_dir, "RPG Images", "slime.png")
        imageOpen2 = Image.open(image_path2)
        new_width2 = imageOpen2.size[0] // 24
        new_height2 = imageOpen2.size[1] // 24
        resized_image2 = imageOpen2.resize((new_width2, new_height2))
        photo2 = ImageTk.PhotoImage(resized_image2)
        image2 = canvas.create_image(425, 300, anchor=right, image=photo2)

        # Display enemy health above the image
        enemyHealth_label = canvas.create_text(450, 230, text=f"Enemy Health: {enemy_health}", fill="black", font=("Arial", 12), anchor=right)
        
        sleep(1)

        while enemy_health > 0 and player["health"] > 0:
            # Player attacks enemy
            random_number = random.random()

            if random_number <= player["critical_chance"] / 100:
                enemy_health -= player["attack"] * 2
                print(f"You attack the {enemy_name} for {player['attack'] * 2} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(415, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(465, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            else:
                enemy_health -= player["attack"]
                print(f"You attack the {enemy_name} for {player['attack']} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text
                canvas.itemconfig(info_label, text=f"You attack the {enemy_name} for {player['attack']} damage.") 

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(300, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(350, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            sleep(1)

            if enemy_health <= 0:
                print(f"The {enemy_name} is defeated!\n")
                canvas.itemconfig(info_label, text=f"The {enemy_name} is defeated!") 
                canvas.delete(enemyHealth_label) # delete the enemy health label
                canvas.delete(image2) # delete the image
                sleep(2)
                enemies_defeated += 1
                player["level"] += 1
                print(f"You leveled up to level {player['level']}")
                canvas.itemconfig(info_label, text=f"You leveled up to level {player['level']}") 
                sleep(2)
                break
            
            # Enemy attacks player
            player["health"] -= enemy_attack
            print(f"The {enemy_name} attacks you for {enemy_attack} damage.")
            canvas.itemconfig(playerHealth_label, text=f"Your Health: {player['health']}") # update text
            canvas.itemconfig(info_label, text=f"The {enemy_name} attacks you for {enemy_attack} damage.") 

            canvas.delete(image2)
            image2 = canvas.create_image(150, 300, anchor=right, image=photo2)
            sleep(0.5)
            canvas.delete(image2)
            image2 = canvas.create_image(425, 300, anchor=right, image=photo2)
            sleep(1)

            if player["health"] <= 0:
                sleep(2)
                clear()
                print("You have been defeated. Game Over.")
                sleep(1)
                print(f"\nYou killed a total of {enemies_defeated} enemies")
                print(f"You died with {player['level']} levels")
                canvas.itemconfig(info_label, text=f"You have been defeated. Game Over.\n\nYou killed a total of {enemies_defeated} enemies\nYou died with {player['level']} levels") 
                sleep(5)
                exit()

        if player["health"] > 0:
            print("You survived the encounter.")
            canvas.itemconfig(info_label, text=f"You survived the encounter.") 
            sleep(2)
            clear()
    elif player["level"] <= 10:
        enemy_name = enemy
        enemy_health = tier2_enemies[enemy]["health"]
        enemy_attack = tier2_enemies[enemy]["attack"]

        print(f"A wild {enemy_name} appears!\n")

        image_path2 =os.path.join(current_dir, "RPG Images", "slime.png")
        imageOpen2 = Image.open(image_path2)
        new_width2 = imageOpen2.size[0] // 24
        new_height2 = imageOpen2.size[1] // 24
        resized_image2 = imageOpen2.resize((new_width2, new_height2))
        photo2 = ImageTk.PhotoImage(resized_image2)
        image2 = canvas.create_image(425, 300, anchor=right, image=photo2)

        # Display enemy health above the image
        enemyHealth_label = canvas.create_text(450, 230, text=f"Enemy Health: {enemy_health}", fill="black", font=("Arial", 12), anchor=right)
        
        sleep(1)

        while enemy_health > 0 and player["health"] > 0:
            # Player attacks enemy
            random_number = random.random()

            if random_number <= player["critical_chance"] / 100:
                enemy_health -= player["attack"] * 2
                print(f"You attack the {enemy_name} for {player['attack'] * 2} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(415, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(465, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            else:
                enemy_health -= player["attack"]
                print(f"You attack the {enemy_name} for {player['attack']} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text
                canvas.itemconfig(info_label, text=f"You attack the {enemy_name} for {player['attack']} damage.") 

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(300, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(350, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            sleep(1)

            if enemy_health <= 0:
                print(f"The {enemy_name} is defeated!\n")
                canvas.itemconfig(info_label, text=f"The {enemy_name} is defeated!") 
                canvas.delete(enemyHealth_label) # delete the enemy health label
                canvas.delete(image2) # delete the image
                sleep(2)
                enemies_defeated += 1
                player["level"] += 1
                print(f"You leveled up to level {player['level']}")
                canvas.itemconfig(info_label, text=f"You leveled up to level {player['level']}") 
                sleep(2)
                break
            
            # Enemy attacks player
            player["health"] -= enemy_attack
            print(f"The {enemy_name} attacks you for {enemy_attack} damage.")
            canvas.itemconfig(playerHealth_label, text=f"Your Health: {player['health']}") # update text
            canvas.itemconfig(info_label, text=f"The {enemy_name} attacks you for {enemy_attack} damage.") 

            canvas.delete(image2)
            image2 = canvas.create_image(150, 300, anchor=right, image=photo2)
            sleep(0.5)
            canvas.delete(image2)
            image2 = canvas.create_image(425, 300, anchor=right, image=photo2)
            sleep(1)

            if player["health"] <= 0:
                sleep(2)
                clear()
                print("You have been defeated. Game Over.")
                sleep(1)
                print(f"\nYou killed a total of {enemies_defeated} enemies")
                print(f"You died with {player['level']} levels")
                canvas.itemconfig(info_label, text=f"You have been defeated. Game Over.\n\nYou killed a total of {enemies_defeated} enemies\nYou died with {player['level']} levels") 
                sleep(5)
                exit()

        if player["health"] > 0:
            print("You survived the encounter.")
            canvas.itemconfig(info_label, text=f"You survived the encounter.") 
            sleep(2)
            clear()
    elif player["level"] <= 15:
        enemy_name = enemy
        enemy_health = tier3_enemies[enemy]["health"]
        enemy_attack = tier3_enemies[enemy]["attack"]

        print(f"A wild {enemy_name} appears!\n")

        image_path2 =os.path.join(current_dir, "RPG Images", "slime.png")
        imageOpen2 = Image.open(image_path2)
        new_width2 = imageOpen2.size[0] // 24
        new_height2 = imageOpen2.size[1] // 24
        resized_image2 = imageOpen2.resize((new_width2, new_height2))
        photo2 = ImageTk.PhotoImage(resized_image2)
        image2 = canvas.create_image(425, 300, anchor=right, image=photo2)

        # Display enemy health above the image
        enemyHealth_label = canvas.create_text(450, 230, text=f"Enemy Health: {enemy_health}", fill="black", font=("Arial", 12), anchor=right)
        
        sleep(1)

        while enemy_health > 0 and player["health"] > 0:
            # Player attacks enemy
            random_number = random.random()

            if random_number <= player["critical_chance"] / 100:
                enemy_health -= player["attack"] * 2
                print(f"You attack the {enemy_name} for {player['attack'] * 2} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(415, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(465, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            else:
                enemy_health -= player["attack"]
                print(f"You attack the {enemy_name} for {player['attack']} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text
                canvas.itemconfig(info_label, text=f"You attack the {enemy_name} for {player['attack']} damage.") 

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(300, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(350, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            sleep(1)

            if enemy_health <= 0:
                print(f"The {enemy_name} is defeated!\n")
                canvas.itemconfig(info_label, text=f"The {enemy_name} is defeated!") 
                canvas.delete(enemyHealth_label) # delete the enemy health label
                canvas.delete(image2) # delete the image
                sleep(2)
                enemies_defeated += 1
                player["level"] += 1
                print(f"You leveled up to level {player['level']}")
                canvas.itemconfig(info_label, text=f"You leveled up to level {player['level']}") 
                sleep(2)
                break
            
            # Enemy attacks player
            player["health"] -= enemy_attack
            print(f"The {enemy_name} attacks you for {enemy_attack} damage.")
            canvas.itemconfig(playerHealth_label, text=f"Your Health: {player['health']}") # update text
            canvas.itemconfig(info_label, text=f"The {enemy_name} attacks you for {enemy_attack} damage.") 

            canvas.delete(image2)
            image2 = canvas.create_image(150, 300, anchor=right, image=photo2)
            sleep(0.5)
            canvas.delete(image2)
            image2 = canvas.create_image(425, 300, anchor=right, image=photo2)
            sleep(1)

            if player["health"] <= 0:
                sleep(2)
                clear()
                print("You have been defeated. Game Over.")
                sleep(1)
                print(f"\nYou killed a total of {enemies_defeated} enemies")
                print(f"You died with {player['level']} levels")
                canvas.itemconfig(info_label, text=f"You have been defeated. Game Over.\n\nYou killed a total of {enemies_defeated} enemies\nYou died with {player['level']} levels") 
                sleep(5)
                exit()

        if player["health"] > 0:
            print("You survived the encounter.")
            canvas.itemconfig(info_label, text=f"You survived the encounter.") 
            sleep(2)
            clear()
    elif player["level"] <= 20:
        enemy_name = enemy
        enemy_health = tier4_enemies[enemy]["health"]
        enemy_attack = tier4_enemies[enemy]["attack"]

        print(f"A wild {enemy_name} appears!\n")

        image_path2 =os.path.join(current_dir, "RPG Images", "slime.png")
        imageOpen2 = Image.open(image_path2)
        new_width2 = imageOpen2.size[0] // 24
        new_height2 = imageOpen2.size[1] // 24
        resized_image2 = imageOpen2.resize((new_width2, new_height2))
        photo2 = ImageTk.PhotoImage(resized_image2)
        image2 = canvas.create_image(425, 300, anchor=right, image=photo2)

        # Display enemy health above the image
        enemyHealth_label = canvas.create_text(450, 230, text=f"Enemy Health: {enemy_health}", fill="black", font=("Arial", 12), anchor=right)
        
        sleep(1)

        while enemy_health > 0 and player["health"] > 0:
            # Player attacks enemy
            random_number = random.random()

            if random_number <= player["critical_chance"] / 100:
                enemy_health -= player["attack"] * 2
                print(f"You attack the {enemy_name} for {player['attack'] * 2} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(415, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(465, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            else:
                enemy_health -= player["attack"]
                print(f"You attack the {enemy_name} for {player['attack']} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text
                canvas.itemconfig(info_label, text=f"You attack the {enemy_name} for {player['attack']} damage.") 

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(300, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(350, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            sleep(1)

            if enemy_health <= 0:
                print(f"The {enemy_name} is defeated!\n")
                canvas.itemconfig(info_label, text=f"The {enemy_name} is defeated!") 
                canvas.delete(enemyHealth_label) # delete the enemy health label
                canvas.delete(image2) # delete the image
                sleep(2)
                enemies_defeated += 1
                player["level"] += 1
                print(f"You leveled up to level {player['level']}")
                canvas.itemconfig(info_label, text=f"You have been defeated. Game Over.\n\nYou killed a total of {enemies_defeated} enemies\nYou died with {player['level']} levels") 
                sleep(2)
                break
            
            # Enemy attacks player
            player["health"] -= enemy_attack
            print(f"The {enemy_name} attacks you for {enemy_attack} damage.")
            canvas.itemconfig(playerHealth_label, text=f"Your Health: {player['health']}") # update text
            canvas.itemconfig(info_label, text=f"The {enemy_name} attacks you for {enemy_attack} damage.") 

            canvas.delete(image2)
            image2 = canvas.create_image(150, 300, anchor=right, image=photo2)
            sleep(0.5)
            canvas.delete(image2)
            image2 = canvas.create_image(425, 300, anchor=right, image=photo2)
            sleep(1)

            if player["health"] <= 0:
                sleep(2)
                clear()
                print("You have been defeated. Game Over.")
                sleep(1)
                print(f"\nYou killed a total of {enemies_defeated} enemies")
                print(f"You died with {player['level']} levels")
                canvas.itemconfig(info_label, text=f"You killed a total of {enemies_defeated} enemies\nYou died with {player['level']} levels") 
                sleep(5)
                exit()

        if player["health"] > 0:
            print("You survived the encounter.")
            canvas.itemconfig(info_label, text=f"You survived the encounter.") 
            sleep(2)
            clear()
    elif player["level"] <= 25:
        enemy_name = enemy
        enemy_health = tier5_enemies[enemy]["health"]
        enemy_attack = tier5_enemies[enemy]["attack"]

        print(f"A wild {enemy_name} appears!\n")

        image_path2 =os.path.join(current_dir, "RPG Images", "slime.png")
        imageOpen2 = Image.open(image_path2)
        new_width2 = imageOpen2.size[0] // 24
        new_height2 = imageOpen2.size[1] // 24
        resized_image2 = imageOpen2.resize((new_width2, new_height2))
        photo2 = ImageTk.PhotoImage(resized_image2)
        image2 = canvas.create_image(425, 300, anchor=right, image=photo2)

        # Display enemy health above the image
        enemyHealth_label = canvas.create_text(450, 230, text=f"Enemy Health: {enemy_health}", fill="black", font=("Arial", 12), anchor=right)
        
        sleep(1)

        while enemy_health > 0 and player["health"] > 0:
            # Player attacks enemy
            random_number = random.random()

            if random_number <= player["critical_chance"] / 100:
                enemy_health -= player["attack"] * 2
                print(f"You attack the {enemy_name} for {player['attack'] * 2} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(415, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(465, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            else:
                enemy_health -= player["attack"]
                print(f"You attack the {enemy_name} for {player['attack']} damage.")
                canvas.itemconfig(enemyHealth_label, text=f"Enemy Health: {enemy_health}") # update text
                canvas.itemconfig(info_label, text=f"You attack the {enemy_name} for {player['attack']} damage.") 

                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(300, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(350, 300, anchor=left, image=photo3)
                sleep(0.5)
                canvas.delete(image1)
                canvas.delete(image3)
                image1 = canvas.create_image(75, 300, anchor=left, image=photo1)
                image3 = canvas.create_image(125, 300, anchor=left, image=photo3)
            sleep(1)

            if enemy_health <= 0:
                print(f"The {enemy_name} is defeated!\n")
                canvas.itemconfig(info_label, text=f"The {enemy_name} is defeated!") 
                canvas.delete(enemyHealth_label) # delete the enemy health label
                canvas.delete(image2) # delete the image
                sleep(2)
                enemies_defeated += 1
                player["level"] += 1
                print(f"You leveled up to level {player['level']}")
                canvas.itemconfig(info_label, text=f"You leveled up to level {player['level']}") 
                sleep(2)
                break
            
            # Enemy attacks player
            player["health"] -= enemy_attack
            print(f"The {enemy_name} attacks you for {enemy_attack} damage.")
            canvas.itemconfig(playerHealth_label, text=f"Your Health: {player['health']}") # update text
            canvas.itemconfig(info_label, text=f"The {enemy_name} attacks you for {enemy_attack} damage.") 

            canvas.delete(image2)
            image2 = canvas.create_image(150, 300, anchor=right, image=photo2)
            sleep(0.5)
            canvas.delete(image2)
            image2 = canvas.create_image(425, 300, anchor=right, image=photo2)
            sleep(1)

            if player["health"] <= 0:
                sleep(2)
                clear()
                print("You have been defeated. Game Over.")
                sleep(1)
                print(f"\nYou killed a total of {enemies_defeated} enemies")
                print(f"You died with {player['level']} levels")
                canvas.itemconfig(info_label, text=f"You have been defeated. Game Over.\n\nYou killed a total of {enemies_defeated} enemies\nYou died with {player['level']} levels") 
                sleep(5)
                exit()

        if player["health"] > 0:
            print("You survived the encounter.")
            canvas.itemconfig(info_label, text=f"You survived the encounter.") 
            sleep(2)
            clear()

def select_enemy():
    if player["level"] <= 5:
        return random.choice(list(tier1_enemies.keys()))
    elif player["level"] <= 10:
        return random.choice(list(tier2_enemies.keys()))
    elif player["level"] <= 15:
        return random.choice(list(tier3_enemies.keys()))
    elif player["level"] <= 20:
        return random.choice(list(tier4_enemies.keys()))
    elif player["level"] <= 25:
        return random.choice(list(tier5_enemies.keys()))

def handle_option():
    global heal_amount, option_var, button_pressed, option_menu, submit_button

    button_pressed = True

    option = option_var.get()

    option_menu.destroy()
    submit_button.destroy()

    try:
        if option == "1":
            game_loop()
        elif option == "2":
            handle_upgrade()
        elif option == "3":
            handle_heal()
        else:
            handle_exit()
    except Exception as e:
        print(e)

def handle_upgrade():
    global heal_amount, upgrade_button_pressed1, root, option_menu, submit_button

    clear()
    sleep(1)
    if player["level"] <= 5:
        def upgrade1():
            global heal_amount, upgrade_button_pressed1, root, option_menu, submit_button

            option_menu.destroy()
            submit_button.destroy()

            upgrade_option1 = option_var.get()
            if upgrade_option1 == "1":
                sleep(1)
                clear()
                print("Adding 5 attack damage to you...")
                player["attack"] += 5
                sleep(3)
                clear()
            elif upgrade_option1 == "2":
                sleep(1)
                clear()
                print("Increasing heal amount by 10...")
                heal_amount += 10
                sleep(3)
                clear()
            else:
                sleep(1)
                clear()
                print("No upgrade was added")
                canvas.itemconfig(info_label, text=f"No upgrade was added")
                sleep(2)
                clear()

            upgrade_button_pressed1 = True

        print("Tier 1 upgrades\n")
        print("1. Increase attack damage by 5\n2. Increase healing amount by 10")
        canvas.itemconfig(info_label, text=f"Tier 1 upgrades\n\n1. Increase attack damage by 5\n2. Increase healing amount by 10")
        sleep(1)
        options = ["Choose an option", "1", "2"]

        option_var = StringVar()
        option_var.set(options[0])

        option_menu = OptionMenu(root, option_var, *options)
        canvas.create_window(80, 125, window=option_menu)

        submit_button = tk.Button(root, text="Submit", command=upgrade1, height=1, width=5, font=('Arial', '10'))
        canvas.create_window(80, 155, window=submit_button)

        while not upgrade_button_pressed1:
            root.update_idletasks()
            root.update()
        
        upgrade_button_pressed1 = False
    elif player["level"] <= 10:
        def upgrade2():
            global heal_amount, upgrade_button_pressed2, root, option_menu, submit_button

            option_menu.destroy()
            submit_button.destroy()

            upgrade_option2 = option_var.get()
            if upgrade_option2 == "1":
                sleep(1)
                clear()
                print("Adding 7.5 attack damage to you...")
                player["attack"] += 7.5
                sleep(3)
                clear()
            elif upgrade_option2 == "2":
                sleep(1)
                clear()
                print("Increasing heal amount by 20...")
                heal_amount += 20
                sleep(3)
                clear()
            elif upgrade_option2 == "3":
                sleep(1)
                clear()
                player["critical_chance"] += 1
                print("Increasing critical chance by 1%...")
                canvas.itemconfig(info_label, text=f"Increasing critical chance by 1%...")
                sleep(3)
                clear()
            else:
                sleep(1)
                clear()
                print("No upgrade was added")
                canvas.itemconfig(info_label, text=f"No upgrade was added")
                sleep(2)
                clear()
            
            upgrade_button_pressed2 = True

        print("Tier 2 upgrades\n")
        print("1. Increase attack damage by 7.5\n2. Increase healing amount by 20\n3. Increase critical chance by 1%")
        canvas.itemconfig(info_label, text=f"Tier 2 upgrades\n\n1. Increase attack damage by 7.5\n2. Increase healing amount by 20\n3. Increase critical chance by 1%")
        sleep(1)
        options = ["Choose an option", "1", "2", "3"]

        option_var = StringVar()
        option_var.set(options[0])

        option_menu = OptionMenu(root, option_var, *options)
        canvas.create_window(80, 125, window=option_menu)

        submit_button = tk.Button(root, text="Submit", command=upgrade2, height=1, width=5, font=('Arial', '10'))
        canvas.create_window(80, 155, window=submit_button)

        while not upgrade_button_pressed2:
            root.update_idletasks()
            root.update()
        
        upgrade_button_pressed2 = False
    elif player["level"] <= 15:
        def upgrade3():
            global heal_amount, upgrade_button_pressed3, root, option_menu, submit_button

            option_menu.destroy()
            submit_button.destroy()

            upgrade_option3 = option_var.get()
            if upgrade_option3 == "1":
                sleep(1)
                clear()
                print("Adding 10 attack damage to you...")
                player["attack"] += 10
                sleep(3)
                clear()
            elif upgrade_option3 == "2":
                sleep(1)
                clear()
                print("Increasing heal amount by 25...")
                heal_amount += 25
                sleep(3)
                clear()
            elif upgrade_option3 == "3":
                sleep(1)
                clear()
                player["critical_chance"] += 2
                print("Increasing critical chance by 2%...")
                sleep(3)
                clear()
            else:
                sleep(1)
                clear()
                print("No upgrade was added")
                canvas.itemconfig(info_label, text=f"No upgrade was added")
                sleep(2)
                clear()
            
            upgrade_button_pressed3 = True

        print("Tier 3 upgrades")
        print("1. Increase attack damage by 10\n2. Increase healing amount by 25\n3. Increase critical chance by 2%")
        canvas.itemconfig(info_label, text=f"Tier 3 upgrades\n\n1. Increase attack damage by 10\n2. Increase healing amount by 25\n3. Increase critical chance by 2%")
        sleep(1)
        options = ["Choose an option", "1", "2", "3"]

        option_var = StringVar()
        option_var.set(options[0])

        option_menu = OptionMenu(root, option_var, *options)
        canvas.create_window(80, 125, window=option_menu)

        submit_button = tk.Button(root, text="Submit", command=upgrade3, height=1, width=5, font=('Arial', '10'))
        canvas.create_window(80, 155, window=submit_button)

        while not upgrade_button_pressed3:
            root.update_idletasks()
            root.update()

        upgrade_button_pressed3 = False
    elif player["level"] <= 20:
        def upgrade4():
            global heal_amount, upgrade_button_pressed4, root, option_menu, submit_button

            option_menu.destroy()
            submit_button.destroy()

            upgrade_option4 = option_var.get()
            if upgrade_option4 == "1":
                sleep(1)
                clear()
                print("Adding 12.5 attack damage to you...")
                player["attack"] += 12.5
                sleep(3)
                clear()
            elif upgrade_option4 == "2":
                sleep(1)
                clear()
                print("Increasing heal amount by 30...")
                heal_amount += 30
                sleep(3)
                clear()
            elif upgrade_option4 == "3":
                sleep(1)
                clear()
                player["critical_chance"] += 2
                print("Increasing critical chance by 2%...")
                sleep(3)
                clear()
            else:
                sleep(1)
                clear()
                print("No upgrade was added")
                canvas.itemconfig(info_label, text=f"No upgrade was added")
                sleep(2)
                clear()
            
            upgrade_button_pressed4 = True

        print("Tier 4 upgrades")
        print("1. Increase attack damage by 12.5\n2. Increase healing amount by 30\n3. Increase critical chance by 2%")
        canvas.itemconfig(info_label, text=f"Tier 4 upgrades\n\n1. Increase attack damage by 12.5\n2. Increase healing amount by 30\n3. Increase critical chance by 2%")
        sleep(1)
        options = ["Choose an option", "1", "2", "3"]

        option_var = StringVar()
        option_var.set(options[0])

        option_menu = OptionMenu(root, option_var, *options)
        canvas.create_window(80, 125, window=option_menu)

        submit_button = tk.Button(root, text="Submit", command=upgrade4, height=1, width=5, font=('Arial', '10'))
        canvas.create_window(80, 155, window=submit_button)

        while not upgrade_button_pressed4:
            root.update_idletasks()
            root.update()

        upgrade_button_pressed4 = False
    elif player["level"] <= 25:
        def upgrade5():
            global heal_amount, upgrade_button_pressed5, root, option_menu, submit_button

            option_menu.destroy()
            submit_button.destroy()

            upgrade_option5 = option_var.get()
            if upgrade_option5 == "1":
                sleep(1)
                clear()
                print("Adding 12.5 attack damage to you...")
                player["attack"] += 12.5
                sleep(3)
                clear()
            elif upgrade_option5 == "2":
                sleep(1)
                clear()
                print("Increasing heal amount by 30...")
                heal_amount += 30
                sleep(3)
                clear()
            elif upgrade_option5 == "3":
                sleep(1)
                clear()
                player["critical_chance"] += 2
                print("Increasing critical chance by 2%...")
                sleep(3)
                clear()
            else:
                sleep(1)
                clear()
                print("No upgrade was added")
                canvas.itemconfig(info_label, text=f"No upgrade was added")
                sleep(2)
                clear()
            
            upgrade_button_pressed5 = True

        print("Tier 5 upgrades")
        print("1. Increase attack damage by 15\n2. Increase healing amount by 35\n3. Increase critical chance by 3%")
        canvas.itemconfig(info_label, text=f"Tier 5 upgrades\n\n1. Increase attack damage by 15\n2. Increase healing amount by 35\n3. Increase critical chance by 3%")
        sleep(1)
        options = ["Choose an option", "1", "2", "3"]

        option_var = StringVar()
        option_var.set(options[0])

        option_menu = OptionMenu(root, option_var, *options)
        canvas.create_window(80, 125, window=option_menu)

        submit_button = tk.Button(root, text="Submit", command=upgrade5, height=1, width=5, font=('Arial', '10'))
        canvas.create_window(80, 155, window=submit_button)

        while not upgrade_button_pressed5:
            root.update_idletasks()
            root.update()

        upgrade_button_pressed5 = False

def handle_heal():
    global heal_amount

    clear()
    sleep(1)
    print("Healing...\n")
    canvas.itemconfig(info_label, text=f"Healing...")
    sleep(2)
    player["health"] += heal_amount
    print(f"Your health is now at {player['health']}")
    canvas.itemconfig(info_label, text=f"Your health is now at {player['health']}")
    canvas.itemconfig(playerHealth_label, text=f"Your Health: {player['health']}")
    sleep(2)
    clear()

def handle_exit():
    clear()
    print("Thanks for playing!")
    canvas.itemconfig(info_label, text=f"Thanks for playing!")
    sleep(3)
    exit()

def game_loop():
    global heal_amount, running, playerHealth_label, option_chosen, option_var, option_menu, submit_button, button_pressed

    left = "w"
    right = "e"
    up = "n"
    down = "s"
    bottom_left = "sw"
    bottom_right = "se"
    top_left = "nw"
    top_right = "ne"

    try:
        while True:
            enemy = select_enemy()
            fight_enemy(enemy)

            print(f"You healed by {heal_amount} health\n")
            player["health"] += heal_amount
            canvas.itemconfig(info_label, text=f"You healed by {heal_amount} health") 
            canvas.itemconfig(playerHealth_label, text=f"Your Health: {player['health']}")
            sleep(2)
            print(f"You are level {player['level']}, have {player['health']} health left, {player['attack']} attack damage, heal {heal_amount} health per battle, and have a {player['critical_chance']}% chance to crit\n")
            canvas.itemconfig(info_label, text=f"You are level {player['level']}\nhave {player['health']} health left\n{player['attack']} attack damage\nheal {heal_amount} health per battle\nand have a {player['critical_chance']}% chance to crit") 
            sleep(7.5)

            print("Here are your options:\n")
            print(f"1. Continue fighting\n2. Upgrade\n3. Heal again (Heal by {heal_amount})\n4. Leave")
            canvas.itemconfig(info_label, text=f"Here are your option\n\n1. Continue fighting\n2. Upgrade\n3. Heal again (Heal by {heal_amount})\n4. Leave") 

            options = ["Choose an option", "1", "2", "3", "4"]

            option_var = StringVar()
            option_var.set(options[0])

            option_menu = OptionMenu(root, option_var, *options)
            canvas.create_window(80, 125, window=option_menu)

            option_chosen = False

            submit_button = tk.Button(root, text="Submit", command=handle_option, height=1, width=5, font=('Arial', '10'))
            canvas.create_window(80, 155, window=submit_button)

            while not button_pressed:
                root.update_idletasks()
                root.update()

            button_pressed = False
    except Exception as e:
        print(f"Exception caught: {e}")


def start_game():
    global running, start_button

    start_button.destroy()

    if not running:
        running = True
        task_thread = Thread(target=game_loop)
        task_thread.start()

def start_gui():
    global root, start_button

    start_button = tk.Button(root, text="Begin Game", command=start_game, height=2, width=10, font=('Arial', '20'))
    canvas.create_window(250, 450, window=start_button)

    root.mainloop()

start_gui()