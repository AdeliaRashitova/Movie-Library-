# Movie Library (Personal Movie Collection)
**Author:** Adelia Rashitova 
**Repository:** [https://github.com/AdeliaRashitova/Movie-Library](https://github.com/AdeliaRashitova/Movie-Library)
## Description
A desktop GUI application built with Python and Tkinter for managing a personal movie collection.  
Users can add, delete, filter, and view movies. Data is stored locally in JSON format, and input validation ensures correct year and rating values.
## Features
- Add movies with title, genre, year, rating (0–10)
- View all movies in a sortable table
- Filter by genre (case-insensitive partial match) and exact year
- Delete selected movies
- Persistent storage using JSON
- Input validation (year = integer, rating 0–10)
## Requirements
- Python 3.6+
- No external libraries required (uses only standard library: tkinter, json, os)
## How to Run
```bash
python movie_library.py
