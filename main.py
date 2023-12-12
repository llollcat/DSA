import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from DSA import DSA

if __name__ == '__main__':
    window_size = "1350x400"
    # Create the main window
    sender_window = tk.Tk()
    sender_window.title("Отправитель")
    sender_window.geometry(window_size)
    sender_window.resizable(False, False)
    sender_window.attributes("-topmost", True)

    h = None
    r = None
    s = None
    x = None
    y = None
    message = None

    seed = simpledialog.askinteger("Seed", "Введите seed для генерации", initialvalue=0)

    dsa = DSA(512, 160, seed)

    # Add labels, entries, and buttons
    ttk.Label(sender_window, text="Параметры системы").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    ttk.Label(sender_window, text="p").grid(column=0, row=1, sticky=tk.W, padx=5)
    ttk.Label(sender_window, text="q").grid(column=0, row=2, sticky=tk.W, padx=5)
    ttk.Label(sender_window, text="g").grid(column=0, row=3, sticky=tk.W, padx=5)
    ttk.Label(sender_window, text="Hash:").grid(column=0, row=4, sticky=tk.W, padx=5)
    ttk.Label(sender_window, text="r").grid(column=0, row=5, sticky=tk.W, padx=5)
    ttk.Label(sender_window, text="s").grid(column=0, row=6, sticky=tk.W, padx=5)
    ttk.Label(sender_window, text="Закрытый ключ x").grid(column=0, row=7, sticky=tk.W, padx=5)
    ttk.Label(sender_window, text="Открытый ключ y").grid(column=0, row=8, sticky=tk.W, padx=5)

    label_p_key = ttk.Label(sender_window, text="---")
    label_p_key.grid(column=1, row=1, sticky=tk.W, padx=5)
    label_q_key = ttk.Label(sender_window, text="---")
    label_q_key.grid(column=1, row=2, sticky=tk.W, padx=5)
    label_g_key = ttk.Label(sender_window, text="---")
    label_g_key.grid(column=1, row=3, sticky=tk.W, padx=5)

    hash_text = tk.Text(sender_window, height=1, width=50)
    hash_text.grid(column=1, row=4, sticky=tk.W, padx=5)

    label_r_key = ttk.Label(sender_window, text="---")
    label_r_key.grid(column=1, row=5, sticky=tk.W, padx=5)
    label_s_key = ttk.Label(sender_window, text="---")
    label_s_key.grid(column=1, row=6, sticky=tk.W, padx=5)
    label_x_key = ttk.Label(sender_window, text="---")
    label_x_key.grid(column=1, row=7, sticky=tk.W, padx=5)
    label_y_key = ttk.Label(sender_window, text="---")
    label_y_key.grid(column=1, row=8, sticky=tk.W, padx=5)

    frame_message_box = ttk.LabelFrame(sender_window, text="Окно сообщения", height=100)
    frame_message_box.grid(column=0, row=10, columnspan=3, sticky=tk.EW, padx=5, pady=5)
    frame_message_box.grid_propagate(False)

    text_message = tk.Text(frame_message_box, height=5, width=50)
    text_message.pack(expand=True, padx=5, pady=5)

    param = dsa.get_crypto_parameters()
    label_p_key.config(text=param['p'])
    label_q_key.config(text=param['q'])
    label_g_key.config(text=param['g'])


    def calculate_hash():
        global text_message, h
        h = dsa.get_str_hash(text_message.get("1.0", "end-1c"))

        hash_text.delete("1.0", "end-1c")
        hash_text.insert("1.0", h)


    ttk.Button(sender_window, text="Подсчитать хеш сообщение", command=calculate_hash).grid(column=3, row=1,
                                                                                            sticky=tk.W,
                                                                                            padx=5, pady=5)


    def generate_parameters():
        global dsa, x, y
        p = dsa.generate_new_keys()
        x = p['x']
        y = p['y']
        label_x_key.config(text=str(x))
        label_y_key.config(text=str(y))


    ttk.Button(sender_window, text="Сгенерировать открытый и закрытый ключ", command=generate_parameters).grid(column=3,
                                                                                                               row=2,
                                                                                                               sticky=tk.W,
                                                                                                               padx=5,
                                                                                                               pady=5)


    def sign():
        global label_r_key, label_s_key, h, r, s

        if h is None:
            messagebox.showerror("Ошибка", "Подсчитайте хеш")
            return

        if x is None:
            messagebox.showerror("Ошибка", "Сгенерируйте ключи")
            return

        out = dsa.sign(h, x)

        r = out['r']
        s = out['s']

        label_r_key.config(text=out['r'])
        label_s_key.config(text=out['s'])


    ttk.Button(sender_window, text="Подписать сообщение", command=sign).grid(column=3, row=3, sticky=tk.W,
                                                                             padx=5, pady=5)

    is_send = False


    def send():
        global is_send
        if r is None or s is None:
            messagebox.showerror("Ошибка", "Необходимо подписать")
            return

        is_send = True


    ttk.Button(sender_window, text="Отправить", command=send).grid(column=3, row=4, sticky=tk.W, padx=5, pady=5)

    # receiver side ------------------------------------------------------------------------------------------
    receiver_window = tk.Tk()
    receiver_window.title("Получатель")
    receiver_window.geometry(window_size)
    receiver_window.resizable(False, False)
    receiver_window.attributes("-topmost", True)

    r_s = None
    s_s = None
    y_s = None
    message_s = None

    # Add labels, entries, and buttons
    ttk.Label(receiver_window, text="Параметры системы").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    ttk.Label(receiver_window, text="p").grid(column=0, row=1, sticky=tk.W, padx=5)
    ttk.Label(receiver_window, text="q").grid(column=0, row=2, sticky=tk.W, padx=5)
    ttk.Label(receiver_window, text="g").grid(column=0, row=3, sticky=tk.W, padx=5)
    ttk.Label(receiver_window, text="Hash:").grid(column=0, row=4, sticky=tk.W, padx=5)
    ttk.Label(receiver_window, text="r").grid(column=0, row=5, sticky=tk.W, padx=5)
    ttk.Label(receiver_window, text="s").grid(column=0, row=6, sticky=tk.W, padx=5)
    ttk.Label(receiver_window, text="Открытый ключ y").grid(column=0, row=8, sticky=tk.W, padx=5)

    label_p_key_s = ttk.Label(receiver_window, text="---")
    label_p_key_s.grid(column=1, row=1, sticky=tk.W, padx=5)
    label_q_key_s = ttk.Label(receiver_window, text="---")
    label_q_key_s.grid(column=1, row=2, sticky=tk.W, padx=5)
    label_g_key_s = ttk.Label(receiver_window, text="---")
    label_g_key_s.grid(column=1, row=3, sticky=tk.W, padx=5)

    hash_text_s = tk.Text(receiver_window, height=1, width=50)
    hash_text_s.grid(column=1, row=4, sticky=tk.W, padx=5)

    label_r_key_s = ttk.Label(receiver_window, text="---")
    label_r_key_s.grid(column=1, row=5, sticky=tk.W, padx=5)
    label_s_key_s = ttk.Label(receiver_window, text="---")
    label_s_key_s.grid(column=1, row=6, sticky=tk.W, padx=5)
    label_y_key_s = ttk.Label(receiver_window, text="---")
    label_y_key_s.grid(column=1, row=8, sticky=tk.W, padx=5)

    frame_message_box_s = ttk.LabelFrame(receiver_window, text="Окно сообщения", height=100)
    frame_message_box_s.grid(column=0, row=10, columnspan=3, sticky=tk.EW, padx=5, pady=5)
    frame_message_box_s.grid_propagate(False)

    text_message_s = tk.Text(frame_message_box_s, height=5, width=50)
    text_message_s.pack(expand=True, padx=5, pady=5)


    def receive():
        global text_message_s, label_p_key_s, label_q_key_s, label_g_key_s, label_r_key_s, label_s_key_s, label_y_key_s
        global is_send, r_s, s_s, y_s
        if not is_send:
            messagebox.showerror("Ошибка", "Ничего не отправлено")
            return
        text_message_s.delete("1.0", "end-1c")
        text_message_s.insert("1.0", text_message.get("1.0", "end-1c"))
        pqg = dsa.get_crypto_parameters()
        label_p_key_s.config(text=pqg['p'])
        label_q_key_s.config(text=pqg['q'])
        label_g_key_s.config(text=pqg['g'])

        r_s = r
        s_s = s
        y_s = y
        label_r_key_s.config(text=str(r))
        label_s_key_s.config(text=str(s))
        label_y_key_s.config(text=str(y))
        is_send = False


    ttk.Button(receiver_window, text="Получить параметры и сообщение", command=receive).grid(column=3, row=0,
                                                                                             sticky=tk.W, padx=5,
                                                                                             pady=5)


    def calculate_hash_receiver():
        global text_message_s
        mess_s = text_message_s.get("1.0", "end-1c")

        h_s = dsa.get_str_hash(mess_s)

        hash_text_s.delete("1.0", "end-1c")
        hash_text_s.insert("1.0", h_s)


    ttk.Button(receiver_window, text="Подсчитать хеш сообщение",
               command=calculate_hash_receiver).grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)


    def verify():
        global text_message_s
        if y_s is None or r_s is None or s_s is None:
            messagebox.showerror("Ошибка", "Заданы не все параметры")
            return
        try:
            h_s = int(hash_text_s.get("1.0", "end-1c"))
        except ValueError:
            messagebox.showerror("Ошибка", "Ошибка в хеше")
            return
        is_sign_valid = dsa.check_sign(h_s, y_s, r_s, s_s)
        messagebox.showinfo('Проверка подписи', "Подпись верна" if is_sign_valid else "Подпись не верна")


    ttk.Button(receiver_window, text="Проверить подпись", command=verify).grid(column=3, row=2, sticky=tk.W, padx=5,
                                                                               pady=5)
    sender_window.lift()
    sender_window.mainloop()
