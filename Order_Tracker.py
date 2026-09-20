#Created by Ashleigh Molinet
#Title: Order_Tracker
#Created on 2026-09-12
#Last Modified: 2026-09-19
# All ideas are my own, however, AI was used in the course of this project to help debug. AI model used is the Co-Pilot Github agent.
    #any AI code incorporated has be throughougly reviewed for accuracy and relevance to this Order Tracking Application.
#Sources: 
    # Coding Assistance Previous Project: https://github.com/amolinet/SDEV140_FinalProject/blob/main/MolinetAshleighFinalProject.py A previous project using tkinter. Helped with setting up window classes
    # Coding Assistance Website: https://www.youtube.com/watch?v=8m4uDS_nyCk used to help with treeview
    # Coding Assistance Website: https://www.youtube.com/watch?v=fvIThtPt6Nc helped with creating data entry form
    # 

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
from tkinter import ttk
import pandas as pd
import os
import openpyxl as opy
from datetime import datetime

#creates a window called "new orders"
class OrderWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.title("New Orders Window")
        self.geometry("500x450")
        self.configure(bg='gold')

        tk.Label(self, text='Enter new order information here.', bg='gold').pack(pady=20)

        # enumerating the list and setting the labels/inputs as a for loop makes it so i can add more fields easily
        form = tk.Frame(self, bg='gold')
        form.pack(pady=10)
        self.entries = {}
        fields = ('Order ID', 'User', 'Order Date', 'Order Status', 'Cost', 'Lab Group')
        for row, field in enumerate(fields):
            tk.Label(form, text=f'{field}:', bg='gold').grid(
                row=row, column=0, padx=10, pady=8, sticky='e')
            entry = tk.Entry(form, width=30)
            entry.grid(row=row, column=1, padx=10, pady=8)
            self.entries[field] = entry

        self.message = tk.Label(self, text='', bg='gold')
        self.message.pack(pady=5)
        controls = tk.Frame(self, bg='gold')
        controls.pack(pady=10)
        #buttons for saving order, returning to root screen and killing the app.
        tk.Button(controls, text='Save Order', command=self.save_order).pack(
            side='left', padx=5)
        tk.Button(controls, text='Home', command=self.destroy).pack(
            side='left', padx=5)
        tk.Button(controls, text='Exit', command=self.master.destroy).pack(
            side='left', padx=5)
    #takes order data and uses pandas to add to an excel workbook
    def save_order(self):
        """Append the entered order to the Excel workbook."""
        order = {field: entry.get().strip() for field, entry in self.entries.items()}
        if not all(order.values()):
            self.message.config(text='Please complete every field.', fg='red')
            return

        filename = 'Order_Tracker_Data.xlsx'
        try:
            if os.path.exists(filename):
                existing = pd.read_excel(filename)
                columns = list(existing.columns)
                for field in order:
                    if field not in columns:
                        columns.append(field)
                new_order = pd.DataFrame([order]).reindex(columns=columns)
                data = pd.concat([existing, new_order], ignore_index=True)
            else:
                data = pd.DataFrame([order])
            data.to_excel(filename, index=False)
        except (OSError, ValueError, ImportError) as error:
            self.message.config(text=f'Unable to save order: {error}', fg='red')
            return

        self.message.config(text='Order saved successfully.', fg='green')
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        


#creates a tree view and displays last 10 orders
class ExcelWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.title("Recent Orders Window")
        self.geometry("1200x600")
        self.configure(bg='maroon')
        self.transient(master) #prevents main window from hiding the excel window

        tk.Label(self, text='10 Most Recent Orders.', bg='maroon', fg='white').pack(pady=20)

        self.tree = ttk.Treeview(self, show='headings')
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        controls = tk.Frame(self, bg='maroon')
        controls.pack(pady=10)
        tk.Button(controls, text='Refresh', command=self.load_orders).pack(side='left', padx=5)
        tk.Button(controls, text='Home', command=self.destroy).pack(side='left', padx=5)
        tk.Button(controls, text='Exit', command=self.master.destroy).pack(side='left', padx=5)

        self.load_orders()

    def load_orders(self):
        """Load and display the ten newest rows from the order workbook."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        filename = 'Order_Tracker_Data.xlsx'
        if not os.path.exists(filename):
            self.tree['columns'] = ('Message',)
            self.tree.heading('Message', text='Message')
            self.tree.insert('', 'end', values=('No order data found.',))
            return

        try:
            df = pd.read_excel(filename).tail(10)
        except (OSError, ValueError, ImportError) as error:
            self.tree['columns'] = ('Message',)
            self.tree.heading('Message', text='Message')
            self.tree.insert('', 'end', values=(f'Unable to read orders: {error}',))
            return

        columns = [str(column) for column in df.columns]
        self.tree['columns'] = columns
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=140, anchor='w')
        for row in df.itertuples(index=False, name=None):
            self.tree.insert('', 'end', values=[str(value) for value in row])


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
