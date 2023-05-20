from simulator import Simulator
from tkinter import *

class Car_options(Toplevel):
    def __init__(self, list, simulations, element=None, max_acceleration=10, min_acceleration=-10, max_speed=10, mass=50):
        super().__init__()
        
        self.geometry("300x220")
        self.resizable(False, False)

        #zmienne umożliwiają modyfikowanie tych elementów z poziomu klasy
        self.simulations = simulations 
        self.list = list

        #jeżeli tworzony jest nowy pojazd wartość jest równa None
        #jeżeli modyfikowane są wartości istniejącego pojazdu wtedy wartośc jest równa indeksowi tego pojazdu
        self.element = element 


        #tworzenie wigdetów
        max_speed_label = Label(self, text="Max Speed")
        self.max_speed_value = Entry(self)
        self.max_speed_value.insert(0, max_speed)

        max_acceleration_label = Label(self, text="Max Acceleration")
        self.max_acceleration_value = Entry(self)
        self.max_acceleration_value.insert(0, max_acceleration)

        min_acceleration_label = Label(self, text="Min Acceleration")
        self.min_acceleration_value = Entry(self)
        self.min_acceleration_value.insert(0, min_acceleration)

        mass_label = Label(self, text="Mass")
        self.mass_value = Entry(self)
        self.mass_value.insert(0, mass)

        button_frame = Frame(self)
        save_button = Button(button_frame, text="Save", command=self.save)
        cancel_button = Button(button_frame, text="Cancel", command=self.cancel)

        self.bind("<Return>", self.save)

        #pozycjonowanie elementów
        max_speed_label.pack()
        self.max_speed_value.pack()

        max_acceleration_label.pack()
        self.max_acceleration_value.pack()

        min_acceleration_label.pack()
        self.min_acceleration_value.pack()

        mass_label.pack()
        self.mass_value.pack()

        button_frame.pack(pady=10)
        save_button.pack(side=LEFT)
        cancel_button.pack(side=RIGHT)

    def save(self, e=None):
        #zapisuje dane wpisane przez użytkownika oraz dodaje nowy lub aktualizuje istniejący pojazd

        #zbiera wartosci wpisane przez użytkownika 
        max_speed = int(self.max_speed_value.get())
        max_acceleration = int(self.max_acceleration_value.get())
        min_acceleration = int(self.min_acceleration_value.get())
        mass = int(self.mass_value.get())

        if self.element == None:
            #tworzy nowy pojazd
            self.simulations.append(Simulator(max_speed, max_acceleration, min_acceleration, mass))
            list_size = self.list.size()
            self.list.insert(list_size, "Car" + str(list_size))
        else:
            #modyfikuje wartości istniejącego pojazdu
            self.simulations[self.element].max_speed = max_speed
            self.simulations[self.element].max_acceleration = max_acceleration
            self.simulations[self.element].min_acceleration = min_acceleration
            self.simulations[self.element].mass = mass

        self.destroy()

    def cancel(self):
        #jeżeli użytkownik nie chce zapisać zmian
        #okno jest po prostu zamykane
        self.destroy()

