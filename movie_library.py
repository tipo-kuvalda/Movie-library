import tkinter as tk
from tkinter import ttk, messagebox
import json

# === РАБОТА С ФАЙЛОМ ===
FILENAME = "movies.json"

def load_movies():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_movies(movies):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# === ВАЛИДАЦИЯ ===
def validate_year(year):
    return year.isdigit() and 1900 <= int(year) <= 2025

def validate_rating(rating):
    try:
        value = float(rating)
        return 0 <= value <= 10
    except ValueError:
        return False

# === ОБНОВЛЕНИЕ ТАБЛИЦЫ ===
def update_table(movies_list):
    for row in table.get_children():
        table.delete(row)
    for movie in movies_list:
        table.insert("", "end", values=(
            movie.get("title", ""),
            movie.get("genre", ""),
            movie.get("year", ""),
            movie.get("rating", "")
        ))

# === ДОБАВЛЕНИЕ ===
def add_movie():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre:
        messagebox.showwarning("Ошибка", "Название и жанр обязательны")
        return

    if not validate_year(year):
        messagebox.showwarning("Ошибка", "Год должен быть числом от 1900 до 2025")
        return

    if not validate_rating(rating):
        messagebox.showwarning("Ошибка", "Рейтинг должен быть числом от 0 до 10")
        return

    movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    }

    movies.append(movie)
    save_movies(movies)
    update_table(movies)

    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)
    messagebox.showinfo("Успех", "Фильм добавлен!")

# === ФИЛЬТРАЦИЯ ===
def apply_filter():
    genre_filter = entry_filter_genre.get().strip().lower()
    year_filter = entry_filter_year.get().strip()

    filtered = movies
    if genre_filter:
        filtered = [m for m in filtered if genre_filter in m.get("genre", "").lower()]
    if year_filter and year_filter.isdigit():
        filtered = [m for m in filtered if m.get("year") == int(year_filter)]

    update_table(filtered)

def reset_filter():
    entry_filter_genre.delete(0, tk.END)
    entry_filter_year.delete(0, tk.END)
    update_table(movies)

# === УДАЛЕНИЕ ВЫБРАННОГО ===
def delete_selected():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите фильм для удаления")
        return

    confirm = messagebox.askyesno("Удаление", "Удалить выбранный фильм?")
    if not confirm:
        return

    for item in selected:
        values = table.item(item, "values")
        for i, movie in enumerate(movies):
            if (movie["title"] == values[0] and
                movie["genre"] == values[1] and
                movie["year"] == int(values[2]) and
                movie["rating"] == float(values[3])):
                del movies[i]
                break

    save_movies(movies)
    update_table(movies)
    messagebox.showinfo("Успех", "Фильм удалён")

# === ОКНО ===
window = tk.Tk()
window.title("Movie Library")
window.geometry("800x600")

movies = load_movies()

# === ПОЛЯ ВВОДА ===
frame_input = tk.LabelFrame(window, text="Добавление фильма", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=10)

tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky="e")
entry_title = tk.Entry(frame_input, width=25)
entry_title.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Жанр:").grid(row=0, column=2, sticky="e")
entry_genre = tk.Entry(frame_input, width=20)
entry_genre.grid(row=0, column=3, padx=5)

tk.Label(frame_input, text="Год:").grid(row=0, column=4, sticky="e")
entry_year = tk.Entry(frame_input, width=10)
entry_year.grid(row=0, column=5, padx=5)

tk.Label(frame_input, text="Рейтинг (0–10):").grid(row=0, column=6, sticky="e")
entry_rating = tk.Entry(frame_input, width=8)
entry_rating.grid(row=0, column=7, padx=5)

btn_add = tk.Button(frame_input, text="Добавить", command=add_movie, bg="#4CAF50", fg="white")
btn_add.grid(row=0, column=8, padx=10)

# === ФИЛЬТР ===
frame_filter = tk.LabelFrame(window, text="Фильтрация", padx=10, pady=10)
frame_filter.pack(fill="x", padx=10, pady=5)

tk.Label(frame_filter, text="По жанру:").grid(row=0, column=0, sticky="e")
entry_filter_genre = tk.Entry(frame_filter, width=20)
entry_filter_genre.grid(row=0, column=1, padx=5)

tk.Label(frame_filter, text="По году:").grid(row=0, column=2, sticky="e")
entry_filter_year = tk.Entry(frame_filter, width=10)
entry_filter_year.grid(row=0, column=3, padx=5)

btn_apply = tk.Button(frame_filter, text="Применить фильтр", command=apply_filter, bg="#2196F3", fg="white")
btn_apply.grid(row=0, column=4, padx=10)

btn_reset = tk.Button(frame_filter, text="Сбросить", command=reset_filter, bg="#FF9800", fg="white")
btn_reset.grid(row=0, column=5, padx=10)

# === ТАБЛИЦА ===
frame_table = tk.Frame(window)
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Название", "Жанр", "Год", "Рейтинг")
table = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=140, anchor="center")

table.pack(side="left", fill="both", expand=True)

scroll = ttk.Scrollbar(frame_table, orient="vertical", command=table.yview)
scroll.pack(side="right", fill="y")
table.configure(yscrollcommand=scroll.set)

btn_delete = tk.Button(window, text="Удалить выбранный фильм", command=delete_selected, bg="#f44336", fg="white")
btn_delete.pack(pady=10)

update_table(movies)

window.mainloop()