# no wildcard import such that all new tcl/ tkk widgets are all accesable by tk
import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import utils

# Display Class
class Display(tk.Frame):

    # Constructor - init parent plus set some private attrs
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        # attrs
        self._parent = parent 
        self.headers = ["dataType|enum/DataType", "dataConvention", "label1|variant/string", "select", "dataValue"]
        self.count = 0
        self.ids = []
        self.curveNames = []
        self.rows = defaultdict(list)

        # frames
        self._frame = tk.Frame(self._parent, borderwidth=5, bg = "#323f54")
        self._frame_title = tk.Label(self._frame, text = "Display", bg = "#4287f5", fg = 'white')
        self.table_frame = tk.Frame(self._frame, bg = "white" )
        self.display_scroll = tk.Scrollbar(self.table_frame, orient= "vertical")
        self.table = ttk.Treeview(self.table_frame, yscrollcommand= self.display_scroll.set ,  columns = self.headers , style = "Custom.Treeview" )
        
        # packing
        self._frame.pack(expand = 0, anchor = 'ne', fill = 'both',padx = 5, pady = 5)
        self._frame_title.pack(anchor = "nw", side = "top", expand = 0)
        self.table_frame.pack(expand = 1, fill = "both")
        self.table.pack( fill = "y", side = "left", expand = 1)
        self.display_scroll.pack(side="right", fill="y")
        self.table.pack(expand = 1, fill = 'both')
        
        # events
        self.table.bind('<Button-3>', self.rightclick)
        
        # configs
        self.display_scroll.config(command=self.table.yview)
        
        # name and format columns
        for col in self.headers:
            self.table.heading(col, text=col.title(), anchor = "center")

        
        

    # I wanted to keep most class attributes and methods private. theses get/set methods are for encapulation purposes.
    def get_frame(self):
        return self._frame

    # function called from main to service the display
    def prepare( self , curve_data , curveName ):
        # curvenames holds all actuve curves used a list as had probelms with iids. Now this is not an issue but list functions for now
        if curveName in self.curveNames:
            
            # return error to main
            return  f"Error: {curveName} Componant already displayed"
        
        else:
            # add curve name to list + call data to be cleaned and inserted
            self.curveNames.append(curveName)
            self.clean_data(curve_data)
            self.insert_data(curveName)
        
    # called from prepare and strips into rows from curvedata
    def clean_data(self, curve_data):

        group_data = {}

        # groupdata added to row 
        for group in curve_data:
            data1ds = group["item|UQL/Data1d"]

            
            group_data["dataType|enum/DataType"] = data1ds["dataType|enum/DataType"]
            group_data["dataConvention"] = data1ds["dataConvention"]
            curve_instrums = data1ds['dataPointList|sequence/object']

            # recour
            self.traverse_data1ds( group_data, curve_instrums )

    
    # recoursive procedure for instrument data
    def traverse_data1ds(self, group_data, curve_instrums):
        for curve_instrum in curve_instrums:
            
            for k in group_data:
                v = group_data[k]
                self.rows[self.count].append(v)
            
            # unique row values added. hard for now needs dynamic/ varables
            self.rows[self.count].append(curve_instrum["item|UQL/DataPointCurveInstrument"]["label1|variant/string"])
            self.rows[self.count].append(curve_instrum["item|UQL/DataPointCurveInstrument"]["select"])
            self.rows[self.count].append(round(curve_instrum["item|UQL/DataPointCurveInstrument"]["dataValue"], 4))
            

            self.count +=1

    # called by prepare and inserts in correct order into columns
    def insert_data(self, curveName):
        model = self.table.insert('', 'end', text = curveName )
        for index in self.rows:
            values = tuple(self.rows[index])
            self.ids.append( self.table.insert( model , 'end', text = index,  values=values) )


    # rightclick callbackfunction
    def rightclick(self, event):

        # create a popup menu
        self.aMenu = tk.Menu(self.table, tearoff=0)
        self.aMenu.add_command(label='Delete', command=self.delete)
        self.aMenu.add_command(label='Select All', command=self.select_all)
        self.aMenu.post(event.x_root, event.y_root)
        self.table_items = self.table.focus()

    # delete method for rc menu
    def delete(self):
        if self.table.selection():
            for i in self.table.selection():
                item = self.table.item(i)
                if item['text'] in self.curveNames:
                    self.curveNames.remove(item['text'])
                self.table.delete(i)
    
    # selcet all method for rc menu
    def select_all(self):
        children = self.table.get_children(self.table_items)
        for child in children:
            self.table.selection_add(child)
        

