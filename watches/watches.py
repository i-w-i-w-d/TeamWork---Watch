import time
from turtle import *


class Watch:
    time_dict = {} #Спільний час для усіх годинників
    watches = [] #Список усіх синхронізованих годинників

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.__class__.watches.append(self) #Додаємо в перелік синхронізованих годинників
        self.get_time()


    @staticmethod
    def get_time(): #Отримуємо реальний ас в вигляді словника
        local_time = time.gmtime(time.time() + 2 * 3600)
        Watch.time_dict = {
            "year": local_time.tm_year,
            "mon": local_time.tm_mon,
            "day": local_time.tm_mday,
            "hour": local_time.tm_hour,
            "min": local_time.tm_min,
            "sec": local_time.tm_sec
        }

    def update_all(self):
        self.get_time()
        clear()

        for obj in self.watches:
            if isinstance(obj, AnalogWatch):
                obj.an_update()





class AnalogWatch(Watch):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.an_update()

    def an_update(self):

        up()
        goto(self.x, self.y)
        down()
        tracer(10, 0)
        circle(100)
        update()
        real_time = [i for i in Watch.time_dict.values()]
        write(real_time[-3:])






