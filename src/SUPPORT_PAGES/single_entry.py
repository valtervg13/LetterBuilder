import tkinter as tk
from tkinter import ttk


class single_entry(tk.Toplevel):
    DEFAULT_SIZE = '300x150'

    def __init__(self, parent, parent_func, master, size=DEFAULT_SIZE, f_kwargs={}, **kwargs):
        super().__init__(master=master)
        self.parent = parent
        self.parent_func = parent_func
        self.master = master
        self.size = size
        self.f_kwargs = f_kwargs
        self.label_text = kwargs.pop('label_text', 'Entre com os dados:')
        self.default_var = kwargs.pop('default_var', '')
        self.button_text = kwargs.pop('button_text', 'Avançar')
        self.id = kwargs.pop('id', '')
        self.var = tk.StringVar(value=self.default_var)
        self._create_widgets()
        self._set_geometry()
        self.focus_set()
        self.master.attributes('-disabled', True)
        self.protocol("WM_DELETE_WINDOW", self.close)

    def _create_widgets(self):
        label = ttk.Label(self, text=self.label_text)
        label.grid(row=0, column=0, padx=10, pady=10)

        entry = ttk.Entry(self, textvariable=self.var)
        entry.grid(row=1, column=0, padx=10, pady=10)

        confirm_button = ttk.Button(self, text=self.button_text, command=self.action)
        confirm_button.grid(row=2, column=0, padx=10, pady=10)
        
    def _set_geometry(self):
        x_screen = self.master.winfo_screenwidth() / 2
        y_screen = self.master.winfo_screenheight() / 2
        x_widget, y_widget = map(int, self.size.split('x'))

        x = int(x_screen - x_widget / 2)
        y = int(y_screen - y_widget / 2)

        self.geometry(f'{self.size}+{x}+{y}')
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def action(self):
        try:
            popup_output = ({str(self.id): self.var.get()}
                            if self.id != ''
                            else self.var.get())
            self.parent_func(popup_output, **self.f_kwargs)
            self.close()
        except Exception as e:
            print(e)
            
    def close(self):
        self.master.attributes('-disabled', False)
        self.destroy()