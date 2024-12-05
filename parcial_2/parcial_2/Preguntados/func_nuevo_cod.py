import os
import pygame
import random
import csv
import json
from datetime import datetime

# Iniciar Pygame
pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Preguntas")

fondo = pygame.image.load("prueba_juego/fondoprincipal.jpg")  # Asegúrate de tener la imagen de fondo en la carpeta correcta
fondo = pygame.transform.scale(fondo, (800, 600))
fondo_final = fondo
fondo_final = pygame.transform.scale(fondo_final, (800, 600))

fondo_solo_juego = pygame.image.load("C:/Users/maria/OneDrive/Escritorio/prueba/parcial_2/parcial_2/Preguntados/fondo_solo_juego.jpg")
fondo_solo_juego = pygame.transform.scale(fondo_solo_juego, (800, 600))


imagen_boton = pygame.image.load("prueba_juego/boton1.jpg")  # Imagen de botones
imagen_boton_hover = pygame.image.load("prueba_juego/boton2.jpg")  # Imagen de botones cuando pasas el mouse

imagen_boton_jugar = pygame.transform.scale(imagen_boton, (200, 50))
imagen_boton_jugar_hover = pygame.transform.scale(imagen_boton_hover, (200, 50))

# Puedes hacer lo mismo para los otros botones si los necesitas (TOP 10, Configuración)
imagen_boton_top10 = pygame.transform.scale(imagen_boton, (200, 50))
imagen_boton_top10_hover = pygame.transform.scale(imagen_boton_hover, (200, 50))

imagen_boton_config = pygame.transform.scale(imagen_boton, (200, 50))
imagen_boton_config_hover = pygame.transform.scale(imagen_boton_hover, (200, 50))

imagen_boton_activado = pygame.image.load("C:/Users/maria/OneDrive/Escritorio/prueba/parcial_2/parcial_2/Preguntados/boton_activado.jpg") 
imagen_boton_activado = pygame.transform.scale(imagen_boton_activado, (200, 50))
imagen_boton_desactivado = pygame.image.load("C:/Users/maria/OneDrive/Escritorio/prueba/parcial_2/parcial_2/Preguntados/boton_desactivado.jpg") 
imagen_boton_desactivado = pygame.transform.scale(imagen_boton_desactivado, (200, 50))

imagen_fondo_para_pregunta = pygame.image.load("C:/Users/maria/OneDrive/Escritorio/prueba/parcial_2/parcial_2/Preguntados/fondo_para_pregunta.jpg") 
imagen_fondo_para_pregunta = pygame.transform.scale(imagen_fondo_para_pregunta, (700, 50))

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
GRIS = (169, 169, 169)

# Fuentes
fuente = pygame.font.SysFont("Arial", 30)
fuente_pequeña = pygame.font.SysFont("Arial", 24)
fuente_nombre = pygame.font.SysFont("Arial", 24)


#musica
# Cargar el sonido de activación y desactivación de la música
#sonido_activar_musica = pygame.mixer.Sound('sonido_juego (1).mp3')
sonido_activar_musica = pygame.mixer.Sound('C:/Users/maria/OneDrive/Escritorio/prueba/parcial_2/parcial_2/Preguntados/sonido_juego.mp3')


# Variables de juego
vidas = 3
puntos = 0
respuestas_correctas = 0
categoria_seleccionada = None
comodin_duplicar_puntos_usado = False
comodin_pasado_usado = False
musica_activada = True
volumen_musica = 0.5  # Volumen inicial

# Cargar preguntas desde el archivo CSV
def cargar_preguntas(categoria):
    preguntas = []
    with open('C:/Users/maria/OneDrive/Escritorio/prueba/parcial_2/parcial_2/Preguntados/preguntas.csv', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            preguntas.append(fila)
    return preguntas

def agregar_pregunta():
    """
    Permite al usuario agregar una pregunta manualmente.
    """
    pregunta = input("Introduce la pregunta: ")
    opciones = []
    for i in range(4):  # Suponiendo que hay 4 opciones
        opcion = input(f"Introduce la opción {i+1}: ")
        opciones.append(opcion)
    respuesta_correcta = int(input("Introduce el número de la opción correcta (1-4): "))
    
    # Guardar la nueva pregunta en el archivo CSV
    with open('preguntas.csv', mode='a', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([pregunta] + opciones + [respuesta_correcta])

    print("Pregunta agregada correctamente.")

    
def cargar_preguntas_csv():
    """
    Permite al usuario cargar un archivo CSV con preguntas y agregarlas.
    """
    path = input("Introduce el path del archivo CSV con las preguntas: ")
    try:
        with open(path, mode='r') as archivo:
            reader = csv.reader(archivo)
            for row in reader:
                # Suponiendo que el formato es: pregunta, 4 opciones, respuesta correcta
                pregunta = row[0]
                opciones = row[1:5]
                respuesta_correcta = int(row[5])
                
                # Agregar las preguntas al juego o guardarlas en un archivo
                with open('preguntas.csv', mode='a', newline='') as archivo_guardado:
                    writer = csv.writer(archivo_guardado)
                    writer.writerow([pregunta] + opciones + [respuesta_correcta])

        print("Preguntas cargadas correctamente.")
    except FileNotFoundError:
        print("No se pudo encontrar el archivo.")


def modificar_opciones():
    """
    Permite al usuario modificar las opciones del juego.
    """
    global puntos_acierto, puntos_error, oportunidades, tiempo_disponible

    print("Opciones actuales:")
    print(f"Puntaje por acierto: {puntos_acierto}")
    print(f"Puntaje por error: {puntos_error}")
    print(f"Oportunidades: {oportunidades}")
    print(f"Tiempo por pregunta: {tiempo_disponible} segundos")
    
    puntos_acierto = int(input("Introduce el puntaje por respuesta correcta: "))
    puntos_error = int(input("Introduce el puntaje por respuesta incorrecta: "))
    oportunidades = int(input("Introduce la cantidad de oportunidades: "))
    tiempo_disponible = int(input("Introduce el tiempo por pregunta (en segundos): "))
    
    print("Opciones modificadas correctamente.")


# Función para mostrar texto en pantalla
def mostrar_texto(texto, x, y, color, fuente):
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))


def manejar_boton_clicks():
    # Detectar clics en los botones
    accion = None
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()  # Obtener la posición del mouse
            # Comprobar si se hizo clic en el botón "Jugar"
            if 300 <= pos_mouse[0] <= 500 and 300 <= pos_mouse[1] <= 350:
                accion = "jugar"
            # Comprobar si se hizo clic en el botón "TOP 10"
            elif 300 <= pos_mouse[0] <= 500 and 400 <= pos_mouse[1] <= 450:
                accion = "top10"
            # Comprobar si se hizo clic en el botón "Configuración"
            elif 300 <= pos_mouse[0] <= 500 and 500 <= pos_mouse[1] <= 550:
                accion = "configuracion"
    
    return accion


def mostrar_categorias():
    global categoria_seleccionada
    pantalla.blit(fondo, (0, 0))  # Mostrar fondo
    mostrar_texto("Elige una categoría:", 300, 100, NEGRO, fuente)

    categorias = ['Historia', 'Matematica', 'Entretenimiento', 'Deportes']
    botones_categorias = []  # Guardamos los rectángulos de los botones para cada categoría

    for i, categoria in enumerate(categorias):
        # Definir la posición de cada botón de categoría
        categoria_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
        botones_categorias.append(categoria_rect)

        # Detectar si el mouse está sobre el botón para mostrar el efecto hover
        if categoria_rect.collidepoint(pygame.mouse.get_pos()):
            pantalla.blit(imagen_boton_jugar_hover, (categoria_rect.x, categoria_rect.y))  # Hover
        else:
            pantalla.blit(imagen_boton_jugar, (categoria_rect.x, categoria_rect.y))  # Normal

        # Mostrar el texto de la categoría sobre el botón
        mostrar_texto(categoria, categoria_rect.x + 50, categoria_rect.y + 10, NEGRO, fuente)

    pygame.display.flip()

    # Esperar a que el jugador seleccione una categoría
    esperando_categoria = True
    while esperando_categoria:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Verificar si el clic fue dentro de algún botón de categoría
                for i, categoria_rect in enumerate(botones_categorias):
                    if categoria_rect.collidepoint(pos):
                        categoria_seleccionada = categorias[i]
                        esperando_categoria = False
                        print(f"Categoría seleccionada: {categoria_seleccionada}")
                        break


# Función para mostrar la configuración
def mostrar_configuracion():
    global musica_activada, volumen_musica
    pantalla.fill(BLANCO)
    mostrar_texto("Configuración", 300, 50, NEGRO, fuente)

    # Botón para activar/desactivar música
    pygame.draw.rect(pantalla, AZUL, (300, 150, 200, 50))
    mostrar_texto("Música: " + ("Activada" if musica_activada else "Desactivada"), 350, 160, BLANCO, fuente_pequeña)

    # Botón para subir volumen
    pygame.draw.rect(pantalla, AZUL, (300, 220, 200, 50))
    mostrar_texto("Subir Volumen", 350, 230, BLANCO, fuente_pequeña)

    # Botón para bajar volumen
    pygame.draw.rect(pantalla, AZUL, (300, 290, 200, 50))
    mostrar_texto("Bajar Volumen", 350, 300, BLANCO, fuente_pequeña)

    # Control deslizante para volumen de música
    pygame.draw.rect(pantalla, GRIS, (300, 360, 200, 10))  # Fondo del control deslizante
    pygame.draw.rect(pantalla, AZUL, (300, 355, 200 * volumen_musica, 20))  # Control deslizante
    mostrar_texto(f"Volumen: {int(volumen_musica * 100)}%", 350, 375, NEGRO, fuente_pequeña)
    
    # Botón para detener música
    pygame.draw.rect(pantalla, AZUL, (300, 450, 200, 50))  # Rectángulo para detener música
    mostrar_texto("Detener Música", 350, 460, BLANCO, fuente_pequeña)

    # Botón para volver al menú
    pygame.draw.rect(pantalla, AZUL, (300, 520, 200, 50))  # Botón "Volver" movido
    mostrar_texto("Volver", 350, 530, BLANCO, fuente)

    pygame.display.flip()


# Función para reproducir música
def reproducir_musica():
    if musica_activada:
        # Reemplaza 'musica_fondo.mp3' por el archivo de música que deseas utilizar.
        pygame.mixer.music.load('C:/Users/maria/OneDrive/Escritorio/prueba/parcial_2/parcial_2/Preguntados/sonido_juego.mp3')

        pygame.mixer.music.set_volume(volumen_musica)  # Ajustar volumen
        pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle
    

# Función para detener la música
def detener_musica():
    pygame.mixer.music.stop()  # Detener la música
    sonido_activar_musica.stop()  # Detener sonido de activación


def manejar_configuracion():
    global musica_activada, volumen_musica
    configuracion_abierta = True
    while configuracion_abierta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Activar o desactivar la música
                if 300 < mouse_x < 500 and 150 < mouse_y < 200:
                    musica_activada = not musica_activada
                    if musica_activada:
                        reproducir_musica()  # Reproducir música
                        sonido_activar_musica.play()
                    else:
                        detener_musica()  # Detener música

                # Subir volumen
                if 300 < mouse_x < 500 and 220 < mouse_y < 270:
                    if volumen_musica < 1.0:
                        volumen_musica += 0.1
                    if musica_activada:
                        reproducir_musica()

                # Bajar volumen
                if 300 < mouse_x < 500 and 290 < mouse_y < 340:
                    if volumen_musica > 0.0:
                        volumen_musica -= 0.1
                    if musica_activada:
                        reproducir_musica()

                # Ajustar volumen con el control deslizante
                if 300 < mouse_x < 500 and 355 < mouse_y < 375:
                    volumen_musica = (mouse_x - 300) / 200  # Calcular el volumen basado en la posición del ratón
                    if musica_activada:
                        reproducir_musica()

                if 300 < mouse_x < 500 and 450 < mouse_y < 500:
                    detener_musica()  # Detener música
                    musica_activada = False  # Desactivar música


                # Volver al menú principal
                if 300 < mouse_x < 500 and 520 < mouse_y < 570:
                    configuracion_abierta = False  # Salir del bucle de configuración
                    return  # Volver al menú principal

        pygame.time.wait(10)


# Función para mostrar la pregunta y respuestas
def mostrar_pregunta(pregunta):
    global comodin_duplicar_puntos_usado, puntos
    pantalla.blit(fondo_solo_juego, (0, 0))
    pantalla.blit(imagen_fondo_para_pregunta, (50, 100)) 
    mostrar_texto(pregunta[1], 50, 100, NEGRO, fuente)
    


    for i in range(4):
        mostrar_texto(f"{i+1}. {pregunta[i+2]}", 50, 200 + i*50, NEGRO, fuente_pequeña)

    # Botón "Duplicar Puntos"
    if not comodin_duplicar_puntos_usado:
        pantalla.blit(imagen_boton_activado, (600, 200))
        #pygame.draw.rect(pantalla, AZUL, (600, 200, 150, 50))  # Rectángulo para el botón
        mostrar_texto("Duplicar Puntos", 610, 210, BLANCO, fuente_pequeña)
    else:
        pantalla.blit(imagen_boton_desactivado, (600, 200))  # Dibujar la imagen de botón desactivado
        #pygame.draw.rect(pantalla, GRIS, (600, 200, 150, 50))  # Botón desactivado (gris)
        mostrar_texto("Duplicar Puntos", 610, 210, GRIS, fuente_pequeña)

    # Botón "Pasar Pregunta"
    if not comodin_pasado_usado:
        pantalla.blit(imagen_boton_activado, (600, 270))  # Dibujar la imagen en lugar de un rectángulo
        mostrar_texto("Pasar Pregunta", 610, 280, BLANCO, fuente_pequeña)
    else:
        pantalla.blit(imagen_boton_desactivado, (600, 270))  # Dibujar la imagen de botón desactivado
        mostrar_texto("Pasar Pregunta", 610, 280, GRIS, fuente_pequeña)

    pygame.display.flip()

# Función para usar el comodín de Duplicar Puntos
def usar_comodin_duplicar_puntos():
    global comodin_duplicar_puntos_usado, puntos
    if not comodin_duplicar_puntos_usado:
        puntos *= 2  # Multiplicar los puntos por 2
        comodin_duplicar_puntos_usado = True
        # Mostrar mensaje de que se duplicaron los puntos
        pantalla.fill(BLANCO)  # Limpiar pantalla para el mensaje
        mostrar_texto("Duplicaste tu puntuación!", 250, 250, (0, 255, 0), fuente)
        pygame.display.flip()
        pygame.time.wait(1000)  # Esperar 1 segundo para que el mensaje se vea

        # Continuar con el juego mostrando la siguiente pregunta
        return True  # Señal de que se puede continuar con el juego
    return False

# Función para pasar a la siguiente pregunta sin afectar puntos ni vidas
def pasar_siguiente_pregunta():
    global comodin_pasado_usado
    comodin_pasado_usado = True

# Función para verificar la respuesta
def verificar_respuesta(respuesta_usuario, pregunta):
    global puntos, vidas, respuestas_correctas
    respuesta_correcta = int(pregunta[6]) - 1  # Convertir la respuesta correcta a índice (0-3)
    
    if respuesta_usuario == respuesta_correcta:
        # Si el comodín de duplicar puntos no ha sido usado, sumar 10 puntos
        if not comodin_duplicar_puntos_usado:
            puntos += 10
        else:
            puntos += 20  # Duplicar los puntos si se usó el comodín
        respuestas_correctas += 1
        if respuestas_correctas == 5:  # Si ha acertado 5 veces seguidas
            vidas += 1
            respuestas_correctas = 0
    else:
        puntos -= 5
        vidas -= 1
        respuestas_correctas = 0


# Función para pedir el nombre del jugador
def pedir_nombre():
    pantalla.fill(BLANCO)
    mostrar_texto("Ingresa tu nombre:", 250, 200, NEGRO, fuente_nombre)
    pygame.display.flip()

    nombre = ""
    esperando_nombre = True
    while esperando_nombre:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre != "":
                    esperando_nombre = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.key <= 127:  # Aceptar caracteres
                    nombre += evento.unicode
        pantalla.fill(BLANCO)
        mostrar_texto("Ingresa tu nombre:", 250, 200, NEGRO, fuente_nombre)
        mostrar_texto(nombre, 250, 250, NEGRO, fuente_nombre)
        pygame.display.flip()
    return nombre

# Función para mostrar el mensaje "Perdiste"
def mostrar_mensaje_perdido():
    pantalla.blit(fondo_solo_juego, (0, 0))
    mostrar_texto("¡PERDISTE!", 350, 250, GRIS, fuente)
    pygame.display.flip()
    pygame.time.wait(1000)  # Mostrar el mensaje por 1 segundo

# Función para guardar la partida en JSON
def guardar_partida(nombre, puntaje):
    partida = {
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Cargar el archivo de partidas si existe
    if os.path.exists("partidas.json"):
        with open("partidas.json", "r") as archivo:
            partidas = json.load(archivo)
    else:
        partidas = []

    # Agregar la nueva partida
    partidas.append(partida)

    # Guardar el archivo
    with open("partidas.json", "w") as archivo:
        json.dump(partidas, archivo, indent=4)

# Función para obtener y mostrar el TOP 10 de puntajes
def mostrar_top_10():
    pantalla.fill(BLANCO)
    mostrar_texto("TOP 10 Puntajes", 300, 50, NEGRO, fuente)

    # Cargar el archivo de partidas
    if os.path.exists("partidas.json"):
        with open("partidas.json", "r") as archivo:
            partidas = json.load(archivo)

        # Ordenar las partidas por puntaje (de mayor a menor)
        partidas.sort(key=lambda x: x['puntaje'], reverse=True)

        # Mostrar las mejores 10 partidas
        for i in range(min(10, len(partidas))):
            mostrar_texto(f"{i+1}. {partidas[i]['nombre']} - {partidas[i]['puntaje']} puntos", 50, 100 + i * 40, NEGRO, fuente_pequeña)
    else:
        mostrar_texto("No hay partidas guardadas.", 250, 100, NEGRO, fuente_pequeña)

    pygame.display.flip()

    # Esperar que el jugador regrese al menú
    esperando_regreso = True
    while esperando_regreso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Volver al menú principal al hacer clic
                if 300 < pygame.mouse.get_pos()[0] < 500 and 500 < pygame.mouse.get_pos()[1] < 550:
                    esperando_regreso = False
                    return


# Función para iniciar el juego
def iniciar_juego(preguntas):
    global vidas, puntos, respuestas_correctas, comodin_duplicar_puntos_usado, comodin_pasado_usado
    while vidas > 0:
        pregunta = random.choice(preguntas)  # Seleccionar una pregunta aleatoria
        mostrar_pregunta(pregunta)
        pygame.display.flip()

        # Establecer el tiempo límite para la respuesta (20 segundos)
        tiempo_limite = pygame.time.get_ticks() + 20000  # 20 segundos desde el

        esperando_respuesta = True
        while esperando_respuesta:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if evento.type == pygame.KEYDOWN:  # Detectar pulsaciones de teclas para respuestas
                    if evento.key == pygame.K_1:  # Responder con la opción 1
                        verificar_respuesta(0, pregunta)
                        esperando_respuesta = False
                    elif evento.key == pygame.K_2:  # Responder con la opción 2
                        verificar_respuesta(1, pregunta)
                        esperando_respuesta = False
                    elif evento.key == pygame.K_3:  # Responder con la opción 3
                        verificar_respuesta(2, pregunta)
                        esperando_respuesta = False
                    elif evento.key == pygame.K_4:  # Responder con la opción 4
                        verificar_respuesta(3, pregunta)
                        esperando_respuesta = False

                    # Verificar si se presionaron teclas para usar los comodines
                    if evento.key == pygame.K_d:  # Duplicar puntos
                        if not comodin_duplicar_puntos_usado:
                            if usar_comodin_duplicar_puntos():
                                esperando_respuesta = False  # Después de duplicar, ir a la siguiente pregunta

                    elif evento.key == pygame.K_p:  # Pasar pregunta
                        if not comodin_pasado_usado:
                            pasar_siguiente_pregunta()
                            esperando_respuesta = False  # Avanzar a la siguiente pregunta sin penalización

                if evento.type == pygame.MOUSEBUTTONDOWN:  # Detectar clics del ratón
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Verificar si se hizo clic en el botón "Duplicar Puntos"
                    if 600 < mouse_x < 750 and 200 < mouse_y < 250:
                        if not comodin_duplicar_puntos_usado:
                            if usar_comodin_duplicar_puntos():
                                esperando_respuesta = False  # Después de duplicar, ir a la siguiente pregunta

                    # Verificar si se hizo clic en el botón "Pasar Pregunta"
                    if 600 < mouse_x < 750 and 270 < mouse_y < 320:
                        if not comodin_pasado_usado:
                            pasar_siguiente_pregunta()
                            esperando_respuesta = False  # Avanzar a la siguiente pregunta sin penalización

                    # Verificar si se hizo clic en una de las opciones de respuesta
                    if 50 < mouse_x < 300:
                        if 200 < mouse_y < 250:  # Opción 1
                            verificar_respuesta(0, pregunta)
                            esperando_respuesta = False
                        elif 250 < mouse_y < 300:  # Opción 2
                            verificar_respuesta(1, pregunta)
                            esperando_respuesta = False
                        elif 300 < mouse_y < 350:  # Opción 3
                            verificar_respuesta(2, pregunta)
                            esperando_respuesta = False
                        elif 350 < mouse_y < 400:  # Opción 4
                            verificar_respuesta(3, pregunta)
                            esperando_respuesta = False
            # Mostrar el temporizador
            tiempo_restante = max(0, (tiempo_limite - pygame.time.get_ticks()) // 1000)  # Tiempo restante en segundos
            pygame.draw.rect(pantalla, GRIS, (300, 50, 200, 20))  # Fondo del temporizador
            pygame.draw.rect(pantalla, (255, 0, 0), (300, 50, 200 * (tiempo_restante / 20), 20))  # Barra de tiempo restante
            mostrar_texto(f"{tiempo_restante}s", 370, 50, NEGRO, fuente)

            pygame.display.flip()

            # Verificar si el tiempo ha expirado
            if pygame.time.get_ticks() > tiempo_limite:
                # Si el tiempo se acabó, restar una vida y continuar con el siguiente turno
                vidas -= 1
                esperando_respuesta = False  # Terminar la espera por la respuesta
                pantalla.fill(BLANCO)
                mostrar_texto("¡Tiempo agotado!", 300, 250, (255, 0, 0), fuente)
                pygame.display.flip()
                pygame.time.wait(1000)  # Esperar 1 segundo para mostrar el mensaje


        # Mostrar puntos y vidas restantes
        pantalla.fill(BLANCO)
        mostrar_texto(f"Puntos: {puntos}", 50, 50, NEGRO, fuente)
        mostrar_texto(f"Vidas: {vidas}", 50, 100, NEGRO, fuente)
        pygame.display.flip()
        pygame.time.wait(1000)  # Esperar un segundo antes de mostrar la siguiente pregunta

    # Fin del juego
    mostrar_mensaje_perdido()
    nombre = pedir_nombre()
    if nombre:
        guardar_partida(nombre, puntos)


def mostrar_menu():
    pantalla.fill((255, 255, 255))  # Limpiar pantalla
    pantalla.blit(fondo, (0, 0))  # Dibujar fondo

    # Obtener la posición del mouse
    pos_mouse = pygame.mouse.get_pos()

    # Crear los rectángulos de los botones
    boton_jugar = pygame.Rect(270, 100, 300, 50)
    boton_top_10 = pygame.Rect(250, 200, 300, 50)
    boton_configuracion = pygame.Rect(270, 300, 300, 50)
    boton_agregar_pregunta = pygame.Rect(245, 400, 300, 50)
    boton_modificar_opciones = pygame.Rect(245, 500, 300, 50)

    # Dibujar los botones con imágenes
    if boton_jugar.collidepoint(pos_mouse):
        pantalla.blit(imagen_boton_jugar_hover, (300, 100))  # Botón "Jugar" con hover
    else:
        pantalla.blit(imagen_boton_jugar, (300, 100))  # Botón "Jugar" normal

    if boton_top_10.collidepoint(pos_mouse):
        pantalla.blit(imagen_boton_top10_hover, (300, 200))  # Botón "TOP 10" con hover
    else:
        pantalla.blit(imagen_boton_top10, (300, 200))  # Botón "TOP 10" normal

    if boton_configuracion.collidepoint(pos_mouse):
        pantalla.blit(imagen_boton_config_hover, (300, 300))  # Botón "Configuración" con hover
    else:
        pantalla.blit(imagen_boton_config, (300, 300))  # Botón "Configuración" normal

    if boton_agregar_pregunta.collidepoint(pos_mouse):
        pantalla.blit(imagen_boton_config_hover, (300, 400))  # Botón "Agregar Pregunta" con hover
    else:
        pantalla.blit(imagen_boton_config, (300, 400))  # Botón "Agregar Pregunta" normal

    if boton_modificar_opciones.collidepoint(pos_mouse):
        pantalla.blit(imagen_boton_config_hover, (300, 500))  # Botón "Modificar Opciones" con hover
    else:
        pantalla.blit(imagen_boton_config, (300, 500))  # Botón "Modificar Opciones" normal

    # Mostrar los textos de los botones
    texto_jugar = fuente.render("Jugar", True, NEGRO)
    texto_top_10 = fuente.render("TOP 10", True, NEGRO)
    texto_configuracion = fuente.render("Configuración", True, NEGRO)
    texto_agregar_pregunta = fuente.render("Agregar Preguntas", True, NEGRO)
    texto_modificar_opciones = fuente.render("Modificar Opciones", True, NEGRO)

    pantalla.blit(texto_jugar, (boton_jugar.x + 100, boton_jugar.y + 10))
    pantalla.blit(texto_top_10, (boton_top_10.x + 100, boton_top_10.y + 10))
    pantalla.blit(texto_configuracion, (boton_configuracion.x + 50, boton_configuracion.y + 10))
    pantalla.blit(texto_agregar_pregunta, (boton_agregar_pregunta.x + 50, boton_agregar_pregunta.y + 10))
    pantalla.blit(texto_modificar_opciones, (boton_modificar_opciones.x + 50, boton_modificar_opciones.y + 10))

    pygame.display.flip()

    # Manejo de eventos
    ejecutar = True
    jugando = False
    while not jugando and ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                ejecutar = False
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detectar clic en los botones
                if boton_jugar.collidepoint(evento.pos):
                    print("Iniciando juego...")
                    mostrar_categorias()
                    # Esperar la selección de categoría
                    while categoria_seleccionada is None:
                        pygame.time.wait(100)
                    preguntas = cargar_preguntas(categoria_seleccionada)
                    iniciar_juego(preguntas)
                    jugando = True

                elif boton_top_10.collidepoint(evento.pos):
                    mostrar_top_10()

                elif boton_configuracion.collidepoint(evento.pos):
                    mostrar_configuracion()
                    manejar_configuracion()
                    mostrar_menu()

                elif boton_agregar_pregunta.collidepoint(evento.pos):
                    agregar_pregunta()  # Agregar preguntas manualmente o desde archivo

                elif boton_modificar_opciones.collidepoint(evento.pos):
                    modificar_opciones()  # Modificar opciones del juego



# Iniciar el juego
mostrar_menu()