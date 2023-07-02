import socket
import threading
import tkinter as tk
from random import random
from string import ascii_letters, digits
from tkinter import scrolledtext, messagebox, simpledialog


class ChatClient:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55556
        self.nickname = None
        self.client = None

        self.gui = tk.Tk()
        self.gui.title('Chat Client')
        self.gui.geometry('400x500')

        self.chat_frame = tk.Frame(self.gui)
        self.chat_frame.pack(padx=10, pady=10, expand=True, fill='both')

        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, state='disabled')
        self.chat_area.pack(padx=10, pady=10, expand=True, fill='both')

        self.message_entry = tk.Entry(self.gui)
        self.message_entry.pack(padx=10, pady=10, fill='x')

        self.send_button = tk.Button(self.gui, text='Wyślij', command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.user_list_frame = tk.Frame(self.gui)
        self.user_list_frame.pack(padx=10, pady=10, side='right', fill='y')

        self.user_list_label = tk.Label(self.user_list_frame, text='Lista użytkowników')
        self.user_list_label.pack(padx=10, pady=10)

        self.user_list = tk.Listbox(self.user_list_frame)
        self.user_list.pack(padx=10, pady=10, fill='both')

        self.gui.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        self.nickname = self.prompt_for_nickname()

        self.client.send(self.nickname.encode('utf-8'))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.gui.mainloop()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message.startswith('[USERS]'):
                    self.update_user_list(message)
                else:
                    self.display_message(message)
                self.gui.update()  # Odświeżenie interfejsu użytkownika
            except:
                messagebox.showerror('Błąd', 'Wystąpił błąd podczas odbierania wiadomości!')
                self.client.close()
                break

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, 'end')
        self.client.send(message.encode('utf-8'))

    def display_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert('end', message + '\n')
        self.chat_area.configure(state='disabled')
        self.chat_area.see('end')

    def update_user_list(self, message):
        users = message[7:].split(', ')
        self.user_list.delete(0, 'end')
        for user in users:
            self.user_list.insert('end', user)

    def prompt_for_nickname(self):
        nickname = simpledialog.askstring('Nickname', 'Podaj swój nickname')
        if nickname:
            return nickname
        else:
            return self.generate_nickname()

    def on_closing(self):
        if messagebox.askokcancel('Zamknij', 'Czy na pewno chcesz zamknąć program?'):
            self.client.send('koniec'.encode('utf-8'))
            self.client.close()
            self.gui.destroy()

    @staticmethod
    def generate_nickname():
        letters_digits = ascii_letters + digits
        return 'Guest_' + ''.join(letters_digits[int(random() * len(letters_digits))] for _ in range(4))


if __name__ == '__main__':
    client = ChatClient()
    client.connect()
