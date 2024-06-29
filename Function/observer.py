from tkinter import messagebox

class Observer:
    def update(self, car, action):
        pass

class CarStatusObserver(Observer):
    def __init__(self, gui):
        self.gui = gui

    def update(self, car, action):
        self.gui.update_car_list()
        messagebox.showinfo("Info", f"Car '{car.model}' has been {action}. Status: {car.status}")