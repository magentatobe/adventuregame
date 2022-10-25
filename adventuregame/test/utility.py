#!/usr/bin/python3

import os
import tempfile

import iniconfig

__name__ = 'adventuregame.utility'


# dungeon map
#
# Room_2,1 xx Room_2,2
#     ||          ||
# Room_1,1 xx Room 2,1

Doors_Ini_Config_Text = """
[Room_1,1_x_Room_1,2]
title=wooden door
description=This door is made of wooden planks secured together with iron divots.
door_type=wooden_door
is_locked=false
is_closed=true
closable=true

[Room_1,1_x_Room_2,1]
title=iron door
description=This door is bound in iron plates with a small barred window set up high.
door_type=iron door
is_locked=true
is_closed=true
closable=true

[Room_1,2_x_Room_2,2]
title=doorway
description=This open doorway is outlined by a stone arch set into the wall.
door_type=doorway
is_locked=false
is_closed=false
closable=false

[Room_2,1_x_Room_2,2]
title=iron door
description=This door is bound in iron plates with a small barred window set up high.
door_type=iron door
is_locked=true
is_closed=true
closable=true
"""

Items_Ini_Config_Text = """
[Short_Sword]
attack_bonus=0
damage=1d8
description=A smaller sword with a short blade and a narrower grip.
item_type=weapon
thief_can_use=true
title=short sword
value=10
warrior_can_use=true
weight=2

[Rapier]
attack_bonus=0
damage=1d8
description=A slender, sharply pointed blade with a basket hilt.
item_type=weapon
thief_can_use=true
title=rapier
value=25
warrior_can_use=true
weight=2

[Mace]
attack_bonus=0
damage=1d6
description=A hefty, blunt instrument with a dully-spiked weighted metal head.
item_type=weapon
priest_can_use=true
title=mace
value=5
warrior_can_use=true
weight=4

[Small_Leather_Armor]
armor_bonus=2
description=A suit of leather armor designed for a humanoid of 4 feet in height.
item_type=armor
title=small leather armor
value=10
weight=7.5

[Longsword]
attack_bonus=0
damage=1d8
description=A hefty sword with a long blade, a broad hilt and a leathern grip.
item_type=weapon
title=longsword
value=15
warrior_can_use=true
weight=3

[Staff]
attack_bonus=0
damage=1d6
description=A balanced pole 6 feet in length with metal-shod ends.
item_type=weapon
mage_can_use=true
title=staff
value=0.2
warrior_can_use=true
weight=4

[Dagger]
attack_bonus=0
damage=1d4
description=A simple bladed weapon with a plain iron hilt and a notched edge.
mage_can_use=true
priest_can_use=true
thief_can_use=true
title=dagger
item_type=weapon
value=2
warrior_can_use=true
weight=1

[Warhammer]
attack_bonus=0
damage=1d8
description=A heavy hammer with a heavy iron head with a tapered striking point and a long leather-wrapped hast.
item_type=weapon
priest_can_use==true
title=warhammer
warrior_can_use=true
weight=5

[Studded_Leather]
armor_bonus=2
description=A suit of fire-hardened leather plates and padding that provides some protection from attack.
item_type=armor
thief_can_use=true
title=studded leather armor
value=45
warrior_can_use=true
weight=15

[Shield]
armor_bonus=2
description=A broad panel of leather-bound wood with a metal rim that is useful for sheltering behind.
item_type=shield
priest_can_use=true
title=shield
value=10
warrior_can_use=true
weight=6

[Scale_Mail]
armor_bonus=4
description=A suit of small steel scales linked together in a flexible plating that provides strong protection from attack.
item_type=armor
priest_can_use=true
title=scale mail armor
value=50
warrior_can_use=true
weight=45

[Magic_Sword]
attack_bonus=3
damage=1d12+3
description=A magic sword with a palpable magic aura and an unnaturally sharp blade.
item_type=weapon
title=magic sword
value=15
warrior_can_use=true
weight=3

[Magic_Wand]
attack_bonus=3
damage=2d12+3
description=A palpably magical tapered length of polished ash wood tipped with a glowing red carnelian gem.
item_type=wand
mage_can_use=true
title=magic wand
value=100
weight=0.5

[Mana_Potion]
description=A small, stoppered bottle that contains a pungeant but drinkable blue liquid with a discernable magic aura.
item_type=consumable
mage_can_use=true
priest_can_use=true
title=mana potion
value=25
weight=.1

[Health_Potion]
description=A small, stoppered bottle that contains a pungeant but drinkable red liquid with a discernable magic aura.
item_type=consumable
mage_can_use=true
priest_can_use=true
thief_can_use=true
title=health potion
value=25
warrior_can_use=true
weight=.1

[Gold_Coin]
description=A small shiny gold coin imprinted with an indistinct bust on one side and a worn state seal on the other.
item_type=coin
title=gold coin
value=1
weight=0.02
"""

Rooms_Ini_Config_Text = """
[Room_1,1]
description=Entrance room
east_exit=Room_1,2
is_entrance=true
north_exit=Room_2,1
title=Southwest dungeon room
creature_here=Kobold_Trysk
container_here=Wooden_Chest_1
items_here=[1xMana_Potion,2xHealth_Potion]

[Room_1,2]
description=Nondescript room
north_exit=Room_2,2
title=Southeast dungeon room
west_exit=Room_1,1

[Room_2,1]
description=Nondescript room
east_exit=Room_2,2
south_exit=Room_1,1
title=Northwest dungeon room

[Room_2,2]
description=Exit room
is_exit=true
south_exit=Room_1,2
title=Northeast dungeon room
west_exit=Room_2,1
"""

Chests_Ini_Config_Text = """
[Wooden_Chest_1]
contents=[20xGold_Coin,1xWarhammer,1xMana_Potion]
description=This small, serviceable chest is made of wooden slat bounds within an iron framing, and features a sturdy-looking lock.
is_locked=true
is_closed=true
container_type=chest
title=wooden chest
"""

Creatures_Ini_Config_Text = """
[Kobold_Trysk]
# This creature was adapted from the Dungeons & Dragons 3rd edition _Monster Manual_, p.123.
armor_equipped=Small_Leather_Armor
base_hit_points=20
character_class=Thief
character_name=Trysk
charisma=8
constitution=10
description_dead=This diminuitive draconic humanoid is recently slain.
description=This diminuitive draconic humanoid is dressed in leather armor and has a short sword at its hip. It eyes you warily.
dexterity=13
intelligence=10
inventory_items=[1xShort_Sword,1xSmall_Leather_Armor,30xGold_Coin,1xHealth_Potion]
species=Kobold
strength=9
title=kobold
weapon_equipped=Short_Sword
wisdom=9

[Sorcerer_Ardren]
# This creature was adapted from the Dungeons & Dragons 3rd edition _Enemies & Allies_, p.55
base_hit_points=30
base_mana_points=20
character_class=Thief
character_name=Ardren
charisma=18
constitution=15
description_dead=This dead half-elf is dressed in breeches but shirtless. He is recently slain and has the pallor of death.
description=Stripped to the waist and inscribed with dragon chest tattoos, this half-elf is clearly a sorcerer.
dexterity=16
intelligence=10
inventory_items=[2xMana_Potion,1xDagger,10xGold_Coin]
magic_key_stat=charisma
species=human
strength=8
title=sorcerer
weapon_equipped=Dagger
wisdom=12
"""


def create_temp_ini_file_and_instance_IniConfig(ini_config_text):
    _, temp_ini_config_file = tempfile.mkstemp(suffix='.ini')
    temp_ini_config_fh = open(temp_ini_config_file, 'w')
    temp_ini_config_fh.write(ini_config_text)
    temp_ini_config_fh.close()
    ini_config_obj = iniconfig.IniConfig(temp_ini_config_file)
    os.remove(temp_ini_config_file)
    return ini_config_obj