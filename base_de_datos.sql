import sqlite3

con = sqlite3.connect("base_de_datos.sql")

cur = con.cursor()


cur.execute("CREATE TABLE personas(Jugador, Puntuacion)")

con = close()