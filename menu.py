#!/usr/bin/env python2
# Import libraries
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
    import pygame, sys, singleplayer, settings
    from pygame.locals import *

except:
    import pygame, sys, singleplayer, settings
    from pygame.locals import *


def launch():
    
    # Initialize pygame
    pygame.init()

    # Initialize the pygame font module
    pygame.font.init()
    
    # Set the width and height of the window
    width, height = int(pygame.display.Info().current_w), int(pygame.display.Info().current_h)
    # Create the window
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    # Set title
    OurTitle = "Candy Mountain"
    pygame.display.set_caption(OurTitle)
    
    
    # Set choice
    choice = 1
    Schoice = 1
    MorS = "main"
    # Set 1/12 height
    height12 = height/12
    
    # Load images
    # Load the background image
    grass = pygame.image.load("resources/images/grass.png")

    # Set display mode
    prevFS = settings.getFullscreen()
    if settings.getFullscreen() == True:
        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    elif settings.getFullscreen() == False:
        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)

    
    # Keep looping through
    while True:
        # Set display mode if changed
        if prevFS != settings.getFullscreen():
            if settings.getFullscreen() == True:
                screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
                prevFS = settings.getFullscreen()
            elif settings.getFullscreen() == False:
                screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
                prevFS = settings.getFullscreen()

        # Clear the screen before drawing it again
        screen.fill(0)
        # Draw the background
        for x in range(width/grass.get_width()+1):
            for y in range(height/grass.get_height()+1):
                screen.blit(grass,(x*100,y*100))
    
        # Loop through the events
        for event in pygame.event.get():
            # Check if the event is the X button 
            if event.type == pygame.QUIT:
                # If it is quit the game
                pygame.quit()
                sys.exit()
            # Check if a key is pressed
            elif event.type == pygame.KEYDOWN:
                # Check if arrow down is pressed
                if event.key == K_DOWN:
                    if MorS == "main":
                        if choice == 1:
                            choice = 2
                        elif choice == 2:
                            choice = 3
                        elif choice == 3:
                            choice = 1
                    elif MorS == "settings":
                        if Schoice == 1:
                            Schoice = 2
                        elif Schoice == 2:
                            Schoice = 1
                # Check if arrow up is pressed
                elif event.key == K_UP:
                    if MorS == "main":
                        if choice == 1:
                            choice = 3
                        elif choice == 2:
                            choice = 1
                        elif choice == 3:
                            choice = 2
                    elif MorS == "settings":
                        if Schoice == 1:
                            Schoice = 2
                        elif Schoice == 2:
                            Schoice = 1
                # Check if return is pressed
                elif event.key == K_RETURN:
                    if MorS == "main":
                        if choice == 1:
                            singleplayer.play()
                        elif choice == 2:
                            MorS = "settings"
                        elif choice == 3:
                            pygame.quit()
                            sys.exit()
                    elif MorS == "settings":
                        if Schoice == 1:
                            settings.changeFullscreen()
                        elif Schoice == 2:
                            MorS = "main"
                # Quit by pressing escape
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Fullscreen by pressing F4
                elif event.key == K_F4:
                    settings.changeFullscreen()

    
        # Set font
        font = pygame.font.Font("freesansbold.ttf", 24)
        bigfont = pygame.font.Font("freesansbold.ttf", 48)
    
        if MorS == "main":
            # Check for cursor
            if choice == 1:
                spText = "-- Single Player --"
                stText = "Settings"
                xtText = "Exit"
            elif choice == 2:
                spText = "Single Player"
                stText = "-- Settings --"
                xtText = "Exit"
            elif choice == 3:
                spText = "Single Player"
                stText = "Settings"
                xtText = "-- Exit --"
    
            # Render text
            # Render title text
            title = bigfont.render(OurTitle, True, (0,0,0))
            titleRect = title.get_rect()
            titleRect.centerx = screen.get_rect().centerx
            titleRect.centery = height12*2
            # Render single player text
            sp = font.render(spText, True, (0,0,0))
            spRect = sp.get_rect()
            spRect.centerx = screen.get_rect().centerx
            spRect.centery = height12*5
            # Render settings text
            st = font.render(stText, True, (0,0,0))
            stRect = st.get_rect()
            stRect.centerx = screen.get_rect().centerx
            stRect.centery = height12*6
            # Render exit text
            xt = font.render(xtText, True, (0,0,0))
            xtRect = xt.get_rect()
            xtRect.centerx = screen.get_rect().centerx
            xtRect.centery = height12*7
    
            # Draw text
            screen.blit(title, titleRect)
            screen.blit(sp, spRect)
            screen.blit(st, stRect)
            screen.blit(xt, xtRect)

        elif MorS == "settings":
            # Check for cursor
            if Schoice == 1:
                fsText = "-- Fullscreen: " + str(settings.getFullscreen()) + " --"
                bcText = "Back"
            elif Schoice == 2:
                fsText = "Fullscreen: " + str(settings.getFullscreen())
                bcText = "-- Back --"

            # Render text
            # Render title text
            title = bigfont.render(OurTitle, True, (0,0,0))
            titleRect = title.get_rect()
            titleRect.centerx = screen.get_rect().centerx
            titleRect.centery = height12*2
            # Render fullscreen text
            fs = font.render(fsText, True, (0,0,0))
            fsRect = fs.get_rect()
            fsRect.centerx = screen.get_rect().centerx
            fsRect.centery = height12*5
            # Render back text
            bc = font.render(bcText, True, (0,0,0))
            bcRect = bc.get_rect()
            bcRect.centerx = screen.get_rect().centerx
            bcRect.centery = height12*6

            # Draw text
            screen.blit(title, titleRect)
            screen.blit(fs, fsRect)
            screen.blit(bc, bcRect)
    
        # Flip the display
        pygame.display.flip()
