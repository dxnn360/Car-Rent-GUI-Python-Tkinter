import sqlite3

class Database:
    def __init__(self, db_name="car_rental.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, model TEXT, type TEXT, status TEXT)"
            )

    def add_car(self, model, car_type):
        with self.connection:
            self.connection.execute(
                "INSERT INTO cars (model, type, status) VALUES (?, ?, ?)", (model, car_type, "available")
            )

    def remove_car(self, car_id):
        with self.connection:
            self.connection.execute(
                "DELETE FROM cars WHERE id = ?", (car_id,)
            )

    def update_car_status(self, car_id, status):
        with self.connection:
            self.connection.execute(
                "UPDATE cars SET status = ? WHERE id = ?", (status, car_id)
            )

    def get_all_cars(self):
        with self.connection:
            return self.connection.execute(
                "SELECT * FROM cars"
            ).fetchall()
