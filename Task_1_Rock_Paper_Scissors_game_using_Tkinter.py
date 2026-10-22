from cProfile import label
from tkinter import *
import random
root=Tk()

root.title("Rock Paper Scissors")
root.geometry("400x400")  
root.config(bg="#87CEEB")

title=Label(root, text="Rock Paper Scissors",font=("Arial", 18, "bold"))
title.pack(pady=10)

computer=random.choice(["🪨 Rock", "📄 Paper", "✂️ Scissors"])

result_label = Label(root, text="", font=("Arial", 15, "bold"))
result_label.pack(anchor="w", padx=20, pady=10)
result_label.place(x=20, y=250)

def play(user_choice):
    label=Label(root,text="You chose: " + user_choice,font=("Arial",12))
    label.pack(anchor="w", padx=20, pady=20)
    label.place(x=20, y=150)

    label=Label(root,text="Computer chose: " + computer,font=("Arial",12))
    label.pack(anchor="w", padx=20, pady=20)
    label.place(x=20, y=200)
    if user_choice == computer:
        result = "It's a Tie!"
    elif (
        (user_choice == "🪨 Rock" and computer == "✂️ Scissors") or
        (user_choice == "📄 Paper" and computer == "🪨 Rock") or
        (user_choice == "✂️ Scissors" and computer == "📄 Paper")
    ):
        result = "You Win!"
    else:
        result = "Computer Wins!"

    result_label.config(text=result)

display=Label(root, text="Choose your weapon",font=("Arial", 12))
display.pack(anchor="w", padx=20)
display.place(x=20, y=50)

but_rock=Button(root, text="🪨 Rock",bg="#171616",fg="white",command=lambda: play("🪨 Rock"))
but_rock.place(x=50, y=100)

but_paper=Button(root, text="📄 Paper",bg="#CBCD4E",fg="white",command=lambda: play("📄 Paper"))
but_paper.place(x=150, y=100)

but_scissor=Button(root, text="✂️ Scissors",bg="#D14545",fg="white",command=lambda: play("✂️ Scissors") )
but_scissor.place(x=250, y=100)


root.mainloop()
