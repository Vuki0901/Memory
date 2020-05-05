import pygame
from pygame.locals import*
import random
import datetime as dt
from time import sleep
import submit          #modul
from tkinter import*
import os
#2. pokusaj (zamjena collidepoint funkcije i crtanja karata)

kor1 = ''; kor2 = ''



root=Tk()
root.title('Unos korisničkih imena')

user1 = Label(root, text='Ime 1. igrača: ', font=('CooperBlack', 20))
user2 = Label(root, text='Ime 2. igrača: ', font=('CooperBlack', 20))
user1.grid(row=0, column=0)
user2.grid(row=1, column=0)

entry_user1 = Entry(root, font=('CooperBlack', 20)); entry_user2 = Entry(root, font=('CooperBlack', 20))
entry_user1.grid(row=0, column=1); entry_user2.grid(row=1, column=1)

def get_kor(event):
    global kor1
    global kor2

    kor1 = entry_user1.get()
    kor2 = entry_user2.get()

    root.destroy()

send = Button(root, text="Kreni", font=('CooperBlack', 20, 'italic bold'), fg="red")
send.grid(row=2, columnspan=2)
send.bind('<ButtonRelease>', get_kor)



root.mainloop()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,35)

pygame.init()
screen = pygame.display.set_mode((900,780))
pygame.display.set_caption('MultiPlayer')
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

background = pygame.image.load(cwd+'\\slike\\template.png')

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
score_first = 0
score_second = 0
turn = 0
#nakon dvije otvorene kartice provjera ako je otvoren par
def isPair(elapsed):
    global Otv_Karte
    global br_otv
    global base
    global score_first
    global score_second
    global lista_vremena
    global turn

    n = 0
    for red in range(4):
        y = 100 + red*150
        for stupac in range(5):
            x = 100 + stupac*150
            drawOne(n, x, y)
            n+=1

    pygame.display.update()


    if Otv_Karte[0] == Otv_Karte[1]:
        turn+=1
        if turn%2==1:
            score_first+=1
        else:
            score_second+=1
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
            turn+=1


    #Ako su dvije otvorene karte par: score +1, vrijednost u base vise nije True/False nego 'FIX' tako da
    #se vise te dvije karte ne mogu zatvarat i otvarat nego ostaju otvorene do kraja igre

    #Ako nisu par samo se zatvaraju i u oba slučaja se broj otvorenih karata i lista otvorenih karata resetiraju


font = pygame.font.Font(cwd+'\\font.otf', 50)
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
        kraj = font.render('Kraj! :)', True, (0,0,0))
        vrijeme = font.render('Vrijeme: '+str(time)+' sekundi', True, (0,0,0))
        msg = font.render('Za '+str(5-stop)+' sekundi spremi rezultat', True, (0,0,0))
        skor = font.render('Rezultat '+score, True, (0,0,0))
        screen.blit(kraj, (200,300))
        screen.blit(skor, (200,400))
        screen.blit(vrijeme, (200,500))
        screen.blit(msg, (200, 600))


        pygame.display.update()

    pygame.quit()
    submit.MultiPlayer(kor1, kor2, score, time)


start = dt.datetime.now()
while rad:
    screen.blit(background, (0,0))
    vrijeme = dt.datetime.now() - start     #proteklo vrijeme
    rez_first = font.render(kor1+': '+str(score_first), True, (0,0,0))
    rez_second = font.render(kor2+': '+str(score_second), True, (0,0,0))
    timer = font.render('Vrijeme: '+str(vrijeme)[:-4], True, (0,0,0))
    if turn%2==0:
        turn_player = kor1
    else:
        turn_player = kor2
    turn_info = font.render('Na redu: '+turn_player, True, (0,0,0))
    screen.blit(rez_first, (20,0))        #ispis rezultata na ekran
    screen.blit(rez_second, (20, 50))
    screen.blit(timer, (400,0))    #ispis vremena na ekran
    screen.blit(turn_info, (400, 50))

    n = 0
    for red in range(4):
        y = 100 + red*150
        for stupac in range(5):         #crtanje svih karata na ekran
            x = 100 + stupac*150
            drawOne(n, x, y)
            n+=1



    if score_first+score_second==10:
        End(str(score_first)+' : '+str(score_second), vrijeme)         #jel igra završena?
        break


    if br_otv==2:
               #jesu otvorene dvije karte?
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
                        base[positions[n]][1] = False; br_otv-=1; Otv_Karte.remove(base[positions[n]][0])
                    elif base[positions[n]][1] == False:
                        if br_otv<2:
                            base[positions[n]][1] = True; br_otv+=1; Otv_Karte.append(base[positions[n]][0])
                        else:
                            pass
                    else:
                        pass






    clock.tick(60)  #60 fps
    pygame.display.update()
