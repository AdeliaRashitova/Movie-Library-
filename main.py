import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.load_movies()

        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Рейтинг (0–10)").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить фильм", command=self.add_movie).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру").grid(row=5, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(self.root)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по году").grid(row=6, column=0, padx=5, pady=5)
        self.filter_year = tk.Entry(self.root)
        self.filter_year.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(
            row=7, column=0, columnspan=2, pady=10
        )

        # Таблица
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def validate_input(self, title, genre, year, rating):
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр обязательны!")
            return False
        try:
            year = int(year)
            if year < 1800 or year > 2026:
                messagebox.showerror("Ошибка", "Год должен быть от 1800 до 2026!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return False
        try:
            rating = float(rating)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False
        return True

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        if self.validate_input(title, genre, year, rating):
            movie = {
                "title": title,
                "genre": genre,
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_movies()
            self.update_table()
            self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def update_table(self, filtered_movies=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        movies_to_show = filtered_movies if filtered_movies else self.movies
        for movie in movies_to_show:
            self.tree.insert("", "end", values=(
                movie["title"], movie["genre"], movie["year"], movie["rating"]
            ))

    def apply_filters(self):
        genre_filter = self.filter_genre.get().lower()
        year_filter = self.filter_year.get()

        filtered = self.movies
        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]
        if year_filter:
            try:
                year_filter = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтра должен быть числом!")
                return
        self.update_table(filtered)

    def load_movies(self):
        try:
            if os.path.exists("movies.json"):
                with open("movies.json", "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.movies = []

    def save_movies(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
