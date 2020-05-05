import pygame
from pygame.locals import*
import random
import datetime as dt
from time import sleep
import submit          #modul
from tkinter import*
import os


kraj = False

imena = [
    'Šime',
    'Joža',
    'Štef',
    'Dragec',
    'Mirko'

]

kor1=''
kor2 = random.choice(imena)

root = Tk()
root.title('Unos korisničkih imena')

user1 = Label(root, text='Ime 1. igrača: ', font=('CooperBlack', 20))
user2 = Label(root, text='Ime protivnika:', font=('CooperBlack', 20))
user1.grid(row=0, column=0)
user2.grid(row=1, column=0)

entry_user1 = Entry(root, font=('CooperBlack', 20)); user2_ime = Label(root, text=kor2, font=('CooperBlack', 20))
entry_user1.grid(row=0, column=1); user2_ime.grid(row=1, column=1)

def get_kor(event):
    global kor1
    global kor2

    kor1 = entry_user1.get()

    root.destroy()

send = Button(root, text="Spremi", font=('CooperBlack', 20, 'italic bold'), fg="red")
send.grid(row=2, columnspan=2)
send.bind('<ButtonRelease>', get_kor)

root.mainloop()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,35)

pygame.init()
screen = pygame.display.set_mode((900,780))
pygame.display.set_caption('Igra protiv računala')

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

#kao na sahovskoj ploci
positions = ['a1', 'a2', 'a3', 'a4', 'a5',
             'b1', 'b2', 'b3', 'b4', 'b5',
             'c1', 'c2', 'c3', 'c4', 'c5',
             'd1', 'd2', 'd3', 'd4', 'd5']

#sve karte na ekranu (parovi)
karteAll = karteList + karteList

#zakomentirati ovu naredbu u svrhu testiranja
random.shuffle(karteAll)


#pozicija kartice : [Kartica, Otvorena?, koordinate topleft kuta]
base = {positions[i] : [karteAll[i], False, (0,0)] for i in range(20)}


#kada računalo otvori karticu ta se sa svojom pozicijom sprema u ovu list
poznate_karte = []

Otv_Karte = []  #otvorene karte
br_otv = 0      #broj otvorenih karata
score_player = 0
score_comp = 0

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


def isPair(elapsed):
    global Otv_Karte
    global br_otv
    global base
    global score_player
    global lista_vremena
    global player_turn

    n = 0
    for red in range(4):
        y = 100 + red*150
        for stupac in range(5):
            x = 100 + stupac*150
            drawOne(n, x, y)
            n+=1

    pygame.display.update()


    if Otv_Karte[0] == Otv_Karte[1]:
        score_player+=1
        for n in range(20):
            if Otv_Karte[0] == base[positions[n]][0] or Otv_Karte[1] == base[positions[n]][0]:
                base[positions[n]][1] = True
                if base[positions[n]][0] in poznate_karte:
                    poznate_karte.remove(base[positions[n]][0])
        br_otv = 0
        Otv_Karte.clear()
        lista_vremena.clear()
        player_turn = False

    else:
        if elapsed.seconds >=1:
            for n in range(20):
                if Otv_Karte[0] == base[positions[n]][0] or Otv_Karte[1] == base[positions[n]][0]:
                    base[positions[n]][1] = False
            lista_vremena.clear()
            br_otv = 0
            Otv_Karte.clear()

            player_turn = False

    #Ako su dvije otvorene karte par: score +1, vrijednost u base vise nije True/False nego 'FIX' tako da
    #se vise te dvije karte ne mogu zatvarat i otvarat nego ostaju otvorene do kraja igre

    #Ako nisu par samo se zatvaraju i u oba slučaja se broj otvorenih karata i lista otvorenih karata resetiraju

def comTurn():
    global Otv_Karte




    global pos1
    global pos2


    valjano = False
    while valjano == False:
        pos1 = random.choice(positions)     #sa varijablom valjano pratimo jel odabrana kartica slobodna
        if base[pos1][1] == False:
            valjano = True

    if base[pos1][0] in poznate_karte:
        if bool(random.getrandbits(1)) == True:         #50% šanse da će računalo pogoditi par
            for n in range(20):
                if base[positions[n]][0] == base[pos1][0] and pos1 != positions[n]:
                    pos2 = positions[n]

        else:
            valjano = False
            while valjano == False:
                pos2 = random.choice(positions)         #ako ne pogodi bira drugu bilo koju slobodnu karticu
                if base[pos2][1] == False and pos2 != pos1:
                    valjano = True

    else:
        valjano = False
        while valjano == False:
            pos2 = random.choice(positions)         #ako ne pogodi bira drugu bilo koju slobodnu karticu
            if base[pos2][1] == False and pos2 != pos1:
                valjano = True



    Otv_Karte.append(pos1)
    Otv_Karte.append(pos2)
    #print(Otv_Karte)


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
    submit.VScom(kor1, time, score)









lista_vremena = []
font = pygame.font.Font(cwd+'\\font.otf', 50)
clock = pygame.time.Clock()
player_turn = True
vrijeme1 = dt.datetime.now()
while not kraj:

    screen.blit(background, (0,0))
    vrijeme = dt.datetime.now() - vrijeme1
    rezultat_player = font.render(kor1+': '+str(score_player), True, (0,0,0))
    rezultat_comp = font.render(kor2+': '+str(score_comp), True, (0,0,0))
    screen.blit(rezultat_player, (10,0))
    screen.blit(rezultat_comp, (10,30))
    time = font.render('Vrijeme: '+str(vrijeme)[:-4], True, (0,0,0))
    screen.blit(time, (400,0))

    n = 0
    for red in range(4):
        y = 100 + red*150
        for stupac in range(5):         #crtanje svih karata na ekran
            x = 100 + stupac*150
            drawOne(n, x, y)
            n+=1

    if player_turn == False:
        if len(Otv_Karte) != 2:
            comTurn()

        if len(lista_vremena) != 1:
            lista_vremena.append(dt.datetime.now())

        time = dt.datetime.now()

        elapsed = time - lista_vremena[0]
        if elapsed.seconds in range (1,2):
            pos1 = Otv_Karte[0]
            base[pos1][1] = True

        elif elapsed.seconds in range (2,5):
            pos2 = Otv_Karte[1]
            base[pos2][1] = True


            if base[Otv_Karte[0]][0] == base[Otv_Karte[1]][0]:
                score_comp+=1
                for n in range(20):
                    if base[Otv_Karte[0]][0] == base[positions[n]][0] or base[Otv_Karte[1]][0] == base[positions[n]][0]:
                        base[positions[n]][1] = True
                        if base[positions[n]][0] in poznate_karte:
                            poznate_karte.remove(base[positions[n]][0])
                Otv_Karte.clear()
                lista_vremena.clear()
                player_turn = True

            else:
                if elapsed.seconds >=4:
                    for n in range(20):
                        if base[Otv_Karte[0]][0] == base[positions[n]][0] or base[Otv_Karte[1]][0] == base[positions[n]][0]:
                            base[positions[n]][1] = False
                    lista_vremena.clear()
                    Otv_Karte.clear()

                    player_turn = True


    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            kraj = True

        if player_turn:
            if e.type == pygame.MOUSEBUTTONUP:
                x, y = e.pos
                for n in range(20):
                    if isPressed(n, x, y):          #jel otvorena neka kartica?
                        if base[positions[n]][1] == True:
                            pass
                        elif base[positions[n]][1] == False:
                            if br_otv<2:
                                base[positions[n]][1] = True; br_otv+=1; Otv_Karte.append(base[positions[n]][0])
                                if base[positions[n]][0] not in poznate_karte:
                                    poznate_karte.append(base[positions[n]][0])
                            else:
                                pass
                        else:
                            pass

















    if br_otv==2:
               #jesu otvorene dvije karte?
        if len(lista_vremena) != 1:
            lista_vremena.append(dt.datetime.now())

        c = dt.datetime.now() - lista_vremena[0]


        isPair(c)


    if score_comp + score_player == 10:
        End(str(score_player)+' : '+str(score_comp), vrijeme)



    clock.tick(60)
    pygame.display.update()
