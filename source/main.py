import pygame
import picross
import characterselect
import endgame

# Initialize Pygame
pygame.init()
pygame.mixer.init(44100, -16, 2, 4096)
start0 = pygame.mixer.Sound('source/music/start0.wav')
extend0 = pygame.mixer.Sound('source/music/extend0.wav')
extend0.set_volume(0.5)

char_bubble_waffle = {
    # 0 for bubble waffle,  1 for bubble chocolate, 2 for green bubble tea, 3 for bubble gum
    'effect' : 0,
    # between 1 and 0
    'multiplier' : 0.5, 

    'win_quote' : 'The was a nice try... Punk.',
    'effect_description' : "Blow up the enemy's board!", 
    'character_description' : 'The nomadic fiend', 

    'neutral_sprite' : 'source/art/0_idle.png',
    'hit_sprite' : 'source/art/0_hurt.png',
    'attack_sprite' : 'source/art/0_attack.png', 
    'bar_sprite' : 'source/art/0_border.png',
    'progression_meter_sprite' : 'source/art/0_uncharged.png', 
    'charged_meter_sprite' : 'source/art/0_charged.png', 

    'colour_rgb' : (255, 252, 227)
}

char_bubble_chocolate = {
    # 0 for bubble waffle,  1 for bubble chocolate, 2 for green bubble tea, 3 for bubble gum
    'effect' : 1,
    # between 1 and 0
    'multiplier' : 1.0, 

    'win_quote' : 'The was a nice try... Punk.',
    'effect_description' : "Blow up the enemy's board!", 
    'character_description' : 'The nomadic fiend', 

    'neutral_sprite' : 'source/art/1_idle.png',
    'hit_sprite' : 'source/art/1_hurt.png',
    'attack_sprite' : "source/art/1_attack.png", 
    'bar_sprite' : 'source/art/1_border.png',
    'progression_meter_sprite' : 'source/art/1_uncharged.png', 
    'charged_meter_sprite' : 'source/art/1_charged.png', 

    'colour_rgb' : (255, 227, 227)
}

char_bubble_tea = {
    # 0 for bubble waffle,  1 for bubble chocolate, 2 for green bubble tea, 3 for bubble gum
    'effect' : 2,
    # between 1 and 0
    'multiplier' : 1.0, 

    'win_quote' : 'The was a nice try... Punk.',
    'effect_description' : "Blow up the enemy's board!", 
    'character_description' : 'The nomadic fiend', 

    'neutral_sprite' : 'source/art/2_idle.png',
    'hit_sprite' : 'source/art/2_hurt.png',
    'attack_sprite' : "source/art/2_attack.png", 
    'bar_sprite' : 'source/art/2_border.png',
    'progression_meter_sprite' : 'source/art/2_uncharged.png', 
    'charged_meter_sprite' : 'source/art/2_charged.png', 

    'colour_rgb' : (228, 255, 227)
}

char_bubble_gum = {
    # 0 for bubble waffle,  1 for bubble chocolate, 2 for green bubble tea, 3 for bubble gum
    'effect' : 3,
    # between 1 and 0
    'multiplier' : 0.5, 

    'win_quote' : 'The was a nice try... Punk.',
    'effect_description' : "Blow up the enemy's board!", 
    'character_description' : 'The nomadic fiend', 

    'neutral_sprite' : 'source/art/3_idle.png',
    'hit_sprite' : 'source/art/3_hurt.png',
    'attack_sprite' : "source/art/3_attack.png", 
    'bar_sprite' : 'source/art/3_border.png',
    'progression_meter_sprite' : 'source/art/3_uncharged.png', 
    'charged_meter_sprite' : 'source/art/3_charged.png', 

    'colour_rgb' : (239, 227, 255)
}


characters = {
    '0' : char_bubble_waffle,
    '1' : char_bubble_chocolate,
    '2' : char_bubble_tea,
    '3' : char_bubble_gum
}

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Picross")

# Can be one of: 
# - "CHARACTER_SELECT"
# - "PICROSS"
# - "END_SCREEN"
GAME_STATE = "CHARACTER_SELECT"

VOLUME = 1.0
pygame.mixer.music.set_volume(VOLUME)

while True:    
    if GAME_STATE == "CHARACTER_SELECT":
        extend0.play(loops=-1) 
        characters_chosen = characterselect.character_select_screen()
        GAME_STATE = 'PICROSS'
    elif GAME_STATE == "PICROSS":
        extend0.stop()
        extend0.play(loops=-1) 
        winner = picross.start_picross(characters[characters_chosen[0]], characters[characters_chosen[1]])
    elif GAME_STATE == "END_SCREEN":
        extend0.stop()
        extend0.play()
        endgame.end_screen(characters["2"])
