import tkinter as tk
import random

root = tk.Tk()


class QuizApp:
    def __init__(self, master):
        self.difficulty_var = None
        self.master = master
        self.master.title("Arithmetic Quiz")
        self.score = 0
        self.current_question = 0
        self.max_questions = 10
        self.attempts = 0  # It tracks the number of attempts for the current question

        # Selecting the font and displaying the question using a Display
        self.question_display = tk.Label(master, text="", font=("Arial", 14))
        self.question_display.pack()

        self.answer_entry = tk.Entry(master)  # Allowing users to answer using A Label
        self.answer_entry.pack()

        # Button to Submit User's Answer
        self.submit_button = tk.Button(master, text="Submit", command=self.check_answer)
        self.submit_button.pack()

        self.result_display = tk.Label(master, text="")
        self.result_display.pack()

        self.play_again_button = tk.Button(master, text="Play Again", command=self.restart_quiz)
        self.play_again_button.pack_forget()  # In the beginning it hides this button.

        self.display_menu()  # Show the menu for difficulty

    def display_menu(self):
        self.score = 0
        self.current_question = 0
        self.attempts = 0
        # Displaying the three levels of Difficulty in the menu
        self.question_display.config(text="Select Difficulty Level: ", font=("Arial", 18, "bold"))
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.play_again_button.pack_forget()

        self.difficulty_var = tk.IntVar()
        # Radio Buttons for Difficulty Level
        self.easy_button = tk.Radiobutton(self.master, text="Easy", variable=self.difficulty_var, value=1,
                                          command=self.start_quiz,font=("Arial", 14), width=15, height=2)
        self.moderate_button = tk.Radiobutton(self.master, text="Moderate", variable=self.difficulty_var, value=2,
                                              command=self.start_quiz, font=("Arial", 14), width=15, height=2)
        self.advanced_button = tk.Radiobutton(self.master, text="Advanced", variable=self.difficulty_var, value=3,
                                              command=self.start_quiz, font=("Arial", 14), width=15, height=2)
        # Packing The radio buttons
        self.easy_button.pack()
        self.moderate_button.pack()
        self.advanced_button.pack()

    def start_quiz(self):
        # Starting the quiz based on difficulty
        self.difficulty = self.difficulty_var.get()
        self.easy_button.pack_forget()
        self.moderate_button.pack_forget()
        self.advanced_button.pack_forget()
        self.next_question()  # First Question to be loaded

    def next_question(self):
        if self.current_question < self.max_questions:
            self.num1, self.num2 = self.random_int()
            self.operator = self.decide_operation()
            self.display_problem()
            self.attempts = 0  # Reset attempts for the new question
        else:
            self.display_results()

    def random_int(self):
        if self.difficulty == 1:
            return random.randint(0, 9), random.randint(0, 9)  # if easy generates single digit
        elif self.difficulty == 2:
            return random.randint(10, 99), random.randint(10, 99)  # if moderate generates 2 digit
        else:
            return random.randint(1000, 9999), random.randint(1000, 9999)  # if advanced generate 3 digit

    def decide_operation(self):
        # function randomly chooses between addition and subtraction
        return random.choice(['+', '-'])

    def display_problem(self):
        # displaying the problem using random arithmetic operation chosen
        self.question_display.config(text=f"{self.num1} {self.operator} {self.num2} =",font=("Arial", 18, "bold"))
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.pack()
        self.submit_button.pack()

    def check_answer(self):
        # checks answer's correction
        answer = self.answer_entry.get()
        if not answer.lstrip('-').isdigit():
            self.result_display.config(text="Please enter a valid number.", font=("Arial", 18, "bold"))
            return

        answer = int(answer)
        correct_answer = eval(f"{self.num1} {self.operator} {self.num2}")

        self.attempts += 1  # Increment the attempt count

        if self.attempts == 1:  # First attempt
            if self.is_correct(answer, correct_answer):
                self.current_question += 1
                self.next_question()
            else:
                self.result_display.config(text="Wrong! Try again.",font=("Arial", 18, "bold"))
                self.answer_entry.delete(0, tk.END)
        elif self.attempts == 2:  # Second attempt
            if self.is_correct(answer, correct_answer):
                self.current_question += 1
                self.next_question()  # moves to the next problem
            else:
                self.result_display.config(text=f"Wrong! The correct answer was {correct_answer}.",font=("Arial", 18, "bold"))
                self.current_question += 1
                self.next_question()  # next question

    def is_correct(self, user_answer, correct_answer):
        # increments score on correct answers
        if user_answer == correct_answer:
            if self.attempts == 1:
                self.score += 10  # First attempt
                self.result_display.config(text="Correct! +10 points.",font=("Arial", 18, "bold"))  # first try
            else:
                self.score += 5  # Second attempt
                self.result_display.config(text="Correct! +5 points.",font=("Arial", 18, "bold"))  # second try
            return True
        return False

    def display_results(self):
        # final results after addition of all correct answers
        self.question_display.config(text="")
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.result_display.config(text=f"Quiz Finished! Your score: {self.score} / 100\n{self.rank_user()}",font=("Arial", 18, "bold"))
        self.play_again_button.pack()

    def rank_user(self):
        # gives a rank based on ur final score
        if self.score >= 90:
            return "Grade: A+"
        elif self.score >= 80:
            return "Grade: A"
        elif self.score >= 70:
            return "Grade: B"
        elif self.score >= 60:
            return "Grade: C"
        elif self.score >= 50:
            return "Grade: D"
        else:
            return "Grade: F"

    def restart_quiz(self):
        # displaying a button to ask if they want to play again
        self.play_again_button.pack_forget()
        self.result_display.config(text="")  # Hide the final score and rank
        self.display_menu()


if __name__ == "__main__":
    app = QuizApp(root)
    root.mainloop()
