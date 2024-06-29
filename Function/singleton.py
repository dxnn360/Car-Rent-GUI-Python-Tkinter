from tkinter import messagebox
from .database import Database

class CarRentalManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CarRentalManager, cls).__new__(cls)
            cls._instance.db = Database()
            cls._instance.observers = []
        return cls._instance

    def add_car(self, car):
        self.db.add_car(car.model, type(car).__name__.replace('Car', '').lower())
        self.notify_observers(car, "added")

    def remove_car(self, car):
        self.db.remove_car(car.id)
        self.notify_observers(car, "removed")

    def rent_car(self, car):
        if car.status == "available":
            car.status = "rented"
            self.db.update_car_status(car.id, car.status)
            self.notify_observers(car, "rented")
        else:
            messagebox.showerror("Error", f"Car '{car.model}' is not available.")

    def return_car(self, car):
        if car.status == "rented":
            car.status = "available"
            self.db.update_car_status(car.id, car.status)
            self.notify_observers(car, "returned")
        else:
            messagebox.showerror("Error", f"Car '{car.model}' is not currently rented.")

    def get_all_cars(self):
        cars_data = self.db.get_all_cars()
        cars = []
        for car_data in cars_data:
            if car_data[2] == "economy":
                car = EconomyCar(car_data[1])
            elif car_data[2] == "luxury":
                car = LuxuryCar(car_data[1])
            car.id = car_data[0]
            car.status = car_data[3]
            cars.append(car)
        return cars

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, car, action):
        for observer in self.observers:
            observer.update(car, action)

class Car:
    def __init__(self, model):
        self.model = model
        self.status = "available"

class EconomyCar(Car):
    def __init__(self, model):
        super().__init__(model)

class LuxuryCar(Car):
    def __init__(self, model):
        super().__init__(model)