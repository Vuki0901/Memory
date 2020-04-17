import tkinter as tk
import sqlite3
import datetime as dt
from tkinter import messagebox
import os


def sqlInput(score, time, vrsta, unos, root):
    date = dt.date.today().strftime('%d.%m.%Y.')
    try:
        username = unos.get()   #ako je SP ili vs Com (entry)
    except:
        username = unos         #ako je MP (label)
    
    conn = sqlite3.connect('rezultati.db')
    c = conn.cursor()

    podaci = (username, vrsta, score, time, date)
    c.execute("INSERT INTO rezultati (username, type, score, time, date) VALUES (?, ?, ?, ?, ?)", podaci)
    conn.commit(); conn.close()
    
    root.destroy()

    

def SinglePlayer(score, time):
    root = tk.Tk()
    root.title('Submit'); root.geometry('600x400+450+150'); root.resizable(False, False)

    canvas = tk.Canvas(root, height=400, width=600)
    canvas.place(x=0, y=0)

    canvas.create_text(300,30, text='Zapamti rezultat', font=('Algerian', 30, 'bold italic underline'))

    canvas.create_text(150, 100, text='Korisničko ime:', font=('CooperBlack', 18, 'italic underline'))

    kime_unos = tk.Entry(root, font=('CooperBlack', 18, 'italic'))
    kime_unos.place(x=250, y=87)

    canvas.create_text(260, 170, text='Vrijeme:', font=('CooperBlack', 18, 'italic underline'))
    canvas.create_text(360, 170, text=str(time)+' sec', font=('CooperBlack', 18, 'italic'))

    canvas.create_text(300, 250, text='Singleplayer:  10', font=('CooperBlack', 18, 'italic'))

    time += ' s'
    submit_button = tk.Button(root, text='Potvrdi', width=15, fg='red', font=('CooperBlack', 20, 'italic bold'))
    submit_button.place(x=150, y=300)
    submit_button.bind('<ButtonRelease>', lambda a: sqlInput(score, time, 'SinglePlayer', kime_unos, root))


    root.mainloop()

def MultiPlayer(user1, user2, score, time):
    root = tk.Tk()
    root.title('Submit'); root.geometry('600x400+450+150'); root.resizable(False, False)

    canvas = tk.Canvas(root, height=400, width=600)
    canvas.place(x=0, y=0)

    canvas.create_text(300,30, text='Zapamti rezultat', font=('Algerian', 30, 'bold italic underline'))

    canvas.create_text(150, 100, text='Korisnička imena:', font=('CooperBlack', 18, 'italic underline'))

    kime_unos1 = tk.Label(root, text=user1, font=('CooperBlack', 18, 'italic'))
    kime_unos1.place(x=250, y=87)

    kime_unos2 = tk.Label(root, text=user2, font=('CooperBlack', 18, 'italic'))
    kime_unos2.place(x=250, y=120)

    canvas.create_text(260, 185, text='Vrijeme:', font=('CooperBlack', 18, 'italic underline'))
    canvas.create_text(360, 185, text=str(time)+' sec', font=('CooperBlack', 18, 'italic'))

    canvas.create_text(300, 250, text='Multiplayer:  '+score, font=('CooperBlack', 18, 'italic'))

    time += ' s'

    submit_button = tk.Button(root, text='Potvrdi', width=15, fg='red', font=('CooperBlack', 20, 'italic bold'))
    submit_button.place(x=150, y=300)
    submit_button.bind('<ButtonRelease>', lambda a: sqlInput(score, time, 'MultiPlayer', user1+' vs '+user2, root))


    root.mainloop()



def VScom(user1, time, score):
    root = tk.Tk()
    root.title('Submit'); root.geometry('600x400+450+150'); root.resizable(False, False)

    canvas = tk.Canvas(root, height=400, width=600)
    canvas.place(x=0, y=0)

    canvas.create_text(300,30, text='Zapamti rezultat', font=('Algerian', 30, 'bold italic underline'))

    canvas.create_text(150, 100, text='Korisničko ime:', font=('CooperBlack', 18, 'italic underline'))

    kime_unos = tk.Entry(root, font=('CooperBlack', 18, 'italic')); kime_unos.insert(tk.END, user1)
    kime_unos.place(x=250, y=87)

    canvas.create_text(260, 170, text='Vrijeme:', font=('CooperBlack', 18, 'italic underline'))
    canvas.create_text(380, 170, text=str(time)+' sec', font=('CooperBlack', 18, 'italic'))

    canvas.create_text(300, 250, text=str(score), font=('CooperBlack', 18, 'italic'))

    time += ' s'
    submit_button = tk.Button(root, text='Potvrdi', width=15, fg='red', font=('CooperBlack', 20, 'italic bold'))
    submit_button.place(x=150, y=300)
    submit_button.bind('<ButtonRelease>', lambda a: sqlInput(score, time, 'vs Com', kime_unos, root))


    root.mainloop()