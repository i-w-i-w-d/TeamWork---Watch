import time #
from turtle import *


class Watch:
    time_dict = {}  # Спільний час для усіх годинників
    watches = []  # Список усіх синхронізованих годинників

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.__class__.watches.append(self)  # Додаємо в перелік синхронізованих годинників
        self.get_time()

    @staticmethod
    def get_time():  # Отримуємо реальний ас в вигляді словника
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


class AnalogDial:
    def __init__(self, parent_watch):
        self.x = parent_watch.x
        self.y = parent_watch.y

    def draw_dial(self):
        up()
        left(90)
        for n in range(12, 0, -1):
            goto(self.x - 6, self.y + 90)
            forward(84)
            write(str(n), font=('Arial', 16, 'normal'))
            left(30)
        right(90)


class Hand:
    def __init__(self, parent_watch, t, lengh=100, thight=10):
        self.x_center = parent_watch.x
        self.y_center = parent_watch.y
        self.t = t
        self.lengh = lengh
        self.thight = thight

    def hand_draw(self):


        up()
        goto(self.x_center, self.y_center + 100)

        left(90)
        right(Watch.time_dict[self.t] * 6)

        forward(int(self.lengh * 0.8))
        left(90)
        fillcolor("black")
        begin_fill()
        down()

        forward(int(self.thight / 2))
        left(90)
        for i in range(2):
            forward(self.lengh)
            left(90)
            forward(self.thight)
            left(90)

        end_fill()
        up()
        goto(self.x_center, self.y_center)
        right(heading())


class AnalogWatch(Watch):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.dial = AnalogDial(self)
        self.sec_hand = Hand(self, 'sec', lengh=110, thight=2)
        self.min_hand = Hand(self, 'min', lengh=90, thight=4)
        self.hour_hand = Hand(self, 'hour', lengh=70, thight=6)
        self.an_update()

    def an_update(self):
        up()
        goto(self.x, self.y)
        down()
        tracer(0)
        circle(100)
        self.dial.draw_dial()
        self.sec_hand.hand_draw()
        self.min_hand.hand_draw()
        self.hour_hand.hand_draw()
        update()
        # real_time = [i for i in Watch.time_dict.values()]
        # write(real_time[-3:])
