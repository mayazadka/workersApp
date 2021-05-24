from tkinter import *
from PIL import ImageTk, Image
from tkinter import font as tkfont, messagebox
import socket
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="WorkersApp",
  password="ottomate2017",
  database = "ottomate"
)
mycursor = mydb.cursor()

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='quicksand', size = 45, weight="bold")
        self.label_font = tkfont.Font(family='quicksand', size=15, weight="bold")
        self.color_btn = "#7BB2FB"

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.customers = []
        self.frames = {}
        for F in (LogInPage, MainMenu, AddCustomer, AddCar, Combine, Customers, Cars, ChangePasswordCar):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LogInPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class LogInPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        frame = LabelFrame(self, text="", padx=150, pady=150)
        frame.pack(padx=10, pady=10)
        frame.configure(background="white")

        logo_img = Image.open("logo.png")
        logo_photo = ImageTk.PhotoImage(logo_img)

        label_logo = Label(frame, bg="white", image=logo_photo)
        label_logo.image = logo_photo
        label_logo.grid(row=0, columnspan=4)

        title_label = Label(frame, text="Log In", bg="white", font=controller.title_font)
        #title_label.pack(side="top", fill="x", pady=10)

        title_label.grid(row=1, columnspan=4)

        Label(frame, text="", bg="white", font=controller.label_font).grid(row=2)

        Label(frame, text="User Name: ", bg="white", font=controller.label_font).grid(row=3, column=0)
        username = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        username.grid(row=3, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=4)

        Label(frame, text="Password: ", bg="white", font=controller.label_font).grid(row=5, column=0)
        self.password = Entry(frame, width=30, bg="white", fg="black", show="*", font=controller.label_font)
        self.password.grid(row=5, column=1, columnspan=2)
        self.img_show = PhotoImage(file="show.png")
        self.img_hide = PhotoImage(file="hide.png")


        self.button_hide = Button(frame, image=self.img_hide, padx=4, bg="white", font=controller.label_font,
                                  command=lambda: hide(self))
        #self.img_show = self.img_show.subsample(1, 1)
        self.button_show = Button(frame, image=self.img_show, padx=4,pady=4,bg="white",
                                 command=lambda: show(self))
        self.button_show.grid(row=5, column=4)

        def show(self):
            current_password = self.password.get()
            self.password = Entry(frame, width=30, fg="black", show="", bg="white", font=controller.label_font)
            self.password.insert(0, current_password)
            self.password.grid(row=5, column=1, columnspan=2)
            self.button_show.grid_remove()
            self.button_hide.grid(row=5, column=3, columnspan=2)

        def hide(self):
            current_password = self.password.get()
            self.password = Entry(frame, width=30, bg="white", fg="black", show="*", font=controller.label_font)
            self.password.insert(0, current_password)
            self.password.grid(row=5, column=1, columnspan=2)
            self.button_hide.grid_remove()
            self.button_show.grid(row=5, column=3, columnspan=2)

        Label(frame, text="", bg="white").grid(row=6, column=0)
        Label(frame, text="", bg="white").grid(row=7)

        wrong = Label(frame, text="wrong user name or password, try again", fg="red", bg="white", font=controller.label_font)

        button_exit = Button(frame, text="EXIT", width=10 , font=controller.label_font, bg=controller.color_btn, \
                            command=self.quit)

        def sendDetailsForCheck(self):
            if (CheckDetails(username.get(), self.password.get())):
                self.password.delete(0, END)
                username.delete(0, END)
                wrong.grid_remove()
                return True
            else:
                return False

        def enterBtn(self):
            if (sendDetailsForCheck(self)):
                controller.show_frame("MainMenu")
            else:
                wrong.grid(row=6, column=0, columnspan=3)

        button_enter = Button(frame, text="ENTER", width= 10, bg=controller.color_btn, font=controller.label_font, command=lambda : enterBtn(self))
        button_enter.grid(row=8, column=2)
        button_exit.grid(row=8, column=0)
        Label(frame, text="", bg="white").grid(row=9)
        Label(frame, text="", bg="white").grid(row=10)
        Label(frame, text="", bg="white").grid(row=11)
        Label(frame, text="", bg="white").grid(row=12)
        Label(frame, text="", bg="white").grid(row=13)

class MainMenu(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        frame = LabelFrame(self, text="", padx=200, pady=100)
        frame.configure(background="white")
        frame.pack(padx=10, pady=10)

        title_label = Label(frame, text="Hello Worker!", bg="white", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        title_label.grid(row=0, columnspan=4)
        Label(frame, text="", bg="white").grid(row=1)

        add_customer_btn = Button(frame, text="ADD CUSTOMER", bg=controller.color_btn, font=controller.label_font, padx=25, pady=20,
                           command=lambda: controller.show_frame("AddCustomer"))
        add_customer_btn.grid(row=2, column=0, columnspan=2)
        Label(frame, text="  ", bg="white").grid(row=2, column=2)
        add_car_btn = Button(frame, text="ADD CAR", bg=controller.color_btn, font=controller.label_font,padx=25, pady=20,
                                  command=lambda: controller.show_frame("AddCar"))
        add_car_btn.grid(row=2,column=3, columnspan=2)

        combine_btn = Button(frame, text="COMBINE", bg=controller.color_btn, font=controller.label_font, padx=25, pady=20,
                                  command=lambda: controller.show_frame("Combine"))
        Label(frame, text=" ", bg="white").grid(row=2, column=5)
        combine_btn.grid(row=2, column=6, columnspan=2)
        Label(frame, text="  ", bg="white").grid(row=4, column=0)

        customers_btn = Button(frame, text="CUSTOMERS", bg=controller.color_btn, font=controller.label_font, padx=30, pady=20,
                             command=lambda: controller.show_frame("Customers"))
        Label(frame, text="", bg="white").grid(row=6)
        customers_btn.grid(row=5, column=0, columnspan=2)

        combine_btn = Button(frame, text="CARS", bg=controller.color_btn, font=controller.label_font, padx=40, pady=20,
                             command=lambda: controller.show_frame("Cars"))
        combine_btn.grid(row=5, column=3, columnspan=2)
        Label(frame, text="", bg="white").grid(row=6)

        exit_btn = Button(frame, text="EXIT",bg=controller.color_btn, font=controller.label_font, padx=10, pady=3,
                           command=lambda: controller.show_frame("LogInPage"))
        Label(frame, text="", bg="white").grid(row=7)
        exit_btn.grid(row=8, column=0)

class AddCustomer(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = LabelFrame(self, text="", padx=75, pady=75)
        frame.configure(background="white")
        frame.grid(padx=10, pady=10)

        title_label = Label(frame, text="Add Customer", bg="white", font=controller.title_font)
        title_label.grid(row=0, columnspan=4)

        #label.pack(side="top", fill="x", pady=10)
        Label(frame, text="", bg="white").grid(row=1)

        Label(frame, text="Id: ", bg="white", font=controller.label_font).grid(row=2, column=0)
        customer_id = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        customer_id.grid(row=2, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=3)

        Label(frame, text="First Name: ", bg="white", font=controller.label_font).grid(row=4, column=0)
        first_name = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        first_name.grid(row=4, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=5)

        Label(frame, text="Last Name: ", bg="white", font=controller.label_font).grid(row=6, column=0)
        last_name = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        last_name.grid(row=6, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=7)

        Label(frame, text="Age: ", bg="white", font=controller.label_font).grid(row=8, column=0)
        age = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        age.grid(row=8, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=9)

        Label(frame, text="Country: ", bg="white", font=controller.label_font).grid(row=10, column=0)
        country = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        country.grid(row=10, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=11)

        Label(frame, text="        ", bg="white").grid(row=2, column=3)

        Label(frame, text="City: ", bg="white", font=controller.label_font).grid(row=2, column=4)
        city = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        city.grid(row=2, column=5, columnspan=2)

        #Label(frame, text="", bg="white").grid(row=3)
        Label(frame, text="        ", bg="white").grid(row=4, column=3)

        Label(frame, text="Street: ", bg="white", font=controller.label_font).grid(row=4, column=4)
        street = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        street.grid(row=4, column=5, columnspan=2)

        Label(frame, text="        ", bg="white").grid(row=6, column=3)

        Label(frame, text="Number: ", bg="white", font=controller.label_font).grid(row=6, column=4)
        number = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        number.grid(row=6, column=5, columnspan=2)

        Label(frame, text="        ", bg="white").grid(row=8, column=3)

        Label(frame, text="Phone Number: ", bg="white", font=controller.label_font).grid(row=8, column=4)
        phone_number = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        phone_number.grid(row=8, column=5, columnspan=2)

        Label(frame, text="        ", bg="white").grid(row=10, column=3)

        Label(frame, text="Email: ", bg="white", font=controller.label_font).grid(row=10, column=4)
        email = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        email.grid(row=10, column=5, columnspan=2)

        must_fill = Label(frame, text="Must fill in all fields", fg="red", bg="white", font=controller.label_font)
        invalid_input = Label(frame, text="invalid input", fg="red", bg="white", font=controller.label_font)
        exist_customer = Label(frame, text="customer allready exist.", fg="red", bg="white", font=controller.label_font)

        Label(frame, text="", bg="white").grid(row=22)

        def clearPage(self):
            customer_id.delete(0, END)
            first_name.delete(0, END)
            last_name.delete(0, END)
            age.delete(0, END)
            country.delete(0, END)
            city.delete(0, END)
            street.delete(0, END)
            number.delete(0, END)
            phone_number.delete(0, END)
            email.delete(0, END)
            must_fill.grid_remove()
            invalid_input.grid_remove()
            exist_customer.grid_remove()
            controller.show_frame("MainMenu")

        button = Button(frame, text="Main Menu", font=controller.label_font, bg=controller.color_btn,
                           command=lambda: clearPage(self))
        button.grid(row=23,column=0)

        def sendDataAddCustomer():
            must_fill.grid_remove()
            invalid_input.grid_remove()
            exist_customer.grid_remove()
            if(customer_id.get() == "" or first_name.get() == "" or last_name.get() == "" or age.get() == "" or country.get() == "" or city.get() == "" or street.get() == "" or number.get() == "" or email.get() == ""):
                must_fill.grid(row=21, column=0, columnspan=8)
                return 0
            elif(not (customer_id.get().isdecimal() and first_name.get().isalpha() and last_name.get().isalpha()
                      and age.get().isdecimal() and country.get().isalpha() and city.get().isalpha() and
                      street.get().isalpha() and number.get().isdecimal() and phone_number.get().isdecimal() and emailPattern(email.get()))):
                invalid_input.grid(row=21, column=0, columnspan=8)
                return 0
            query = "SELECT COUNT(customer_id) FROM customer WHERE customer_id = '" + customer_id.get() + "';"
            mycursor = mydb.cursor()
            mycursor.execute(query)
            result = mycursor.fetchall()
            if(result[0][0] != 0):
                exist_customer.grid(row=21, column=0, columnspan=8)
                return 0
            else:
                query = "INSERT INTO customer (customer_id, first_name, last_name, age, country, city, street, " \
                        "home_number, phone_number, email) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (customer_id.get(), first_name.get(), last_name.get(), age.get(), country.get(), city.get(), street.get(),
                       number.get(), phone_number.get(), email.get())
                mycursor = mydb.cursor()
                mycursor.execute(query, val)
                mydb.commit()

                result = mycursor.rowcount
                if(result == 1):
                    clearPage(self)
                    return messagebox.showinfo('Saved', 'The customer is saved')
            clearPage(self)

        button = Button(frame, text="Save", font=controller.label_font, bg=controller.color_btn,
                        command=sendDataAddCustomer)
        button.grid(row=23, column=1)

class AddCar(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = LabelFrame(self, text="", padx=75, pady=100)
        frame.configure(background="white")
        frame.pack(padx=10, pady=10)

        title_label = Label(frame, text="Add Car", bg="white", font=controller.title_font)
        title_label.grid(row=0, columnspan=4)

        #label.pack(side="top", fill="x", pady=10)
        Label(frame, text="", bg="white").grid(row=1)

        Label(frame, text="Car Id: ", bg="white", font=controller.label_font).grid(row=2, column=0)
        car_id = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        car_id.grid(row=2, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=3)

        Label(frame, text="Manufacturing Year: ", bg="white", font=controller.label_font).grid(row=4, column=0)
        man_year = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        man_year.grid(row=4, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=5)

        Label(frame, text="Model: ", bg="white", font=controller.label_font).grid(row=6, column=0)
        model = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        model.grid(row=6, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=7)

        Label(frame, text="Password: ", bg="white", font=controller.label_font).grid(row=8, column=0)
        password = Entry(frame, width=30, bg="white", fg="black", show="*", font=controller.label_font)
        password.grid(row=8, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=9)

        Label(frame, text="Password Again: ", bg="white", font=controller.label_font).grid(row=10, column=0)
        password_again = Entry(frame, width=30, bg="white", fg="black", show="*", font=controller.label_font)
        password_again.grid(row=10, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=11)
        password_not_match = Label(frame, text="passwords aren't match. try again", fg="red", bg="white", font=controller.label_font)
        must_fill = Label(frame, text="Must fill in all fields", fg="red", bg="white", font=controller.label_font)
        invalid_input = Label(frame, text="invalid input", fg="red", bg="white", font=controller.label_font)
        exist_car = Label(frame, text="car allready exist.", fg="red", bg="white", font=controller.label_font)

        Label(frame, text="", bg="white").grid(row=13)

        def clearPage(self):
            car_id.delete(0, END)
            man_year.delete(0, END)
            model.delete(0, END)
            password.delete(0, END)
            password_again.delete(0, END)
            must_fill.grid_remove()
            invalid_input.grid_remove()
            exist_car.grid_remove()
            password_not_match.grid_remove()
            controller.show_frame("MainMenu")

        back_btn = Button(frame, text="Main Menu", bg=controller.color_btn, font=controller.label_font,
                           command=lambda: clearPage(self))
        back_btn.grid(row=14,column=0)

        def sendDataAddCar():
            must_fill.grid_remove()
            invalid_input.grid_remove()
            exist_car.grid_remove()
            password_not_match.grid_remove()
            if(car_id.get() == "" or man_year.get() == "" or model.get() == "" or password.get() == "" or password_again.get() == ""):
                must_fill.grid(row=12, column=0, columnspan=5)
                return 0
            elif(not (car_id.get().isalnum() and man_year.get().isdecimal() and model.get().isalnum() and emailPattern(password.get()) and emailPattern(password_again.get()))):
                invalid_input.grid(row=12, column=0, columnspan=5)
                return 0
            elif(password.get() != password_again.get()):
                password_not_match.grid(row=12, column=0, columnspan=5)
                return 0
            else:
                query = "SELECT COUNT(car_id) FROM car WHERE car_id = '" + car_id.get() + "';"
                mycursor = mydb.cursor()
                mycursor.execute(query)
                result = mycursor.fetchall()
                if (result[0][0] != 0):
                    exist_car.grid(row=12, column=0, columnspan=5)
                    return 0
                else:
                    massage_to_server = "create_salt"
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server.connect(("127.0.0.1", 8888))

                    server.send(bytearray(massage_to_server.encode()))
                    salt = server.recv(1024)
                    salt = salt.decode("utf-8")
                    server.close()

                    massage_to_server = "hashed_password " + password.get() + " " + salt

                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server.connect(("127.0.0.1", 8888))

                    server.send(bytearray(massage_to_server.encode()))
                    hashed_password = server.recv(1024)
                    hashed_password = hashed_password.decode("utf-8")
                    server.close()

                    query = "INSERT INTO car (car_id, manufacturing_year, model, hashed_password, salt, min_pedal_degree, max_pedal_degree) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    val = (car_id.get(), man_year.get(), model.get(), hashed_password, salt, 0, 100)
                    mycursor = mydb.cursor()
                    mycursor.execute(query, val)
                    mydb.commit()

                    result = mycursor.rowcount

                    query = "INSERT INTO customer_car (car_id, customer_id) VALUES(%s, %s)"
                    val = (car_id.get(), "0")
                    mycursor = mydb.cursor()
                    mycursor.execute(query, val)
                    mydb.commit()
                    result2 = mycursor.rowcount

                    if(result == 1 and result2 == 1):
                        clearPage(self)
                        return messagebox.showinfo('Saved', 'The car is saved')

                clearPage(self)
                controller.show_frame("MainMenu")

        save_btn = Button(frame, text="Save", bg=controller.color_btn, font=controller.label_font,
                        command=sendDataAddCar)
        save_btn.grid(row=14, column=1)

class Combine(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = LabelFrame(self, text="", padx=75, pady=215)
        frame.configure(background="white")
        frame.pack(padx=10, pady=10)

        title_label = Label(frame, text="Combine", bg="white", font=controller.title_font)
        title_label.grid(row=0, columnspan=4)

        #label.pack(side="top", fill="x", pady=10)
        Label(frame, text="", bg="white").grid(row=1)

        Label(frame, text="Car Id: ", bg="white", font=controller.label_font).grid(row=2, column=0)
        car_id = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        car_id.grid(row=2, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=3)

        Label(frame, text="Customer ID: ", bg="white", font=controller.label_font).grid(row=4, column=0)
        customer_id = Entry(frame, width=30, bg="white", fg="black", font=controller.label_font)
        customer_id.grid(row=4, column=1, columnspan=2)

        must_fill = Label(frame, text="Must fill in all fields", fg="red", bg="white", font=controller.label_font)
        invalid_input = Label(frame, text="invalid input", fg="red", bg="white", font=controller.label_font)
        not_exist = Label(frame, text="car or customer isn't exist.", fg="red", bg="white", font=controller.label_font)
        customer_car_exist = Label(frame, text="customer_car allready exist.", fg="red", bg="white", font=controller.label_font)

        Label(frame, text="", bg="white").grid(row=6)

        def clearPage(self):
            car_id.delete(0, END)
            customer_id.delete(0, END)
            must_fill.grid_remove()
            invalid_input.grid_remove()
            not_exist.grid_remove()
            customer_car_exist.grid_remove()
            controller.show_frame("MainMenu")

        button = Button(frame, text="Main Menu", bg=controller.color_btn, font=controller.label_font,
                           command=lambda: clearPage(self))
        button.grid(row=7,column=0)

        def sendDataCombine():
            must_fill.grid_remove()
            invalid_input.grid_remove()
            not_exist.grid_remove()
            customer_car_exist.grid_remove()

            if(car_id.get() == "" or customer_id.get() == ""):
                must_fill.grid(row=5, column=0, columnspan=5)
                return 0
            elif(not (car_id.get().isalnum() and customer_id.get().isdecimal())):
                invalid_input.grid(row=5, column=0, columnspan=5)
                return 0
            else:
                query = "SELECT COUNT(car_id) FROM car WHERE car_id = '" + car_id.get() + "';"
                mycursor = mydb.cursor()
                mycursor.execute(query)
                result = mycursor.fetchall()
                if (result[0][0] != 1):
                    not_exist.grid(row=5, column=0, columnspan=5)
                    return 0
                query = "SELECT COUNT(customer_id) FROM customer WHERE customer_id = '" + customer_id.get() + "';"
                mycursor = mydb.cursor()
                mycursor.execute(query)
                result = mycursor.fetchall()
                if (result[0][0] != 1):
                    not_exist.grid(row=5, column=0, columnspan=5)
                    return 0
                query = "SELECT COUNT(customer_car_id) FROM customer_car WHERE car_id = '" + car_id.get() + "' AND customer_id = '" + customer_id.get() + "';"
                mycursor = mydb.cursor()
                mycursor.execute(query)
                result = mycursor.fetchall()
                if (result[0][0] != 0):
                    customer_car_exist.grid(row=5, column=0, columnspan=5)
                    return 0
                else:
                    query = "INSERT INTO customer_car (car_id, customer_id) VALUES(%s, %s)"
                    val = (car_id.get(), customer_id.get())
                    mycursor = mydb.cursor()
                    mycursor.execute(query, val)
                    mydb.commit()

                    result = mycursor.rowcount
            clearPage(self)
            controller.show_frame("MainMenu")

        button = Button(frame, text="Save", bg=controller.color_btn, font=controller.label_font,
                        command=sendDataCombine)
        #lambda: controller.show_frame("MainMenu")
        button.grid(row=7, column=1)

class Customers(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.frame = LabelFrame(self, text="", padx=75, pady=75)
        self.frame.configure(background="white")
        self.frame.grid(padx=10, pady=10)

        query = "SELECT * FROM customer ORDER BY customer_id;"
        mycursor = mydb.cursor()
        mycursor.execute(query)
        self.result = mycursor.fetchall()
        self.len_result = len(self.result)

        title_label = Label(self.frame, text="Customers", bg="white", font=controller.title_font)
        title_label.grid(row=0, columnspan=4)

        # label.pack(side="top", fill="x", pady=10)
        Label(self.frame, text="", bg="white").grid(row=1)

        Label(self.frame, text="Id: ", bg="white", font=controller.label_font).grid(row=2, column=0)
        self.customer_id = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.customer_id.grid(row=2, column=1, columnspan=2)

        Label(self.frame, text="", bg="white").grid(row=3)

        Label(self.frame, text="First Name: ", bg="white", font=controller.label_font).grid(row=4, column=0)
        self.first_name = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.first_name.grid(row=4, column=1, columnspan=2)

        Label(self.frame, text="", bg="white").grid(row=5)

        Label(self.frame, text="Last Name: ", bg="white", font=controller.label_font).grid(row=6, column=0)
        self.last_name = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.last_name.grid(row=6, column=1, columnspan=2)

        Label(self.frame, text="", bg="white").grid(row=7)

        Label(self.frame, text="Age: ", bg="white", font=controller.label_font).grid(row=8, column=0)
        self.age = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.age.grid(row=8, column=1, columnspan=2)

        Label(self.frame, text="", bg="white").grid(row=9)

        Label(self.frame, text="Country: ", bg="white", font=controller.label_font).grid(row=10, column=0)
        self.country = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.country.grid(row=10, column=1, columnspan=2)

        Label(self.frame, text="        ", bg="white").grid(row=2, column=3)

        Label(self.frame, text="City: ", bg="white", font=controller.label_font).grid(row=2, column=4)
        self.city = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.city.grid(row=2, column=5, columnspan=2)

        Label(self.frame, text="        ", bg="white").grid(row=4, column=3)

        Label(self.frame, text="Street: ", bg="white", font=controller.label_font).grid(row=4, column=4)
        self.street = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.street.grid(row=4, column=5, columnspan=2)

        Label(self.frame, text="        ", bg="white").grid(row=6, column=3)

        Label(self.frame, text="Number: ", bg="white", font=controller.label_font).grid(row=6, column=4)
        self.number = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.number.grid(row=6, column=5, columnspan=2)

        Label(self.frame, text="        ", bg="white").grid(row=8, column=3)

        Label(self.frame, text="Phone Number: ", bg="white", font=controller.label_font).grid(row=8, column=4)
        self.phone_number = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.phone_number.grid(row=8, column=5, columnspan=2)

        Label(self.frame, text="        ", bg="white").grid(row=10, column=3)

        Label(self.frame, text="Email: ", bg="white", font=controller.label_font).grid(row=10, column=4)
        self.email = Entry(self.frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.email.grid(row=10, column=5, columnspan=2)

        Label(self.frame, text="", bg="white").grid(row=11, column=0)
        Label(self.frame, text="", bg="white").grid(row=12)
        self.index = 0

        def getNextCustomer(self):
            normalEntries(self)
            self.customer_id.configure(state="normal")
            self.index=self.index+1
            if(self.index > 1):
                self.prev_btn.configure(state="normal")
            if (self.index == 1):
                self.prev_btn.configure(state="disabled")
            if (self.index == self.len_result - 1):
                self.next_btn.configure(state="disabled")
            if(self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")

            updateEnrties(self)
            disabledEntries(self)

        def getPrevCustomer(self):
            normalEntries(self)
            self.customer_id.configure(state="normal")
            if(self.index > 1):
                self.index=self.index-1
            if (self.index > 1):
                self.prev_btn.configure(state="normal")
            if (self.index == 1):
                self.prev_btn.configure(state="disabled")
            if (self.index == self.len_result - 1):
                self.next_btn.configure(state="disabled")
            if (self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")
            updateEnrties(self)
            disabledEntries(self)

        self.prev_btn = Button(self.frame, text="<<", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: getPrevCustomer(self))
        self.prev_btn.grid(row=13, column=1)
        self.next_btn = Button(self.frame, text=">>", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: getNextCustomer(self))
        self.next_btn.grid(row=13, column=5)
        self.main_btn = Button(self.frame, text="Main Menu", bg=controller.color_btn, font=controller.label_font,
                        command=lambda: controller.show_frame("MainMenu"))

        def normalEntries(self):
            #self.customer_id.configure(state="normal")
            self.first_name.configure(state="normal")
            self.last_name.configure(state="normal")
            self.age.configure(state="normal")
            self.country.configure(state="normal")
            self.city.configure(state="normal")
            self.street.configure(state="normal")
            self.number.configure(state="normal")
            self.phone_number.configure(state="normal")
            self.email.configure(state="normal")

        def disabledEntries(self):
            self.customer_id.configure(state="disabled")
            self.first_name.configure(state="disabled")
            self.last_name.configure(state="disabled")
            self.age.configure(state="disabled")
            self.country.configure(state="disabled")
            self.city.configure(state="disabled")
            self.street.configure(state="disabled")
            self.number.configure(state="disabled")
            self.phone_number.configure(state="disabled")
            self.email.configure(state="disabled")

        def EditCustomer(self):
            normalEntries(self)
            self.prev_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")
            self.main_btn.configure(state="disabled")
            self.cancel_btn.configure(state="normal")
            self.save_btn.configure(state="normal")
            self.edit_btn.configure(state="disabled")


        def SaveDetailsCustomer(self):
            disabledEntries(self)
            mycursor = mydb.cursor()
            query = "UPDATE customer SET first_name = '" + self.first_name.get() + "', last_name = '" + self.last_name.get() + "', age = " + self.age.get() + ", country = '" + self.country.get() + "', city = '" + self.city.get() + "', street = '" + self.street.get() + "', home_number = " + self.number.get() + ", phone_number = '" + self.phone_number.get() + "', email = '" + self.email.get() + "' WHERE customer_id = '" + self.customer_id.get() + "';"
            mycursor.execute(query)
            mydb.commit()
            result = mycursor.rowcount
            if (self.index > 1):
                self.prev_btn.configure(state="normal")
            if (self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")
            query = "SELECT * FROM customer ORDER BY customer_id;"
            mycursor = mydb.cursor()
            mycursor.execute(query)
            self.result = mycursor.fetchall()
            self.len_result = len(self.result)
            self.cancel_btn.configure(state="disabled")
            self.save_btn.configure(state="disabled")
            self.main_btn.configure(state="normal")
            self.edit_btn.configure(state="normal")

        def updateEnrties(self):
            self.customer_id.delete(0, END)
            self.customer_id.insert(0, self.result[self.index][0])
            self.first_name.delete(0, END)
            self.first_name.insert(0, self.result[self.index][1])
            self.last_name.delete(0, END)
            self.last_name.insert(0, self.result[self.index][2])
            self.age.delete(0, END)
            self.age.insert(0, self.result[self.index][3])
            self.country.delete(0, END)
            self.country.insert(0, self.result[self.index][4])
            self.city.delete(0, END)
            self.city.insert(0, self.result[self.index][5])
            self.street.delete(0, END)
            self.street.insert(0, self.result[self.index][6])
            self.number.delete(0, END)
            self.number.insert(0, self.result[self.index][7])
            self.phone_number.delete(0, END)
            self.phone_number.insert(0, self.result[self.index][8])
            self.email.delete(0, END)
            self.email.insert(0, self.result[self.index][9])

        def CancleEditCustomer(self):
            updateEnrties(self)
            disabledEntries(self)
            if (self.index > 1):
                self.prev_btn.configure(state="normal")
            if (self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")
            self.main_btn.configure(state="normal")
            self.save_btn.configure(state="disabled")
            self.edit_btn.configure(state="normal")

        getNextCustomer(self)
        disabledEntries(self)

        self.cancel_btn = Button(self.frame, text="Cancle", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: CancleEditCustomer(self))
        self.cancel_btn.grid(row=13, column=2)
        self.cancel_btn.configure(state="disabled")
        self.edit_btn = Button(self.frame, text="Edit", bg=controller.color_btn, font=controller.label_font,
                        command=lambda: EditCustomer(self))
        self.edit_btn.grid(row=13, column=3)
        self.save_btn = Button(self.frame, text="Save", bg=controller.color_btn, font=controller.label_font,
                        command=lambda: SaveDetailsCustomer(self))
        self.save_btn.configure(state="disabled")
        self.save_btn.grid(row=13, column=4)
        Label(self.frame, text="", bg="white").grid(row=14)


        self.main_btn.grid(row=15, column=0, columnspan=7)

class Cars(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = LabelFrame(self, text="", padx=75, pady=150)
        frame.configure(background="white")
        frame.pack(padx=10, pady=10)

        query = "SELECT * FROM car ORDER BY car_id;"
        mycursor = mydb.cursor()
        mycursor.execute(query)
        self.result = mycursor.fetchall()
        self.len_result = len(self.result)

        title_label = Label(frame, text="Cars", bg="white", font=controller.title_font)
        title_label.grid(row=0, columnspan=4)

        # label.pack(side="top", fill="x", pady=10)
        Label(frame, text="", bg="white").grid(row=1)

        Label(frame, text="Car Id: ", bg="white", font=controller.label_font).grid(row=2, column=1)
        self.car_id = Entry(frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.car_id.grid(row=2, column=2, columnspan=2)

        Label(frame, text="", bg="white").grid(row=3)

        Label(frame, text="Manufacturing Year: ", bg="white", font=controller.label_font).grid(row=4, column=1)
        self.man_year = Entry(frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.man_year.grid(row=4, column=2, columnspan=2)

        Label(frame, text="", bg="white", font=controller.label_font).grid(row=5)

        Label(frame, text="Model: ", bg="white", font=controller.label_font).grid(row=6, column=1)
        self.model = Entry(frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.model.grid(row=6, column=2, columnspan=2)

        Label(frame, text="", bg="white").grid(row=7)
        Label(frame, text="", bg="white").grid(row=8)

        self.index = 0

        def getNextCar(self):
            normalEntries(self)
            self.car_id.configure(state="normal")
            self.index = self.index + 1
            if (self.index > 1):
                self.prev_btn.configure(state="normal")
            if (self.index == 1):
                self.prev_btn.configure(state="disabled")
            if (self.index == self.len_result - 1):
                self.next_btn.configure(state="disabled")
            if (self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")

            updateEnrties(self)
            disabledEntries(self)
            query = "SELECT * FROM car ORDER BY car_id;"
            mycursor = mydb.cursor()
            mycursor.execute(query)
            self.result = mycursor.fetchall()
            self.len_result = len(self.result)

        def getPrevCar(self):
            normalEntries(self)
            self.car_id.configure(state="normal")
            if (self.index > 1):
                self.index = self.index-1
            if (self.index > 1):
                self.prev_btn.configure(state="normal")
            if (self.index == 1):
                self.prev_btn.configure(state="disabled")
            if (self.index == self.len_result - 1):
                self.next_btn.configure(state="disabled")
            if (self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")

            updateEnrties(self)
            disabledEntries(self)
            query = "SELECT * FROM car;"
            mycursor = mydb.cursor()
            mycursor.execute(query)
            self.result = mycursor.fetchall()
            self.len_result = len(self.result)

        self.prev_btn = Button(frame, text="<<", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: getPrevCar(self))
        self.prev_btn.grid(row=9, column=0)
        self.next_btn = Button(frame, text=">>", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: getNextCar(self))
        self.next_btn.grid(row=9, column=4)

        Label(frame, text="", bg="white").grid(row=10)

        self.main_btn = Button(frame, text="Main Menu", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: controller.show_frame("MainMenu"))

        def normalEntries(self):
            #self.car_id.configure(state="normal")
            self.man_year.configure(state="normal")
            self.model.configure(state="normal")

        def disabledEntries(self):
            self.car_id.configure(state="disabled")
            self.man_year.configure(state="disabled")
            self.model.configure(state="disabled")

        def EditCar(self):
            normalEntries(self)
            self.prev_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")
            self.main_btn.configure(state="disabled")
            self.cancel_edit.configure(state="normal")
            self.save_btn.configure(state="normal")

        def SaveDetailsCar(self):
            disabledEntries(self)
            mycursor = mydb.cursor()
            query = "UPDATE car SET manufacturing_year = " + self.man_year.get() + ", model = '" + self.model.get() + "' WHERE car_id = '" + self.car_id.get() + "';"
            mycursor.execute(query)
            mydb.commit()
            result = mycursor.rowcount
            if (self.index > 0):
                self.prev_btn.configure(state="normal")
            if (self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")
            query = "SELECT * FROM car ORDER BY car_id;"
            mycursor = mydb.cursor()
            mycursor.execute(query)
            self.result = mycursor.fetchall()
            self.len_result = len(self.result)
            self.cancel_edit.configure(state="disabled")
            self.main_btn.configure(state="normal")
            self.save_btn.configure(state="disabled")

        def updateEnrties(self):
            self.car_id.delete(0, END)
            self.car_id.insert(0, self.result[self.index][0])
            self.man_year.delete(0, END)
            self.man_year.insert(0, self.result[self.index][1])
            self.model.delete(0, END)
            self.model.insert(0, self.result[self.index][2])

        def CancleEditCar(self):
            updateEnrties(self)
            disabledEntries(self)
            if (self.index > 0):
                self.prev_btn.configure(state="normal")
            if (self.index < self.len_result - 1):
                self.next_btn.configure(state="normal")
            self.main_btn.configure(state="normal")
            self.cancel_edit.configure(state="disabled")
            self.save_btn.configure(state="disabled")

        getNextCar(self)
        disabledEntries(self)

        self.cancel_edit = Button(frame, text="Cancel", bg=controller.color_btn, font=controller.label_font,
                                  command=lambda: CancleEditCar(self))
        self.cancel_edit.grid(row=9, column=1)
        self.cancel_edit.configure(state="disabled")
        self.edit_btn = Button(frame, text="Edit", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: EditCar(self))
        self.edit_btn.grid(row=9, column=2)
        self.save_btn = Button(frame, text="Save", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: SaveDetailsCar(self))
        self.save_btn.grid(row=9, column=3)
        self.save_btn.configure(state="disabled")
        self.main_btn.grid(row=11, column=0, columnspan=2)

        self.change_password = Button(frame, text="Change Password", bg=controller.color_btn, font=controller.label_font,
                          command=lambda: controller.show_frame("ChangePasswordCar"))
        self.change_password.grid(row=11, column=2, columnspan=2)

class ChangePasswordCar(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = LabelFrame(self, text="", padx=75, pady=150)
        frame.configure(background="white")
        frame.pack(padx=10, pady=10)

        title_label = Label(frame, text="Change Password", bg="white", font=controller.title_font)
        title_label.grid(row=0, columnspan=4)

        # label.pack(side="top", fill="x", pady=10)
        Label(frame, text="", bg="white").grid(row=1)

        Label(frame, text="Car Id: ", bg="white", font=controller.label_font).grid(row=2, column=0)
        self.car_id = Entry(frame, width=30, fg="black", bg="white", font=controller.label_font)
        self.car_id.grid(row=2, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=3)

        Label(frame, text="Current Password: ", bg="white", font=controller.label_font).grid(row=5, column=0)
        self.current_password = Entry(frame, width=30, fg="black", show="*", bg="white", font=controller.label_font)
        self.current_password.grid(row=5, column=1, columnspan=2)

        Label(frame, text="", bg="white", font=controller.label_font).grid(row=6)

        Label(frame, text="New Password: ", bg="white", font=controller.label_font).grid(row=7, column=0)
        self.new_password = Entry(frame, width=30, fg="black", show="*", bg="white", font=controller.label_font)
        self.new_password.grid(row=7, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=8)

        Label(frame, text="New Password Again: ", bg="white", font=controller.label_font).grid(row=9, column=0)
        self.new_password_again = Entry(frame, width=30, fg="black", show="*", bg="white", font=controller.label_font)
        self.new_password_again.grid(row=9, column=1, columnspan=2)

        Label(frame, text="", bg="white").grid(row=10)
        password_not_match = Label(frame, text="Passwords aren't match. try again", fg="red", bg="white", font=controller.label_font)
        must_fill = Label(frame, text="Must fill in all fields", fg="red", bg="white", font=controller.label_font)
        invalid_input = Label(frame, text="Invalid input", fg="red", bg="white", font=controller.label_font)
        wrong_details = Label(frame, text="Wrong car id or password, try again", fg="red", bg="white", font=controller.label_font)

        Label(frame, text="", bg="white").grid(row=12)

        self.index = -1

        def SavePassword(self):
            password_not_match.grid_remove()
            must_fill.grid_remove()
            invalid_input.grid_remove()
            wrong_details.grid_remove()

            if(self.car_id.get() == "" or self.current_password.get() == "" or self.new_password.get() == "" or self.new_password_again.get() == ""):
                must_fill.grid(row=11, column=0, columnspan=5)
                return 0
            # input validation
            if (not (self.car_id.get().isalnum() and emailPattern(self.current_password.get()) and emailPattern(self.new_password.get()) and emailPattern(self.new_password_again.get()))):
                invalid_input.grid(row=11,column=0, columnspan=5)
                return 0
            if (self.new_password.get() != self.new_password_again.get()):
                password_not_match.grid(row=11, column=0, columnspan=5)
                return 0
            # check the current password
            query = "SELECT salt,hashed_password FROM car WHERE car_id = '" + self.car_id.get() + "';"

            mycursor = mydb.cursor()
            mycursor.execute(query)
            result = mycursor.fetchall()

            if (len(result) == 0):
                wrong_details.grid(row=11, column=0, columnspan=5)
                return 0
            salt = result[0][0]
            hashed_password = result[0][1]
            massage_to_server = "hashed_password " + self.current_password.get() + " " + salt

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect(("127.0.0.1", 8888))

            server.send(bytearray(massage_to_server.encode()))
            result = server.recv(1024)
            result = result.decode("utf-8")
            server.close()

            if (result != hashed_password):
                wrong_details.grid(row=11, column=0, columnspan=5)
                return 0

            # The password is ok
            # create new salt for the new password:
            massage_to_server = "create_salt"
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect(("127.0.0.1", 8888))

            server.send(bytearray(massage_to_server.encode()))
            salt = server.recv(1024)
            salt = salt.decode("utf-8")
            server.close()

            # create hash for the new password and salt
            massage_to_server = "hashed_password " + self.new_password.get() + " " + salt

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect(("127.0.0.1", 8888))

            server.send(bytearray(massage_to_server.encode()))
            hashed_password = server.recv(1024)
            hashed_password = hashed_password.decode("utf-8")
            server.close()

            # update the new hashed password and new salt in the db
            query = "UPDATE car SET salt = '" + salt + "', hashed_password = '" + hashed_password + "' WHERE car_id = '" + self.car_id.get() + "';"
            mycursor.execute(query)
            mydb.commit()
            result = mycursor.rowcount
            self.car_id.delete(0, END)
            self.current_password.delete(0, END)
            self.new_password.delete(0, END)
            self.new_password_again.delete(0, END)

            controller.show_frame("Cars")

        def clearPage(self):
            self.car_id.delete(0, END)
            self.current_password.delete(0, END)
            self.new_password.delete(0, END)
            self.new_password_again.delete(0, END)
            controller.show_frame("Cars")

        self.save_btn = Button(frame, text="Save", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: SavePassword(self))
        self.save_btn.grid(row=13, column=2, columnspan=2)
        self.next_btn = Button(frame, text="cancel", bg=controller.color_btn, font=controller.label_font,
                               command=lambda: clearPage(self))
        self.next_btn.grid(row=13, column=0, columnspan=2)

def CheckDetails(username, password):
    # input validation
    if ((not username.isdecimal()) or (not emailPattern(password))):
        return False

    query="SELECT salt,hashed_password,permitions FROM worker WHERE worker_id = '" + username + "';"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    result = mycursor.fetchall()

    if(len(result) == 0):
        return False
    salt = result[0][0]
    hashed_password = result[0][1]
    massage_to_server = "hashed_password " + password + " " + salt

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("127.0.0.1", 8888))

    server.send(bytearray(massage_to_server.encode()))
    result = server.recv(1024)
    result = result.decode("utf-8")
    server.close()

    if (result == hashed_password):
        return True
    else:
        return False

def emailPattern(string):
    lenStr = len(string)
    i = 0
    if (lenStr == 0):
        return False
    while (i < lenStr):
        if (not ((string[i] >= 'a' and string[i] <= 'z') or (string[i] >= 'A' and string[i] <= 'Z') or string[i] == '@' or string[i] == '.' or (string[i] >= '0' and string[i] <= '9'))):
            return False
        i=i+1
    return True

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()