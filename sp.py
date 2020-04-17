import pygame
from pygame.locals import*
import random
import datetime as dt
from time import sleep
import submit          #modul
import os


pygame.init()
screen = pygame.display.set_mode((900,780))
pygame.display.set_caption('SinglePlayer')
rad = True

karteList = []  #lista karata

cwd = os.getcwd()
#učitavanje svih prednjih strana karata karata
karta_ps_1 = pygame.image.load(cwd+'\slike\kart_1.jpg'); karteList.append(karta_ps_1)
karta_ps_2 = pygame.image.load(cwd+'\slike\kart_2.jpg'); karteList.append(karta_ps_2)
karta_ps_3 = pygame.image.load(cwd+'\slike\kart_3.jpg'); karteList.append(karta_ps_3)
karta_ps_4 = pygame.image.load(cwd+'\slike\kart_4.jpg'); karteList.append(karta_ps_4)
karta_ps_5 = pygame.image.load(cwd+'\slike\kart_5.jpg'); karteList.append(karta_ps_5)
karta_ps_6 = pygame.image.load(cwd+'\slike\kart_6.jpg'); karteList.append(karta_ps_6)
karta_ps_7 = pygame.image.load(cwd+'\slike\kart_7.jpg'); karteList.append(karta_ps_7)
karta_ps_8 = pygame.image.load(cwd+'\slike\kart_8.jpg'); karteList.append(karta_ps_8)
karta_ps_9 = pygame.image.load(cwd+'\slike\kart_9.jpg'); karteList.append(karta_ps_9)
karta_ps_10 = pygame.image.load(cwd+'\slike\kart_10.jpg'); karteList.append(karta_ps_10)

#zadnja strana karata
karta_zs = pygame.image.load(cwd+'\slike\zadnja_strana.png')



positions = ['a1', 'a2', 'a3', 'a4', 'a5',      #kao na sahovskoj ploci
             'b1', 'b2', 'b3', 'b4', 'b5',
             'c1', 'c2', 'c3', 'c4', 'c5',
             'd1', 'd2', 'd3', 'd4', 'd5']


karteAll = karteList + karteList  #sve karte na ekranu (parovi)

random.shuffle(karteAll)


#pozicija kartice : [Kartica, Otvorena?, koordinate topleft coska]
base = {positions[i] : [karteAll[i], False, (0,0)] for i in range(20)}  

#crtanje jedne kartice na zadanim koordinatama(x,y)
def drawOne(n, x, y):
    global base
    global karteAll
    Open = base[positions[n]][1]    #Otvorena? = True/False
    if Open:    #if Open==True:
        screen.blit(base[positions[n]][0], (x, y))
    else:
        screen.blit(karta_zs, (x, y))
    
    base[positions[n]][2] = (x,y)   #Postavljanje koordinata topleft coska

#provjera kartice jel otvorena il nije; vraća vrijednost True/False 
def isPressed(n, mouse_x, mouse_y):
    global base
    x = base[positions[n]][2][0]
    y = base[positions[n]][2][1]

    rangeX = range(x, x+101)    #širina slike = 100
    rangeY = range(y, y+131)    #dužina slika = 130

    if mouse_x in rangeX and mouse_y in rangeY:
        return True
    return False

Otv_Karte = []  #otvorene karte
br_otv = 0      #broj otvorenih karata
score = 0

#nakon dvije otvorene kartice provjera ako je otvoren par
def isPair(elapsed):
    global Otv_Karte
    global br_otv
    global base
    global score
    global lista_vremena
    n = 0
    for red in range(4):
        y = 100 + red*150
        for stupac in range(5):
            x = 100 + stupac*150
            drawOne(n, x, y)
            n+=1

    pygame.display.update()


    if Otv_Karte[0] == Otv_Karte[1]:       
        score+=1
        for n in range(20):
            if Otv_Karte[0] == base[positions[n]][0] or Otv_Karte[1] == base[positions[n]][0]:
                base[positions[n]][1] = 'FIX'
        br_otv = 0
        Otv_Karte.clear()
        lista_vremena.clear()
    else:
        if elapsed.seconds >=1:
            for n in range(20):
                if Otv_Karte[0] == base[positions[n]][0] or Otv_Karte[1] == base[positions[n]][0]:
                    base[positions[n]][1] = False
            lista_vremena.clear()
            br_otv = 0
            Otv_Karte.clear()
            
    #Ako su dvije otvorene karte par: score +1, vrijednost u base vise nije True/False nego 'FIX' tako da
    #se vise te dvije karte ne mogu zatvarat i otvarat nego ostaju otvorene do kraja igre

    #Ako nisu par samo se zatvaraju i u oba slučaja se broj otvorenih karata i lista otvorenih karata resetiraju


font = pygame.font.Font('freesansbold.ttf', 32)
clock = pygame.time.Clock()
lista_vremena = []

def End(score, time):
    start = dt.datetime.now()
    stop=0
    time = '%.2f' %(float(str(time.seconds)+'.'+str(time.microseconds)))
    while stop<5:
        stop = dt.datetime.now() - start
        stop = stop.seconds
        screen.fill((255,255,255))
        kraj = font.render('Pronađeno svih 10 parova! :)', True, (0,0,0))
        vrijeme = font.render('Vrijeme: '+str(time)+' sekundi', True, (0,0,0))
        msg = font.render('Sačekaj '+str(5-stop)+' sekundi', True, (0,0,0))
        screen.blit(kraj, (200,300))
        screen.blit(vrijeme, (200,400))
        screen.blit(msg, (200, 500))

        pygame.display.update()
    
    pygame.quit()
    submit.SinglePlayer(score, time)
    
    
        

start = dt.datetime.now()
while rad:
    screen.fill((255,255,255))  #bijela pozadina
    vrijeme = dt.datetime.now() - start     #proteklo vrijeme
    rez = font.render('Score: '+str(score), True, (0,0,0))  
    timer = font.render('Vrijeme: '+str(vrijeme)[:-4], True, (0,0,0))
    screen.blit(rez, (0,0))        #ispis rezultata na ekran
    screen.blit(timer, (275,0))    #ispis vremena na ekran


    n = 0
    for red in range(4):
        y = 100 + red*150
        for stupac in range(5):         #crtanje svih karata na ekran
            x = 100 + stupac*150
            drawOne(n, x, y)
            n+=1



    if score==10:
        End(score, vrijeme)         #jel igra završena?
        break


    if br_otv==2:       #jesu otvorene dvije karte?
        if len(lista_vremena) != 1:
            lista_vremena.append(dt.datetime.now())
    
        c = dt.datetime.now() - lista_vremena[0]
        
            
        isPair(c) 


    for e in pygame.event.get():
        if e.type == pygame.QUIT:       #jel pritisnut X?
            rad = False

        if e.type == pygame.MOUSEBUTTONUP:
            x, y = e.pos
            for n in range(20):
                if isPressed(n, x, y):          #jel otvorena neka kartica?
                    if base[positions[n]][1] == True:
                        pass
                    elif base[positions[n]][1] == False:
                        if br_otv<2:
                            base[positions[n]][1] = True; br_otv+=1; Otv_Karte.append(base[positions[n]][0])
                        else:
                            pass
                    else:
                        pass    
                        
    
            
        
    

    clock.tick(60)  #60 fps
    pygame.display.update()
    
