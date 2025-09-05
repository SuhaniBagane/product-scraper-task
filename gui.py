import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import random

# Load product data
def load_products():
    with open("products.json", "r") as f:
        return json.load(f)

# Save table data to CSV
def export_to_csv(data):
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file:
        with open(file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "price", "rating", "category"])
            writer.writeheader()
            writer.writerows(data)
        messagebox.showinfo("Export Success", f"Data saved to {file}")

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Product Explorer 🛍️")
        self.root.geometry("950x600")
        self.root.config(bg="#f4f4f9")

        self.products = load_products()
        self.filtered = self.products.copy()

        # --- Search Bar ---
        search_frame = tk.Frame(root, bg="#f4f4f9")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="🔎 Search:", bg="#f4f4f9", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.apply_filters, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

        # --- Category Filter ---
        tk.Label(search_frame, text="📂 Category:", bg="#f4f4f9", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar()
        categories = ["All"] + sorted(set(p["category"] for p in self.products))
        self.category_menu = ttk.Combobox(search_frame, textvariable=self.category_var, values=categories, state="readonly")
        self.category_menu.current(0)
        self.category_menu.pack(side=tk.LEFT, padx=5)

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg="#f4f4f9")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Sort by Price ↑", command=lambda: self.sort_products("price", True)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sort by Price ↓", command=lambda: self.sort_products("price", False)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sort by Rating ↑", command=lambda: self.sort_products("rating", True)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sort by Rating ↓", command=lambda: self.sort_products("rating", False)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export to CSV 📄", command=lambda: export_to_csv(self.filtered)).pack(side=tk.LEFT, padx=5)

        # --- Product Table ---
        self.tree = ttk.Treeview(root, columns=("Name", "Price", "Rating", "Category"), show="headings", height=15)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        for col in ("Name", "Price", "Rating", "Category"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")

        self.populate_table(self.filtered)

        # --- Robot Assistant ---
        self.robot_button = tk.Button(root, text="🤖 Ask Robo-Assistant", command=self.show_robot_message, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        self.robot_button.pack(pady=10)

        # --- Random Deal of the Day ---
        self.show_deal_of_day()

    def populate_table(self, data):
        self.tree.delete(*self.tree.get_children())
        for p in data:
            self.tree.insert("", tk.END, values=(p["name"], f"₹{p['price']}", p["rating"], p["category"]))

    def apply_filters(self):
        search_term = self.search_entry.get().lower()
        category = self.category_var.get()
        self.filtered = [p for p in self.products if (search_term in p["name"].lower()) and (category == "All" or p["category"] == category)]
        self.populate_table(self.filtered)

    def sort_products(self, key, ascending=True):
        self.filtered.sort(key=lambda x: x[key], reverse=not ascending)
        self.populate_table(self.filtered)

    def show_robot_message(self):
        messages = [
            "💡 Tip: Always compare ratings before buying!",
            "🎉 Fun Fact: Online shopping grows 20% every year!",
            "🛒 Robo says: Don’t forget to check today’s deals!",
            "🤖 I can help you filter faster. Try categories!"
        ]
        messagebox.showinfo("Robo-Assistant", random.choice(messages))

    def show_deal_of_day(self):
        deal = random.choice(self.products)
        messagebox.showinfo("🎉 Deal of the Day 🎉", f"🔥 {deal['name']} just at ₹{deal['price']} (Rating: {deal['rating']}⭐)")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()
