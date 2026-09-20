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
from tkinter import ttk
from datetime import datetime
import pandas as pd
import os
import openpyxl as opy

class OrderWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.title("New Orders Window")
        self.geometry("500x450")
        self.configure(bg='gold')

        tk.Label(self, text='Enter new order information here.', bg='gold').pack(pady=20)

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
        tk.Button(controls, text='Save Order', command=self.save_order).pack(
            side='left', padx=5)
        tk.Button(controls, text='Home', command=self.destroy).pack(
            side='left', padx=5)
        tk.Button(controls, text='Exit', command=self.master.destroy).pack(
            side='left', padx=5)

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
        

        

class ExcelWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.title("Recent Orders Window")
        self.geometry("1200x600")
        self.configure(bg='maroon')
        self.transient(master)

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


class UpdateOrderWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Update Order Window")
        self.geometry("500x500")
        self.configure(bg='orange')

        tk.Label(self, text='Enter an Order ID, load it, and update its information.',
                 bg='orange').pack(pady=20)

        lookup = tk.Frame(self, bg='orange')
        lookup.pack(pady=5)
        tk.Label(lookup, text='Order ID:', bg='orange').pack(side='left', padx=5)
        self.order_id_entry = tk.Entry(lookup, width=24)
        self.order_id_entry.pack(side='left', padx=5)
        tk.Button(lookup, text='Load Order', command=self.load_order).pack(side='left', padx=5)

        form = tk.Frame(self, bg='orange')
        form.pack(pady=10)
        self.entries = {}
        fields = ('User', 'Order Date', 'Order Status', 'Cost', 'Lab Group')
        for row, field in enumerate(fields):
            tk.Label(form, text=f'{field}:', bg='orange').grid(
                row=row, column=0, padx=10, pady=8, sticky='e')
            entry = tk.Entry(form, width=30)
            entry.grid(row=row, column=1, padx=10, pady=8)
            self.entries[field] = entry

        self.message = tk.Label(self, text='', bg='orange')
        self.message.pack(pady=5)
        controls = tk.Frame(self, bg='orange')
        controls.pack(pady=10)
        tk.Button(controls, text='Update Order', command=self.update_order).pack(
            side='left', padx=5)
        tk.Button(controls, text='Home', command=self.destroy).pack(
            side='left', padx=5)
        tk.Button(controls, text='Exit', command=self.master.destroy).pack(
            side='left', padx=5)

    def load_order(self):
        order_id = self.order_id_entry.get().strip()
        filename = 'Order_Tracker_Data.xlsx'
        if not order_id:
            self.message.config(text='Enter an Order ID first.', fg='red')
            return
        if not os.path.exists(filename):
            self.message.config(text='No order data found.', fg='red')
            return

        try:
            data = pd.read_excel(filename, dtype=str).fillna('')
        except (OSError, ValueError, ImportError) as error:
            self.message.config(text=f'Unable to read orders: {error}', fg='red')
            return

        if 'Order ID' not in data.columns:
            self.message.config(text='The workbook has no Order ID column.', fg='red')
            return

        matches = data.index[data['Order ID'].astype(str).str.strip() == order_id]
        if len(matches) == 0:
            self.message.config(text='Order ID not found.', fg='red')
            return

        self.loaded_index = matches[0]
        order = data.loc[self.loaded_index]
        for field, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(order.get(field, '')))
        self.message.config(text='Order loaded. Make changes and select Update Order.', fg='green')

    def update_order(self):
        if not hasattr(self, 'loaded_index'):
            self.message.config(text='Load an order before updating it.', fg='red')
            return

        filename = 'Order_Tracker_Data.xlsx'
        try:
            data = pd.read_excel(filename, dtype=str).fillna('')
            for field, entry in self.entries.items():
                data.at[self.loaded_index, field] = entry.get().strip()
            data['Date Modified'] = data.get('Date Modified', '')
            data.at[self.loaded_index, 'Date Modified'] = datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')
            data.to_excel(filename, index=False)
        except (OSError, ValueError, ImportError) as error:
            self.message.config(text=f'Unable to update order: {error}', fg='red')
            return

        self.message.config(text='Order updated successfully.', fg='green')


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
update_order_btn = tk.Button(root_window, text='Update Order')
update_order_btn.bind("<Button>", lambda e: UpdateOrderWindow(root_window))
update_order_btn.pack(pady=10)




root_window.mainloop()
