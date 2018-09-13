import math as math
import numpy as np
from noise import pnoise2, snoise2

mapSizeX = 1024
mapSizeY = 1024
seaLevel = 100  # Уровень океана
snowLevel = 180  # Уровень снега

class Map:
    """Создание карты мира"""
    def __init__(self):
        octaves = 30
        freq = 16.0 * octaves
        self.m = np.zeros((mapSizeX,mapSizeY), dtype=int)
        for y in range(mapSizeY):
        	for x in range(mapSizeX):
        		self.m[x,y] = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)

    def showMap(self):
        filename = "111.ppm"
        f = open(filename, 'wb')
        f. write(bytearray('P6\n'+str(mapSizeX)+' '+str(mapSizeY)+'\n255\n','utf-8'))
        for y in range(mapSizeY):
            for x in range(mapSizeX):
                v = self.m[x,y]
                if v <= seaLevel:
                    if v <= seaLevel-20:
                        f.write(bytearray([0, 0, 70]))
                    else:
                        f.write(bytearray([0, 0, 140]))
                elif v >= snowLevel:
                    if v >= snowLevel+20:
                        f.write(bytearray([240, 240, 240]))
                    else:
                        f.write(bytearray([200, 200, 200]))
                else:
                    f.write(bytearray([v, 0, 0]))
        f.close()


# Состояния оленя и цели его действой

class Animal:
    def __init__(self, myMap):
        """Constructor"""
        self.map = myMap

        self.hungry = 100  #   100 - не голодный  0 - готов съесть волка
        self.active = 15    # 100 - бешено мчится ничего не замечая вокруг, 0 - глубоко спит, 10 - потягушки
        self.thirst = 100 # 100 - пить не хочет. 0 - мумия оленя (засушенная)
        self.age = 0 # 100 - пора копать могилу. 0 - только что родился
        self.health = 100 # 100 - совершенно здоров. 80 - небольшой насморк  0 - лучше не надо
        self.power = 100 # 100 - полон сил.   0 - очень устал. Влияет на скорость движения и на необходимость поспать.
        self.goal = 100 # 100 - совершенно здоров. 80 - небольшой насморк  0 - лучше не надо
        self.awake = 0 #  сколько секунд бодрствует и отрицательное число, сколько секунд спит.

        # что сохраняем от хода к ходу

        self.direction = 0 # 0 - смотрит направо  90 - смотрит на север
        self.speed = 1 # скорость оленя

    def step(self):
        """
        Выполняет все действия в соответствии с текущей ситуацией.
        """
        return True # Возвращает если еще жив

    def bite(self, strength):
        """
        Его кто-то укусил. Передаем силу укуса. Сила укуса 100 - его сожрали нафиг.
                                                            1 - укусил комар,
                                                            10 - пчелы или слепни кусаются.
                                                            20 и больше - укус хищника
        """
        return True # Возвращает если еще жив

class Deer(Animal):
   def __init__(self, myMap):
        Animal.__init__(self, myMap)
        self.x = 500 # координаты оленя
        self.y = 500 #


class Wolf(Animal):
   def __init__(self, myMap):
        Animal.__init__(self, myMap)
        self.x = 300 # координаты волка
        self.y = 300 #

##########################################################

m = Map()
m.showMap()
print("Done")
