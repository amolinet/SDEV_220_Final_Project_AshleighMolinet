#Created by Ashleigh Molinet
#Title: Order_Tracker
#Created on 2026-09-12
#Last Modified: 2026-09-26
# All ideas are my own, however, AI was used in the course of this project to help debug. AI model used is the Co-Pilot Github agent.
# Sometimes AI was used in an earlier iteration of the code in order to brainstorm layouts but was later replaced with my own code. 
    #any AI code incorporated has be throughougly reviewed for accuracy and relevance to this Order Tracking Application.
        #AI used at lines 70-75
        #AI used in code block at 103 -123
        #AI used in ExcelWindow class
#Sources: 
    # Coding Assistance Previous Project: https://github.com/amolinet/SDEV140_FinalProject/blob/main/MolinetAshleighFinalProject.py A previous project using tkinter. Helped with setting up window classes
    # Coding Assistance Website: https://www.youtube.com/watch?v=8m4uDS_nyCk  
                                # and https://www.tutorialspoint.com/article/how-to-open-an-excel-spreadsheet-in-treeview-widget-in-tkinter 
                                # used to help with treeview
    # Coding Assistance Website: https://www.youtube.com/watch?v=fvIThtPt6Nc helped with creating data entry form

#pseudo code
    #use at least 3 classes
    # navigation buttons in root window for viewing current orders, adding new orders, updating existing orders
    # app should include 3 windows
    # should be able to create, update, and view orders
    # should be able to remove lines from treeview and corresponding excel sheet
    # buttons on each page for returning to home window and exiting the app
#classes
    # OrderWindow
    # ExcelWindow
    # OrderUpdateWindow

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import re
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

        # order window widgets and frames
        
        #form frame
        form_frame = tk.Frame(self, bg='gold')
        form_frame.pack(pady=10)
        
        #form widgets
        order_id_label = tk.Label(form_frame, text='Order ID(SR-000#)', bg='gold')
        order_id_label.pack()
        order_id_entry = tk.Entry(form_frame, width=30)
        order_id_entry.pack(pady=5)
       
        user_label = tk.Label(form_frame, text='User\'s Name', bg='gold')
        user_label.pack()
        user_entry = tk.Entry(form_frame, width=30)
        user_entry.pack(pady=5)
       
        order_date_label = tk.Label(form_frame, text='Date Order Submitted', bg='gold')
        order_date_label.pack()
        order_date_entry = tk.Entry(form_frame, width=30)
        order_date_entry.pack(pady=5)

        cost_label = tk.Label(form_frame, text='Cost($XXX,XXX)', bg='gold')
        cost_label.pack()
        cost_entry = tk.Entry(form_frame, width=30)
        cost_entry.pack(pady=5)

        lab_group_label = tk.Label(form_frame, text='Lab Group', bg='gold')
        lab_group_label.pack()
        lab_group_combobox = ttk.Combobox(form_frame, values = ['HPLC', 'LC/MS', 'ICP/MS', 'GC', 'Wet Chem', 'Micro'])
        lab_group_combobox.pack(pady=5)

        order_status = tk.Label(form_frame, text='Order Status', bg='gold')
        order_status.pack()
        order_status_combobox = ttk.Combobox(form_frame, values = ['Pending Approval', 'Approved - Ordered', 'Approved - Partially Recieved', 'Closed', 'Rejected', 'Revision Requested'])
        order_status_combobox.pack(pady=5)

        # AI Generated Code - Use dictionary to keep references to every input so save_order can read and clear them
        self.entries = {
            "Order ID": order_id_entry,
            "User Name": user_entry,
            "Date Order Submitted": order_date_entry,
            "Cost": cost_entry,
            "Lab Group": lab_group_combobox,
            "Order Status": order_status_combobox,
        }
       
        self.message = tk.Label(self, text='', bg='gold')
        self.message.pack(pady=5)

       #frame for control buttons
        controls = tk.Frame(self, bg='gold')
        controls.pack(pady=10)


        #buttons for saving order, returning to root screen and killing the app.
        save_btn = tk.Button(controls, text='Save Order', command=self.save_order)
        save_btn.pack(side ='left', padx= 5)
        home_btn = tk.Button(controls, text='Home', command=self.destroy)
        home_btn.pack(side='left', padx=5 )
        exit_btn = tk.Button(controls, text='Exit', command=self.master.destroy)
        exit_btn.pack(side='left', padx=5)

    def save_order(self):
        '''Append the order to the excel workbook'''
        order = {field: entry.get().strip() for field, entry in self.entries.items()}
        if not all(order.values()):
            self.message.config(text='Please complete every field.', fg='red')
            return
        
        #validates unique order ID, AI used to debug
        order_id = order["Order ID"].strip().upper()
        if not re.fullmatch(r"SR-\d{4}", order_id):
            self.message.config(
                text="Order ID must use the format SR-0001.",
                fg="red",
            )
            return
        
        order["Order ID"] = order_id

        # AI used to help with file/error handling. 
        filename = 'Order_Tracker_Data.xlsx'
        try:
            if os.path.exists(filename):
                existing = pd.read_excel(filename)

                #checks for duplicate IDs, AI used to debug
                existing = pd.read_excel(filename, dtype={"Order ID": str})
                
                if "Order ID" not in existing.columns:
                    self.message.config(text="Workbook is missing the Order ID column.", fg="red")
                    return
                
                existing_ids = (
                    existing["Order ID"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.upper()
                )
                
                if existing_ids.eq(order_id).any():
                    self.message.config(
                        text=f"Order ID {order_id} already exists.",
                        fg="red",
                    )
                    return

                #saves and appends fields in excel
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
        
#AI used to help with configuring Treeview in a more pleasing way, debugged my loop in def load_orders
class ExcelWindow(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Excel Treeview")
        self.geometry("1200x600")
        self.config(bg="Maroon")
        self.transient(master)

        # Container frame to hold Treeview and its scrollbars together properly
        tree_frame = tk.Frame(self, bg="Maroon")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create scrollbars inside the frame
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        vert_scrollbar.pack(side="right", fill="y")

        horz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        horz_scrollbar.pack(side="bottom", fill="x")

        # Create Treeview inside the frame
        self.tree = ttk.Treeview(
            tree_frame,
            show="headings",
            yscrollcommand=vert_scrollbar.set,
            xscrollcommand=horz_scrollbar.set,
        )
        self.tree.pack(fill="both", expand=True)

        # Configure scrollbar commands
        vert_scrollbar.config(command=self.tree.yview)
        horz_scrollbar.config(command=self.tree.xview)

        # Status Label
        self.status_label = tk.Label(self, text="", bg="maroon", fg="white")
        self.status_label.pack(pady=(0, 10))

        # Frame for control buttons
        controls = tk.Frame(self, bg="maroon")
        controls.pack(pady=10)

        # Buttons 
        delet_line_btn = tk.Button(controls, text="Remove Selected", command=self.remove_selected_line)
        delet_line_btn.pack(side="left", padx=5)
       
        new_order_scr_btn = tk.Button(
            controls,
            text="Add Another Order",
            command=lambda: OrderWindow(self.master),
        )
        new_order_scr_btn.pack(side="left", padx=5)

        home_btn = tk.Button(controls, text="Home", command=self.destroy)
        home_btn.pack(side="left", padx=5)

        exit_btn = tk.Button(
            controls, text="Exit", command=self.master.destroy
        )
        exit_btn.pack(side="left", padx=5)

        # Automatically call the load method when window opens
        self.load_orders()

    def load_orders(self):
        """Loads the ten newest rows from the order_tracker excel file"""
        filename = "Order_Tracker_Data.xlsx"

        try:
            # Reads the excel file with pandas
            df = pd.read_excel(filename)

            # Clear previous data from tree cleanly
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Configures treeview columns using Excel headers
            columns = list(df.columns)
            self.tree["columns"] = columns
            self.tree["show"] = "headings"

            # Sets column headings and width
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="w")

            # GET LAST 10 ROWS: Grab the tail end of the dataframe
            # We reverse it if you want the absolute newest at the very top
            df_last_10 = df.tail(10)

            # Insert data into Treeview
            for index, row in df_last_10.iterrows():
                self.tree.insert("", "end", iid=str(index), values=tuple(row))

            # Update status using correct instance variable reference
            self.status_label.config(text=f"Loaded last 10 entries from: {filename}")

        except ValueError:
            self.status_label.config(text="Error: Invalid file format")
        except FileNotFoundError:
            self.status_label.config(text=f"Error: {filename} not found")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def remove_selected_line(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "No selection", "Please select a line to remove.", parent=self
            )
            return

        confirm = messagebox.askyesno(
            "Confirm deletion",
            "Are you sure you want to delete the selected line(s)?",
            parent=self,
        )
        if not confirm:
            return

        excel_indices_to_drop = [int(item) for item in selected_items]

        try:
            df = pd.read_excel("Order_Tracker_Data.xlsx")
            df = df.drop(index=excel_indices_to_drop)

            df.to_excel("Order_Tracker_Data.xlsx", index=False)

            self.load_orders()
            messagebox.showinfo(
                "Order removed", "Selected line(s) successfully removed from Excel.", parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "Unable to remove order", f"Failed to update Excel file: {e}", parent=self
            )







root_window = tk.Tk()
root_window.configure(bg = 'midnight blue')
root_window.geometry('1200x1200')
root_window.title('Home Screen')
tk.Label(root_window, text='Welcome to the Order Tracking App! \nPlease click one of the buttons to get started.',
          fg='white', bg='midnight blue', font=('Arial', 22)).pack(pady=10)

#buttons
new_order_btn = tk.Button(root_window, text = 'New Orders')
new_order_btn.bind("<Button>", lambda e: OrderWindow(root_window))
new_order_btn.pack(pady=10)
recent_orders_btn = tk.Button(root_window, text = 'Recent Orders')
recent_orders_btn.bind("<Button>", lambda e: ExcelWindow(root_window))
recent_orders_btn.pack(pady=10)




root_window.mainloop()
