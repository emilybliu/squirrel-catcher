# Allison Salata - bwv2qy       Emily Liu - vyj9jn

# Game Description:
# A catcher game: the player uses left and right keys to catch objects falling down the screen. Some objects are
# dangerous and if the player catches them they lose a life. If the player fails to catch a beneficial object they will
# lose a point. If the score drops below 0 the player will lose a life and the score will remain 0 until the player
# catches more objects. When all 3 lives are lost the game is over. The player earns points for catching each non
# hazardous falling item. Game theme: a squirrel is controlled by the player to run back and forth collecting
# acorns (worth 3 points each) and leaves (worth 1 point each) and avoiding bats (lose a life).

import gamebox
import pygame
import random

# Small enough window: our game window will be (500,600). (Required Feature)
camera = gamebox.Camera(500, 600)

# Graphics/ images: we will have a cartoon squirrel (sprite sheet), an acorn image, a leaf image, a bat image(sprite
# sheet), and a background image of a tree. (Required Feature)

# background image citation: fall_background.PNG from https://www.vecteezy.com/vector-art/2773387-fall-in-autumn-season
background = gamebox.from_image(500, 300, "fall_background.PNG")

# squirrel image citation: squirrel_sprite.png from https://rpgtileset.com/sprite/squirrels-sprite-for-rpg-maker-mv/
squirrel_images = gamebox.load_sprite_sheet("squirrel_sprite.png", 1, 3)
squirrel = gamebox.from_image(100, 550, squirrel_images[0])

# bat image citation: bat_sprite_sheet.png from https://opengameart.org/content/animated-rat-and-bat
bat_images = gamebox.load_sprite_sheet('bat_sprite_sheet.png', 1, 10)
bats = [
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), bat_images[0]),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), bat_images[0])
]

# leaf image citation: falling_leaf.png from http://clipart-library.com/free/falling-leaf-png.html
leaves = [
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "falling_leaf.png")
]

# acorn image citation: acorn.png from https://www.clipartmax.com/so/acorn-clipart/
acorns = [
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"),
    gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png")
]

# walls to keep the objects of the game from leaving the sides
walls = [
    gamebox.from_color(0, 400, "black", 2, 2000),
    gamebox.from_color(500, 400, "black", 2, 2000)
]

# variables for squirrel animation
current_squirrel_frame = 0
run_right = False

# variable for bat animation
current_bat_frame = 0

# speed of both acorn and leaf
acorn_leaf_speed = 2

# the score starts at 0, and the lives start at 3
score = 0
lives = 3

# play variable used for reseting the game later
play = False


# User input: Player will use left and right arrow keys to control the squirrel running across the bottom of the
# screen. (Required Feature)

# Sprite Sheet animation: The squirrel running back and forth will be animated using a sprite sheet (Optional
# Feature)


def move_squirrel(keys):
    """
    moves/animates the squirrel using keyboard keys and the sprite sheet. The squirrel flips when it changes direction.
    :param keys: User input of left key and right key
    :return: None
    """
    global current_squirrel_frame, run_right
    squirrel_move = False

    # moving the squirrel left and right and also the squirrel animation will flip.
    if pygame.K_LEFT in keys:
        if run_right:
            squirrel.flip()
            run_right = False
        squirrel.x -= 8
        squirrel_move = True
    if pygame.K_RIGHT in keys:
        if not run_right:
            squirrel.flip()
            run_right = True
        squirrel.x += 8
        squirrel_move = True

    # animates the squirrel to move. If it is not moving, the squirrel image is reset to the stationary image
    if squirrel_move:
        current_squirrel_frame += 0.3
        if current_squirrel_frame >= 2:
            current_squirrel_frame = 0
        squirrel.image = squirrel_images[int(current_squirrel_frame)]
    else:
        squirrel.image = squirrel_images[0]


# Sprite Sheet animation: The bats will be animated to fly using a sprite sheet. (Optional Feature)


def fly_bats():
    """
    Makes the bat flap its wings using sprite sheet animation
    :return: None
    """
    global current_bat_frame
    current_bat_frame += 0.6
    if current_bat_frame >= 9:
        current_bat_frame = 0
    for bat in bats:
        bat.image = bat_images[int(current_bat_frame)]


def move_leaves():
    """
    Makes the leaves fall down the screen. If a leaf touches the squirrel or falls to the bottom of the screen, it
    resets the leaf to the top of the screen. Calculates score by adding 1 to score if the squirrel touches a leaf. If
    leaf reaches the bottom of the screen without being collected, the score decreases by 1
    :return: None
    """
    global score
    # leaves are falling
    for leaf in leaves:
        leaf.speedy = acorn_leaf_speed
        leaf.move_speed()
    # increasing the score and resetting the leaves
    for leaf in leaves:
        if leaf.touches(squirrel) and leaf.y > 540 and int(leaf.x) in range(int(squirrel.x) - 60, int(squirrel.x) + 61):
            score += 1
            if leaf == leaves[0]:
                leaves.remove(leaves[0])
                leaves.insert(0, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[1]:
                leaves.remove(leaves[1])
                leaves.insert(1, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[2]:
                leaves.remove(leaves[2])
                leaves.insert(2, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[3]:
                leaves.remove(leaves[3])
                leaves.insert(3, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[4]:
                leaves.remove(leaves[4])
                leaves.insert(4, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[5]:
                leaves.remove(leaves[5])
                leaves.insert(5, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[6]:
                leaves.remove(leaves[6])
                leaves.insert(6, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[7]:
                leaves.remove(leaves[7])
                leaves.insert(7, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
        # decreasing the score if the leaf is not caught
        if leaf.y >= 615:
            score -= 1
            if leaf == leaves[0]:
                leaves.remove(leaves[0])
                leaves.insert(0, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[1]:
                leaves.remove(leaves[1])
                leaves.insert(1, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[2]:
                leaves.remove(leaves[2])
                leaves.insert(2, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[3]:
                leaves.remove(leaves[3])
                leaves.insert(3, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[4]:
                leaves.remove(leaves[4])
                leaves.insert(4, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[5]:
                leaves.remove(leaves[5])
                leaves.insert(5, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[6]:
                leaves.remove(leaves[6])
                leaves.insert(6, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            if leaf == leaves[7]:
                leaves.remove(leaves[7])
                leaves.insert(7, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))


def move_acorns():
    """
    Makes the acorns fall down the screen. If an acorn touches the squirrel or falls to the bottom of the screen, it
    resets the acorn to the top of the screen. Calculates score by adding 3 to score if the squirrel touches an acorn.
    If an acorn reaches the bottom of the screen without being collected, the score decreases by 3
    :return: None
    """
    global score
    # acorns are falling
    for acorn in acorns:
        acorn.speedy = acorn_leaf_speed
        acorn.move_speed()
    # increasing the score and resetting the acorns
    for acorn in acorns:
        if acorn.touches(squirrel) and acorn.y > 540 and int(acorn.x) in range(int(squirrel.x) - 60,
                                                                               int(squirrel.x) + 61):
            score += 3
            if acorn == acorns[0]:
                acorns.remove(acorns[0])
                acorns.insert(0, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))
            if acorn == acorns[1]:
                acorns.remove(acorns[1])
                acorns.insert(1, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))
            if acorn == acorns[2]:
                acorns.remove(acorns[2])
                acorns.insert(2, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))
            if acorn == acorns[3]:
                acorns.remove(acorns[3])
                acorns.insert(3, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))

        # decreasing the score if the acorn is not caught
        if acorn.y >= 615:
            score -= 3
            if acorn == acorns[0]:
                acorns.remove(acorns[0])
                acorns.insert(0, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))
            if acorn == acorns[1]:
                acorns.remove(acorns[1])
                acorns.insert(1, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))
            if acorn == acorns[2]:
                acorns.remove(acorns[2])
                acorns.insert(2, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))
            if acorn == acorns[3]:
                acorns.remove(acorns[3])
                acorns.insert(3, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))


# Enemies: The bats are the enemies. If the squirrel hits a bat it loses a life. The bats will be able to fly around
# the screen on their own while the player tries to avoid them and collect acorns/leaves. (Optional Feature)


def move_bats():
    """
    Moves the bats by using a random x and y speed (bats are moving on their own).
    :return: None
    """
    global lives
    for bat in bats:
        bat.speedy = random.randrange(3, 6)
        bat.speedx = random.randrange(-15, 16)
        bat.move_speed()
    # bats will not go over the walls and will reset bats once they hit the bottom of the screen
    for bat in bats:
        for wall in walls:
            if bat.touches(wall):
                bat.move_to_stop_overlapping(wall)
        if bat.y >= 615:
            if bat == bats[0]:
                bats.remove(bats[0])
                bats.insert(0, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), bat_images[0]))
            if bat == bats[1]:
                bats.remove(bats[1])
                bats.insert(1, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), bat_images[0]))

        # loses one life when a bat touches the squirrel and resets the bat
        if bat.touches(squirrel) and bat.y > 540 and int(bat.x) in range(int(squirrel.x) - 50, int(squirrel.x) + 51):
            lives -= 1
            if bat == bats[0]:
                bats.remove(bats[0])
                bats.insert(0, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), bat_images[0]))
            if bat == bats[1]:
                bats.remove(bats[1])
                bats.insert(1, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), bat_images[0]))
    # bat animation
    fly_bats()


def setup():
    """
    Allows move_bats, move_acorns, and move_leaves to be called using one function. Sets play equal to True
    :return:
    """
    global score, lives, play
    move_bats()
    move_acorns()
    move_leaves()
    play = True


camera.draw(background)

# Start Screen: Will display the game name "Squirrel Catcher" and the basic instructions "Use left and right arrow
# keys to collect acorns and leaves, avoid the bats. Press the space key to start." Screen will also display our names
# and student ids. (Required Feature)
camera.draw(gamebox.from_text(250, 100, "Squirrel Catcher", 80, "black", bold=False))
camera.draw(gamebox.from_text(250, 200, "Use left and right arrow keys to collect", 35, "black", bold=False))
camera.draw(gamebox.from_text(250, 225, "acorns and leaves, avoid the bats.", 35, "black", bold=False))
camera.draw(gamebox.from_text(250, 300, "Press 'space' to start", 40, "black", bold=False))
camera.draw(gamebox.from_text(400, 555, "Allison Salata - bwv2qy", 25, "Red", bold=False))
camera.draw(gamebox.from_text(400, 575, "Emily Liu - vyj9jn", 25, "Red", bold=False))


def tick(keys):
    """
    draws the gameboxes
    :param keys: keyboard keys
    :return: None
    """
    global score, lives, play, current_squirrel_frame

    # press space to play
    if pygame.K_SPACE in keys:
        play = True

    if play:
        # makes sure squirrel does not overlap a wall
        for wall in walls:
            if squirrel.touches(wall):
                squirrel.move_to_stop_overlapping(wall)

        move_squirrel(keys)

        setup()

        # a life is lost when the score is negative
        if score < 0:
            score = 0
            lives -= 1

        camera.clear('black')
        camera.draw(background)

        # draws the gameboxes
        for wall in walls:
            camera.draw(wall)
        camera.draw(squirrel)
        for bat in bats:
            camera.draw(bat)
        for leaf in leaves:
            camera.draw(leaf)
        for acorn in acorns:
            camera.draw(acorn)

        # Health Bar: There are 3 lives, represented by 3 hearts shown in the corner of the screen. (Optional Feature)
        for i in range(lives):
            heart = gamebox.from_image(475, 25, 'heart.png')
            heart.x -= 50 * i
            heart.scale_by(0.5)
            camera.draw(heart)
        camera.draw("Score:" + str(int(score)), 36, "green", 65, 30)
        # Game Over: the game ends when the player loses all 3 lives. When the game ends the player will be shown a
        # game over screen that displays the score and an option to play again. (Required Feature)
        if lives == 0:
            camera.draw(gamebox.from_text(250, 200, "Game Over!", 80, "black", bold=False))
            camera.draw(gamebox.from_text(250, 300, "Press 'r' to restart", 40, "black", bold=False))
            play = False

    else:
        # Restart feature: when game over screen is shown there will be an option to "Press 'r' to restart" (Optional
        # Feature)
        if pygame.K_r in keys:
            camera.clear('black')
            #acorns, leaves, and bats, are reset
            for i in range(0, 4):
                acorns.remove(acorns[i])
                acorns.insert(i, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), "acorn.png"))
            for i in range(0, 8):
                leaves.remove(leaves[i])
                leaves.insert(i, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0),
                                                    "falling_leaf.png"))
            for i in range(0, 2):
                bats.remove(bats[i])
                bats.insert(i, gamebox.from_image(random.randrange(15, 376), random.randrange(-800, 0), bat_images[0]))

            # lives, squirrel, and scores are reset and play is set to True
            squirrel.x = 100
            lives = 3
            score = 0
            play = True
            setup()

    camera.display()


gamebox.timer_loop(30, tick)