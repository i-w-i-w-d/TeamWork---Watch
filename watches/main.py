from watches import *


def updater(): #Оновлює всі годинники
    a1.update_all()
    ontimer(updater, 1000)


a1 = AnalogWatch(100, 0)
a2 = AnalogWatch(-150, 0)

updater()
mainloop()
