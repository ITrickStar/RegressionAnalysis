from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import numpy as np
import sup
import data_processing

import matplotlib
import pandas as pd
matplotlib.use("TkAgg")


class App(ctk.CTk):

    global filename
    global df

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modes: "System" (standard), "Dark", "Light"
        ctk.set_appearance_mode("light")
        # Themes: "blue" (standard), "green", "dark-blue"
        ctk.set_default_color_theme("blue")

        self.title("Regression Analysis Program")
        self.geometry(f"{1100}x{580}")
        self.resizable(0, 0)  # makes the root window fixed in size.

        """MENU"""
        mainmenu = Menu(self)
        self.config(menu=mainmenu)

        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Открыть...", command=self.Load_excel_data)
        filemenu.add_command(label="Сохранить...")
        filemenu.add_command(label="Выход", command=self.destroy)

        helpmenu = Menu(mainmenu, tearoff=0)
        helpmenu.add_command(label="Помощь")
        helpmenu.add_command(label="О программе")

        mainmenu.add_cascade(label="Файл",
                             menu=filemenu)
        mainmenu.add_cascade(label="Справка",
                             menu=helpmenu)

        """Buttons"""
        button = ctk.CTkButton(
            master=self, text="reform_data", command=self.data_manipulation)
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        """Frame1"""
        frame1 = tk.LabelFrame(self, text="Excel Data")
        frame1.place(height=300, width=600, anchor="nw")
        self.tv1 = ttk.Treeview(frame1)
        # set the height and width of the widget to 100% of its container (frame1).
        self.tv1.place(relheight=1, relwidth=1)
        # command means update the yaxis view of the widget
        treescrolly = tk.Scrollbar(
            frame1, orient="vertical", command=self.tv1.yview)
        # command means update the xaxis view of the widget
        treescrollx = tk.Scrollbar(
            frame1, orient="horizontal", command=self.tv1.xview)
        # assign the scrollbars to the Treeview Widget
        self.tv1.configure(xscrollcommand=treescrollx.set,
                           yscrollcommand=treescrolly.set)
        # make the scrollbar fill the x axis of the Treeview widget
        treescrollx.pack(side="bottom", fill="x")
        # make the scrollbar fill the y axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")

        """Frame2"""
        frame2 = tk.LabelFrame(
            self, text="Описательная статистика", height=300, width=400)
        frame2.place(height=300, width=300, y=300)
        self.tv2 = ttk.Treeview(frame2)
        # set the height and width of the widget to 100% of its container (frame1).
        self.tv2.place(relheight=1, relwidth=1)
        treescrolly = tk.Scrollbar(
            frame2, orient="vertical", command=self.tv2.yview)
        # command means update the xaxis view of the widget
        treescrollx = tk.Scrollbar(
            frame2, orient="horizontal", command=self.tv2.xview)
        # assign the scrollbars to the Treeview Widget
        self.tv1.configure(xscrollcommand=treescrollx.set,
                           yscrollcommand=treescrolly.set)
        # make the scrollbar fill the x axis of the Treeview widget
        treescrollx.pack(side="bottom", fill="x")
        # make the scrollbar fill the y axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")

        self.Load_excel_data()
        self.data_manipulation()

        """Notebook"""
        notebook = ttk.Notebook(self, height=400, width=400)
        notebook.place(height=400, width=400, x=600)
        print(self.df.head())
        notebook.add(
            sup.Tab(notebook, self.df.describe(include='bool')), text='binary')
        notebook.add(sup.Tab(notebook, self.df.describe(
            include='number')), text='numerical')
        notebook.add(sup.Tab(notebook, self.df.describe(include='category')), text='category')
        notebook.pack()

    def File_dialog(self):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        self.filename = fd.askopenfilename(initialdir="/",
                                           title="Select A File",
                                           filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))
        return None

    def Load_excel_data(self):
        self.File_dialog()
        #self.filename = 'D:\Apartment_data.xlsx'
        self.df = sup.Load_DataFrame(self.filename)

        new_header = self.df.iloc[0]  # grab the first row for the header
        self.df = self.df[1:]  # take the data less the header row
        self.df.columns = new_header  # set the header row as the df header
        self.df = self.df.loc[:, self.df.columns.notna()]
        self.df = self.df.convert_dtypes()

        # for i in range(1, self.df.columns.size):
        #     self.df.rename(
        #         columns={self.df.columns[i]: self.df.columns[i].replace('\n', ' ')})

        sup.TVinput(self.tv1, self.df.reset_index())
        sup.TVinput(self.tv2, self.df.describe().reset_index())

        return None

    def data_manipulation(self):
        try:
            data_processing.clean_data(self.df)
            data_processing.reform_data(self.df)
        except ValueError:
            tk.messagebox.showerror(
                "Information", "The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror(
                "Information", f"No such file as {self.filename}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
