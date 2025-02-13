import tkinter as tk
import pyautogui
import threading
import keyboard

class AutoClickerApp:
    def __init__(self, master):
        self.master = master
        master.title("AutoClicker")
        master.geometry("300x200")

        self.click_rate = tk.DoubleVar(value=1.0)

        self.toggle_button = tk.Button(master, text="Start (Press F6)", command=self.start_clicking)
        self.toggle_button.pack()

        self.click_rate_label = tk.Label(master, text="Clicks per second:")
        self.click_rate_label.pack()

        self.click_rate_entry = tk.Entry(master, textvariable=self.click_rate)
        self.click_rate_entry.pack()

        self.is_clicking = False

    def start_clicking(self):
        if self.is_clicking:
            self.is_clicking = False
            self.toggle_button.config(text="Start (Press F6)")
        else:
            self.is_clicking = True
            self.toggle_button.config(text="Stop (Press F7)")
            self.start_clicking_thread()

    def start_clicking_thread(self):
        click_thread = threading.Thread(target=self.click_loop)
        click_thread.daemon = True
        click_thread.start()

    def click_loop(self):
        while self.is_clicking:
            x, y = pyautogui.position()
            pyautogui.click(x, y)
            pyautogui.PAUSE = 1 / self.click_rate.get()

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    
    # Définition des raccourcis clavier
    keyboard.add_hotkey('F6', app.start_clicking)
    keyboard.add_hotkey('F7', app.start_clicking)

    root.mainloop()

if __name__ == "__main__":
    main()
