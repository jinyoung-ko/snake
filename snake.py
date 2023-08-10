# Import modules
import pygame
import time
import random

pygame.init()

# Create the color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKBLUE = (0, 134, 139)
LIGHTBLUE = (0, 255, 255)

# Height / width of screen
displayWidth      = 800
displayHeight     = 600
displayGameHeight = displayHeight - 100

# Display screen & title
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Snake")

# Set Icon
icon = pygame.image.load("images/apple.png")
pygame.display.set_icon(icon)

# Images
backgroundImg  = pygame.image.load("images/background.jpg") # 800px x 600px
imgHead        = pygame.image.load("images/snakeHead.png")  # 20px x 20px
imgApple       = pygame.image.load("images/apple.png")      # 20px x 20px
imgBody        = pygame.image.load("images/snakeBody.png")  # 20px x 20px

# Clock for frames, snake size, frame per sec, apple size, direction
clock          = pygame.time.Clock()
snakeSize      = 20
framePerSec    = 15
appleThickness = 20

def background():
        button("start",     70,  530, 90, 20, LIGHTBLUE, DARKBLUE, WHITE, action = "start")
        button("help",      70,  560, 90, 20, LIGHTBLUE, DARKBLUE, WHITE, action = "help")
        button("pause/play",630, 530, 90, 20, LIGHTBLUE, DARKBLUE, WHITE, action = "pause/play")
        button("quit",      630, 560, 90, 20, LIGHTBLUE, DARKBLUE, WHITE, action = "quit")

"""
------------------------------------------------------------------------------------------
gameIntro
------------------------------------------------------------------------------------------
This function displays the introduction of snake. The user can either exit the game
by pressing Q for quit or the X button. Also the user can press c to continue and
actually play the game.

Returns: nothing (display intro)
------------------------------------------------------------------------------------------
"""
def gameIntro():
    
    intro = True

    # Keep display the intro while the user has not exited or continued
    while intro:    
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Continue snake game
                if event.key ==  pygame.K_c:
                    intro = False
                    
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # Display background and rules to user
        gameDisplay.blit(backgroundImg, (0, 0))
        messageToScreen("Welcome to Snake",
                        WHITE,
                        -100,
                        80)
        messageToScreen("The objective of the game is to eat the apples",
                        WHITE,
                        -30)
        messageToScreen("The more apples you eat the longer you get",
                        WHITE,
                        10)
        messageToScreen("If you run into yourself or the edges, you die!",
                        WHITE,
                        50)
        messageToScreen("Press C to play, P to pause, or Q to quit",
                        WHITE,
                        180)
        
        background()

        pygame.display.update()
        clock.tick(15)

"""
------------------------------------------------------------------------------------------
textObjects
------------------------------------------------------------------------------------------
This function renders the message to display

Returns: a rendered message (text surface and text rectangle)
------------------------------------------------------------------------------------------
"""
def textObjects(text, color, size):

    # Font
    pygame.font.init()
    theFont = pygame.font.Font("font/DS-DIGI.ttf", size)
    textSurface = theFont.render(text, True, color)

    # Text surface, and text rectangle (return tuple)
    return textSurface, textSurface.get_rect()

"""
------------------------------------------------------------------------------------------
button
------------------------------------------------------------------------------------------
This function checks the hover of the button (interactive)

Returns: nothing (display button & hover)
------------------------------------------------------------------------------------------
"""
def button(text, x, y, width, height, inactiveColor, activeColor, textColor = BLACK, action = None):

    # Get mouse position
    cur   = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, activeColor, (x, y, width, height))

        if click[0] == 1 and action != None:
            if action == "quit":
               pygame.quit()
               quit()

            if action == "pause/play":
               pause()

            if action == "start":
               gameLoop()

            if action == "help":
                pass
    else:
        #pygame.draw.circle(gameDisplay, inactiveColor, (x, y), width)
        pygame.draw.rect(gameDisplay, inactiveColor, (x, y, width, height), 2)

    textToButton(text, textColor, x, y, width, height)
    

"""
------------------------------------------------------------------------------------------
textToButton
------------------------------------------------------------------------------------------
This function puts text on button

Returns: nothing (display button message)
------------------------------------------------------------------------------------------
"""
def textToButton(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size = 16):

    textSurf, textRect = textObjects(msg, color, size)
    textRect.center    = ((buttonX + (buttonWidth / 2)), buttonY + (buttonHeight / 2))
    gameDisplay.blit(textSurf, textRect)

"""
------------------------------------------------------------------------------------------
messageToScreen
------------------------------------------------------------------------------------------
This function actually display screen message in center (have a default parameter)

Returns: nothing (display screen message)
------------------------------------------------------------------------------------------
"""
def messageToScreen(msg, color, yDisplace = 0, size = 25):
    textSurf, textRect = textObjects(msg, color, size)
    textRect.center    = (displayWidth / 2), (displayGameHeight / 2) + yDisplace
    gameDisplay.blit(textSurf, textRect)

"""
------------------------------------------------------------------------------------------
checkRandAppLoc
------------------------------------------------------------------------------------------
This function goes through the entire snake list and checks if the random apple
location is in the same position as the snake.

Returns: valid (boolean)
------------------------------------------------------------------------------------------
"""
def checkRandAppLoc(snakeList, randAppleX, randAppleY):
    invalid = False

    for xNy in snakeList:
        if xNy[0] == randAppleX and xNy[1] == randAppleY:
            invalid = True
    
    return invalid

"""
------------------------------------------------------------------------------------------
randAppleGen
------------------------------------------------------------------------------------------
This function is a random apple generator. It gets the x & y coordinates for where
the random apple should go. It will be in increments of 20px. (because the snake & apple
will be both 20px)

Returns: the x & y coordinates of the random apple
------------------------------------------------------------------------------------------
"""
def randAppleGen(snakeList):

    # Don't put the apple where the snake is
    invalid = True

    while invalid:
        randAppleX = round(random.randrange(0, displayWidth - appleThickness) / 20.0) * 20.0
        randAppleY = round(random.randrange(0, displayGameHeight - appleThickness) / 20.0) * 20.0
        invalid      = checkRandAppLoc(snakeList, randAppleX, randAppleY)

    return randAppleX, randAppleY


"""
------------------------------------------------------------------------------------------
snake
------------------------------------------------------------------------------------------
This function draws the entire snake. It rotates the snake accordingly.

Returns: nothing (draws snake onto the screen)
------------------------------------------------------------------------------------------
"""
def snake(snakeSize, snakeList):
    
    # Rotate the head of the snake (actually moves counter clockwise)
    if direction == "right":
        head = pygame.transform.rotate(imgHead, 270)
        
    elif direction == "left":
        head = pygame.transform.rotate(imgHead, 90)

    elif direction == "up":
        head = imgHead

    elif direction == "down":
        head = pygame.transform.rotate(imgHead, 180)
    
    # Draw head of the snake
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    # 2 element list (everythinge except the last element - head)
    for xNy in snakeList[:-1]:
        gameDisplay.blit(imgBody, (xNy[0], xNy[1], snakeSize, snakeSize))
        
"""
------------------------------------------------------------------------------------------
score
------------------------------------------------------------------------------------------
This function render score and display it to the screen

Returns: nothing (draws score onto the screen)
------------------------------------------------------------------------------------------
"""
def score(theScore):

    messageToScreen("SCORE", WHITE, 290, 30)
    messageToScreen(str(theScore), WHITE, 320, 25)

"""
------------------------------------------------------------------------------------------
pause
------------------------------------------------------------------------------------------
This function allows the user to pause the game

Returns: nothing (pauses the game until unpaused)
------------------------------------------------------------------------------------------
"""
def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.blit(backgroundImg, (0, 0))
        messageToScreen("PAUSED",
                        WHITE,
                        -100,
                        100)
        messageToScreen("Press C to continue or Q to quit.",
                        WHITE,
                        25)

        background()
        
        pygame.display.update()
        clock.tick(5)

"""
------------------------------------------------------------------------------------------
gameLoop
------------------------------------------------------------------------------------------
This function is basically the structure of the entire game. The entire snake game
will be running until the user decides to exit the game.

Returns: nothing (keep playing snake until exit)
------------------------------------------------------------------------------------------
"""    
def gameLoop():

    # Exit the entire game and when gameover
    gameExit = False
    gameOver = False

    global direction
    direction      = "right"
    
    # Snake x and y position. The speed (movement) of the snake x & y position
    leadSnakeX  = round((displayWidth / 2) / 20.0) * 20.0
    leadSnakeY  = round((displayGameHeight / 2) / 20.0) * 20.0
    leadChangeX = 20
    leadChangeY = 0

    # Snake List (all parts of the snake)
    snakeList   = []
    snakeLength = 1

    # Call random apple generator
    randAppleX, randAppleY = randAppleGen(snakeList)

    # Game Exit to exit entire game
    while not gameExit:

        # Check if the game is over or not
        if gameOver == True:
            messageToScreen("GAME OVER",
                        WHITE,
                        -100,
                        100)
            messageToScreen("Press C to continue or Q to quit.",
                        WHITE,
                        25)
            pygame.display.update()

            # Keep looping game over until get valid input (quit game or continue)
            while gameOver == True:         
                for event in pygame.event.get():                
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False

                        if event.key == pygame.K_c:
                            gameLoop()

        # Game Exit check keys
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                gameExit = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction   = "left"
                    leadChangeX = -snakeSize
                    leadChangeY = 0
                    
                elif event.key == pygame.K_RIGHT:
                    direction   = "right"
                    leadChangeX = snakeSize
                    leadChangeY = 0
                    
                elif event.key == pygame.K_UP:
                    direction   = "up"
                    leadChangeX = 0                   
                    leadChangeY = -snakeSize                

                elif event.key == pygame.K_DOWN:
                    direction   = "down"
                    leadChangeX = 0
                    leadChangeY = snakeSize
                    
                elif event.key == pygame.K_p:
                    pause()

        # Check game boundaries
        if(leadSnakeX >= displayWidth or leadSnakeX < 0 or
           leadSnakeY >= displayGameHeight or leadSnakeY < 0):
            gameOver = True

        if not gameOver:
            # Movement of snake (the speed)
            leadSnakeX += leadChangeX
            leadSnakeY += leadChangeY

            # Display the background
            gameDisplay.blit(backgroundImg, (0, 0))

            # Display the random apple
            gameDisplay.blit(imgApple, (randAppleX, randAppleY))

            # Add snake head position to snake head. Then add the snake head to head of snake list
            snakeHead = []
            snakeHead.append(leadSnakeX)
            snakeHead.append(leadSnakeY)
            snakeList.append(snakeHead)

            # Only draw snake list (dont draw extra snake length)
            if len(snakeList) > snakeLength:
                del snakeList[0]

            # Check if snake head collides into itself
            for eachSegment in snakeList[:-1]:
                if eachSegment == snakeHead:
                    gameOver = True

            # Call the snake function to draw the snake onto the screen
            snake(snakeSize, snakeList)

            # Call score function to display the current score
            score(snakeLength - 1)

            background()

            # Update the entire screen
            pygame.display.update()

            # Check if ate apple
            if (leadSnakeX >= randAppleX and leadSnakeX < randAppleX + appleThickness or
                leadSnakeX + snakeSize > randAppleX and
                leadSnakeX + snakeSize < randAppleX + appleThickness):

                if (leadSnakeY >= randAppleY and leadSnakeY < randAppleY + appleThickness):
                    randAppleX, randAppleY = randAppleGen(snakeList)
                    snakeLength += 1

                elif (leadSnakeY + snakeSize > randAppleY and
                      leadSnakeY + snakeSize < randAppleY + appleThickness):
                    randAppleX, randAppleY = randAppleGen(snakeList)
                    snakeLength += 1

            # Add the speed
            clock.tick(framePerSec)

    pygame.quit()
    quit()

# Main Starts here. gall function
gameIntro()
gameLoop()
