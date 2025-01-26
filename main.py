import pygame
import picross
import characterselect

# Initialize Pygame
pygame.init()
pygame.mixer.init(44100, -16, 2, 4096)
pygame.mixer.music.load("music\start0.wav")

character_1 = {
    # 0 for bubble waffle,  1 for bubble chocolate, 2 for green bubble tea, 3 for bubble gum
    'effect' : 0,
    # between 1 and 0
    'multiplier' : 0.75, 

    'win_quote' : 'The was a nice try... Punk.',
    'effect_description' : "Blow up the enemy's board!", 
    'character_description' : 'The nomadic fiend', 

    'neutral_sprite' : 'art/0_idle.png',
    'hit_sprite' : 'art/0_hurt.png',
    'attack_sprite' : 'art/2_attack.png', 
    'bar_sprite' : 'art/border.png',
    'progression_meter_sprite' : 'art/0_uncharged.png', 
    'charged_meter_sprite' : 'art/0_charged.png', 

    'colour_hexcodes' : '#fffce3'
}

character_2 = {
    # 0 for bubble waffle,  1 for bubble chocolate, 2 for green bubble tea, 3 for bubble gum
    'effect' : 1,
    # between 1 and 0
    'multiplier' : 0.75, 

    'win_quote' : 'AAAAAAAAAAAAAAAAAAAAAA',
    'effect_description' : "AAAAAAAAAAAAAAAAAAAAAA", 
    'character_description' : 'AAAAAAAAAAAAAAAAAAAAAA', 

    'neutral_sprite' : 'art/0_idle.png',
    'hit_sprite' : 'art/0_hurt.png',
    'attack_sprite' : "art/2_attack.png", 
    'bar_sprite' : 'art/border.png',
    'progression_meter_sprite' : 'art.0_uncharged.png', 
    'charged_meter_sprite' : 'art/0_charged.png', 

    'colour_hexcodes' : '#fffce3'
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
        pygame.mixer.music.play(-1,0,0)
        characters_chosen = characterselect.character_select_screen()
        GAME_STATE = 'PICROSS'
    elif GAME_STATE == "PICROSS":
        pygame.mixer.music.play(-1,0,0)
        picross.start_picross(characters_chosen[0], characters_chosen[1])
    elif GAME_STATE == "END_SCREEN":
        pass
