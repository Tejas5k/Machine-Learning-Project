import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


model = joblib.load('taxi_fare_model.pkl')  #model

#----------------------------------------------------------------
root = tk.Tk()
root.title("Taxi Fare Prediction")
root.geometry("750x950")  

# Title 
title_label = tk.Label(root, text="Taxi Fare Prediction", font=("Arial", 16, "bold"), bg="light gray")
title_label.pack(side="top", pady=10)

# frame
container = tk.Frame(root, bg="light gray")
container.pack(expand=True, fill='both') 


frame = tk.Frame(container, bg="light yellow", padx=20, pady=20, relief="solid", bd=2)
frame.pack(expand=True, fill='both', padx=50, pady=50) 

# Labels and input fields
label_distance = tk.Label(frame, text="Enter Travel Distance (km):", font=("Arial", 15, "bold"), bg="light yellow")
label_distance.grid(row=0, column=0, pady=10)

entry_distance = tk.Entry(frame, width=50)
entry_distance.grid(row=1, column=0, pady=5)

label_pickup_time = tk.Label(frame, text="Enter Pickup Time (YYYY-MM-DD HH:MM:SS):", font=("Arial", 15, "bold"), bg="light yellow")
label_pickup_time.grid(row=2, column=0, pady=10)

entry_pickup_time = tk.Entry(frame, width=50)
entry_pickup_time.grid(row=3, column=0, pady=5)

# Label 
label_predicted_fare = tk.Label(frame, text="", font=("Arial", 15, "bold"), bg="light yellow", fg="green")
label_predicted_fare.grid(row=5, column=0, pady=10)
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(6, 4))

def predict_fare():  # Function 

    try:
        # inputs 
        distance = float(entry_distance.get())
        pickup_time_str = entry_pickup_time.get()

        # datetime obj
        pickup_time = datetime.strptime(pickup_time_str, '%Y-%m-%d %H:%M:%S')
        hour = pickup_time.hour
        day_of_week = pickup_time.weekday()

        # data frame
        input_data = pd.DataFrame([[distance, hour, day_of_week]], columns=['distance', 'hour', 'day_of_week'])
        
        # Prediction 
        predicted_fare = model.predict(input_data)[0]

        # Update  label 
        label_predicted_fare.config(text=f"The estimated fare is: {predicted_fare:.2f} INR")
        
        # Plot 
        plot_fare(distance, predicted_fare)
        
    except ValueError:
        label_predicted_fare.config(text="Please enter valid inputs.")
    except Exception as e:
        label_predicted_fare.config(text=str(e))

# plot 
def plot_fare(distance, predicted_fare):
    
    data = pd.read_csv('taxi_fares.csv')
    data['hour'] = pd.to_datetime(data['pickup_time']).dt.hour
    data['day_of_week'] = pd.to_datetime(data['pickup_time']).dt.dayofweek
    X = data[['distance', 'hour', 'day_of_week']]
    
    
    ax.clear()
    
    ax.scatter(data['distance'], data['fare'], color='blue', label='Actual Fares', alpha=0.7)

    
    predicted_fares = model.predict(X)
    ax.scatter(data['distance'], predicted_fares, color='red', label='Predicted Fares', alpha=0.7)

    
    ax.scatter(distance, predicted_fare, color='green', s=100, edgecolor='black', label='User Input', zorder=5)

    
    ax.set_title('Distance vs Fare')
    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Fare (INR)')
    ax.legend()
    ax.grid(True)
    
    
    canvas.draw()

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=6, column=0, pady=10)

# Predict Button
predict_button = tk.Button(frame, text="Predict Fare", bg="lime", fg="black", font=("Arial", 13, "bold"), padx=10, pady=5, command=predict_fare)
predict_button.grid(row=4, column=0, pady=20)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
container.columnconfigure(0, weight=1)
container.rowconfigure(0, weight=1)

root.mainloop()
