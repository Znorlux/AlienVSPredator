import random
import time
class Node:
  def __init__(self, value):
    self.value = value
    self.next = None
    self.prev = None
#Usamos las listas doblemente enlazadas de la clase, si no sabes como funcionan, revisa la clase 
class DLinkedList:
  def __init__(self):
    self.header = Node(None)
    self.trailer = Node(None)
    self.header.next = self.trailer
    self.trailer.prev = self.header

  def traverse(self):
    current = self.header.next
    while(current != self.trailer):
        current.value.traverse()
        print("<=>", end=" ")
        current = current.next
  
  def add_at_head(self, value):
    if(self.header.next == self.trailer):
      #agrego el primer elemento
      new_node = Node(value)
      self.header.next = new_node
      new_node.prev = self.header
      new_node.next = self.trailer
      self.trailer.prev = new_node
    else:
      new_node = Node(value)
      old_head = self.header.next
      self.header.next = new_node
      new_node.prev = self.header
      new_node.next = old_head
      old_head.prev = new_node

class Alien:
  def __init__(self):
    self.vida = 50
    self.simbolo = "👽 "
    self.coordenadas = None

class Depredador:
  def __init__(self):
    self.vida = 50
    self.simbolo = "🤖 "
    self.coordenadas = None
    
class Tablero:
  #Al tablero se le define un tamaño, será una matriz cuadrada de NxN
  def __init__(self, n):
    self.n = n
    self.matriz = DLinkedList()

    #La variable de probabilidad vacio es solo un porcentaje que se usará para que la matriz no se llene por completo de "+" o "-" sino que tambien hayan "." (espacios vacios)
  def crear_tablero(self, alien, depredador, probabilidad_vacio=0.55):
    simbolos = ['+', '-']
    depredador_coord = [(random.randint(0,self.n-1),random.randint(0,self.n-1))]#El depredadoraparece de manera aleatoria al iniciar el juego
    depredador.coordenadas = depredador_coord
    print("El depredador saldrá en la posición:",depredador.coordenadas)
    alien_coord = [] #El alien deberá elegir su posición de aparición 
    while True:
      coordenadas = str(input("Ingrese las coordenadas en las que desea aparecer al alien: "))
      #coordenadas = "0,0"
      coordenadas = coordenadas.strip()
      coordenadas = coordenadas.split(",")
      #Revisamos que las coordenadas sean dos numeros y que estén en la longitud de la matriz
      if len(coordenadas) != 2 or not coordenadas[0].isdigit() or not coordenadas[1].isdigit() or int(coordenadas[0]) < 0 or int(coordenadas[0]) > self.n-1 or int(coordenadas[1]) < 0 or int(coordenadas[1]) > self.n-1:
        print("Posición inválida")
      else:
        fila_alien_coord = int(coordenadas[0])
        columna_alien_coord = int(coordenadas[1])
        alien_coord.append(fila_alien_coord)
        alien_coord.append(columna_alien_coord)
        alien_coord = [tuple(alien_coord)]
        alien.coordenadas = alien_coord
        break
    #Si las coordenadas del alien resultan ser las mismas que se generaron para el depredador, entonces volvemos a generar nuevas coordenadas
    while(alien_coord == depredador_coord):
      depredador_coord = [(random.randint(0,self.n-1),random.randint(0,self.n-1))]
      depredador.coordenadas = depredador_coord

    for i in range(self.n):
      fila = DLinkedList() #Creamos filas que seran listas doblemente enlazadas
      for j in range(self.n): 
        #print((i,j))
        
        if (i,j) in depredador_coord:
          fila.add_at_head(depredador) #add_at_head sirve para añadir un elemento a la ultima posicion de la lista enlazada
        elif (i,j) in alien_coord:
          fila.add_at_head(alien)
        else:
          if random.random() < probabilidad_vacio:
            fila.add_at_head(' . ')
          else:
            simbolo = random.choice(simbolos)#Los simbolos están almacenados en una lista, se escogerá alguno de los dos de manera aleatoria
            if simbolo == '+':
              fila.add_at_head(' + ')
            else:
              fila.add_at_head(' - ')
              if depredador_coord is None:
                depredador_coord = (i,j)
      self.matriz.add_at_head(fila)#Al finalizar este bucle se añadirá la fila a la matriz del tablero, y se repite N veces segun su tamaño

  def imprimir_tablero(self):
    current = self.matriz.trailer.prev
    #Lo siguiente solo es para imprimir el numero de las columnas arriba, para que sea más facil saber donde se está
    print(" 0  ", end="")
    for i in range(1, self.n):
      print(i, end="  ")
    print()
    while current != self.matriz.header:
        fila = current.value
        node = fila.trailer.prev
        while node != fila.header:
            value = node.value
            if isinstance(value, Alien):
                print(value.simbolo, end='')
            elif isinstance(value, Depredador):
                print(value.simbolo, end='')
            elif len(value) == 1:
                print(' ', end='')
            else:
                print(value, end='')
            node = node.prev
        print()
        current = current.prev

class Juego:
  def __init__(self, tablero, controlador) -> None:
    self.tablero = tablero
    tablero.imprimir_tablero()
    self.controlador_juego(controlador)
  
  def controlador_juego(self,controlador):
    if controlador == False:
      self.obtener_movimiento_alien()
    elif controlador == True:
      print()
      print("El juego ha finalizado")
      exit()

  def obtener_movimiento_alien(self):
    #Averiguamos en que coordenada está el alien para decirle a donde se puede mover 
    coordenadas = alien.coordenadas[0]#Lista con Tupla con las coordenadas del alien
    #Sacamos los movimientos del alien
    movimiento_izquierda = (coordenadas[0], coordenadas[1]-1)
    movimiento_derecha = (coordenadas[0], coordenadas[1]+1)
    movimiento_arriba = (coordenadas[0]-1, coordenadas[1])
    movimiento_abajo = (coordenadas[0]+1, coordenadas[1])
    posibles_ataques= [movimiento_arriba, movimiento_abajo, movimiento_derecha, movimiento_izquierda]
    if depredador.coordenadas[0] in posibles_ataques:
      while True:
        atacar = input("El depredador se encuentra en su rango de ataque, desea atacarlo? (s/n) ").lower()
        if atacar == "s":
          depredador.vida -= 10
          print("La vida del depredador disminuyó a ", depredador.vida)
          break
        elif atacar == "n":
          break
    movimientos_disponibles = ["arriba", "abajo", "derecha", "izquierda"]
    #Si está en la fila 0 entonces no podrá ir para arriba
    if coordenadas[0] == 0:
      movimientos_disponibles.remove("arriba")
      #Si además está en la columna cero, entonces tampoco podrá ir para la izquierda
      if coordenadas[1] == 0:
        movimientos_disponibles.remove("izquierda")
      #O si está en la ultima columna, entonces no puede ir a la derecha
      elif coordenadas[1] == tablero.n-1:
        movimientos_disponibles.remove("derecha")
    if coordenadas[0] == tablero.n-1:
      movimientos_disponibles.remove("abajo")
      if coordenadas[1] == 0:
        movimientos_disponibles.remove("izquierda")
      elif coordenadas[1] == tablero.n-1:
        movimientos_disponibles.remove("derecha")
    #Ahora verificamos que no esté ni en la primera columna ni en la ultima
    if coordenadas[1] == 0:
      if "izquierda" in movimientos_disponibles:
        movimientos_disponibles.remove("izquierda")
    if coordenadas[1] == tablero.n-1:
      if "derecha" in movimientos_disponibles:
        movimientos_disponibles.remove("derecha")
    #Despues de verificar que movimientos puede realizar el Alien, se los mostramos
    print("Ingrese el movimiento que desea realizar: ", end="")
    #Este ciclo solo es para imprimir los elementos de la lista de manera bonita
    for i, movimiento in enumerate(movimientos_disponibles):
      if i == len(movimientos_disponibles) - 1:
          print(movimiento, end="")
      else:
          print(movimiento, end=", ")
    print()
    while True:
      nuevo_mov = input().lower()
      if nuevo_mov not in movimientos_disponibles:
        print("Ingresa un valor valido, no puedes moverte en esa dirección")
      elif nuevo_mov == "arriba":
        direccion = movimiento_arriba
        break 
      elif nuevo_mov == "abajo":
        direccion = movimiento_abajo
        break
      elif nuevo_mov == "derecha":
        direccion = movimiento_derecha
        break
      elif nuevo_mov == "izquierda":
        direccion = movimiento_izquierda
        break
    print("Tu direccion de movimiento es ",nuevo_mov, ", con coordenadas ",direccion)
    self.mover_alien(direccion,alien)

  def mover_alien(self, direccion,alien):
    direccion = [direccion]
    current = tablero.matriz.trailer.prev
    fila = current.value
    node = fila.trailer.prev
    for i in range(tablero.n):
      for j in range(tablero.n):
        #print("coordenadas: ",(i,j))
        #print("NODO:", node.value)
        #Verificamos que si el nodo es None, lo que significa que ya se llego al final de la fila y se debe pasar a la siguiente
        if node.value == None:
          current = current.prev
          fila = current.value
          node = fila.trailer.prev
          
        #Verificamos haber llegado a la coordenada correcta, y de esta manera colocamos al Alien ahí
        if (i,j) in direccion:
          #Verificamos que hay en el value del nodo, para saber si se le resta vida al alien o no
          if node.value == " + ":
            alien.vida += 10
            print("Tu vida ha aumentado 10 puntos, ahora tienes: ",alien.vida, "de vida")
          elif node.value == ' - ':
            alien.vida -= 10
            #if alien.vida >
            print("Tu vida ha disminuido 10 puntos, ahora tienes: ",alien.vida, "de vida")
          elif isinstance(node.value, Depredador):
            print("Por qué intentas suicidarte?")
            alien.vida -= 25
            print("Tu vida ha disminuido a ", alien.vida,"por intentar estar en el mismo lugar que el depredador!")
            tablero.imprimir_tablero()
            self.obtener_movimiento_depredador()
          node.value =  alien
        node = node.prev
    if(self.end_game()):
      self.estado_de_juego(True)
    self.borrar_alien(alien, direccion)

  def borrar_alien(self,alien, nuevas_coord):
    current = tablero.matriz.trailer.prev
    fila = current.value
    node = fila.trailer.prev
    for i in range(tablero.n):
      for j in range(tablero.n):
        if node.value == None:
          current = current.prev
          fila = current.value
          node = fila.trailer.prev
        if (i,j) in alien.coordenadas:
          node.value = ' . '
        node = node.prev
    #Actualizamos las coordenadas del alien
    alien.coordenadas = nuevas_coord
    tablero.imprimir_tablero()
    self.obtener_movimiento_depredador()

  def obtener_movimiento_depredador(self):
    coordenadas = depredador.coordenadas[0]#Lista con Tupla con las coordenadas del depredador
    #Sacamos los movimientos del depreadador
    movimiento_izquierda = (coordenadas[0], coordenadas[1]-1)
    movimiento_derecha = (coordenadas[0], coordenadas[1]+1)
    movimiento_arriba = (coordenadas[0]-1, coordenadas[1])
    movimiento_abajo = (coordenadas[0]+1, coordenadas[1])
    diagonal_arriba_derecha = (movimiento_arriba[0], movimiento_arriba[1]+1)
    diagonal_arriba_izquierda = (movimiento_arriba[0], movimiento_arriba[1]-1)
    diagonal_abajo_derecha = (movimiento_abajo[0], movimiento_abajo[1]+1)
    diagonal_abajo_izquierda = (movimiento_abajo[0], movimiento_abajo[1]-1)

    movimientos_disponibles = [movimiento_abajo, movimiento_arriba, movimiento_derecha, movimiento_izquierda, diagonal_arriba_derecha, diagonal_arriba_izquierda, diagonal_abajo_derecha, diagonal_abajo_izquierda]
    #print(movimientos_disponibles)
    movimientos_validos = []
    for movimiento in movimientos_disponibles:
        if not (-1 in movimiento or tablero.n in movimiento):
            movimientos_validos.append(movimiento)
    movimiento = random.choice(movimientos_validos)
    self.mover_depredador(movimiento)
  
  def mover_depredador(self, coordenadas):
    print()
    print("Es turno del depredador, preparando su movimiento...")
    time.sleep(3)
    print("El depredador se mueve a las coordenadas ", coordenadas)
    coordenadas = [coordenadas]
    current = tablero.matriz.trailer.prev
    fila = current.value
    node = fila.trailer.prev
    for i in range(tablero.n):
      for j in range(tablero.n):
        if node.value == None:
          current = current.prev
          fila = current.value
          node = fila.trailer.prev
        if (i,j) in coordenadas:
          if node.value == " + ":
            depredador.vida += 10
            print("La vida del depredador ha aumentado 10 puntos, ahora tiene: ",depredador.vida, "de vida")
          elif node.value == ' - ':
            depredador.vida -= 10
            print("La vida del depredador ha disminuido 10 puntos, ahora tiene: ",depredador.vida, "de vida")
          elif isinstance(node.value, Alien):
            alien.vida -= 25
            print("El depredador ha atacado al alien, la vida del alien ahora es ", alien.vida)
            tablero.imprimir_tablero()
            print()
            self.estado_de_juego(self.end_game())
          node.value = depredador
        node = node.prev
    if(self.end_game()):
      self.estado_de_juego(True)
    self.borrar_depredador(depredador, coordenadas)

  def borrar_depredador(self, depredador, nuevas_coord):
    current = tablero.matriz.trailer.prev
    fila = current.value
    node = fila.trailer.prev
    for i in range(tablero.n):
      for j in range(tablero.n):
        if node.value == None:
          current = current.prev
          fila = current.value
          node = fila.trailer.prev
        if (i,j) in depredador.coordenadas:
          node.value = ' . '
        node = node.prev
    #Actualizamos las coordenadas del alien
    depredador.coordenadas = nuevas_coord
    tablero.imprimir_tablero()
    print()
    self.estado_de_juego(self.end_game())

  def end_game(self):
    if depredador.vida <= 0:
      print("El alien ha ganado!")
      return True
    elif alien.vida <= 0:
      print("El Depreador ha ganado!")
      return True
    else:
      return False
    
  def estado_de_juego(self, estado):
    if estado == True:
      self.controlador_juego(True)
    else:
      self.controlador_juego(False)
  
alien = Alien()
depredador = Depredador()
tablero = Tablero(6)
tablero.crear_tablero(alien, depredador)
#tablero.imprimir_tablero()

Controlador = Juego(tablero, False)
tablero.imprimir_tablero()
