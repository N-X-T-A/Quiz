import tkinter as tk
from tkinter import W, messagebox
import random
import pathlib
import tomllib

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x300")
        self.content_selection()
        
    def content_selection(self):
        self.question_label = tk.Label(self.root, text="Which topic do you want to be quizzed about", padx=10, pady=10)
        self.question_label.pack()

        self.content_buttons = []
        topics = self.get_available_topics()
        for i, topic in enumerate(topics):
            button = tk.Button(self.root, text=topic, command=lambda t=topic: self.start_quiz(t),width=30,pady=10,bd=5)
            self.content_buttons.append(button)
            button.pack()

    def start_quiz(self, selected_topic):
        self.questions = self.prepare_questions(
            QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ, selected_topic=selected_topic
        )
        self.num_correct = 0
        self.current_question_index = 0
        for widget in self.root.winfo_children():
            widget.pack_forget()
        self.create_quiz_widgets()

    def get_available_topics(self):
        topic_info = tomllib.loads(QUESTIONS_PATH.read_text())
        return sorted(topic_info.keys())

    def create_quiz_widgets(self):
        self.question_label.config(text="")
        self.question_label.pack()

        self.answer_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", width=30,pady=10,bd=5, command=lambda i=i: self.check_answer(i))
            self.answer_buttons.append(button)
            button.pack()

        self.next_question()

    def prepare_questions(self, path, num_questions, selected_topic):
        topic_info = tomllib.loads(path.read_text())
        topics = topic_info.get(selected_topic, {}).get("questions", [])
        num_questions = min(num_questions, len(topics))
        return random.sample(topics, k=num_questions)

    def next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question["question"])
            answers = question["answers"] + question["alternatives"]
            random.shuffle(answers)
            for i, button in enumerate(self.answer_buttons):
                button.config(text=f"{chr(97 + i)}) {answers[i]}", state=tk.NORMAL)
            self.current_question_index += 1
        else:
            self.show_score()

    def check_answer(self, button_index):
        question = self.questions[self.current_question_index - 1]
        selected_answer = self.answer_buttons[button_index]['text'][3:]
        correct_answers = question["answers"]
        if selected_answer in correct_answers:
            self.num_correct += 1
            messagebox.showinfo("Correct!", "⭐ Correct! ⭐")
        else:
            messagebox.showinfo("Incorrect", f"The correct answer is: {', '.join(correct_answers)}")

        if self.current_question_index == len(self.questions):
            self.show_score()
        else:
            for button in self.answer_buttons:
                button.config(state=tk.DISABLED)
            self.root.after(1500, self.next_question)

    def show_score(self):
        score = f"You got {self.num_correct} correct out of {len(self.questions)} questions"
        percentage = round((self.num_correct / len(self.questions)) * 100)
        score += f"\nYour score: {percentage}%"
        messagebox.showinfo("Quiz Completed", score)
        self.root.quit()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
