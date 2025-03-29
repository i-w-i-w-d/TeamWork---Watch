import time  # Імпортуємо time для часу
from turtle import *  # Дістаємо з туртли всі інструменти


class Watch:
    time_dict = {}  # Спільний час для усіх годинників
    watches = []  # Список усіх синхронізованих годинників

    def __init__(self, x=0, y=0):  # При створенні нового годинника запитуємо місце розміщення
        self.x = x
        self.y = y
        self.__class__.watches.append(self)  # Додаємо в перелік синхронізованих годинників
        self.get_time()  # Вперше отримуємо реальний час

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

    def update_all(self):  # Якщо так викликати оновлення одного годинника, воно оновить усіх годинники одночасно
        self.get_time()  # Оновлюємо час
        # Використовувати для оновлення всього екрану зразу
        # clear()

        for obj in self.watches:  # Запускає метод оновлення відповідно до типу годинника
            if isinstance(obj, AnalogWatch):
                obj.an_update()


class AnalogDial:
    def __init__(self, parent_watch):  # Беремо координати годинника
        self.x = parent_watch.x
        self.y = parent_watch.y

    def draw_dial(self):  # Малюємо циферблат разом з цифрами. Клас цифри для аналогового годинника я вважаю зайвим
        circle(100)
        up()
        left(90)
        for n in range(12, 0, -1):  # Пишемо цифри
            goto(self.x - 6, self.y + 90)
            forward(84)
            write(str(n), font=('Arial', 16, 'normal'))
            left(30)
        right(90)


class Hand:
    def __init__(self, parent_watch, t, lengh=100, thight=10):  # Створюємо стрілку. Параметр t позначає
        self.x_center = parent_watch.x  # ключ часу наприклад 'sec'
        self.y_center = parent_watch.y
        self.t = t
        self.lengh = lengh
        self.thight = thight

    def hand_draw(self): #Малюємо стрілку
        up()
        goto(self.x_center, self.y_center + 100)

        left(90)
        right(Watch.time_dict[self.t] * 6) # Повертаємо стрілку відповідно до часу

        forward(int(self.lengh * 0.8)) #Далі малюється сама стрілка
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
        right(heading()) #Пипець ВАЖЛИВО!!! В будь якій незрозумілій ситуації вертає напрямок черепахи по дефолту, юзайте


class AnalogWatch(Watch):
    def __init__(self, x=0, y=0):  # Ініціюємо аналоговий годинник
        super().__init__(x, y)
        self.dial = AnalogDial(self)  # Створюємо для годинника обєкти циферблат та стрілки
        self.sec_hand = Hand(self, 'sec', lengh=110, thight=2)  # Секундна
        self.min_hand = Hand(self, 'min', lengh=90, thight=4)  # Хвилинна
        self.hour_hand = Hand(self, 'hour', lengh=70, thight=6)  # Годинна
        self.an_update()  # Запускаємо перше оновлення

    def an_update(self):  # Оновлює виключно конкретний об'єкт годинник
        up()
        goto(self.x, self.y)  # Йдемо на задані координати
        down()
        tracer(0)  # Припиняємо анімацію
        self.analog_clear()  # Стираємо наш обєкт з неактуальним часом
        self.dial.draw_dial()  # Малюємо циферблат
        self.sec_hand.hand_draw()  # Перемальовуємо стрілки з актуальним часом
        self.min_hand.hand_draw()
        self.hour_hand.hand_draw()
        update()  # Оновлюємо екран
        # real_time = [i for i in Watch.time_dict.values()]
        # write(real_time[-3:])

    @staticmethod
    def analog_clear():  # Метод оновлення аналогового годинника
        pencolor('white')
        fillcolor('white')
        begin_fill()
        circle(100)
        end_fill()
        pencolor('black')
