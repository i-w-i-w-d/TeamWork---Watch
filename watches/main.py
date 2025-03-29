from watches import *
a1 = AnalogWatch(100, 0)
a2 = AnalogWatch(-100, 0)
speed(0)
def updater():
    a1.update_all()

    ontimer(updater, 1000)
updater()
mainloop()
