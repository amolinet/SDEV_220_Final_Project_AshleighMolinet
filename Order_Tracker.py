#Created by Ashleigh Molinet
#Title: Order_Tracker
#Created on 2026-09-12
#Last Modified: 2026-09-19


#pseudo code
    #use at least 3 classes
    # create at least 4 buttons on main window
    # app should include 3 windows
    #should be able to create, update, and view orders
    # buttons on each page for returning to home window and exiting the app
#classes
    # OrderWindow
    # ExcelWindow

import tkinter as tk
import pandas as pd
import os
import openpyxl as opy

class OrderWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.title("New Orders Window")
        self.geometry("1200x1200")
        self.configure(bg='gold')

        tk.Label(self, text='Enter new order information here.').pack(pady=20)

        

class ExcelWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.title("Recent Orders Window")
        self.geometry("1200x1200")
        self.configure(bg='Maroon')

        tk.Label(self, text='10 Most Recent Orders.').pack(pady=20)

    # def open_excel_file():
    #     df = pd.read_excel('Order_Tracker_Data.xlsx')
    #     tree['columns'] = list(df.columns)
    #     tree['show']= 'headings'

    #     for column in df.columns:
    #         tree.heading(column, text=column)
    #         tree.column(column, width=120, anchor='w')
    #     df_rows = df.to_numpy().tolist()
    #     for rows in df_rows:
    #         clean_row = []


root_window = tk.Tk()
root_window.configure(bg = 'midnight blue')
root_window.geometry('1200x1200')
root_window.title('Home Screen')
tk.Label(root_window, text='This is the home screen').pack(pady=10)

#buttons
new_order_btn = tk.Button(root_window, text = 'New Orders')
new_order_btn.bind("<Button>", lambda e: OrderWindow(root_window))
new_order_btn.pack(pady=10)
recent_orders_btn = tk.Button(root_window, text = 'Recent Orders')
recent_orders_btn.bind("<Button>", lambda e: ExcelWindow(root_window))
recent_orders_btn.pack(pady=10)




root_window.mainloop()
