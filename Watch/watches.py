import time
from turtle import Turtle, Screen
import math

class Watch:
    time_dict = {}
    watches = []

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.__class__.watches.append(self)
        self.get_time()

    @staticmethod
    def get_time():
        local_time = time.localtime()
        Watch.time_dict = {
            "hour": local_time.tm_hour,
            "min": local_time.tm_min,
            "sec": local_time.tm_sec
        }

    def update_all(self):
        self.get_time()
        for obj in self.watches:
            if isinstance(obj, AnalogWatch):
                obj.an_update()
            elif isinstance(obj, DigitalWatch):
                obj.d_update()

class AnalogDial:
    def __init__(self, parent_watch):
        self.turtle = Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.x = parent_watch.x
        self.y = parent_watch.y
        self.radius = 100

    def draw_dial(self):
        self.turtle.clear()
        self.turtle.up()
        self.turtle.goto(self.x, self.y - self.radius)
        self.turtle.down()
        self.turtle.circle(self.radius)

        self.turtle.up()
        number_mapping = {
            1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 12,
            7: 11, 8: 10, 9: 9, 10: 8, 11: 7, 12: 6
        }
        for number in range(1, 13):
            angle = (number - 3) * 30
            rad = math.radians(angle)
            x = self.x + (self.radius - 30) * math.cos(rad)
            y = self.y + (self.radius - 30) * math.sin(rad)
            self.turtle.goto(x, y)
            self.turtle.write(str(number_mapping[number]), align="center", font=('Arial', 14, 'normal'))

class Hand:
    def __init__(self, parent_watch, t, length=100, width=10):
        self.turtle = Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.x_center = parent_watch.x
        self.y_center = parent_watch.y
        self.t = t
        self.length = length
        self.width = width

    def hand_draw(self):
        self.turtle.clear()
        self.turtle.up()
        self.turtle.goto(self.x_center, self.y_center)

        time_value = Watch.time_dict[self.t]
        if self.t == "hour":
            angle = (time_value % 12) * 30 + Watch.time_dict["min"] * 0.5
        else:
            angle = time_value * 6

        self.turtle.setheading(90 - angle)
        self.turtle.down()
        self.turtle.width(self.width)
        self.turtle.forward(self.length)
        self.turtle.up()

class AnalogWatch(Watch):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.dial = AnalogDial(self)
        self.sec_hand = Hand(self, 'sec', length=90, width=1)
        self.min_hand = Hand(self, 'min', length=80, width=3)
        self.hour_hand = Hand(self, 'hour', length=60, width=5)
        self.visible = False

    def an_update(self):
        if not self.visible:
            return
        self.dial.draw_dial()
        self.hour_hand.hand_draw()
        self.min_hand.hand_draw()
        self.sec_hand.hand_draw()

class DigitalWatch(Watch):
    def __init__(self, x=0, y=0, format_24=True):
        super().__init__(x, y)
        self.turtle = Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.format_24 = format_24
        self.visible = False

    def d_update(self):
        if not self.visible:
            self.turtle.clear()
            return

        self.turtle.clear()
        hour = Watch.time_dict["hour"]
        if not self.format_24:
            period = "AM" if hour < 12 else "PM"
            hour = hour % 12
            if hour == 0:
                hour = 12
            time_str = f"{hour:02d}:{Watch.time_dict['min']:02d}:{Watch.time_dict['sec']:02d} {period}"
        else:
            time_str = f"{hour:02d}:{Watch.time_dict['min']:02d}:{Watch.time_dict['sec']:02d}"

        self.turtle.up()
        self.turtle.goto(self.x, self.y)
        self.turtle.write(time_str, font=('Arial', 16, 'normal'), align='center')

def display_menu():
    print("\nВиберіть годинники для відображення:")
    print("1. Аналоговий годинник")
    print("2. Цифровий годинник (24-годинний формат)")
    print("3. Цифровий годинник (12-годинний формат)")
    print("4. Всі годинники")
    print("0. Вийти")

def get_user_choice():
    while True:
        try:
            choice = int(input("Ваш вибір (0-4): "))
            if 0 <= choice <= 4:
                return choice
            print("Будь ласка, введіть число від 0 до 4")
        except ValueError:
            print("Будь ласка, введіть коректне число")

def main():
    screen = Screen()
    screen.title("Аналоговий та цифровий годинник")
    screen.setup(800, 400)
    screen.tracer(0)

    analog = AnalogWatch(0, 0)
    digital24 = DigitalWatch(200, -100)
    digital12 = DigitalWatch(-200, -100, format_24=False)

    try:
        while True:
            display_menu()
            choice = get_user_choice()

            if choice == 0:
                screen.bye()
                return

            for watch in Watch.watches:
                watch.visible = False
                if isinstance(watch, DigitalWatch):
                    watch.d_update()
                elif isinstance(watch, AnalogWatch):
                    watch.an_update()

            if choice == 1:
                analog.visible = True
            elif choice == 2:
                digital24.visible = True
            elif choice == 3:
                digital12.visible = True
            elif choice == 4:
                analog.visible = True
                digital24.visible = True
                digital12.visible = True

            while True:
                Watch().update_all()
                screen.update()

                if not screen._RUNNING:
                    break

                try:
                    if screen._check_kbd():
                        break
                except:
                    pass

                time.sleep(1)

    except Exception as e:
        print(f"Сталася помилка: {e}")
    finally:
        screen.bye()

if __name__ == "__main__":
    main()