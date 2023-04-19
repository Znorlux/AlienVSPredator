import random
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
  def __init__(self, tablero) -> None:
    self.tablero = tablero
    self.realizar_movimiento()
     
  def realizar_movimiento(self):
    #Averiguamos en que coordenada está el alien para decirle a donde se puede mover 
    coordenadas = alien.coordenadas[0]#Tupla con las coordenadas del alien
    #Sacamos los movimientos del alien
    movimiento_izquierda = (coordenadas[0], coordenadas[1]-1)
    movimiento_derecha = (coordenadas[0], coordenadas[1]+1)
    movimiento_arriba = (coordenadas[0]-1, coordenadas[1])
    movimiento_abajo = (coordenadas[0]+1, coordenadas[1])
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
    self.actualizar_matriz(direccion,alien)

  def actualizar_matriz(self, direccion,alien):
     current = tablero.matriz.trailer.prev
     fila = current.value
     node = fila.trailer.prev 
     for i in range(tablero.n):
      for j in range(tablero.n):
        if (i,j) == direccion:
          print(node.value)
          node.value = alien.simbolo
          #node.value = alien.simbolo
          #alien.coordenadas = ' . '
    

    
alien = Alien()
depredador = Depredador()
tablero = Tablero(6)
tablero.crear_tablero(alien, depredador)
tablero.imprimir_tablero()

Controlador = Juego(tablero)
tablero.imprimir_tablero()
