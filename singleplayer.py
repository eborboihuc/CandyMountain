#!/usr/bin/env python2
# Import libraries
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
    import pygame, math, random, sys, menu, settings
    from pygame.locals import *
    import cv2, numpy
    import dlib
except:
    import pygame, math, random, sys, menu, settings
    from pygame.locals import *
    import cv2, numpy
    import dlib


def getFrame(color,frame):
    if not color:
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=numpy.rot90(frame)
    frame=pygame.surfarray.make_surface(frame) #I think the color error lies in this line?
    return frame


def play():

    detector = dlib.get_frontal_face_detector()

    # Set the width and height of the window
    width, height = int(pygame.display.Info().current_w), int(pygame.display.Info().current_h)

    # Create the window
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)

    # Initial camera
    cap = cv2.VideoCapture(0) # or 1
    imRawWidth = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    imRawHeight = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    imWidth = 1080 #640 #360
    imHeight = 960 #480 #240
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, imWidth)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, imHeight)

    #imWidth = imRawWidth
    #imHeight = imRawHeight

    # Set playing time
    gaming_time = 90000

    # Set level state
    level = 0
    moving_speed = [5,7,9] # original: [3,5,7]
    score_factor = [1,2,3]
    candy_size_factor = [0.7,0.5,0.3]
    shit_size_factor = [0.2,0.3,0.4]  # [0.2,0.3,0.5]
    leveltxt = ['EASY','HARD','CRAZY!!!']
    # Make an list for the accuracy
    acc=[0,0,0]
    loss=[0,0,0]
    _color=(255,0,0)
    # Set your health value
    healthvalue=[194,194,194] # 194
    blood_loss=20 

    # Set pressed keys
    keys = [False, False, False, False]
    # Flag for change player skin
    playerbadflag = 0
    # Make an list for where the arrows are
    arrows=[]
    # Set the timer for spawning badgers
    badtimer=100
    badtimer1=0
    candytimer=100
    candytimer1=0
    # Make an list for where the badgers are
    badguys=[[800,100]]
    candies=[[800,100]]
    # Set the wait times
    waitforexit=0
    waitforarrows=3 # 0
    waitforballoons=0
    waitforballoons2=2
    # Set displaying balloon on/off
    balloon1display = False
    balloon2display = False

    # Initialize the mixer (for sound)
    pygame.mixer.init()
    # Set title
    pygame.display.set_caption("Candy Mountain")
   
    # Load images
    # Load the background image
    grass = pygame.image.load("resources/images/BckGnd.jpg") #grass.png") # add at front
    grass = pygame.transform.scale(grass, (width, height))
    # Load the image of the castles
    castle = pygame.image.load("resources/images/castle.png")
    # Load the image for the arrows
    arrow = pygame.image.load("resources/images/bullet.png")
    # Load the image for the badgers
    badguyimg = pygame.image.load("resources/images/poopoo.png") #badguy.png")
    # Load the image for the candies
    candyimg = pygame.image.load("resources/images/candy.png") #badguy.png")
    # Load the overlays
    greenoverlay = pygame.image.load("resources/images/Win.jpg") #greenoverlay.png")
    redoverlay = pygame.image.load("resources/images/GameOver.jpg") #redoverlay.png")
    greenoverlay = pygame.transform.scale(greenoverlay, (width, height))
    redoverlay = pygame.transform.scale(redoverlay, (width, height))
    # Load the healthbar images
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    # Load the text balloons
    balloon1 = pygame.image.load("resources/images/balloon1.png")
    balloon2 = pygame.image.load("resources/images/balloon2.png")
    
    # Load audio
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/ohShit.wav") #enemy.wav")
    candySound = pygame.mixer.Sound("resources/audio/candy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    takePicture = pygame.mixer.Sound("resources/audio/takePic.wav")
    loseGame = pygame.mixer.Sound("resources/audio/loseGame.wav")
    winGame = pygame.mixer.Sound("resources/audio/winGame.wav")
    # Set the audio volume
    hit.set_volume(0.40)
    enemy.set_volume(0.60)
    candySound.set_volume(0.40)
    shoot.set_volume(0.40)
    takePicture.set_volume(0.60)
    loseGame.set_volume(0.60)
    winGame.set_volume(0.60)
    # Set the background music
    pygame.mixer.music.load('resources/audio/mix90.mp3') #level_easy.mp3') #background.mp3')
    pygame.mixer.music.set_volume(0.50)

    
    # Set positions
    castle1 = (2*width/16, height-150)    #castle1 = (0,height/16)
    castle2 = (6*width/16, height-150)    #castle2 = (0,height/3.5)
    castle3 = (10*width/16, height-150)    #castle3 = (0,height/2)
    castle4 = (14*width/16, height-150)    #castle4 = (0,height/1.4)

    # Set display mode
    prevFS = settings.getFullscreen()
    if settings.getFullscreen() == True:
        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    elif settings.getFullscreen() == False:
        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)

    # Capture frame-by-frame
    setting = 1
    roi = []
    _P,_Q,_R,_S = 0,0,0,0
    while(setting):
        ret, frame = cap.read()
        img = frame.copy()

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # face detection
        faces = detector(img)
        for d in faces:
            #print "left,top,right,bottom:", d.left(), d.top(), d.right(), d.bottom()
            _P,_Q,_R,_S = d.left(), d.top(), d.right()-d.left(), d.bottom()-d.top()
            cv2.rectangle(img,(_P,_Q),(_P+_R,_Q+_S),(255,0,0),2)

        # set up the ROI for tracking
        roi = img[_Q:_Q+_S, _P:_P+_R]

        # Draw the background
        screen.blit(grass,(0,0))
        ba = getFrame(True,cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        screen.blit(ba,(width/2-400,height/2-300))
        # Flip the display
        pygame.display.flip()
        # Loop through the events
        for event in pygame.event.get():
            # Check if the event is the X button 
            if event.type == pygame.KEYDOWN:
                # select
                if event.key==K_s:
                    takePicture.play()
                    print "Selecting"
                    setting = 0

    # Load the players image
    player = getFrame(True,roi.copy()) #frame.copy())
    playerBad = pygame.image.load("resources/images/shitFaceJustin.png")
    mainChar = player

    # Set player position
    playerpos = [width/2,height/2]
    faceCenter = playerpos

    # Keep looping through
    running = 1
    exitcode = 0
    # Set start ticks
    startticks = pygame.time.get_ticks()
    pygame.mixer.music.play(0, 0.0)
    while running:
        # Capture frame-by-frame
        ret, frame = cap.read()
        img = frame.copy()

        # Detect face
        faces = detector(img)
        for d in faces:
            #print "left,top,right,bottom:", d.left(), d.top(), d.right(), d.bottom()
            _P,_Q,_R,_S = d.left(), d.top(), d.right()-d.left(), d.bottom()-d.top()
        faceCenter=[(_P+_R/2), (_Q+_S/2)]
        #print faceCenter

        # Update player image
        if _P&_Q&_R&_S != 0:
            face = img[_Q:_Q+_S, _P:_P+_R, :]
            #print face.shape
            img2 = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            if img2 != None:
                player = getFrame(color,img2)


        # Set display mode if changed
        if prevFS != settings.getFullscreen():
            if settings.getFullscreen() == True:
                screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
                prevFS = settings.getFullscreen()
            elif settings.getFullscreen() == False:
                screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
                prevFS = settings.getFullscreen()

           
        badtimer-=2 #1
        candytimer-=1
        # Clear the screen before drawing it again
        screen.fill(0)
        # Draw the background
        screen.blit(grass,(0,0))

        # Draw the castles
        screen.blit(castle, castle1)
        screen.blit(castle, castle2)
        screen.blit(castle, castle3)
        screen.blit(castle, castle4)

        # Set player position and rotation
        position = pygame.mouse.get_pos()
        #angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        #playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        #playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        Wplayer = width - (float(faceCenter[0])/imWidth*width) #-playerpos[0])
        Hplayer = float(faceCenter[1])/imHeight*height #-playerpos[1]
        playerpos = [Wplayer, Hplayer]
        #screen.blit(playerrot, playerpos1)
        if playerbadflag == 0:
            mainChar = player
        else:
            mainChar = pygame.transform.scale(playerBad, (_R, _S))
        screen.blit(mainChar, playerpos)

        # Draw arrows
        for bullet in arrows:
            index=0
            velx=math.cos(bullet[0])*30 # *10
            vely=math.sin(bullet[0])*30
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>width or bullet[2]<-64 or bullet[2]>height:
                arrows.pop(index)
            index+=1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))

        # Draw badgers
        badguyImg = pygame.transform.scale(badguyimg, (int(badguyimg.get_width()*shit_size_factor[level]), int(badguyimg.get_height()*shit_size_factor[level])))
        if badtimer==0:
            badwidth1 = width/5 #9.6
            badwidth2 = 4*width/5 #1.1
            badwidth = random.randint(int(badwidth1), int(badwidth2))
            badguys.append([badwidth, 0]) # ([badwidth, height])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5 #random.randint(3,7) #5
        index=0
        for badguy in badguys:
            if badguy[1]<-64: # if badguy reached, pop out
                badguys.pop(index)
            badguy[1]+=moving_speed[level] # move badguy
            # Attack castle
            badrect=pygame.Rect(badguyImg.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if badrect.top>height-64: # top<64
                hit.play()
                badguys.pop(index)
            # Check for collisions
            index1=0
            # bullet collisions
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    hit.play() #enemy.play()
                    #acc[level]+=1
                    badguys.pop(index)
                    arrows.pop(index1)
                index1+=1
            # main char. collisions
            mainrect=pygame.Rect(mainChar.get_rect())
            mainrect.left=playerpos[0]
            mainrect.top=playerpos[1]
            if badrect.colliderect(mainrect):
                enemy.play()
                playerbadflag = 1
                #loss[level]+=1
                healthvalue[level] -= blood_loss #random.randint(5,20)
                badguys.pop(index)
            # Next bad guy
            index+=1

        # Draw badgers
        for badguy in badguys:
            screen.blit(badguyImg, badguy)


        # Draw candies
        candyImg = pygame.transform.scale(candyimg, (int(candyimg.get_width()*candy_size_factor[level]), int(candyimg.get_height()*candy_size_factor[level])))
        if candytimer==0:
            loss[level] += 1 
            candywidth1 = width/5#9.6
            candywidth2 = 4*width/5#1.1
            candywidth = random.randint(int(candywidth1), int(candywidth2))
            candies.append([candywidth, 0]) # ([candywidth, height])
            candytimer=100-(candytimer1*2)
            if candytimer1>=35:
                candytimer1=35
            else:
                candytimer1+= 5#random.randint(3,7) # 5
            #print str((gaming_time-pygame.time.get_ticks()+startticks)/1000%60)
            #print candytimer
        index=0
        for candy in candies:
            if candy[1]<-64: # if candy reached, pop out
                candies.pop(index)
            candy[1]+=moving_speed[level] # move candy
            # Attack castle
            candyrect=pygame.Rect(candyImg.get_rect())
            candyrect.top=candy[1]
            candyrect.left=candy[0]
            if candyrect.top>height+64: # top<64
                hit.play()
                healthvalue[level] -=  blood_loss  #random.randint(5,20)
                candies.pop(index)
            # Check for collisions
            index1=0
            # bullet collisions
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if candyrect.colliderect(bullrect):
                    candySound.play()
                    healthvalue[level] -= blood_loss  #random.randint(5,20)
                    candies.pop(index)
                    arrows.pop(index1)
                index1+=1
            # main char. collisions
            mainrect=pygame.Rect(mainChar.get_rect())
            mainrect.left=playerpos[0]
            mainrect.top=playerpos[1]
            if candyrect.colliderect(mainrect):
                candySound.play()
                if loss[level] - 1 >= 0:
                    acc[level]+=1
                    loss[level]-=1
                playerbadflag = 0
                candies.pop(index)
            # Next bad guy
            index+=1

        # Draw badgers
        for candy in candies:
            screen.blit(candyImg, candy)

        # Draw clock, score and level
        font = pygame.font.Font("freesansbold.ttf", 48)
        font2 = pygame.font.Font("freesansbold.ttf", 56)
        survivedtext = font.render(str((gaming_time-pygame.time.get_ticks()+startticks)/60000)+":"+str((gaming_time-pygame.time.get_ticks()+startticks)/1000%60).zfill(2), True, (0,0,0))
        scoretext = font.render("Score: "+str(acc[level])+" x " + str(score_factor[level]) + " = " + str(acc[level]*score_factor[level]), True, (0,0,0))
        lvtext = font.render("Level: "+ leveltxt[level], True, (0,0,0))
        textRect = survivedtext.get_rect()
        textRect2 = scoretext.get_rect()
        textRect3 = lvtext.get_rect()
        textRect.topright=[width-120, 5] # width-5 ,5
        textRect2.topright=[width-120, 55] # width-5 ,5
        textRect3.topleft=[20, 55] # width-5 
        screen.blit(survivedtext, textRect)
        screen.blit(scoretext, textRect2)
        screen.blit(lvtext, textRect3)

        # Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue[level]):
            screen.blit(health, (health1+8,8))

        # Loop through the events
        for event in pygame.event.get():
            # Check if the event is the X button 
            if event.type==pygame.QUIT:
                # If it is stop the music and go back to the main menu
                pygame.mixer.music.stop()
                cap.release()
                cv2.destroyAllWindows()
                menu.launch()
            if event.type == pygame.KEYDOWN:
                # Move up
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_UP:
                    keys[0]=True
                # Move left
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_LEFT:
                    keys[1]=True
                # Move down
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_DOWN:
                    keys[2]=True
                # Move right
                elif event.key==K_d:
                    keys[3]=True
                elif event.key==K_RIGHT:
                    keys[3]=True
                # Quit by pressing escape
                elif event.key==K_ESCAPE:
                    pygame.mixer.music.stop()
                    cap.release()
                    cv2.destroyAllWindows()
                    menu.launch()
                # Fullscreen by pressing F4
                elif event.key==K_F4:
                    settings.changeFullscreen()
            if event.type == pygame.KEYUP:
                # Move up
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_UP:
                    keys[0]=False
                # Move left
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_LEFT:
                    keys[1]=False
                # Move down
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_DOWN:
                    keys[2]=False
                # Move right
                elif event.key==pygame.K_d:
                    keys[3]=False
                elif event.key==pygame.K_RIGHT:
                    keys[3]=False

            # Check if you pressed a mouse button for shooting arrows
            if event.type==pygame.MOUSEBUTTONDOWN:
                if waitforarrows == 0:
                    shoot.play()
                    position=pygame.mouse.get_pos()
                    arrows.append([math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26)),playerpos[0]+32,playerpos[1]+32])
                    # Set wait time for arrows in frames
                    waitforarrows=15 # 15
                    if waitforballoons2:
                        waitforballoons2-=1
                    else:
                        # Choose balloon
                        balloonnr = random.randint(1, 2)
                        if balloonnr == 1:
                            balloon1display = True
                        elif balloonnr == 2:
                            balloon2display = True
                        waitforballoons2=2
        if waitforarrows:
            waitforarrows-=1
            waitforballoons = waitforarrows
        # Display balloon
        if waitforballoons:
            waitforballoons-=1
            if balloon1display:
                screen.blit(balloon1, (playerpos[0]+10, playerpos[1]-60))
            elif balloon2display:
                screen.blit(balloon2, (playerpos[0]+10, playerpos[1]-60))
        else:
            balloon1display = False
            balloon2display = False
    
   
        # Move player
        # Up
        if keys[0]:
            playerpos[1]-=10 # 5
        # Down
        elif keys[2]:
            playerpos[1]+=10
        # Left
        if keys[1]:
            playerpos[0]-=10
        # Right
        elif keys[3]:
            playerpos[0]+=10

    
        # Win/Lose check
        # Win
        past_time = (pygame.time.get_ticks()-startticks)
        if past_time>=gaming_time: # 90000
            running=0
            exitcode=1
        elif past_time>=gaming_time/3 and level == 0: # for simplicity, didn't add "and past_time<2*gaming_time/3"
            level = 1
            badtimer=1
            candytimer=1
            for candy in candies:
                candies.pop(0)
            for badguy in badguys:
                badguys.pop(0)
        elif past_time>=2*gaming_time/3 and level == 1:
            level = 2
            badtimer=1
            candytimer=1
            for candy in candies:
                candies.pop(0)
            for badguy in badguys:
                badguys.pop(0)

        # Lose
        if healthvalue[level]<=0:
            running=0
            exitcode=0

        # Final scores
        if running == 0:
            Score1 = "Easy: "+str(acc[0])+" x " + str(score_factor[0]) + " = " + str(acc[0]*score_factor[0])
            Score2 = "Hard: "+str(acc[1])+" x " + str(score_factor[1]) + " = " + str(acc[1]*score_factor[1])
            Score3 = "Crazy: "+str(acc[2])+" x " + str(score_factor[2]) + " = " + str(acc[2]*score_factor[2])

        #if acc[1]!=0:
        #    accuracy=acc[0]*1.0/acc[1]*100
        #else:
        #    accuracy=0

        # Flip the display
        pygame.display.flip()

    # Stop the music
    pygame.mixer.music.stop()

    # Win/lose display        
    # Lose
    if exitcode==0:
        # Change the text color
        _color = (255,255,255)
        # Draw red overlay
        screen.blit(redoverlay,(0, 0))
        loseGame.play()
    # Win
    else:
        _color = (255,0,0)
        # Draw green overlay
        screen.blit(greenoverlay,(0, 0))
        winGame.play()

    # Initialize the font
    pygame.font.init()
    # Set font
    font = pygame.font.Font("freesansbold.ttf", 48) # 24
    bigfont = pygame.font.Font("freesansbold.ttf", 56) # 48

    # Render text
    text1 = bigfont.render("Score:", True, _color)
    text2 = font.render(Score1, True, _color)
    text3 = font.render(Score2, True, _color)
    text4 = font.render(Score3, True, _color)

    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect4 = text4.get_rect()

    textRect1.centerx = screen.get_rect().centerx-width/3
    textRect1.centery = screen.get_rect().centery+60
    textRect2.centerx = screen.get_rect().centerx-width/3
    textRect2.centery = screen.get_rect().centery+110
    textRect3.centerx = screen.get_rect().centerx-width/3
    textRect3.centery = screen.get_rect().centery+160
    textRect4.centerx = screen.get_rect().centerx-width/3
    textRect4.centery = screen.get_rect().centery+210

    # Draw text
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text4, textRect4)

    print "ACC: " + str(acc)
    print "LOSS: " + str(loss)

    # Exit automatic when the game is stopped
    while 1:
        waitforexit+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loseGame.stop()
                winGame.stop()
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
        if waitforexit == 1500:
            loseGame.stop()
            winGame.stop()
            cap.release()
            cv2.destroyAllWindows()
            menu.launch()
        # Update the screen
        pygame.display.flip()
