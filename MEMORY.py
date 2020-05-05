import tkinter as tk
import datetime as dt
import sqlite3
from PIL import Image, ImageTk
import sys
import os
from tksheet import Sheet
import subprocess


cwd = os.getcwd()

#Dobavljanje zapisa iz .db datoteke
class RezultatiFetch:

    def listaRezultataAll():

        conn = sqlite3.connect('rezultati.db'); c = conn.cursor()

        c.execute("SELECT * FROM rezultati")

        return c.fetchall()

    def listaRezultataSP():
        conn = sqlite3.connect('rezultati.db'); c = conn.cursor()

        c.execute("SELECT * FROM rezultati WHERE type = ?", ("SinglePlayer",))

        return c.fetchall()

    def listaRezultataMP():
        conn = sqlite3.connect('rezultati.db'); c = conn.cursor()

        c.execute("SELECT * FROM rezultati WHERE type = ?", ("MultiPlayer",))

        return c.fetchall()

    def listaRezultataVSCOM():
        conn = sqlite3.connect('rezultati.db'); c = conn.cursor()

        c.execute("SELECT * FROM rezultati WHERE type = ?", ("vs Com",))

        return c.fetchall()

#Kreiranje Sheet objekta sa podacima iz prethodne klase
class Tables:
    headers = ['Korisničko ime', 'Rezultat', 'Datum', 'Vrijeme', 'Vrsta']
    def TableAll(subRoot):
        data = RezultatiFetch.listaRezultataAll()
        table = Sheet(subRoot, height=600,
                    width=600,
                    data=data,
                    headers=['Korisničko ime', 'Rezultat', 'Datum', 'Vrijeme', 'Vrsta'])

        return table

    def TableSinglePlayer(subRoot):
        data = RezultatiFetch.listaRezultataSP()
        table = Sheet(subRoot,
                    height=600,
                    width=600,
                    data=data,
                    headers=['Korisničko ime', 'Rezultat', 'Datum', 'Vrijeme', 'Vrsta'])

        return table

    def TableMultiPlayer(subRoot):
        data = RezultatiFetch.listaRezultataMP()
        table = Sheet(subRoot,
                    height=600,
                    width=600,
                    data=data,
                    headers=['Korisničko ime', 'Rezultat', 'Datum', 'Vrijeme', 'Vrsta'])

        return table

    def TableVsCom(subRoot):
        data = RezultatiFetch.listaRezultataVSCOM()
        table = Sheet(subRoot,
                    height=600,
                    width=600,
                    data=data,
                    headers=['Korisničko ime', 'Rezultat', 'Datum', 'Vrijeme', 'Vrsta'])

        return table


class subMenus:
    #Prikaz tablica iz prethodne klase
    def RezultatiTableShow(root, i):
        subRoot = tk.Toplevel(root)
        subRoot.title('Tablica Rezultata'); subRoot.geometry('600x750+400+0'); subRoot.resizable(False, False)
        subRoot.iconbitmap(cwd+'\slike\ikona.ico')

        canvas = tk.Canvas(subRoot, width=600, height=750)
        canvas.place(x=0, y=0)

        poz1 = Image.open(cwd+'\slike\poz1.png').convert("RGBA")
        poz1 = poz1.resize((poz1.size[0]*5, poz1.size[1]*6), resample = Image.NEAREST)
        poz1 = ImageTk.PhotoImage(image=poz1, master=subRoot)

        canvas.create_image(300,300,image=poz1)

        izlaz = tk.Button(subRoot, text=u"\u23CE", font=('Calibri', 20), width=5, relief=tk.GROOVE)
        izlaz.place(x=510, y=10)
        izlaz.bind('<ButtonRelease>', lambda a: subRoot.destroy())

        canvas.create_text(270, 50, text="Zapisani Rezultati", font=('Algerian', 30, 'italic bold underline'), fill='white')

        if i==1:
            t = Tables.TableAll(subRoot)
        elif i==2:
            t = Tables.TableSinglePlayer(subRoot)
        elif i==3:
            t = Tables.TableMultiPlayer(subRoot)
        else:
            t = Tables.TableVsCom(subRoot)
        t.column_width(column=3, width=70)
        t.place(x=0, y=150)

        subRoot.mainloop()


class Menu:


    def opis_igre(root):
        root.destroy()
        subRoot = tk.Tk()
        subRoot.title('Opis igre'); subRoot.geometry('600x750+400+0'); subRoot.resizable(False, False)
        subRoot.iconbitmap(cwd+'\slike\ikona.ico')

        canvas = tk.Canvas(subRoot, width=600, height=750)
        canvas.place(x=0, y=0)

        poz1 = Image.open(cwd+'\slike\poz1.png').convert("RGBA")
        poz1 = poz1.resize((poz1.size[0]*5, poz1.size[1]*6), resample = Image.NEAREST)
        poz1 = ImageTk.PhotoImage(image=poz1, master=subRoot)

        canvas.create_image(300,300,image=poz1)

        izlaz = tk.Button(subRoot, text=u"\u23CE", font=('Calibri', 20), width=5, relief=tk.GROOVE)
        izlaz.place(x=510, y=10)
        izlaz.bind('<ButtonRelease>', lambda a: subRoot.destroy())

        memory = '''U 20 nasumično raspoređenih kartica nalazi\nse deset parova koje morate pronaći, u svakom
potezu otvarate po dvije kartice i ako\none nisu iste okreću se nazad te je vaš\ncilj upamtiti na kojem su mjestu te kartice bile;
kada pronađete jedan par - kartice\nostaju okrenute te vam se pribraja jedan bod\n\n\n'''
        titles = "Singleplayer\n\n\n\nMultiplayer\n\n\n\nVs com\n\n\n\n"
        sp = "        - pronađi sve parove u što\n       manje vremena te pokušaj oboriti rekord\n\n\n"
        "Multiplayer"
        mp = "        - pronađi više parova nego\n       tvoj protivnik, svatko ima po jedan potez\n\n\n"
        "Vs com"
        vscom = " - bori se protiv računala => u borbi protiv računala\n pronađi više parova\n\n\n"
        rez = "Nakon odigrane igre rezultat spremi\n pod željenim korisničkim imenom"

        canvas.create_text(270,50, text='Opis i pravila', font=('Algerian', 30, 'italic bold underline'), fill='white')
        canvas.create_text(260,230, text=memory, font=('CooperBlack', 16, 'italic bold'), fill='white')
        canvas.create_text(80, 475, text=titles, font=('CooperBlack', 16, 'italic bold underline'), fill='white')
        canvas.create_text(350, 475, text=sp+mp+vscom, font=('Emberly', 16, 'italic'), fill='white')
        canvas.create_text(300, 650, text=rez, font=('Emberly', 18, 'italic underline bold'), fill='white')

        subRoot.mainloop()


    def rezultati(root):
        root.destroy()
        subRoot = tk.Tk()
        subRoot.title('Rezultati'); subRoot.geometry('600x750+400+0'); subRoot.resizable(False, False)
        subRoot.iconbitmap(cwd+'\slike\ikona.ico')

        canvas = tk.Canvas(subRoot, height=750, width=600)
        canvas.place(x=0, y=0)

        poz1 = Image.open(cwd+'\slike\poz1.png').convert("RGBA")
        poz1 = poz1.resize((poz1.size[0]*5, poz1.size[1]*6), resample = Image.NEAREST)
        poz1 = ImageTk.PhotoImage(image=poz1, master=subRoot)
        canvas.create_image(300,300, image=poz1)

        izlaz = tk.Button(subRoot, text=u"\u23CE", font=('Calibri', 20), width=5, relief=tk.GROOVE)
        izlaz.place(x=510, y=10)
        izlaz.bind('<ButtonRelease>',  lambda a: subRoot.destroy())

        but1 = tk.Button(subRoot, text='Svi rezultati', width=15, height=2, bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
        but2 = tk.Button(subRoot, text='SP rezultati',width=15, height=2,bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
        but3 = tk.Button(subRoot, text='MP rezultati',width=15, height=2,bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
        but4 = tk.Button(subRoot, text='vs Com rezultati', width=15, height=2,bg='#EEEEEE',relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))

        but1.place(x=170, y=200)
        but2.place(x=170, y=330)
        but3.place(x=170, y=460)
        but4.place(x=170, y=590)

        but1.bind('<ButtonRelease>', lambda a: subMenus.RezultatiTableShow(subRoot, 1))
        but2.bind('<ButtonRelease>', lambda a: subMenus.RezultatiTableShow(subRoot, 2))
        but3.bind('<ButtonRelease>', lambda a: subMenus.RezultatiTableShow(subRoot, 3))
        but4.bind('<ButtonRelease>', lambda a: subMenus.RezultatiTableShow(subRoot, 4))

        subRoot.mainloop()


    def igra(root):
        root.destroy()
        subRoot = tk.Tk()
        subRoot.title('Igra'); subRoot.geometry('600x750+400+0'); subRoot.resizable(False, False)
        subRoot.iconbitmap(cwd+'\slike\ikona.ico')

        canvas = tk.Canvas(subRoot, height=750, width=600)
        canvas.place(x=0, y=0)

        poz1 = Image.open(cwd+'\slike\poz1.png').convert("RGBA")
        poz1 = poz1.resize((poz1.size[0]*5, poz1.size[1]*6), resample = Image.NEAREST)
        poz1 = ImageTk.PhotoImage(image=poz1, master=subRoot)
        canvas.create_image(300,300, image=poz1)

        izlaz = tk.Button(subRoot, text=u"\u23CE", font=('Calibri', 20), width=5, relief=tk.GROOVE)
        izlaz.place(x=510, y=10)
        izlaz.bind('<ButtonRelease>',  lambda a: subRoot.destroy())

        canvas.create_text(300, 50, text="Igraj", font=('Algerian', 30, 'italic bold underline'), fill='white')

        but1 = tk.Button(subRoot, text='SinglePlayer', width=15, height=2, bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
        but2 = tk.Button(subRoot, text='MultiPlayer',width=15, height=2,bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
        but3 = tk.Button(subRoot, text='vs Com',width=15, height=2,bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))

        but1.place(x=170, y=250)
        but2.place(x=170, y=380)
        but3.place(x=170, y=510)

        but1.bind('<ButtonRelease>', lambda a: subprocess.run('sp.py', shell=True))
        but2.bind('<ButtonRelease>', lambda a: subprocess.run('mp.py', shell=True))
        but3.bind('<ButtonRelease>', lambda a: subprocess.run('vscom.py', shell=True))




        subRoot.mainloop()

def start():




    root=tk.Tk()
    root.title('MEMORY'); root.geometry('600x750+400+0');root.resizable(False, False)
    root.iconbitmap(cwd+'\slike\ikona.ico')

    root.protocol("WM_DELETE_WINDOW", lambda:sys.exit())

    canvas = tk.Canvas(root, height=750, width=600)
    canvas.place(x=0, y=0)


    poz0 = Image.open(cwd+'\slike\poz0.jpg')
    poz0 = poz0.resize((poz0.size[0]*2,poz0.size[1]*2), resample=Image.NEAREST)
    poz0 = ImageTk.PhotoImage(poz0)

    canvas.create_image(0,0,image=poz0)


    canvas.create_text(300,80,text='Memory', font=('Algerian', 60, 'bold italic underline'), fill='white')

    but1 = tk.Button(root, text='Igra', width=15, height=2, bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
    but2 = tk.Button(root, text='Rezultati',width=15, height=2,bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
    but3 = tk.Button(root, text='Opis igre',width=15, height=2,bg='#EEEEEE', relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))
    but4 = tk.Button(root, text='Izlaz', width=15, height=2,bg='#EEEEEE',relief=tk.GROOVE, borderwidth=2, font=('Algerian', 20, 'italic'))

    but1.place(x=170, y=200)
    but2.place(x=170, y=330)
    but3.place(x=170, y=460)
    but4.place(x=170, y=590)

    but1.bind('<ButtonRelease>', lambda a: Menu.igra(root))
    but2.bind('<ButtonRelease>', lambda a: Menu.rezultati(root))
    but3.bind('<ButtonRelease>', lambda a: Menu.opis_igre(root))
    but4.bind('<ButtonRelease>', lambda a: sys.exit())
    root.mainloop()


###################################
###################################
###################################
if 'rezultati.db' not in os.listdir():
        conn = sqlite3.connect('rezultati.db'); c = conn.cursor()


        c.execute("CREATE TABLE rezultati (username text, score integer, date text, time text, type text)")

        conn.commit(); conn.close()

else:
    pass

while True:
    start() #root.protocol("WM_DELETE_WINDOW", lambda:sys.exit())
            #u funkciji start() - line 247
            #omogućuje izlaz iz petlje
