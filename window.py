from tkinter import *
from new_car import Car_options
import threading
import plot

WINDOWS_WIDTH = 1200
WINDOWS_HEIGHT = 750


def motion(event, canvas, lines, road):
    #funkcja śledzi ruch kursora i na tej podstawie rysuje potencjalną linię na trasie
    mouse_x = event.x
    mouse_y = event.y

    canvas.coords(lines[-1], road[-1][0], road[-1][1], mouse_x, mouse_y)

def set_point(event, canvas, lines, road):
    #ustawienie nowego punktu na trasie

    mouse_x = event.x
    mouse_y = event.y

    lines.append(canvas.create_line(road[-1][0], road[-1][1], mouse_x, mouse_y))
    road.append([mouse_x, mouse_y])

def new_point(x, y, canvas, lines, road):

    x = int(x)
    y = WINDOWS_HEIGHT - int(y)

    if x == 0 and len(road) == 1:
        road[0] = [x, y]
    else:
        canvas.coords(lines[-1], road[-1][0], road[-1][1], x, y)
        lines.append(canvas.create_line(road[-1][0], road[-1][1], x, y))
        road.append([x, y])

def delete_point(event, canvas, lines, road):
    #usuwanie punktu z trasy

    mouse_x = event.x
    mouse_y = event.y

    if len(road) == 1:
        #jeżeli wszystkie linie zostały usunięte
        #funkcja zmienia położenie punktu startowego w osi Y
        road[0][1] = mouse_y
        canvas.coords(lines[-1], road[-1][0], road[-1][1], mouse_x, mouse_y)
    else:
        road.pop()
        canvas.delete(lines[-1])
        lines.pop()
        canvas.coords(lines[-1], road[-1][0], road[-1][1], mouse_x, mouse_y)

def open_car_options(e, list, simulations):
    #otwiera okno umożliwiające zmianę ustawień dla istniejącego pojazdu

    car_number = list.curselection()[0]

    Car_options(list, simulations, car_number, simulations[car_number].max_acceleration, simulations[car_number].min_acceleration, \
                simulations[car_number].max_speed, simulations[car_number].mass)

def new_car(list, simulations):
    #otwiera okno w którym można ustawić dane dla nowego pojazdu
    Car_options(list, simulations)

def delete_car(list, simulations):
    #usuwa pojazd z listy

    deleted_elements = list.curselection()
    
    for element in deleted_elements:
        simulations.pop(element)
        list.delete(element)


def run_simulations(list, simulations, road):
    
    threads = []    #lista uruchomionych wątków
    for simulation in simulations:
        #dla każdej symulacji tworzony jest nowy wątek w którym jest ona przeprowadzana
        threads.append(threading.Thread(target=simulation.simulate, args=(road,)))
        threads[-1].start()
    
    for thread in threads:
        #oczekuje na zakończenie wszystkich wątków
        thread.join()

    #przekazuje dane do funkcji zajmującej się rysowaniem wykresów
    plot.plot(simulations, list)

def main():
    window = Tk()
    lines = []                             #linie przedstawiające trase
    simulations = []                       #lista pojazdów na których wykonywana będzie symulacja
    road = [[0, WINDOWS_HEIGHT]]           #trasa którą będą musiały pokonać pojazdy podczas symulacji


    window.geometry(str(WINDOWS_WIDTH) + "x" + str(WINDOWS_HEIGHT))
    window.resizable(False, False)

    #tworzenie widgetów
    car_options_frame = Frame(window)
    list = Listbox(car_options_frame, width=20)
    add_car = Button(car_options_frame, text="Add", font="Arial, 10", width=5, command=lambda: new_car(list, simulations))
    del_car = Button(car_options_frame, text="Delete", font="Arial, 10", command=lambda: delete_car(list, simulations))

    canvas = Canvas(window, width=str(WINDOWS_HEIGHT + 200), height=str(WINDOWS_HEIGHT), bd=-2, bg="#999966")
    button = Button(window, text="Start", font="Arial, 20", command=lambda: run_simulations(list, simulations, road))

    new_point_frame = Frame(window)
    new_point_label = Label(new_point_frame, text="New Point")
    x_label = Label(new_point_frame, text="X")
    x_value = Entry(new_point_frame, width=10)
    y_label = Label(new_point_frame, text="Y")
    y_value = Entry(new_point_frame, width=10)
    new_point_button = Button(new_point_frame, text="Add", font="Arial, 10", command=lambda: new_point(x_value.get(), y_value.get(), \
                                                                                                       canvas, lines, road))
    x_value.insert(0, "0")
    y_value.insert(0, "0")


    #pozycjonowanie elementów
    canvas.grid(row=0, column=0, rowspan=3)
    car_options_frame.grid(row=0, column=1, padx=50)

    list.grid(row=0, column=0, columnspan=2)
    add_car.grid(row=1, column=0, pady=3)
    del_car.grid(row=1, column=1, pady=3)
    
    new_point_frame.grid(row=1, column=1)
    new_point_label.grid(row=0, column=0, columnspan=4)
    x_label.grid(row=1, column=0)
    x_value.grid(row=1, column=1)
    y_label.grid(row=1, column=2)
    y_value.grid(row=1, column=3)
    new_point_button.grid(row=2, column=0, columnspan=4, pady=5)

    button.grid(row=2, column=1)

    #tworzenie pierwszej linii trasy
    lines.append(canvas.create_line(road[0][0], road[0][1], 1, WINDOWS_HEIGHT - 1))

    #śledzenie wydarzeń
    canvas.bind("<Motion>", lambda e: motion(e, canvas, lines, road))
    canvas.bind("<Button-1>", lambda e: set_point(e, canvas, lines, road))
    canvas.bind("<Button-3>", lambda e: delete_point(e, canvas, lines, road))
    list.bind("<Double-1>", lambda e: open_car_options(e, list, simulations))

    window.mainloop()



if __name__ == "__main__":
    main()