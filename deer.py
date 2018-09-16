import math as math
import numpy as np
from noise import pnoise2, snoise2

mapSizeX = 1024
mapSizeY = 1024
seaLevel = 100  # Уровень океана
snowLevel = 180  # Уровень снега
dryLevel = 120  # Уровень снега
tMin = -20
tMax = 50

class Map:
    """Создание карты мира"""
    def __init__(self):
        octaves = 30
        freq = 16.0 * octaves
        self.h = np.zeros((mapSizeX,mapSizeY), dtype=int)
        self.dr = np.zeros((mapSizeX,mapSizeY), dtype=int)
        self.t = np.zeros((mapSizeX,mapSizeY), dtype=int)
        # Создаем карту высот и влажности, температурный градиент
        for y in range(mapSizeY):
        	for x in range(mapSizeX):
        		self.h[x,y] = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)
        		self.dr[x,y] = 1 if self.h[x,y] > dryLevel else 0
        		self.t[x,y] =(tMax-tMin)*(y/mapSizeY)+tMin + (128-self.h[x,y])/127 * 10

        # Создаем карту лесов
        self.f = np.zeros((mapSizeX,mapSizeY), dtype=int)
        octaves = 6
        freq = 16.0 * octaves
        for y in range(mapSizeY):
        	for x in range(mapSizeX):
        		self.f[x,y] = 200 if int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)>140 else 0


# По параметрам влажности, температуры и высоты определяем тип ландшафта

    def blockType(self,x,y):
        h = int(middle(self.h,x,y))
        t = int(middle(self.t,x,y))
        vl = 1 if middle(self.dr,x,y) < 0.5 else 0
        f = 0 if int(middle(self.f,x,y))<100 else 1
        t1 = 1 # определяем низкая температура (0) средняя (1) или высокая (2)
        if t < 5:
            t1 = 0
        if t > 30:
            t1 = 2

        h1 = 0;
        if h<= seaLevel-20:     # глубокое море
            h1 = 0
        elif h<= seaLevel:      # вода
            h1 = 1
        elif h<= seaLevel+30:   # низко
            h1 = 2
        elif h <  snowLevel - 20:   # равнина
            h1 = 3
        elif h <  snowLevel:    # прегорья
            h1 = 4
        elif h <  snowLevel+20: # гора
            h1 = 5
        else:                   # вершина горы
            h1 = 6

        r = [
            [[[7,7,7],[7,7,7]], # нет леса # глубокое море
            [[7,7,7],[7,7,7]]], # лес # глубокое море
            [[[6,6,6],[6,6,6]], # нет леса # вода
            [[6,6,6],[6,6,6]]], # лес # вода
            [[[],[]], # нет леса # низко
            [[],[]]], # лес # низко
            [[[],[]], # нет леса # равнина
            [[],[]]], # лес  # равнина
            [[[],[]], # нет леса # прегорья
            [[],[]]], # лес   # прегорья
            [[[],[]], # нет леса # гора
            [[],[]]], # лес # гора
            [[[5,5,5],[5,5,5]], # нет леса # вершина горы
            [[5,5,5],[5,5,5]]], # лес # вершина горы
        ]


        # t1 = 0 # определяем низкая температура (-1) средняя (0) или высокая (1)
        # if t < 5:
        #     t1 = -1
        # if t > 30:
        #     t1 = 1
        #
        # if h<= seaLevel-20: # уровень глубокого моря
        #     return 7
        # if h<= seaLevel: # уровень моря
        #     return 6
        # if h >= snowLevel+20: # вершина горы
        #     return 5
        # if h >= snowLevel: # гора
        #     return 4 if f > 100 else 5
        # if h >= snowLevel - 20: # прегорья
        #     if f > 100: # прегорья с лесом
        #         if dr > 0.5: # Сухо
        #             if t1 == -1 : # [холодно]
        #                 return 24 #!!!!!!!!!!!!!!!!!!! пока тут закончили
        #             elif t1 == 0: # [нормально]
        #                 return 0
        #             else:         # [жарко]
        #                 return 0
        #
        #         else: # Влажно
        #             if t1 == -1 : # [холодно]
        #                 return 0
        #             elif t1 == 0: # [нормально]
        #                 return 0
        #             else:         # [жарко]
        #                 return 0
        #     else: # предгорья без леса
        #         if dr > 0.5: # Сухо
        #             if t1 == -1 : # [холодно]
        #                 return 0
        #             elif t1 == 0: # [нормально]
        #                 return 0
        #             else:         # [жарко]
        #                 return 0
        #
        #         else: # Влажно
        #             if t1 == -1 : # [холодно]
        #                 return 0
        #             elif t1 == 0: # [нормально]
        #                 return 0
        #             else:         # [жарко]
        #                 return 0


    def showMap(self):
        filename = "111.ppm"
        f = open(filename, 'wb')
        f. write(bytearray('P6\n'+str(mapSizeX)+' '+str(mapSizeY)+'\n255\n','utf-8'))
        for y in range(mapSizeY):
            for x in range(mapSizeX):
                v = self.h[x,y]
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
                    if self.f[x,y] < 200:
                        f.write(bytearray([245, 245, 0]))
                    else:
                        f.write(bytearray([0, 220, 0]))
        f.close()
    def showMapTemp(self):
        filename = "222.ppm"
        f = open(filename, 'wb')
        f. write(bytearray('P6\n'+str(mapSizeX)+' '+str(mapSizeY)+'\n255\n','utf-8'))
        for y in range(mapSizeY):
            for x in range(mapSizeX):
                v = self.t[x,y]
                vh = self.h[x,y]

                if vh <= seaLevel:
                    if vh <= seaLevel-20:
                        f.write(bytearray([0, 0, 70]))
                    else:
                        f.write(bytearray([0, 0, 140]))
                else:
                        if v<0:
                            c = int(v/tMin*(240-50)+50) # tMin<0
                            c = 255 if c>255 else c
                            f.write(bytearray([c, c, c]))
                        else:
                            c = int(v/tMax*(240-50)+50)
                            c = 255 if c>255 else c
                            f.write(bytearray([c, c, 0]))
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
m.showMapTemp()
print("Done")
