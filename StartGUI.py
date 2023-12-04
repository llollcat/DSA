from CheckSignGUI import *


class StartGUI(tk.Tk):

    def sign(self):
        self.destroy()
        CheckSignGUI(self.L, self.N)

    def check_sign(self):
        self.destroy()
        CheckSignGUI(self.L, self.N)

    def __init__(self, L, N):
        self.L = L
        self.N = N
        super().__init__()
        self.wm_title("DSA")

        button_select_file = tk.Button(self, text="Подписать", command=self.sign)
        button_check = tk.Button(self, text="Проверить подпись", command=self.check_sign)

        button_select_file.grid(row=0, column=0)
        button_check.grid(row=1, column=0)

        self.mainloop()
