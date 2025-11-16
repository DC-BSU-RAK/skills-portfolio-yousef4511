import tkinter as tk
from tkinter import messagebox
import random
import os

# --------------------------
# LOAD JOKES
# --------------------------
def load_jokes(filename):
    jokes = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline.strip()))
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found!")
    return jokes

script_dir = os.path.dirname(os.path.abspath(__file__))
jokes_file = os.path.join(script_dir, "randomJokes.txt")
jokes = load_jokes(jokes_file)
if not jokes:
    print("No jokes loaded! Check randomJokes.txt")
else:
    print(f"Loaded {len(jokes)} jokes")

current_joke = None
dark_mode = True

# --------------------------
# FUNCTIONS
# --------------------------
def tell_joke():
    global current_joke
    if not jokes:
        messagebox.showerror("Error", "No jokes found!")
        return
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")

def show_punchline():
    if current_joke:
        punchline_label.config(text=current_joke[1])
    else:
        messagebox.showinfo("Info", "Click 'Alexa tell me a Joke' first!")

def next_joke():
    tell_joke()

def quit_app():
    root.destroy()

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    if dark_mode:
        bg = "#1E1E1E"
        fg = "white"
        setup_fg = "lightblue"
        punchline_fg = "lightgreen"
        btn_fg = "white"
    else:
        bg = "#F5F5F5"
        fg = "#222"
        setup_fg = "#0B3D91"
        punchline_fg = "#2E8B57"
        btn_fg = "white"

    # Root and frames
    root.config(bg=bg)
    start_frame.config(bg=bg)
    joke_frame.config(bg=bg)
    button_frame.config(bg=bg)

    # Labels
    start_label.config(bg=bg, fg=fg)
    title_label.config(bg=bg, fg=fg)
    setup_label.config(bg=bg, fg=setup_fg)
    punchline_label.config(bg=bg, fg=punchline_fg)

    # Buttons
    for btn in button_frame.winfo_children():
        btn.config(fg=btn_fg)
    for btn in start_frame.winfo_children():
        if isinstance(btn, tk.Button):
            btn.config(fg=btn_fg)

def show_start_page():
    start_frame.pack(fill="both", expand=True)
    joke_frame.pack_forget()

def start_app():
    start_frame.pack_forget()
    joke_frame.pack(fill="both", expand=True)
    tell_joke()

# --------------------------
# GUI SETUP
# --------------------------
root = tk.Tk()
root.title("Alexa Jokes - Programmer & Islamic Edition")
root.geometry("450x450")
root.resizable(False, False)

# ---------- START PAGE ----------
start_frame = tk.Frame(root)
start_label = tk.Label(start_frame, text="🤖 Alexa Jokes 🤖\n\n• Click Start to hear a random joke\n• Jokes are from randomJokes.txt\n• You can change theme anytime",
                       font=("Arial", 14), justify="left", wraplength=450)
start_label.pack(pady=60)

tk.Button(start_frame, text="Start", command=start_app, width=15, height=2, bg="#4CAF50").pack(pady=10)
tk.Button(start_frame, text="Toggle Dark/Light", command=toggle_theme, width=15, height=2, bg="#9C27B0").pack(pady=5)
tk.Button(start_frame, text="Exit", command=quit_app, width=15, height=2, bg="#F44336").pack(pady=5)

# ---------- MAIN JOKE PAGE ----------
joke_frame = tk.Frame(root)

title_label = tk.Label(joke_frame, text="😂 Alexa, tell me a Joke 😂", font=("Arial Rounded MT Bold", 20))
title_label.pack(pady=20)

setup_label = tk.Label(joke_frame, text="", font=("Arial", 16), wraplength=500)
setup_label.pack(pady=15)

punchline_label = tk.Label(joke_frame, text="", font=("Arial", 16, "italic"), wraplength=500)
punchline_label.pack(pady=10)

button_frame = tk.Frame(joke_frame)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Alexa tell me a Joke", command=tell_joke, width=20, height=2, bg="#4CAF50").grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Show Punchline", command=show_punchline, width=20, height=2, bg="#2196F3").grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Next Joke", command=next_joke, width=20, height=2, bg="#FF9800").grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Quit", command=quit_app, width=20, height=2, bg="#F44336").grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Toggle Theme", command=toggle_theme, width=42, height=2, bg="#9C27B0").grid(row=2, column=0, columnspan=2, pady=10)

# ---------- INITIALIZE ----------
show_start_page()
apply_theme()
root.mainloop()
