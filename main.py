import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
DATA_FILE = "movies.json"
class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Personal Movie Collection")
        self.root.geometry("800x500")
        self.movies = []
        self.load_data()
        # Input fields
        tk.Label(root, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(root, text="Genre:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(root, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(root, text="Year:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = tk.Entry(root, width=30)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(root, text="Rating (0-10):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.rating_entry = tk.Entry(root, width=20)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)
        add_btn = tk.Button(root, text="Add Movie", command=self.add_movie, bg="lightblue")
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        # Filter frame
        filter_frame = tk.LabelFrame(root, text="Filters", padx=5, pady=5)
        filter_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
        tk.Label(filter_frame, text="Filter by Genre:").grid(row=0, column=0, padx=5)
        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5)
        self.genre_filter.bind("<KeyRelease>", self.apply_filters)
        tk.Label(filter_frame, text="Filter by Year:").grid(row=0, column=2, padx=5)
        self.year_filter = tk.Entry(filter_frame, width=20)
        self.year_filter.grid(row=0, column=3, padx=5)
        self.year_filter.bind("<KeyRelease>", self.apply_filters)
        clear_filter_btn = tk.Button(filter_frame, text="Clear Filters", command=self.clear_filters)
        clear_filter_btn.grid(row=0, column=4, padx=10)
        # Table (Treeview)
        self.tree = ttk.Treeview(root, columns=("Title", "Genre", "Year", "Rating"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Rating", text="Rating")
        self.tree.column("Title", width=250)
        self.tree.column("Genre", width=150)
        self.tree.column("Year", width=100)
        self.tree.column("Rating", width=100)
        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        # Delete button
        del_btn = tk.Button(root, text="Delete Selected", command=self.delete_movie, bg="lightcoral")
        del_btn.grid(row=5, column=0, columnspan=4, pady=5)
        # Configure grid weights
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(3, weight=1)
        self.update_table()
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Error", "Year must be a number")
            return
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 0 and 10")
            return
        self.movi
        es.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })
        self.save_data()
        self.clear_inputs()
        self.update_table()
        messagebox.showinfo("Success", f"Movie '{title}' added!")
    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No movie selected")
            return
        # Get movie title from selected row
        item = self.tree.item(selected[0])
        title = item['values'][0]
        # Find and remove
        for movie in self.movies[:]:
            if movie["title"] == title:
                self.movies.remove(movie)
                break
        self.save_data()
        self.update_table()
        messagebox.showinfo("Deleted", f"Movie '{title}' removed")
    def apply_filters(self, event=None):
        self.update_table()
    def clear_filters(self):
        self.genre_filter.delete(0, tk.END)
        self.year_filter.delete(0, tk.END)
        self.update_table()
    def update_table(self):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)
        genre_filter = self.genre_filter.get().strip().lower()
        year_filter = self.year_filter.get().strip()
        for movie in self.movies:
            # Filter by genre
            if genre_filter and genre_filter not in movie["genre"].lower():
                continue
            # Filter by year (exact match)
            if year_filter:
                try:
                    if movie["year"] != int(year_filter):
                        continue
                except ValueError:
                    pass  # if year_filter is not a number, skip filter
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))
    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except:
                self.movies = []
if __name__ == "__main__":
    root = tk.Tk
()
    app = MovieLibrary(root)
    root.mainloop()
