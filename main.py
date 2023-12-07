import tkinter as tk
from tkinter import messagebox
import requests
import html

def get_trivia_questions():
    url = "https://opentdb.com/api.php?amount=10&type=boolean"
    response = requests.get(url)
    data = response.json()
    return data["results"]

class TriviaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Trivia Question App")

        self.questions = get_trivia_questions()
        self.current_question_index = 0

        self.question_text = tk.StringVar()
        self.question_text.set(html.unescape(self.questions[self.current_question_index]["question"]))

        self.question_label = tk.Label(master, textvariable=self.question_text, wraplength=300, justify=tk.LEFT)
        self.question_label.pack(pady=(50, 20))

        self.true_button = tk.Button(master, text="True", command=self.check_answer_true)
        self.true_button.pack(side=tk.LEFT, padx=(40, 5))

        self.false_button = tk.Button(master, text="False", command=self.check_answer_false)
        self.false_button.pack(side=tk.RIGHT, padx=(5, 40))

    def check_answer_true(self):
        self.check_answer(True)

    def check_answer_false(self):
        self.check_answer(False)

    def check_answer(self, user_answer):
        correct_answer = html.unescape(self.questions[self.current_question_index]["correct_answer"])
        if user_answer == (correct_answer.lower() == "true"):
            messagebox.showinfo("Correct", "You got it right!")
        else:
            messagebox.showinfo("Incorrect", f"Sorry, the correct answer is {correct_answer}.")

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.update_question()
        else:
            self.show_game_over()

    def update_question(self):
        self.question_text.set(html.unescape(self.questions[self.current_question_index]["question"]))

    def show_game_over(self):
        result = messagebox.askyesno("Game Over", "You've completed all the questions!\nDo you want to play again?")
        if result:
            self.reset_game()
        else:
            self.master.destroy()

    def reset_game(self):
        self.current_question_index = 0
        self.update_question()

def main():
    root = tk.Tk()
    app = TriviaApp(root)
    root.geometry("400x250")
    root.mainloop()

if __name__ == "__main__":
    main()
