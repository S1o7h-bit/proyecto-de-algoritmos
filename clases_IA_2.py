import streamlit as st
import random
import time
from collections import deque

# Configuración de la página de Streamlit
st.set_page_config(page_title="Simulador RPG Automático", page_icon="⚔️", layout="centered")

# --- CLASES DE TU LÓGICA ---
class PNJ:
    def __init__(self, nombre, vida, mod, adano):
        self.nombre = nombre
        self.vida_max = vida
        self.vida = vida
        self.mod = mod
        self.adano = adano

# --- INICIALIZACIÓN DEL ESTADO DEL JUEGO ---
if "jugador" not in st.session_state:
    st.session_state.jugador = None
if "cola_enemigos" not in st.session_state:
    st.session_state.cola_enemigos = deque()
if "enemigo_actual" not in st.session_state:
    st.session_state.enemigo_actual = None
if "historial" not in st.session_state:
    st.session_state.historial = []
if "juego_iniciado" not in st.session_state:
    st.session_state.juego_iniciado = False
if "turno_actual" not in st.session_state:
    st.session_state.turno_actual = 1
if "quien_ataca" not in st.session_state:
    st.session_state.quien_ataca = "Jugador"

# Diccionario de avatares
avatares = {"Jugador": "🧙‍♂️", "Goblin": "👺", "Kobold": "🦎", "Esbirro": "💀"}

# --- FUNCIONES DE CONTROL ---
def iniciar_nueva_partida():
    st.session_state.jugador = PNJ("Jugador", random.randint(90, 110), 1.0, random.randint(12, 16))
    
    enemigos_lista = [
        PNJ("Goblin", random.randint(40, 50), 1.0, random.randint(6, 10)),
        PNJ("Kobold", random.randint(45, 55), 1.0, random.randint(7, 11)),
        PNJ("Esbirro", random.randint(50, 60), 1.0, random.randint(8, 12))
    ]
    st.session_state.cola_enemigos = deque(enemigos_lista)
    st.session_state.enemigo_actual = st.session_state.cola_enemigos.popleft()
    st.session_state.historial = [f"🏁 ¡Comienza la aventura! Aparece un {st.session_state.enemigo_actual.nombre}."]
    st.session_state.turno_actual = 1
    st.session_state.quien_ataca = "Jugador"
    st.session_state.juego_iniciado = True

def avanzar_turno():
    jugador = st.session_state.jugador
    enemigo = st.session_state.enemigo_actual
    
    if not jugador or not enemigo:
        return

    # Definir atacante y defensor
    if st.session_state.quien_ataca == "Jugador":
        atacante, defensor = jugador, enemigo
    else:
        atacante, defensor = enemigo, jugador

    # Lógica de la acción
    accion = random.choice(["atacar", "mejorar"])
    if accion == "atacar":
        dano = int(atacante.adano * atacante.mod)
        defensor.vida = max(0, defensor.vida - dano)
        st.session_state.historial.append(
            f"⚔️ **Turno {st.session_state.turno_actual}**: {avatares.get(atacante.nombre, '👾')} **{atacante.nombre}** ataca a **{defensor.nombre}** y hace {dano} de daño."
        )
    elif accion == "mejorar":
        atacante.mod += 0.4
        st.session_state.historial.append(
            f"🛡️ **Turno {st.session_state.turno_actual}**: {avatares.get(atacante.nombre, '👾')} **{atacante.nombre}** aumentó su modificador de daño."
        )

    st.session_state.turno_actual += 1

    # Comprobación de estados (Muerte/Victoria)
    if enemigo.vida <= 0:
        st.session_state.historial.append(f"🎉 ¡{enemigo.nombre} ha sido derrotado!")
        if st.session_state.cola_enemigos:
            st.session_state.enemigo_actual = st.session_state.cola_enemigos.popleft()
            curacion = random.randint(15, 25)
            jugador.vida = min(jugador.vida_max, jugador.vida + curacion)
            st.session_state.historial.append(
                f"❤️ El Jugador se recupera {curacion} PV. ¡Aparece un {st.session_state.enemigo_actual.nombre}!"
            )
            st.session_state.quien_ataca = "Jugador"
        else:
            st.session_state.enemigo_actual = None
            st.session_state.historial.append("🏆 ¡FELICIDADES! Has derrotado a todos los enemigos de la fila.")
            st.session_state.juego_iniciado = False
    elif jugador.vida <= 0:
        st.session_state.historial.append("💀 El Jugador ha muerto. JUEGO TERMINADO.")
        st.session_state.juego_iniciado = False
    else:
        # Alternar turno
        st.session_state.quien_ataca = "Enemigo" if st.session_state.quien_ataca == "Jugador" else "Jugador"


# --- INTERFAZ VISUAL ---
st.title("⚔️ Arena de Batalla RPG (Auto)")

# Control de velocidad en la barra lateral (Sidebar)
st.sidebar.header("⚙️ Configuración")
velocidad = st.sidebar.slider("Velocidad del combate (segundos por turno)", 0.5, 3.0, 1.2, step=0.1)

# Botón para iniciar
if st.button("✨ Iniciar Nueva Partida", type="primary"):
    iniciar_nueva_partida()

# Dibujar la interfaz de combate si hay un jugador creado
if st.session_state.jugador:
    jugador = st.session_state.jugador
    enemigo = st.session_state.enemigo_actual

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h1 style='text-align: center;'>{avatares['Jugador']}</h1>", unsafe_allow_html=True)
        st.subheader(jugador.nombre)
        st.progress(jugador.vida / jugador.vida_max)
        st.write(f"❤️ HP: **{jugador.vida}** / {jugador.vida_max}")
        st.caption(f"Modificador de daño: {jugador.mod:.2f}")

    with col2:
        if enemigo:
            st.markdown(f"<h1 style='text-align: center;'>{avatares.get(enemigo.nombre, '👾')}</h1>", unsafe_allow_html=True)
            st.subheader(enemigo.nombre)
            st.progress(enemigo.vida / enemigo.vida_max)
            st.write(f"❤️ HP: **{enemigo.vida}** / {enemigo.vida_max}")
            st.caption(f"Modificador de daño: {enemigo.mod:.2f}")
        else:
            st.markdown("<h1 style='text-align: center;'>🏳️</h1>", unsafe_allow_html=True)
            st.subheader("Sin enemigos")
            st.write("Todos los rivales fueron derrotados.")

    st.markdown("---")

    # Historial
    st.write("### 📜 Historial del Combate")
    for log in reversed(st.session_state.historial):
        st.markdown(log)

    # 👇 EL TRUCO DE LA MAGIA AUTOMÁTICA 👇
    # Si el juego está activo, espera el tiempo seleccionado y fuerza la recarga de la página
    if st.session_state.juego_iniciado:
        time.sleep(velocidad)
        avanzar_turno()
        st.rerun()  # Vuelve a ejecutar todo el archivo procesando el nuevo turno automáticamente