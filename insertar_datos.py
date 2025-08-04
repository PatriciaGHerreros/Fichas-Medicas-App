import sqlite3
conexion = sqlite3.connect("fichas.db")
cursor = conexion.cursor()

cursor.execute(
  """ 
CREATE TABLE IF NOT EXISTS ficha (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  edad INTEGER NOT NULL,
  area TEXT NOT NULL,
  done BOOLEAN NOT NULL DEFAULT 0
)
"""
)

fichasrecibidas = [
  ("Juan Perez", 30, "Medicina General", False),
  ("Ana Gomez", 25, "Cardiología", False),
  ("Luis Torres", 40, "Dermatología", False),
  ("Maria Lopez", 35, "Ginecología", True),
]

cursor.executemany (
  "INSERT INTO ficha (nombre, edad, area, done) VALUES (?, ?, ?, ?)",
  fichasrecibidas
)

conexion.commit()
conexion.close()
print("Datos insertados correctamente")