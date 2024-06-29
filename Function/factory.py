from .singleton import EconomyCar, LuxuryCar

class CarFactory:
    @staticmethod
    def create_car(car_type, model):
        if car_type == "economy":
            return EconomyCar(model)
        elif car_type == "luxury":
            return LuxuryCar(model)
        else:
            raise ValueError("Unknown car type")