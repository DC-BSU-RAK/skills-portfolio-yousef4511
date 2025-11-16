import tkinter as tk
from tkinter import messagebox
import random
import pygame
from PIL import Image, ImageTk
import os


# ---------------- SOUND SETUP ----------------
pygame.mixer.init()

def play_sound(file):
    try:
        sound = pygame.mixer.Sound(file)
        sound.play()
    except:
        print(f"Missing sound: {file}")

# ---------------- FUNCTIONS ----------------

def displayMenu():
    clear_window()
    stop_timer()

    title = tk.Label(root, text="🧮 Maths Quiz 🧮", font=("Arial Rounded MT Bold", 22),
                     bg="#000000", fg="white")
    title.pack(pady=20)

    subtitle = tk.Label(root, text="Select Difficulty Level", font=("Arial", 14),
                        bg="#000000", fg="white")
    subtitle.pack(pady=10)

    frame = tk.Frame(root, bg="#000000")
    frame.pack(pady=10)

    make_button(frame, "Easy", lambda: start_quiz("easy")).pack(pady=5)
    make_button(frame, "Moderate", lambda: start_quiz("moderate")).pack(pady=5)
    make_button(frame, "Advanced", lambda: start_quiz("advanced")).pack(pady=5)


def randomInt(level):
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation():
    return random.choice(["+", "-"])


def displayProblem():
    clear_window()
    global num1, num2, operation, attempt, time_left

    num1, num2 = randomInt(difficulty)
    operation = decideOperation()
    attempt = 1
    time_left = 10

    header = tk.Label(root, text=f"Question {question_number + 1} of 10",
                      font=("Arial Rounded MT Bold", 18), bg="#000000", fg="white")
    header.pack(pady=10)

    timer_label.config(text=f"⏳ Time Left: {time_left}s")
    timer_label.pack(pady=2)

    problem_label = tk.Label(root, text=f"{num1} {operation} {num2} = ?", font=("Arial", 26, "bold"),
                             bg="#000000", fg="white")
    problem_label.pack(pady=15)

    answer_entry.delete(0, tk.END)
    answer_entry.pack(pady=8, ipady=5)

    frame = tk.Frame(root, bg="#000000")
    frame.pack()
    make_button(frame, "Submit Answer", isCorrect).pack(pady=5)

    start_timer()


def start_timer():
    global timer_job, time_left
    time_left -= 1
    timer_label.config(text=f"⏳ Time Left: {time_left}s")

    if time_left <= 0:
        play_sound("timeout.wav")
        messagebox.showwarning("Time Up!", "You ran out of time!")
        next_question()
        return
    
    timer_job = root.after(1000, start_timer)


def stop_timer():
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None


def isCorrect():
    global score, attempt
    stop_timer()

    try:
        user_ans = int(answer_entry.get())
    except:
        messagebox.showwarning("Error", "Enter a valid number.")
        start_timer()
        return

    correct = num1 + num2 if operation == "+" else num1 - num2

    if user_ans == correct:
        play_sound("correct.wav")
        score += 10 if attempt == 1 else 5
        messagebox.showinfo("Correct!", "Great job!")
        next_question()
    else:
        play_sound("wrong.wav")
        if attempt == 1:
            attempt += 1
            messagebox.showwarning("Try Again", "Wrong! You get one more chance.")
            start_timer()
        else:
            messagebox.showinfo("Wrong", f"Correct answer was {correct}")
            next_question()


def next_question():
    global question_number
    question_number += 1

    if question_number < 10:
        displayProblem()
    else:
        displayResults()


def displayResults():
    clear_window()
    stop_timer()

    grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "D"

    result = tk.Label(root, text=f"Final Score: {score}/100", font=("Arial Rounded MT Bold", 22),
                      bg="#000000", fg="white")
    result.pack(pady=10)

    grade_label = tk.Label(root, text=f"Grade: {grade}", font=("Arial", 18),
                           bg="#000000", fg="lightgreen")
    grade_label.pack(pady=10)

    frame = tk.Frame(root, bg="#000000")
    frame.pack(pady=10)

    make_button(frame, "Play Again", displayMenu).pack(pady=5)
    make_button(frame, "Exit", root.destroy).pack(pady=5)


def clear_window():
    for widget in root.winfo_children():
        if widget not in (bg_label, timer_label, answer_entry):
            widget.pack_forget()


def make_button(parent, text, command):
    btn = tk.Button(parent, text=text, command=command, font=("Arial", 12, "bold"),
                    width=15, bg="#222", fg="white", bd=2, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="#404040"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#222"))
    return btn


def start_quiz(level):
    global difficulty, question_number, score
    difficulty = level
    question_number = 0
    score = 0
    displayProblem()

# ---------------- UI SETUP ----------------
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("600x500")

# Get absolute path to bg image reliably
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "..", "bg_img.jpg")  # adjust path if needed

# Load image using PIL (works with JPG)
bg_image = Image.open(bg_path)
bg_img = ImageTk.PhotoImage(bg_image)

# Create background label once
bg_label = tk.Label(root, image=bg_img)
bg_label.place(relwidth=1, relheight=1)

# Entry and timer
answer_entry = tk.Entry(root, font=("Arial", 14))
timer_label = tk.Label(root, font=("Arial Rounded MT Bold", 14), bg="#000000", fg="yellow")

timer_job = None

displayMenu()
root.mainloop()