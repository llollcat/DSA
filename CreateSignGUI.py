import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

import DSA
from DSA import *


class CreateSignGUI(tk.Tk):
    def sign_and_save(self):
        self.sign = self.dsa.sign(self.file_hash, self.keys['x'])
        self.dsa.save_public_certificate(filedialog.asksaveasfilename(defaultextension='pub'), self.keys['y'], **self.sign)

    def save_sign(self):
        self.dsa.save_private_certificate(filedialog.asksaveasfilename(defaultextension='prk'), self.keys['x'])

    def __init__(self, L, N):
        super().__init__()
        self.sign = None
        self.wm_title("DSA")

        result = messagebox.askyesnocancel("Загрузить параметры из файла?", "Загрузить параметры из файла?")
        if result == 'yes':
            param = DSA.load_private_certificate(filedialog.askopenfilename())
            self.dsa = DSA(L, N, param['p'], param['q'], param['g'])
        elif result == 'no':
            self.dsa = DSA(L, N)

            seed = simpledialog.askinteger("Seed", "Введите seed для генерации", initialvalue=0)
            self.dsa.set_random_seed(seed)
        else:
            self.dsa = DSA(L, N)

        messagebox.showinfo('Info', 'Выберите файл для подписи')
        self.filename = filedialog.askopenfilename()
        self.file_hash = DSA.get_file_hash(self.filename)

        self.keys = self.dsa.generate_new_keys()

        button_sign_and_save = tk.Button(self, text="Подписать и сохранить сертификат", command=self.sign_and_save)
        button_save_sign = tk.Button(self, text="Сохранить подпись", command=self.save_sign)

        button_sign_and_save.grid(row=0, column=0)
        button_save_sign.grid(row=1, column=0)

        self.mainloop()
