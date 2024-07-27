import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

rolls = [
    {"size": 1524, "price": 830},
    {"size": 1066, "price": 575},
    {"size": 914, "price": 500},
    {"size": 750, "price": 450},
    {"size": 650, "price": 400},
    {"size": 450, "price": 280},
]

def get_page_sizes(pdf_path):
    page_sizes = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            media_box = page.mediabox
            width = media_box.width
            height = media_box.height
            # Convert dimensions to millimeters (1 point = 0.352778 mm)
            width_mm = width * 0.352778
            height_mm = height * 0.352778
            page_sizes.append((round(width_mm, 2), round(height_mm, 2)))
    return page_sizes

def find_closest_higher_roll(height):
    higher_rolls = [roll for roll in rolls if roll["size"] >= height]
    if not higher_rolls:
        return None
    return min(higher_rolls, key=lambda roll: roll["size"])

def calculate_cost(dimension):
    first, second = map(float, dimension.split('x'))
    height = max(first, second)
    lower_dimension = min(first, second)

    if dimension == '841x1180' or dimension == '1180x841':
        lower_dimension_decimal = 1.18
        total_cost = lower_dimension_decimal * 500
        roll_size = 914
        roll_price = 500
    else:
        closest_roll = find_closest_higher_roll(height)
        if closest_roll:
            lower_dimension_decimal = lower_dimension / 1000
            total_cost = lower_dimension_decimal * closest_roll["price"]
            roll_size = closest_roll["size"]
            roll_price = closest_roll["price"]
        else:
            roll_size = None
            total_cost = 0
            roll_price = 0

    return roll_size, roll_price, lower_dimension_decimal, total_cost

def open_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        try:
            page_sizes = get_page_sizes(pdf_path)
            total_costs = {}

            for size in page_sizes:
                dimension = f"{size[0]}x{size[1]}"
                roll_size, roll_price, lower_dimension_decimal, cost = calculate_cost(dimension)
                if roll_size:
                    if roll_size not in total_costs:
                        total_costs[roll_size] = {"cost": 0, "total_mm": 0}
                    total_costs[roll_size]["cost"] += cost
                    total_costs[roll_size]["total_mm"] += lower_dimension_decimal

            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Total Costs:\n")
            for roll_size, data in total_costs.items():
                total_mm = data["total_mm"]
                total_cost = data["cost"]
                roll = next(roll for roll in rolls if roll["size"] == roll_size)
                output_text.insert(tk.END, f"{total_mm:.2f} x {roll['price']} ({roll_size}mm) = {total_cost:.2f} din\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("PDF Page Size and Cost Calculator")

# Create and place the widgets
open_button = tk.Button(root, text="Open PDF", command=open_pdf)
open_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
output_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()