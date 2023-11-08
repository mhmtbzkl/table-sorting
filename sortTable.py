import argparse
import pandas as pd
import tkinter as tk
from  tkinter import ttk
from functools import partial


data = []
inlineRows = []
fileRows = []
rows = []
columns = []

parser = argparse.ArgumentParser(description="sorting table example")
parser.add_argument('-r','--rows', nargs='+')
parser.add_argument('-o','--open', type=argparse.FileType('r'))

args = parser.parse_args()

if not (args.rows or args.open):
    parser.error('No action requested, add -r ROWS or -o OPENFILE')

if(args.rows):
    rows.clear()
    inlineRows.clear()
    for i in args.rows: 
        row = []
        for j in i.strip('[]').split(','):
            row.append(j)
        inlineRows.append(row)

    data = pd.DataFrame(inlineRows)
    data.columns = data.iloc[0]
    data = data[1:]
    #print(data)

if(args.open):
    data = pd.read_csv(args.open)
    #print(data)



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        print(*args)
        print(**kwargs)

        global data

        window = tk.Frame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["Table"] = Table(parent=window, controller=self, columns=data.head(), rows=data)

        self.show_frame("Table")


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


    def update_globals(self):
        frame = self.frames["Table"]
        frame.update_globals()



class Table(tk.Frame):
    def __init__(self, parent, controller, columns=list(), rows=pd.DataFrame):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.scroll = tk.Scrollbar(parent)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.columns = columns
        self.rows = rows

        self.table = ttk.Treeview(self.parent, height= 20, yscrollcommand = self.scroll.set)
        self.table.pack()
        self.scroll.config(command=self.table.yview)

        self.table['columns'] = tuple(self.columns)
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.heading("#0",text="", anchor=tk.CENTER)

        for i, col in enumerate(self.columns):
            self.table.column(f"#{i+1}", width=80, stretch=tk.NO)
            self.table.heading(col, text=f"{col}", command=partial(self.update_globals, f"{col}"), anchor=tk.CENTER)
        
        for i, row in self.rows.iterrows():
            self.table.insert(parent='', index='end', text='', values=tuple(row))

        self.table.pack()


    def update_globals(self, option):
        global data
        rows = data.sort_values(by=option, ascending=True)
        self.controller.show_frame("Table")

        for item in self.table.get_children():
            self.table.delete(item)

        for i, row in rows.iterrows():
            self.table.insert(parent='', index='end', text='', values=tuple(row))
        
        #print(rows)

        
app = App()
app.mainloop()
