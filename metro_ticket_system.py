import pandas as pd
import numpy as np
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import NearestNeighbors
import tkinter as tk
from tkinter import messagebox, ttk

np.random.seed(42)
random.seed(42)

def get_price_by_stations(station_count):
    if station_count <= 9:
        return 8
    elif station_count <= 16:
        return 10
    elif station_count <= 22:
        return 15
    else:
        return 20

# البيانات المدخلة يدويًا
lines_data = {
    "Line 1": (
        pd.DataFrame({"station": ["Helwan", "Ain Helwan", "Helwan University", "Wadi Hof", "Hadayek Helwan", "El-Maasara", "Tora El-Asmant", "Kozzika", "Tora El-Balad", "Sakanat El-Maad"],
            "next station": ["Ain Helwan", "Helwan University", "Wadi Hof", "Hadayek Helwan", "El-Maasara", "Tora El-Asmant", "Kozzika", "Tora El-Balad", "Sakanat El-Maad", "Maadi"],
            "time": [1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4]
        }),
        ["Helwan", "Ain Helwan", "Helwan University", "Wadi Hof", "Hadayek Helwan", "El-Maasara", "Tora El-Asmant", "Kozzika", "Tora El-Balad", "Sakanat El-Maad"]
    ),
            
    "Line 2": (
        pd.DataFrame({"station": ["El-Mounib", "Sakiat Mekky", "Omm El-Masryeen", "El Giza", "Faisal", "Cairo University", "El Bohoth", "Dokki", "Opera", "Sadat"],
            "next station": ["Sakiat Mekky", "Omm El-Masryeen", "El Giza", "Faisal", "Cairo University", "El Bohoth", "Dokki", "Opera", "Sadat", "Mohamed Naguib"],
            "time": [1.6, 1.3, 2.5, 1.4, 1.5, 1.5, 1.5, 1.5, 1.2, 1.5]
        }),
        ["El-Mounib", "Sakiat Mekky", "Omm El-Masryeen", "El Giza", "Faisal", "Cairo University", "El Bohoth", "Dokki", "Opera", "Sadat", "Mohamed Naguib"]
    ),
            
    "Line 3": (
        pd.DataFrame({"station": ["Mansour", "El Haykestep", "Omar Ibn El-Khattab", "Qobaa", "Hesham Barakat", "El-Nozha", "Nadi El-Shams", "Alf Maskan", "Heliopolis Square", "Haroun"],
            "next station": ["El Haykestep", "Omar Ibn El-Khattab", "Qobaa", "Hesham Barakat", "El-Nozha", "Nadi El-Shams", "Alf Maskan", "Heliopolis Square", "Haroun", "Al-Ahram"],
            "time": [1.3, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4]
        }),
        ["Mansour", "El Haykestep", "Omar Ibn El-Khattab", "Qobaa", "Hesham Barakat", "El-Nozha", "Nadi El-Shams", "Alf Maskan", "Heliopolis Square", "Haroun"]
    ),
            
}

def calculate_distance_and_price(df, start, end):
    path = [df['station'].iloc[0]] + df['next station'].tolist()
    times = [0] + df['time'].tolist()
    times = pd.Series(times).cumsum().tolist()
    station_times = dict(zip(path, times))

    if start not in station_times or end not in station_times:
        return None, None

    time_diff = abs(station_times[end] - station_times[start])
    price = get_price_by_stations(time_diff)
    return time_diff, price

def show_selection_screen():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="white", bd=5, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

    title = tk.Label(frame, text="Select Line and Stations", font=("Helvetica", 20, "bold"), bg="white", fg="red")
    title.pack(pady=30)

    line_var = tk.StringVar()
    start_var = tk.StringVar()
    end_var = tk.StringVar()

    line_menu = ttk.Combobox(frame, textvariable=line_var, values=list(lines_data.keys()), font=("Helvetica", 14), state="readonly", width=40)
    line_menu.pack(pady=10)

    start_menu = ttk.Combobox(frame, textvariable=start_var, font=("Helvetica", 14), state="readonly", width=40)
    start_menu.pack(pady=10)

    end_menu = ttk.Combobox(frame, textvariable=end_var, font=("Helvetica", 14), state="readonly", width=40)
    end_menu.pack(pady=10)

    def update_stations(event):
        line = line_var.get()
        if line in lines_data:
            stations = lines_data[line][1]
            start_menu['values'] = stations
            end_menu['values'] = stations

    line_menu.bind("<<ComboboxSelected>>", update_stations)

    def submit():
        line = line_var.get()
        start = start_var.get()
        end = end_var.get()
        if line and start and end and start != end:
            df = lines_data[line][0]
            distance, price = calculate_distance_and_price(df, start, end)
            if distance is not None:
                messagebox.showinfo("Ticket Info", f"Line: {line}\nFrom: {start}\nTo: {end}\nDistance: {distance} minutes\nPrice: {price} EGP")
            else:
                messagebox.showerror("Error", "Stations not found.")
        else:
            messagebox.showwarning("Warning", "Please select a line and two different stations.")

    submit_btn = tk.Button(frame, text="Calculate Ticket", font=("Helvetica", 16, "bold"), bg="#007BFF", fg="black", width=22, height=2, command=submit)
    submit_btn.pack(pady=20)

def on_start_click():
    if not lines_data:
        messagebox.showerror("Data Error", "No metro lines found. Make sure data is available.")
    else:
        show_selection_screen()

root = tk.Tk()
root.title("Cairo Metro Ticketing System")
root.geometry("1000x750")
root.configure(bg="#E8E8E8")

outer_frame = tk.Frame(root, bg="white", bd=8, relief="groove")
outer_frame.place(relx=0.5, rely=0.5, anchor="center", width=750, height=400)

welcome_label = tk.Label(outer_frame, text="Welcome to Cairo Metro Ticketing System", font=("Helvetica", 22, "bold"), bg="white", fg="red")
welcome_label.pack(pady=50)

start_button = tk.Button(outer_frame, text="Click here to start", font=("Helvetica", 18, "bold"), width=25, height=2, bg="#007BFF", fg="black", command=on_start_click)
start_button.pack(pady=20)

root.mainloop()