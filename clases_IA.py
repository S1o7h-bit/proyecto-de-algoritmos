from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from collections import deque

app = FastAPI()

# Permitir que tu HTML abra el backend sin problemas de seguridad (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PNJ:
    def __init__(self, nombre, vida, mod, adano):
        self.nombre = nombre
        self.vida_max = vida
        self.vida = vida
        self.mod = mod
        self.adano = adano

    def to_dict(self):
        return {"nombre": self.nombre, "vida": self.vida, "vida_max": self.vida_max}

@app.get("/simular-pelea")
def simular_pelea():
    jugador = PNJ("Jugador", random.randint(90, 110), 1.0, random.randint(12, 16))
    
    enemigos_lista = [
        PNJ("Goblin", random.randint(40, 50), 1.0, random.randint(6, 10)),
        PNJ("Kobold", random.randint(45, 55), 1.0, random.randint(7, 11)),
        PNJ("Esbirro", random.randint(50, 60), 1.0, random.randint(8, 12))
    ]
    cola_enemigos = deque(enemigos_lista)
    
    historial_turnos = []
    num_turno = 1

    while cola_enemigos and jugador.vida > 0:
        enemigo = cola_enemigos.popleft()
        
        # Guardar evento de aparición de enemigo
        historial_turnos.append({
            "tipo": "evento",
            "mensaje": f"¡Un {enemigo.nombre} salvaje aparece!",
            "jugador": jugador.to_dict(),
            "enemigo": enemigo.to_dict()
        })

        pj_turno = jugador
        pj_rival = enemigo

        while jugador.vida > 0 and enemigo.vida > 0:
            # IA elige acción
            act = random.choice(["atacar", "mejorar"])
            mensaje = ""

            if act == "atacar":
                daño = int(pj_turno.adano * pj_turno.mod)
                pj_rival.vida = max(0, pj_rival.vida - daño)
                mensaje = f"💥 {pj_turno.nombre} ataca a {pj_rival.nombre} y hace {daño} de daño."
            elif act == "mejorar":
                pj_turno.mod += 0.4
                mensaje = f"🛡️ {pj_turno.nombre} aumentó su modificador de daño."

            # Guardar el estado actual de este turno para la animación web
            historial_turnos.append({
                "tipo": "turno",
                "numero": num_turno,
                "mensaje": mensaje,
                "accion": act,
                "atacante": pj_turno.nombre,
                "jugador": jugador.to_dict(),
                "enemigo": enemigo.to_dict()
            })

            num_turno += 1
            # Cambiar turno
            pj_turno, pj_rival = pj_rival, pj_turno

        # Resultado del combate individual
        if jugador.vida <= 0:
            historial_turnos.append({"tipo": "final", "mensaje": "💀 El Jugador ha sido derrotado. JUEGO TERMINADO."})
            break
        else:
            curacion = random.randint(15, 25)
            jugador.vida = min(jugador.vida_max, jugador.vida + curacion)
            historial_turnos.append({
                "tipo": "evento",
                "mensaje": f"🎉 ¡{enemigo.nombre} derrotado! El jugador recupera {curacion} PV.",
                "jugador": jugador.to_dict(),
                "enemigo": enemigo.to_dict()
            })

    if jugador.vida > 0:
        historial_turnos.append({"tipo": "final", "mensaje": "🏆 ¡Felicidades! Derrotaste a todos los enemigos."})

    return {"historial": historial_turnos}