"""
Este codigo hace lo siguiente:
1. Genera y despliega una ventana pygame
2. Esta ventana contiene una cruz en el centro de la ventana que cambia de color
   y multiples circulos que giran en sentido horario o anti-horario con 
   distintas velocidades. La duracion de cada circulo es de aproximadamente 
   0.2 fps, luego de esto el circulo sera reemplazado por otro circulo con una 
   nueva posicion aleatoria.
3. Estos movimientos permiten al viusalizador sacar una conclusion respecto a si
   los circulos estan realmente cambiando de velocidad, permitiendo asi hacer un
   analisis mental


Aspectos tecnicos
 - El color de la cruz, la velocidad y el sentido de rotacion de los circulos 
   (a lo que les llamaremos estados) varian dependiendo de la cantidad de 
   segundos que hayan transcurrido desde el inicio del programa. El cambio entre 
   estados es siempre constante. Por ejemplo, el cambio entre el estado A y el 
   estado B siempre sucedera a los 4 segundos desde el inicio del programa.
 - El tiempo definido para el cambio entre estados se extrajo de un estudio 
   realizado por la universidad de Michigan
 - La duracion de cada circulo es de aproximadamente 6 fps, luego de esto el
   circulo desaparecera y se creara un nuevo circulo en una posicion aleatoria
"""

#todo: hacer que los circulos aparezcan y desaparezcan dado un intervalo de 
# tiempo

import pygame
import random
from math import sin, cos
import sys
from random import uniform, randint, choice
from time import time

pygame.init()

#colors
BLACK = (0, 0, 0)
BLUE = (103, 199, 235)
WHITE = (255, 255, 255)
YELLOW = (255,255,51)

#Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 668
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Create Screen
SCREEN.fill(WHITE)

#tiempo
tiempo_actual = time()

#Variables
running = True
timer = pygame.time.Clock()

#Scene index
global scene_index 
scene_index = 0

class Cruz:
   """
   Cruz localizada en el centro de la pantalla.
   Sirve como punto de mira para los sujetos de prueba.
   Dependiendo del estado, es de color azul o amarillo
   """

   def __init__(self):
      self.length = 10
      self.colores = [BLUE, YELLOW]
      self.color_index = 0
      self.width = 5
      self.linea_horizontal = [(int(SCREEN_WIDTH/2) - self.length, 
                                int(SCREEN_HEIGHT/2)), 
                               (int(SCREEN_WIDTH/2) + self.length, 
                                int(SCREEN_HEIGHT/2))]
      self.linea_vertical = [(int(SCREEN_WIDTH/2), 
                              int(SCREEN_HEIGHT/2) - self.length),
                             (int(SCREEN_WIDTH/2), 
                              int(SCREEN_HEIGHT/2) + self.length)]

   def update(self):
      raise NotImplementedError
   
   def render(self):
      """
      Renderiza la cruz en la superficie SCREEN

      Input:
         None
      Output:
         None
      """
      #dibjuar linea vertical de la cruz
      pygame.draw.line(SCREEN, self.colores[self.color_index], 
                       self.linea_vertical[0], 
                       self.linea_vertical[1], 
                       self.width)

      #dibujar linea horizontal de la cruz
      pygame.draw.line(SCREEN, self.colores[self.color_index], 
                       self.linea_horizontal[0], 
                       self.linea_horizontal[1], 
                       self.width)

   def elegir_color(self, color):
      """
      Elige el color de la cruz. 
      Utiliza un input para recibir le color mediante la consola.
      Al recibir el intput, cambia el valor de self.color_index para ajustar al
      color adecuado.

      Input:
         color (str): color entre azul y amarillo

      Output:
         None
      """      
      assert type(color) == str, "el tipo de color debe ser str, obtuvo {}".\
         format(type(color))
      if (color == "azul"):
         self.color_index = 0
      elif (color == "amarillo"):
         self.color_index = 1
      else:
         raise ValueError('El color ingresado no corresponde a amarillo ni a \
            azul')

class Circulo:
   """
   Circulo negro que rota al rededor del centro de la ventana. 
   Utiliza una parametrizacion de la forma canonica del circulo como trayectoria.
   Desaparece y vuelve a aparecer cada cierto tiempo aleatorio
   """

   def __init__(self, radio_trayectoria):
      #Aspecto
      self.color = BLACK
      self.es_visible = False

      #Velocidad
      self.velocidad = 0

      #Posicion
      self.h = SCREEN_WIDTH/2
      self.k = SCREEN_HEIGHT/2
      self.t = 0
      self.x = self.h
      self.y = self.k
      self.radio_trayectoria = radio_trayectoria

      #tiempo
      self.current_time = time() 
      
   def update(self):
      self.visibilidad()
      self.t += self.velocidad
      self.x = int(self.h + self.radio_trayectoria*cos(self.t))
      self.y = int(self.k + self.radio_trayectoria*sin(self.t))
   
   def render(self):
      """
      Renderiza el circulo en la superficie SCREEN

      Input:
         None
      Output:
         None
      """
      if (self.es_visible):
         pygame.draw.circle(SCREEN, self.color, (self.x, self.y), 5)

   def set_velocidad(self, nueva_velocidad):
      """
      Cambia self.velocidad por nueva_velocidad

      Input:
         nueva_velocidad (int): nueva velocidad

      Output:
         None
      """

      assert type(nueva_velocidad) == int or type(nueva_velocidad) == float, \
         "nueva_velocidad debe ser un \'int\' o \'float\', obtuvo {}".format(
                                                         type(nueva_velocidad))
      self.velocidad = nueva_velocidad

   def visibilidad(self):
      """
      Cambia el atributo self.es_visible cada 0.1 segundos, esto significa que
      el circulo se va a ver por 0.1 segundos y luego desaparecera por otros 0.1
      segundos. Aunque el circulo no sea visible, este seguira con su 
      trayectoria.
      """
      if (tiempo_actual >= self.current_time):
         self.es_visible = not self.es_visible
         self.current_time = time() + uniform(0.2, 0.5)

   def empezar_localizacion_aleatoria(self):
      """
      Elije un valor aleatorio para el parametro t, lo que indica la posicion
      en la trayectoria dadas las ecuaciones parametricas.
      """
      self.t = uniform(-3,3) 

class Flecha:

   def __init__(self):
      self.right_arrow = pygame.image.load('Arrow.png')
      self.right_arrow = pygame.transform.scale(self.right_arrow, (100, 100))
      self.image_rect = self.right_arrow.get_rect()
      self.image_rect.center = (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2) - 50)
      self.left_arrow = pygame.transform.flip(self.right_arrow, True, False)
      self.renderizar_flecha_izquierda = None
      self.visibilidad = True

   def render(self):
      """
      Renderiza una de las dos flechas (flecha que apunta a la izquierda o a la 
      derecha) en la superficie SCREEN. 
      Renderiza por defecto la flecha izquierda

      Input:
         None
      Output:
         None
      """
      if (self.visibilidad):
         if (self.renderizar_flecha_izquierda):
            SCREEN.blit(self.left_arrow, self.image_rect)
         else:
            SCREEN.blit(self.right_arrow, self.image_rect)

   def update(self):
      pass

   def set_visibilidad(self, nueva_visibilidad):
      """
      Cambia self.visibilidad por nueva_visibilidad

      Input:
         nueva_visibilidad (bool): nueva_visibilidad

      Output:
         None
      """

      assert type(nueva_visibilidad) == bool, "nueva_visibilidad debe ser un \
         \'int\' o \'float\', obtuvo {}".format(type(nueva_visibilidad))
      self.visibilidad = nueva_visibilidad

   def elegir_direccion(self, direccion):
      """
      Elige la direccion de la flecha dada esa direccion

      Input:
         direccion (str): la direccion a la cual la flecha va a apuntar

      Output:
         None
      """
      if (direccion == "izquierda"):
         self.renderizar_flecha_izquierda = True
      else:
         self.renderizar_flecha_izquierda = False

class Scene:

    def __init__(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class SceneHandler:

    def __init__(self):
      escena1 = Escena1()
      self.color_cruz_incial = escena1.retornar_color_elegido()
      
      self.scenes_list = [escena1]

      self.iniciar_escena2 = False


    def render(self):
      global scene_index
      try:
         self.scenes_list[scene_index].render()
      except:
         pass

    def update(self):
      global scene_index
      if (scene_index == 1 and not self.iniciar_escena2):
         self.iniciar_escena2 = True
         escena2 = Escena2()
         escena2.obtener_color_cruz(self.color_cruz_incial)
         self.scenes_list.append(escena2)
      try:
         self.scenes_list[scene_index].update()
      except:
         pass
      

class Escena1(Scene):
   """
      Muestra la cruz y la flecha por 1 segundo, luego desaparece la flecha, 
      crea y renderiza los circulos en movimiento en sentido horario y 
      anti-horarioen la pantalla y mantiene ese estado de movimiento por 4.1 
      segundos.
      Posteriormente puede que solo le aplica un aumento de velocidad a los 
      circulos que se mueven en la direccion de la flecha (es aleatorio el 
      aumento de velocidad)
      El tiempo total de esta escena 15.4 segundos.

      """

   def __init__(self):
      self.direccion = input("Elige la dirección a la cual se debe enfocar " \
         "\'izquierda\' o \'derecha\': \n")
      
      if (self.direccion != "izquierda" and self.direccion != "derecha"):
         raise ValueError("la direccion debe ser \'izquierda\' o \'derecha\'")
      
      self.color = input("Ingrese un color, puede ser \'amarillo\' o \'azul\': \n")

      #flecha
      self.flecha = Flecha()
      self.flecha.elegir_direccion(self.direccion)

      #cruz
      self.cruz = Cruz()
      self.cruz.elegir_color(self.color)

      #circulos
      self.lista_de_circulos_sentido_horario = []
      self.lista_de_circulos_sentido_antihorario = []

      #tiempos
      self.tiempo_desplegar_circulos = time() + 1
      self.tiempo_aumentar_velocidad_circulos = time() + 5.1

      #aumentar_direccion_aleatoria
      direcciones_posibles = ["izquierda", "derecha"]
      self.aumentar_direccion_aleatoria = choice(direcciones_posibles)
      print("la direccion de circulos que van a aumentar la velocidad es:", 
            "{}".format(self.aumentar_direccion_aleatoria))

      self.tiempo_total = time() + 6.1

   def update(self):
      if (self.tiempo_total <= tiempo_actual):
         global scene_index
         print("cambio a escena 2!")
         scene_index = 1
      if (self.tiempo_desplegar_circulos <= tiempo_actual):
         self.crear_puntos(0.04) #0.04
         self.flecha.set_visibilidad(False)
      if (self.tiempo_aumentar_velocidad_circulos <= tiempo_actual):
         """
         Si el tiempo es el correcto para aumentar la velocidad, 
         """
         if (self.aumentar_direccion_aleatoria == "izquierda"):
            for c in self.lista_de_circulos_sentido_antihorario:
               c.set_velocidad(-0.05)
         else:
            for c in self.lista_de_circulos_sentido_horario:
               c.set_velocidad(0.05)

      self.flecha.update()

   def render(self):
      for c in self.lista_de_circulos_sentido_horario + \
               self.lista_de_circulos_sentido_antihorario:
         c.update()
         c.render()

      self.flecha.render()
      self.cruz.render()
    
   def crear_puntos(self, velocidad):
      """
      Crea los circulos que se van a mover en ambos sentidos en la pantalla.
      Añade los circulos a una lista dependiendo de su sentido

      Si self.lista_de_circulos_sentido_horario no esta vacia, no hace nada.
      Esto sucede debido a que este metodo se va a llamar multiples veces en 
      update y solo se quiere llamar una vez.

      Input:
      - velocidad (int): velocidad de rotacion de los circulos
      Output:
      - None
      """
      if (len(self.lista_de_circulos_sentido_horario) != 0):
         return
      
      #Puntos que giran en sentido horario
      for circulos_en_radio in range(11):
         radio_trayectoria = 150
         for numero_de_radios in range(10):
            c = Circulo(radio_trayectoria)
            c.set_velocidad(velocidad)
            c.empezar_localizacion_aleatoria()
            self.lista_de_circulos_sentido_horario.append(c)
            radio_trayectoria += 20

      #Puntos que giran en sentido anti-horario
      for circulos_en_radio in range(10):
         radio_trayectoria = 150
         for numero_de_radios in range(11):
            c = Circulo(radio_trayectoria)
            c.set_velocidad(-velocidad)
            c.empezar_localizacion_aleatoria()
            self.lista_de_circulos_sentido_antihorario.append(c)
            radio_trayectoria += 20

   def retornar_color_elegido(self):
      """
      Retorna el color elegido para la cruz
      """
      return self.color

class Escena2(Scene):
   """
   Muestra la cruz por 11.8 segundos (da tiempo para responder si la velocidad 
   aumento en la escena anterior), luego crea y renderiza los circulos en 
   moviento en un solo sentido (es aleatorio el sentido). 
   Despues de 15.1 segundos (desde el inicio de la escena) se decide 
   aleatoriamente si los circulos van a aumentar la velocidad. 
   La escena dura 2 segundos mas.
   Posteriormente se tienen 10.8 segundos en los cuales solo hay presencia de la
   cruz.
   La duracion total es de 28.0 segundos.
   """

   def __init__(self):
      #Lista de circulos
      self.lista_de_circulos = []

      #Sentido de circulos
      lista_opciones_multiplicador_de_sentido = [-1, 1]
      self.multiplicador_de_sentido = choice(
         lista_opciones_multiplicador_de_sentido)
      if (self.multiplicador_de_sentido == 1):
         print("velocidad aumentada en segundo caso!")
      else:
         print("no se aumento la velocidad")

      #cruz
      self.color_cruz = None
      self.cruz = Cruz()
      
      #tiempos
      self.tiempo_desplegar_circulos = time() + 11.8
      self.tiempo_aumentar_velocidad_circulos = time() + 15.1
      self.tiempo_esperar_respuesta = time() + 28


   def update(self):
      if (self.tiempo_esperar_respuesta <= tiempo_actual):
         self.lista_de_circulos.clear()

      elif (self.tiempo_aumentar_velocidad_circulos <= tiempo_actual and 
            self.multiplicador_de_sentido == 1):

         if (self.multiplicador_de_sentido < 0):
            for c in self.lista_de_circulos:
               c.set_velocidad(-0.5)
         else:
            for c in self.lista_de_circulos:
               c.set_velocidad(0.5)
      elif (self.tiempo_desplegar_circulos <= tiempo_actual):
         self.crear_puntos(0.04)
         
   def render(self):
      for c in self.lista_de_circulos:
         c.update()
         c.render()
      self.cruz.render()

   def crear_puntos(self, velocidad):
      """
      Crea los circulos que se van a mover en un solo sentido en la pantalla.
      El sentido es aleatorio
      Añade esos circulos a self.lista_de_circulos

      Si self.lista_de_circulos no esta vacia, no hace nada.
      Esto sucede debido a que este metodo se va a llamar multiples veces en 
      update y solo se quiere llamar una vez.

      Input:
      - velocidad (int): velocidad de rotacion de los circulos
      Output:
      - None
      """
      if (len(self.lista_de_circulos) != 0):
         return
      
      velocidad = velocidad * self.multiplicador_de_sentido

      for circulos_en_radio in range(11):
         radio_trayectoria = 150
         for numero_de_radios in range(10):
            c = Circulo(radio_trayectoria)
            c.set_velocidad(velocidad)
            c.empezar_localizacion_aleatoria()
            self.lista_de_circulos.append(c)
            radio_trayectoria += 20

   def obtener_color_cruz(self, color):
      """
      Obtiene un color para asignarselo a la cruz

      Input: 
         color (str): color entre amarillo o azul
      """
      if (color == "azul"):
         self.color_cruz = "amarillo"
      else:
         self.color_cruz = "azul"
      
      self.cruz.elegir_color(self.color_cruz)

def crear_puntos(velocidad):
   lista_de_circulos = []
   
   #Puntos que giran en sentido horario
   

   #Puntos que giran en sentido anti-horario
   for circulos_en_radio in range(10):
      radio_trayectoria = 150
      for numero_de_radios in range(11):
         c = Circulo(radio_trayectoria)
         c.set_velocidad(-velocidad)
         c.empezar_localizacion_aleatoria()
         lista_de_circulos.append(c)
         radio_trayectoria += 20

   return lista_de_circulos

def cue(flecha):
   """
   Es la escena que indica la rotacion de los circulos (ya sea sentido horario o
   anti-horario), se hace mediante una flecha que apunta a la izquierda o a la 
   derecha.
   """
   assert type(flecha) == Flecha

def stimulus(lista_de_circulos):
   assert type(lista_de_circulos) == list, "type(lista_de_circulos) debe ser \
      del tipo \'list\', se obtuvo {}".format(type(lista_de_circulos))
   for c in lista_de_circulos:
      c.update()
      c.render()



if __name__ == "__main__":

   #lista_de_circulos = crear_puntos(0.04)
   
   
   fuente = pygame.font.Font(None, 30)
   Escenas = SceneHandler()

   while running:
      timer.tick(60) 
      tiempo_actual = time()
      SCREEN.fill(WHITE)
      fps = fuente.render(str(int(timer.get_fps())), True, pygame.Color('black'))
      SCREEN.blit(fps, (50, 50))
      events = pygame.event.get()
      
      for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and bool(event.mod and pygame.KMOD_ALT):  
                    print("Alt+F4")
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
      

      Escenas.update()
      Escenas.render()
      
      

      pygame.display.flip()

sys.exit()