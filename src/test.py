import tkinter as tk
from tkinter import ttk
from SUPPORT_PAGES.alt_singleentry import single_entry


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.button = ttk.Button(self, text='Open Pop-up', command=self.open_popup)
        self.button.pack()

    def open_popup(self):
        popup_window = single_entry(parent=self,
                                    parent_func=lambda output: self.callback_function(output),
                                    master=self,
                                    size='300x150',
                                    label_text='Enter your name:',
                                    default_var='',
                                    button_text='Submit',
                                    id='name')

    def callback_function(self,output):
        print(output)

app = MainApp()
app.mainloop()
