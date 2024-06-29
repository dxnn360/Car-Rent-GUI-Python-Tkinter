import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Untuk menggunakan gambar

from Function.singleton import CarRentalManager
from Function.factory import CarFactory
from Function.observer import CarStatusObserver

class CarRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental Management")
        self.root.geometry("1200x600")  # Mengatur ukuran aplikasi menjadi 1200x600
        self.root.configure(bg="#2A52BE")

        # Membuat style untuk mengatur latar belakang
        self.style = ttk.Style()
        self.style.configure('Left.TFrame', background='#2A52BE')

        # Membuat frame utama sebagai container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Mengatur rasio lebar kolom 70:30
        main_frame.grid_columnconfigure(0, weight=7)  # Sebelah kiri (list cars)
        main_frame.grid_columnconfigure(1, weight=3)  # Sebelah kanan (add cars)

        self.manager = CarRentalManager()
        self.observer = CarStatusObserver(self)
        self.manager.add_observer(self.observer)

        self.create_widgets()
        self.update_car_list()

        # Menambahkan teks "Dan Car Rent" di bagian bawah kanan (rata kanan dan bold)
        dan_car_rent_label = ttk.Label(self.root, text="Dan Car Rent", font=("Helvetica", 12, "bold"))
        dan_car_rent_label.pack(side=tk.BOTTOM, padx=10, pady=10, anchor=tk.SE)  # Anchor SE untuk posisi rata kanan

    def create_widgets(self):
        # Frame untuk list mobil (sebelah kiri)
        list_frame = ttk.Frame(self.root, style='Left.TFrame', padding="10")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(list_frame, text="Rented Cars List", font=("Helvetica", 16, "bold"), background="#2A52BE", foreground="white").pack(pady=10)
        self.car_listbox = tk.Listbox(list_frame, font=("Helvetica", 12), height=20, width=50)
        self.car_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.car_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.car_listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(list_frame, text="Rent Car", command=self.rent_car).pack(padx=10, pady=5, fill=tk.X)
        ttk.Button(list_frame, text="Return Car", command=self.return_car).pack(padx=10, pady=5, fill=tk.X)
        ttk.Button(list_frame, text="Remove Car", command=self.remove_car).pack(padx=10, pady=5, fill=tk.X)

        # Frame untuk menambah mobil (sebelah kanan)
        add_frame = ttk.Frame(self.root, padding="10")
        add_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(add_frame, text="Add Cars", font=("Helvetica", 16, "bold")).pack(pady=10)

        car_type_frame = ttk.Frame(add_frame)
        car_type_frame.pack(pady=10)
        self.car_type_var = tk.StringVar(value="economy")
        ttk.Radiobutton(car_type_frame, text="Economy", variable=self.car_type_var, value="economy").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(car_type_frame, text="Luxury", variable=self.car_type_var, value="luxury").pack(side=tk.LEFT, padx=5)

        ttk.Label(add_frame, text="Car Model", font=("Helvetica", 12)).pack(pady=5)
        self.model_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.model_var, font=("Helvetica", 12)).pack(padx=10, pady=5, fill=tk.X)

        ttk.Button(add_frame, text="Add Car", command=self.add_car).pack(padx=10, pady=10, fill=tk.X)

    def add_car(self):
        car_type = self.car_type_var.get()
        model = self.model_var.get()
        if model:
            car = CarFactory.create_car(car_type, model)
            self.manager.add_car(car)
            self.update_car_list()
        else:
            messagebox.showerror("Error", "Please enter a car model.")

    def rent_car(self):
        selected_index = self.car_listbox.curselection()
        if selected_index:
            car = self.manager.get_all_cars()[selected_index[0]]
            self.manager.rent_car(car)
            self.update_car_list()
        else:
            messagebox.showerror("Error", "Please select a car to rent.")

    def return_car(self):
        selected_index = self.car_listbox.curselection()
        if selected_index:
            car = self.manager.get_all_cars()[selected_index[0]]
            self.manager.return_car(car)
            self.update_car_list()
        else:
            messagebox.showerror("Error", "Please select a car to return.")

    def remove_car(self):
        selected_index = self.car_listbox.curselection()
        if selected_index:
            car = self.manager.get_all_cars()[selected_index[0]]
            self.manager.remove_car(car)
            self.update_car_list()
        else:
            messagebox.showerror("Error", "Please select a car to remove.")

    def update_car_list(self):
        self.car_listbox.delete(0, tk.END)
        cars = self.manager.get_all_cars()
        for car in cars:
            self.car_listbox.insert(tk.END, f"{car.model} - {car.status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarRentalApp(root)
    root.mainloop()
