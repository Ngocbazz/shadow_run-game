import pygame,sys 
import random
from pygame import mixer
pygame.init()
caption=pygame.display.set_caption("SHADOW_RUN.NB")
window=pygame.display.set_mode((500,600))

#run game
run=True
menu_open=True
menu_run=True

#Colors
white=(245, 245, 245)
black=(13, 13, 13)
red=(252, 36, 3)

#music
mixer.init()
jump_sound=mixer.Sound('music/mixkit-player-jumping-in-a-video-game-2043.wav')
score_sound=mixer.Sound('music/mixkit-space-coin-win-notification-271.wav')
lazer_sound=mixer.Sound('music/mixkit-sci-fi-laser-in-space-sound-2825.wav')


#text
font=pygame.font.SysFont("Times New Roman",36)
font2=pygame.font.SysFont("Times New Roman",50)
font3=pygame.font.SysFont("Times New Roman",20)

#player
player_y=340
player_x=10
player=pygame.image.load('pictures/shadow (1) (1) (1).png')
player_size=pygame.transform.scale(player,(230,100))
player_pos=0

#obstacle(chướng ngại vật)
ob1=pygame.image.load('pictures/Untitled (1).png')
ob1_size=pygame.transform.scale(ob1,(140,150))
ob1_x=600

ob2=pygame.image.load('pictures/Untitled2 (1).png')
ob2_size=pygame.transform.scale(ob2,(200,150))
ob2_x=800

#coin
coin=pygame.image.load('pictures/coin.png')
coin_x=650
coin_y=250
coin_size=pygame.transform.scale(coin,(180,100))
coin_run=True

#sun
#0
sun=pygame.image.load('pictures/sun.png')
sun_size=pygame.transform.scale(sun,(380,200))
sun_run=True
sun_blit=True
#1
sun1=pygame.image.load('pictures/sun1 .png')
sun1_size=pygame.transform.scale(sun1,(380,200))
#2
sun2=pygame.image.load('pictures/sun2 .png')
sun2_size=pygame.transform.scale(sun2,(380,200))

sun_x=280
next_sun_blit=True

#sun lazer
sun_lazer_y=10
sun_lazer_run=False
sun_lazer_count=0


#menu text
text1_y=100
text2_y=180
text3_y=400

#FPS
clock=pygame.time.Clock()

#gravity
gravity=0.5

#score
score=0
high_score=0


def draw_floor():
    pygame.draw.rect(window,black,(0,400,500,400))
   

    
def move():
  global player_y,player_x,player_pos
  global ob1_x,ob2_x
  global coin_run, coin_x,coin_y

  #player
  player_pos +=gravity
  player_y +=player_pos
     # jump limit
  if player_y>=340:
      player_y=340

  if player_y<=100:
     player_y=100
     # walk limit
  if player_x<-100:
     player_x=-100
  if player_x>400:
     player_x=400
  #coin
  coin_x-=1.5
    #coin return
  if coin_x <=-100:
     coin_x=random.randint(700,900)
    #coin effect
  if coin_run ==True:
     coin_y+=0.5
  if coin_run ==False:
     coin_y-=0.5
  if coin_y==270:
     coin_run=False 
  if coin_y==250:
     coin_run=True  

  #chướng ngại vật
  ob1_x -=2
  ob2_x-=2

  if ob1_x  <-600:
     ob1_x=600

   
  if ob2_x <-800:
     ob2_x=800
     


    

def pictures():

    #player model
   window.blit(player_size,(player_x,player_y))
  
   #chướng ngại vật model
   window.blit(ob1_size,(ob1_x,310))
   window.blit(ob2_size,(ob2_x,310))

   #coin model
   window.blit(coin_size,(coin_x,coin_y))

   #sun model
   if sun_blit==True :
    window.blit(sun_size,(280,0))



def text():
   
    score_font=font.render("SCORE: " + str(score),True,black)
    window.blit(score_font,(0,0))




   

def collision():
   global player_x,player_y
   global game_continue
   global score
   global coin_x
   global sun_lazer
   #player
      #rect
   rect_size=pygame.transform.scale(player_size,(50,50))
   player_rect=rect_size.get_rect(center=(player_x+115,player_y+40))
  
   #coin 
      # rect
   coin_rect=(coin_x+65,coin_y+35,30,30)


   #chướng ngại vật
   #rect
     #1
   ob1_rect=(ob1_x+40,350,50,50)
  
     #2
   ob2_rect=(ob2_x+75,350,35,50)
   #sun lazer rect
   if sun_lazer_run==True:
     sun_lazer=(sun_x+160,sun_lazer_y+100,20,400)  



   #collision
   if player_rect.colliderect(ob1_rect) or player_rect.colliderect(ob2_rect):
      game_continue=False
 
   if player_rect.colliderect(coin_rect):
       score+=1
       score_sound.play()
       
       coin_x=random.randint(700,900)
   
   if sun_lazer_run==True:    
    if player_rect.colliderect(sun_lazer):
       pygame.draw.rect(window,red,sun_lazer)
       game_continue=False
  



a=0
def sun_animation():
  global a
  global next_sun_blit
  if next_sun_blit==True and sun_blit==False:
     a+=2
     window.blit(sun1_size,(sun_x,0))
  if next_sun_blit==False and sun_blit==False:
     a-=0.5
     window.blit(sun2_size,(sun_x,0))
  if a==100:
     next_sun_blit=False
  if a==0:
     next_sun_blit=True

    
def sun_attack():
   global sun_lazer_y,sun_lazer_count,sun_lazer_run
   if game_continue==True:
     if sun_lazer_run==False:
        sun_lazer_count+=0.5
     if sun_lazer_run==True:
        sun_lazer_count-=0.5
        pygame.draw.rect(window,red,sun_lazer)

     if sun_lazer_count==150:
       sun_lazer_run=True
       lazer_sound.play()
     if sun_lazer_count==0:
       sun_lazer_run=False
      
       

   
     
def over_screen():
   #text
   over_text=font2.render("GAME OVER",True,red)
   score_over_text=font.render("Score: "+ str(score),True,red)
   high_score_over_text=font.render("High Score: "+ str(high_score),True,red)
   window.blit(over_text,(100,100))
   window.blit(score_over_text,(180,150))
   window.blit(high_score_over_text,(140,200))
   #button
   return_button=pygame.image.load('pictures/return icon.png')
   return_button_size=pygame.transform.scale(return_button,(400,200))
   window.blit(return_button_size,(-150,-30))
   #floor
   draw_floor()

   

def menu_screen():
      text_run=True
      global run,menu_run

      while menu_run==True:
        global text1_y,text2_y,text3_y
        run=False
       
        clock.tick(60)
        window.fill(white)
      
        text2_y-=0
        text3_y-=0

        #text
        text1=font2.render("SHADOW RUN",True,black)
        text2=font3.render("Make by NB",True,black)
        text3=font.render("Press ENTER to play",True,red)

        window.blit(text1,(90,text1_y))
        window.blit(text2,(100,text2_y))
        window.blit(text3,(90,text3_y))
        

         #text effect
        if text_run==True: 
          text1_y-=0.5
          text2_y-=0.5
          text3_y-=0.5
        if text_run==False:
           text1_y+=0.5
           text2_y+=0.5
           text3_y+=0.5

        if text3_y==390:
           text_run=False
        if text3_y==400:
           text_run=True
         
      
        for event in pygame.event.get():
           if event.type==pygame.QUIT:
              pygame.quit()
              sys.exit() 
           if event.type==pygame.KEYDOWN:
              if event.key==pygame.K_RETURN and menu_run==True:
                 run=True
                 menu_run=False 
        pygame.display.flip()


# MAIN loop
if __name__=="__main__":
 game_continue=True
 
 while run==True:
 
     clock.tick(120)
     window.fill(white)
     
     mouse_x,mouse_y=pygame.mouse.get_pos()
    
     if menu_open==True:
        menu_screen()
    
     for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
           if event.key==pygame.K_RETURN and game_continue==False:
              game_continue=True
              score=0
              #player jump
           if event.key==pygame.K_SPACE and game_continue==True:
              player_pos=0
              player_pos-=15

              jump_sound.play()
        
        # Go back to menu
        if event.type==pygame.MOUSEBUTTONDOWN and game_continue==False:
              if 60>mouse_x>20 and 45>mouse_y>20 and event.button==1:
                 menu_run=True
                 game_continue=True

                 score=0
      
     key_input=pygame.key.get_pressed()
         #player walk
     if key_input[pygame.K_RIGHT] and game_continue==True:
              player_x+=2
     if  key_input[pygame.K_LEFT] and game_continue==True:
              player_x-=2

     if score > high_score:
       high_score=score
     if score >=5:
        sun_animation()
        sun_attack()
      
        sun_blit=False
        if sun_run==True:
           sun_x-=1
        if sun_run==False:
           sun_x+=1
         
        if sun_x==-100:
           sun_run=False
        if sun_x==280:
           sun_run=True
         
     if score>=10:
          ob1_x-=1
          ob2_x-=1          

     if game_continue== False:
         over_screen()      

         player_x=10
         ob1_x=600
         ob2_x=800
         sun_x=280
         coin_x=650

         sun_run=True
         sun_blit=True
         next_sun_blit=True
         sun_lazer_count=0
         sun_lazer_run=False
         a=0
         
         pygame.display.flip()

     if game_continue==True:
       move()
       collision()
       draw_floor()
       pictures()
       text()
       
       pygame.display.flip()

       
    
  