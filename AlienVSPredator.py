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

class Depredador:
  def __init__(self):
    self.vida = 50
    self.simbolo = "🤖 "
    
class Tablero:
  #Al tablero se le define un tamaño, será una matriz cuadrada de NxN
  def __init__(self, n):
    self.n = n
    self.matriz = DLinkedList()

    #La variable de probabilidad vacio es solo un porcentaje que se usará para que la matriz no se llene por completo de "+" o "-" sino que tambien hayan "." (espacios vacios)
  def crear_tablero(self, alien, depredador, probabilidad_vacio=0.55):
    simbolos = ['+', '-']
    depredador_coord = [(random.randint(0,self.n-1),random.randint(0,self.n-1))]#El depredador_coord aparece de manera aleatoria al iniciar el juego
    print("El depredador_coord saldrá en la posición:",depredador_coord)
    alien_coord = [] #El alien_coord deberá elegir su posición de aparición 
    while True:
      coordenadas = str(input("Ingrese las coordenadas en las que desea aparecer al alien: "))
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
        break
    #Si las coordenadas del alien_coord resultan ser las mismas que se generaron para el depredador_coord, entonces volvemos a generar nuevas coordenadas
    while(alien_coord == depredador_coord):
      depredador_coord = [(random.randint(0,self.n-1),random.randint(0,self.n-1))]

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

alien_coord = Alien()
depredador = Depredador()
tablero = Tablero(6)
tablero.crear_tablero(alien_coord, depredador)
tablero.imprimir_tablero()