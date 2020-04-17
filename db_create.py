import sqlite3
import os


def main():


    if 'rezultati.db' not in os.listdir():
        conn = sqlite3.connect('rezultati.db'); c = conn.cursor()


        c.execute("CREATE TABLE rezultati (username text, score integer, date text, time text, type text)")

        conn.commit(); conn.close()

    else:
        pass
    
