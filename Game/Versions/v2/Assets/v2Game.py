import tkinter as tk
from tkinter import messagebox
import random

class GuessingGame:
    def __init__(self, master, player_name, max_tries):
        try:
            self.master = master
            self.master.title("Guessing Game")
            self.master.geometry("800x600")
            self.master.configure(bg="#F0F0F0")

            self.player_name = player_name
            self.max_tries = max_tries
            self.secret_number = random.randint(1, 20)
            self.remaining_tries = self.max_tries

            self.loop_game_var = tk.IntVar(value=1)
            self.high_scores = self.load_high_scores()

            self.create_game_frame()
        except Exception as e:
            self.show_error_popup("Initialization Error", str(e))

    def create_game_frame(self):
        try:
            self.game_frame = tk.Frame(self.master, bg="#F0F0F0")

            self.guess_label = tk.Label(self.game_frame, text="Enter your guess:", font=("Arial", 14), bg="#F0F0F0")
            self.guess_label.pack(pady=10)
            self.guess_entry = tk.Entry(self.game_frame, font=("Arial", 14))
            self.guess_entry.pack(pady=10)
            self.guess_entry.bind("<Return>", self.check_guess)

            submit_button = tk.Button(self.game_frame, text="Submit Guess", command=self.check_guess, font=("Arial", 14),
                                      bg="#4CAF50", fg="white")
            submit_button.pack(pady=10)

            self.hint_label = tk.Label(self.game_frame, text="", font=("Arial", 14), bg="#F0F0F0")
            self.hint_label.pack()

            self.blank_line_label = tk.Label(self.game_frame, text="", font=("Arial", 14), bg="#F0F0F0")
            self.blank_line_label.pack()

            self.previous_guess_label = tk.Label(self.game_frame, text="Previous guess: None", font=("Arial", 14),
                                                 bg="#F0F0F0")
            self.previous_guess_label.pack()

            self.lives_label = tk.Label(self.game_frame, text=f"Lives left: {self.remaining_tries}", font=("Arial", 14),
                                        bg="#F0F0F0")
            self.lives_label.pack()

            self.high_scores_label = tk.Label(self.game_frame, text="High Scores", font=("Arial", 14, "bold"),
                                              bg="#F0F0F0")
            self.high_scores_label.pack()

            self.show_high_scores()

            loop_game_checkbox = tk.Checkbutton(self.game_frame, text="Loop Game", variable=self.loop_game_var,
                                                font=("Arial", 14), bg="#F0F0F0")
            loop_game_checkbox.pack(pady=10)

            self.master.bind("<Destroy>", self.cleanup)

            self.game_frame.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            self.show_error_popup("Frame Creation Error", str(e))

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = [line.strip().split(":") for line in file]
                return [(name, int(score)) for name, score in high_scores]
        except (FileNotFoundError, ValueError) as e:
            self.show_error_popup("High Scores Loading Error", str(e))
            return []

    def save_high_scores(self):
        try:
            with open("high_scores.txt", "w") as file:
                for name, score in self.high_scores:
                    file.write(f"{name}:{score}\n")
        except Exception as e:
            self.show_error_popup("High Scores Saving Error", str(e))

    def show_high_scores(self):
        try:
            sorted_high_scores = sorted(self.high_scores, key=lambda x: x[1], reverse=True)

            for i, (name, score) in enumerate(sorted_high_scores[:5], start=1):
                label = tk.Label(self.game_frame, text=f"{i}. {name}: {score}", font=("Arial", 12), bg="#F0F0F0")
                label.pack()
        except Exception as e:
            self.show_error_popup("High Scores Display Error", str(e))

    def check_guess(self, event=None):
        try:
            user_guess = int(self.guess_entry.get())
        except ValueError as e:
            self.show_error_popup("Guess Entry Error", str(e))
            return

        if user_guess == self.secret_number:
            self.handle_win()
        elif user_guess < self.secret_number:
            self.hint_label.config(text="Hint: Try a higher number.")
        else:
            self.hint_label.config(text="Hint: Try a lower number.")

        self.show_previous_guess(user_guess)
        self.remaining_tries -= 1
        self.update_lives_label()

        if self.remaining_tries == 0:
            self.handle_loss()

        self.clear_entry()

    def update_lives_label(self):
        self.lives_label.config(text=f"Lives left: {self.remaining_tries}")

    def handle_loss(self):
        messagebox.showinfo("Game Over", f"{self.player_name}, you've run out of tries. The correct number was {self.secret_number}.")
        self.game_frame.destroy()

    def handle_win(self):
        try:
            messagebox.showinfo("Congratulations", f"{self.player_name}, you guessed the correct number!")

            if self.max_tries >= self.get_player_high_score():  # Fix: Use >= instead of >
                self.set_player_high_score()

                if self.loop_game_var.get():
                    self.save_high_scores()

            self.game_frame.destroy()

            if self.loop_game_var.get():
                self.__init__(self.master, self.player_name, self.max_tries)  # Fix: Pass max_tries parameter
        except Exception as e:
            self.show_error_popup("Win Handling Error", str(e))

    def show_previous_guess(self, user_guess):
        try:
            self.previous_guess_label.config(text=f"Previous guess: {user_guess}")
        except Exception as e:
            self.show_error_popup("Previous Guess Display Error", str(e))

    def clear_entry(self):
        try:
            if self.guess_entry.winfo_exists():
                self.guess_entry.delete(0, tk.END)
        except Exception as e:
            self.show_error_popup("Entry Clearing Error", str(e))

    def cleanup(self, event):
        pass

    def get_player_high_score(self):
        try:
            return next(score for name, score in self.high_scores if name == self.player_name)
        except StopIteration:
            return 0

    def set_player_high_score(self):
        try:
            for i, (name, score) in enumerate(self.high_scores):
                if name == self.player_name and self.max_tries >= score:  # Fix: Use >= instead of >
                    self.high_scores[i] = (self.player_name, self.max_tries)
                    self.show_high_scores()
                    break
            else:
                self.high_scores.append((self.player_name, self.max_tries))
                self.show_high_scores()
        except Exception as e:
            self.show_error_popup("Setting Player High Score Error", str(e))

    def show_error_popup(self, title, message):
        try:
            error_frame = tk.Toplevel(self.master)
            error_frame.title("Error")
            error_frame.geometry("400x300")
            error_frame.configure(bg="#F0F0F0")

            error_label_1 = tk.Label(error_frame, text="An error has occurred! Please contact a game admin!",
                                     font=("Arial", 16, "bold"), bg="#F0F0F0")
            error_label_1.pack(pady=10)

            error_label_2 = tk.Label(error_frame, text=f"Error Code: {random.randint(1, 400)}",
                                     font=("Arial", 14), bg="#F0F0F0")
            error_label_2.pack(pady=10)

            details_label = tk.Label(error_frame, text=f"Details: {title}\n{message}", font=("Arial", 12), bg="#F0F0F0")
            details_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

class NameEntryFrame:
    def __init__(self, master):
        try:
            self.master = master
            self.master.title("Enter Your Name")
            self.master.geometry("800x600")
            self.master.configure(bg="#F0F0F0")

            self.name_frame = tk.Frame(self.master, bg="#F0F0F0")

            self.name_label = tk.Label(self.name_frame, text="Enter your name:", font=("Arial", 14), bg="#F0F0F0")
            self.name_label.pack(pady=10)
            self.name_entry = tk.Entry(self.name_frame, font=("Arial", 14))
            self.name_entry.pack(pady=10)

            submit_name_button = tk.Button(self.name_frame, text="Submit Name", command=self.submit_name,
                                           font=("Arial", 14), bg="#4CAF50", fg="white")
            submit_name_button.pack(pady=10)

            self.name_frame.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            self.show_error_popup("Initialization Error", str(e))

    def submit_name(self):
        try:
            player_name = self.name_entry.get()
            if player_name:
                self.name_frame.destroy()
                game = GuessingGame(self.master, player_name, 5)  # Pass max_tries parameter
        except Exception as e:
            self.show_error_popup("Submit Name Error", str(e))

    def show_error_popup(self, title, message):
        try:
            error_frame = tk.Toplevel(self.master)
            error_frame.title("Error")
            error_frame.geometry("400x300")
            error_frame.configure(bg="#F0F0F0")

            error_label_1 = tk.Label(error_frame, text="An error has occurred! Please contact a game admin!",
                                     font=("Arial", 16, "bold"), bg="#F0F0F0")
            error_label_1.pack(pady=10)

            error_label_2 = tk.Label(error_frame, text=f"Error Code: {random.randint(1, 400)}",
                                     font=("Arial", 14), bg="#F0F0F0")
            error_label_2.pack(pady=10)

            details_label = tk.Label(error_frame, text=f"Details: {title}\n{message}", font=("Arial", 12), bg="#F0F0F0")
            details_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    name_entry = NameEntryFrame(root)
    root.mainloop()

