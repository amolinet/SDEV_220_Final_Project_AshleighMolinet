#Created by Ashleigh Molinet
#Title: Order_Tracker
#Created on 2026-09-12
#Last Modified:

import tkinter as tk
root = tk.Tk() 

root.title('Order Tracker')
root.geometry('400x800')

class Orders:
    def __init__(self, Order_ID):
        self.Order_ID = Order_ID

class Labs:
    def __init__(self, lab_name):
        self.lab_name = lab_name

class Order_Details(Orders, Labs):
    def __init__(self):
        super.__init__()
        self.Order_status = input('Order_status')
        self.Estimated_Cost = float(input('Estimated_Cost'))
        self.Username = input('Username')
        self.Date_Submitted = input('Date_Submitted')

stop_button = tk.Button(root, text="Stop", width=25, command=root.destroy) #creates button that kills window
stop_button.pack() #places button in the window

root.mainloop() #runs window/
