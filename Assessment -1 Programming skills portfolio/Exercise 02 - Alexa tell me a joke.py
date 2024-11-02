import tkinter as tk
import random

root = tk.Tk()


class JokeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Random Joke Teller")

        # jokes to be loaded from file
        self.jokes = self.load_jokes()

        # to display the joke setup adding Label
        self.setup_label = tk.Label(master, text="", wraplength=300, font=("Arial", 14, "bold"))
        self.setup_label.pack(pady=20)

        # to display the punchline adding a label
        self.punchline_label = tk.Label(master, text="", wraplength=300, font=("Arial", 12, "bold"))
        self.punchline_label.pack(pady=10)

        # button to display a random joke setup
        self.get_joke_button = tk.Button(master, text="TELL ME A JOKE", command=self.show_joke, width=20, height=2,
                                         font=("Arial", 12, "bold"))
        self.get_joke_button.pack(pady=5)

        # using a button showing the punchline
        self.show_punchline_button = tk.Button(master, text="SHOW PUNCHLINE", command=self.show_punchline, width=20,
                                               height=2, font=("Arial", 12, "bold"))

        # button to close the application
        self.quit_button = tk.Button(master, text="QUIT", command=master.quit, width=20, height=2, font=("Arial", 12, "bold"))
        self.quit_button.pack(pady=5)

        # storing the current joke in a variable (setup and punchline)
        self.current_joke = None

    def load_jokes(self):

        # Loading jokes from a text file

        try:
            with open("randomJokes.txt", "r") as file:
                # Read each line, split into joke setup and punchline, and return only valid pairs
                jokes = [line.strip().split('?') for line in file]
                return [joke for joke in jokes if len(joke) == 2]
        except FileNotFoundError:
            # error message is displayed if the file is not found
            self.setup_label.config(text="Joke file not found!")
            return []

    def show_joke(self):

        # Select a random joke and display its first part

        # Choosing a random joke
        self.current_joke = random.choice(self.jokes)

        # Displaying the first part of the joke
        self.setup_label.config(text=self.current_joke[0])

        # Clearing any punchline that is displayed
        self.punchline_label.config(text="")

        # Showing the 'Show Punchline' button and Hiding the TELL ME A JOKE Button
        self.show_punchline_button.pack(pady=5)
        self.get_joke_button.pack_forget()

    def show_punchline(self):

        # Displaying the punchline of the current joke

        if self.current_joke:
            # the punchline of the current joke
            self.punchline_label.config(text=self.current_joke[1])

            # Hide the 'Show Punchline' button and display the 'Tell me a Joke' button
            self.show_punchline_button.pack_forget()
            self.get_joke_button.pack(pady=5)


if __name__ == "__main__":
    # Creates the main window and run the JokeApp
    app = JokeApp(root)
    root.mainloop()
