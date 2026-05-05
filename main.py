import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import requests

# Конфигурация
MOVIES_FILE = 'data/movies.json'
TMDB_API_KEY = 'your_api_key_here'  # Замените на реальный API‑ключ TMDB


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("900x600")

        # Загрузка данных
        self.movies = self.load_movies()

        # Создание интерфейса
        self.setup_ui()
        self.update_table()

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Поля ввода
        ttk.Label(main_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.grid(row=0, column=1, pady=5, padx=(0, 10))

        ttk.Label(main_frame, text="Жанр:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.genre_entry = ttk.Entry(main_frame, width=40)
        self.genre_entry.grid(row=1, column=1, pady=5, padx=(0, 10))

        ttk.Label(main_frame, text="Год выпуска:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.year_entry = ttk.Entry(main_frame, width=40)
        self.year_entry.grid(row=2, column=1, pady=5, padx=(0, 10))

        ttk.Label(main_frame, text="Рейтинг (0–10):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.rating_entry = ttk.Entry(main_frame, width=40)
        self.rating_entry.grid(row=3, column=1, pady=5, padx=(0, 10))

        # Кнопка добавления
        add_btn = ttk.Button(main_frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky=tk.W)
        self.genre_filter = ttk.Combobox(filter_frame, values=["Все"] + self.get_genres())
        self.genre_filter.set("Все")
        self.genre_filter.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="По году:").grid(row=0, column=2, sticky=tk.W)
        self.year_filter = ttk.Entry(filter_frame, width=15)
        self.year_filter.grid(row=0, column=3, padx=5, pady=5)

        filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filters)
        filter_btn.grid(row=0, column=4, padx=10)

        clear_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтры", command=self.clear_filters)
        clear_filter_btn.grid(row=0, column=5, padx=10)

        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=6, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(control_frame, text="Сохранить в JSON", command=self.save_movies)
        save_btn.grid(row=0, column=0, padx=5)

        load_btn = ttk.Button(control_frame, text="Загрузить из JSON", command=self.load_and_refresh)
        load_btn.grid(row=0, column=1, padx=5)

        random_btn = ttk.Button(control_frame, text="Случайная рекомендация", command=self.get_random_recommendation)
        random_btn.grid(row=0, column=2, padx=5)

        # Таблица
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

    def validate_input(self, title, genre, year, rating):
        if not title.strip():
            messagebox.showerror("Ошибка", "Название не может быть пустым!")
            return False
        if not genre.strip():
            messagebox.showerror("Ошибка", "Жанр не может быть пустым!")
            return False

        try:
            year_int = int(year)
            if year_int < 1888 or year_int > 2026:
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2026.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return False

        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
                return False
            # Проверка на один знак после запятой
            if len(rating.split('.')[-1]) > 1:
                messagebox.showerror("Ошибка", "Рейтинг может иметь максимум один знак после запятой.")
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
                "title": title.strip(),
                "genre": genre.strip(),
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_movies()
            self.update_table()
            self.clear_entries()
            messagebox.showinfo("Успех", "Фильм успешно добавлен!")

    def clearentries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.
