import sqlite3

CONN = sqlite3.connect('liquorStore.db')
CURSOR = CONN.cursor()