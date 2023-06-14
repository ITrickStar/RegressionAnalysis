import tkinter as tk
from tkinter import ttk
import pandas as pd
import data_processing


def TVinput(tv: ttk.Treeview, df: pd.DataFrame):  # Dataframe in Treeview
    def clear_data():
        tv.delete(*tv.get_children())
        return None

    clear_data()
    tv["column"] = list(df.columns)
    tv["show"] = "headings"
    for column in tv["columns"]:
        # let the column heading = column name
        tv.heading(column, text=column)
        tv.column(column, minwidth=0, width=200)
    # turns the dataframe into a list of lists
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        tv.insert("", "end", values=row)
    return None


def Load_DataFrame(input: str):  # Dataframe path input
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = input
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)
    except ValueError:
        tk.messagebox.showerror(
            "Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror(
            "Information", f"No such file as {file_path}")
        return None

    return df


class Tab(tk.Frame):  # Tab object for notebook
    def __init__(self, parent, df: pd.DataFrame):
        tk.Frame.__init__(self)
        shell_frame = tk.LabelFrame(
            self, text="Описательная статистика", width=600, height=600)
        shell_frame.grid(row=0, column=0, padx=5, pady=5)
        shell_frame.pack(fill='both', expand=True)
        self.treeview = ttk.Treeview(shell_frame)
        # set the height and width of the widget to 100% of its container (frame1).
        self.treeview.place(relheight=1, relwidth=1)
        # command means update the yaxis view of the widget
        treescrolly = tk.Scrollbar(
            shell_frame, orient="vertical", command=self.treeview.yview)
        # command means update the xaxis view of the widget
        treescrollx = tk.Scrollbar(
            shell_frame, orient="horizontal", command=self.treeview.xview)
        # assign the scrollbars to the Treeview Widget
        self.treeview.configure(xscrollcommand=treescrollx.set,
                                yscrollcommand=treescrolly.set)
        # make the scrollbar fill the x axis of the Treeview widget
        treescrollx.pack(side="bottom", fill="x")
        # make the scrollbar fill the y axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")
        TVinput(self.treeview, df.reset_index())
