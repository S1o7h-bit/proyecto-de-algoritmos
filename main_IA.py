from clases_IA import pnj, pelea
import random
from collections import deque

# Creación del jugador
fighter1 = pnj("Jugador", random.randint(90, 110), 1.0, random.randint(10, 15))

print(f"👤 Estadísticas de {fighter1._name}:")
print(f" -> Vida inicial: {fighter1._vida}")
print(f" -> Daño base: {fighter1._adano}\n")

# Creación de la cola de enemigos
enemigos = deque()
nombres = ["Goblin", "Kobold", "Esbirro"]

for nombre in nombres: 
    # Enemigos un poco más débiles que el jugador para que sea justo
    fighter2 = pnj(nombre, random.randint(40, 55), 1.0, random.randint(6, 10))
    enemigos.append(fighter2)

# Inicializamos la pelea pasando solo al jugador y la cola
fight = pelea(fighter1, enemigos)

# Ejecutamos el simulador
fight.run()