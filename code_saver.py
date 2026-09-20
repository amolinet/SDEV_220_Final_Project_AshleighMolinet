

class Main_Window_Cl(): 
    def __init__(self):
        self.title('QC Lab Order Tracker')
        self.create_main_frame()


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

#creates root window
hello_window = tk.Tk()
hello_window.title('QC Lab Order Tracker')
hello_window.configure(bg="midnight blue")
hello_window.geometry('1200x1200')

#creates a frame widget
hello_window_frame = tk.Frame(hello_window, bg = 'dodger blue', width=1000, height=1000)

#position frame in window and prevent frame from shrinking to fit 
hello_window_frame.pack_propagate(False)
hello_window_frame.pack(pady=10)

#add button widgets inside of the hello_window_frame 
recent_order_button = tk.Button(hello_window_frame, text = 'View Recent Orders')
recent_order_button.place(x=500, y=300)
recent_order_button.pack()
new_order_entry_button = tk.Button(hello_window_frame, text = 'Create New Order Entry')
new_order_entry_button.pack()
leave_app_button = tk.Button(hello_window_frame, text= 'Click here to leave app')
leave_app_button.pack()
update_order_entry_button = tk.Button(hello_window_frame, text='Click here to update an order')
update_order_entry_button.pack()




# class Main_Window_Cl(tk.Toplevel):
#     def __init__(self):
#         super().__init__(self)
#         self.title('QC Lab Order Tracker')
#         self.create_main_frame()
#         self.create_button_frame(self)

#     def create_main_frame(self):
#         self.frame = tk.Frame(self, bg='midnight blue')
#         self.frame.grid(row=0, column=0, sticky = "nsew")
#         self.frame.pack(fill = tk.BOTH, expand=True)

#     #button subframe
#     def create_button_frame(self, frame):
#         button_width = 20
#         self.button_frame = tk.frame(frame, bg='dodger blue')
#         self.button_frame.grid(row=0, column=1, sticky='nsew')
#         new_entry_button = tk.Button(self.button_frame, text = 'Create A New Order', width=button_width, command=self.new_order_window)





