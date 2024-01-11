import tkinter as tk
from tkinter import messagebox
import random
import os

class GuessingGame:
    def __init__(self, master, player_name, max_tries=5):
        self.master = master
        self.master.title("Guessing Game")
        self.master.geometry("800x600")
        self.master.configure(bg="#F0F0F0")

        self.player_name = player_name
        self.max_tries = max_tries
        self.secret_number = random.randint(1, 20)

        self.loop_game_var = tk.IntVar(value=1)
        self.high_scores = self.load_high_scores()

        self.create_game_frame()

    def create_game_frame(self):
        self.game_frame = tk.Frame(self.master, bg="#F0F0F0")

        # Entry Section
        entry_frame = tk.Frame(self.game_frame, bg="#F0F0F0")
        entry_frame.pack(pady=20)

        tk.Label(entry_frame, text="Enter your guess:", font=("Arial", 14), bg="#F0F0F0").pack(side=tk.LEFT)
        self.guess_entry = tk.Entry(entry_frame, font=("Arial", 14))
        self.guess_entry.pack(side=tk.LEFT)
        self.guess_entry.bind("<Return>", self.check_guess)

        tk.Button(entry_frame, text="Submit Guess", command=self.check_guess, font=("Arial", 14), bg="#4CAF50", fg="white").pack(side=tk.LEFT)

        # Hint Section
        self.hint_label = tk.Label(self.game_frame, text="", font=("Arial", 14), bg="#F0F0F0")
        self.hint_label.pack()

        # Previous Guess Section
        self.previous_guess_label = tk.Label(self.game_frame, text="Previous guess: None", font=("Arial", 14), bg="#F0F0F0")
        self.previous_guess_label.pack()

        # Lives Section
        self.lives_label = tk.Label(self.game_frame, text=f"Lives left: {self.max_tries}", font=("Arial", 14), bg="#F0F0F0")
        self.lives_label.pack()

        # High Scores Section
        self.high_scores_label = tk.Label(self.game_frame, text="High Scores", font=("Arial", 14, "bold"), bg="#F0F0F0")
        self.high_scores_label.pack()

        self.show_high_scores()

        # Loop Game Checkbox
        loop_game_checkbox = tk.Checkbutton(self.game_frame, text="Loop Game", variable=self.loop_game_var, font=("Arial", 14), bg="#F0F0F0")
        loop_game_checkbox.pack(pady=10)

        # Reset Scores Button
        tk.Button(self.game_frame, text="Reset Scores", command=self.reset_scores, font=("Arial", 14), bg="#FF6347", fg="white").pack(pady=10)

        self.master.bind("<Destroy>", self.cleanup)

        self.game_frame.pack(fill=tk.BOTH, expand=True)

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = [line.strip().split(":") for line in file]
                return [(name, int(score)) for name, score in high_scores]
        except FileNotFoundError:
            return []  # Return an empty list if the file is not found
        except ValueError as e:
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
        sorted_high_scores = sorted(self.high_scores, key=lambda x: x[1], reverse=True)

        for i, (name, score) in enumerate(sorted_high_scores[:5], start=1):
            label = tk.Label(self.game_frame, text=f"{i}. {name}: {score}", font=("Arial", 12), bg="#F0F0F0")
            label.pack()

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
        self.clear_entry()

    def handle_win(self):
        messagebox.showinfo("Congratulations", f"{self.player_name}, you guessed the correct number!")

        if self.max_tries > self.get_player_high_score():
            self.set_player_high_score()

            if self.loop_game_var.get():
                self.save_high_scores()

        self.game_frame.destroy()

        if self.loop_game_var.get():
            self.__init__(self.master, self.player_name)

    def show_previous_guess(self, user_guess):
        self.previous_guess_label.config(text=f"Previous guess: {user_guess}")

    def clear_entry(self):
        self.guess_entry.delete(0, tk.END)

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
                if name == self.player_name and self.max_tries > score:
                    self.high_scores[i] = (self.player_name, self.max_tries)
                    self.show_high_scores()
                    break
            else:
                self.high_scores.append((self.player_name, self.max_tries))
                self.show_high_scores()
        except Exception as e:
            self.show_error_popup("Setting Player High Score Error", str(e))

    def reset_scores(self):
        try:
            os.remove("high_scores.txt")
            messagebox.showinfo("Scores Reset", "High scores have been reset.")
            self.high_scores = []  # Clear the current high scores
            self.show_high_scores()  # Reload and display the updated high scores
        except FileNotFoundError:
            messagebox.showinfo("No Scores to Reset", "No high scores found.")
        except Exception as e:
            self.show_error_popup("Scores Reset Error", str(e))

    def show_error_popup(self, title, message):
        error_frame = tk.Toplevel(self.master)
        error_frame.title("Error")
        error_frame.geometry("400x300")
        error_frame.configure(bg="#F0F0F0")

        tk.Label(error_frame, text="An error has occurred! Please contact a game admin!", font=("Arial", 16, "bold"), bg="#F0F0F0").pack(pady=10)
        tk.Label(error_frame, text=f"Details: {title}\n{message}", font=("Arial", 12), bg="#F0F0F0").pack(pady=10)


class NameEntryFrame:
    def __init__(self, master):
        self.master = master
        self.master.title("Enter Your Name")
        self.master.geometry("800x600")
        self.master.configure(bg="#F0F0F0")

        self.name_frame = tk.Frame(self.master, bg="#F0F0F0")

        tk.Label(self.name_frame, text="Enter your name:", font=("Arial", 14), bg="#F0F0F0").pack(pady=10)
        self.name_entry = tk.Entry(self.name_frame, font=("Arial", 14))
        self.name_entry.pack(pady=10)

        tk.Button(self.name_frame, text="Submit Name", command=self.submit_name, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)

        self.name_frame.pack(fill=tk.BOTH, expand=True)

    def submit_name(self):
        player_name = self.name_entry.get()
        if player_name:
            self.name_frame.destroy()
            game = GuessingGame(self.master, player_name)


if __name__ == "__main__":
    root = tk.Tk()
    name_entry = NameEntryFrame(root)
    root.mainloop()
