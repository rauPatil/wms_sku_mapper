import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from sku_mapper import SKUMapping
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_mapping_file():
    filepath = filedialog.askopenfilename(title="Select Master Mapping CSV")
    mapping_path_var.set(filepath)

def load_sales_file():
    filepath = filedialog.askopenfilename(title="Select Sales Data CSV")
    sales_path_var.set(filepath)

def process_files():
    try:
        sku_mapper = SKUMapping(mapping_path_var.get())
        sales_df = pd.read_csv(sales_path_var.get())

        if 'SKU' not in sales_df.columns:
            messagebox.showerror("Error", "Sales CSV must contain a 'SKU' column.")
            return

        sales_df['MSKU'] = sales_df['SKU'].apply(sku_mapper.map_sku)
        output_path = os.path.join(OUTPUT_DIR, "cleaned_sales.csv")
        sales_df.to_csv(output_path, index=False)

        with open("mapping_log.txt", "w") as f:
            for line in sku_mapper.get_log():
                f.write(line + "\n")

        messagebox.showinfo("Success", f"Cleaned data saved to:\n{output_path}\n\nLog written to mapping_log.txt")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("SKU to MSKU Mapper")
root.geometry("500x300")

mapping_path_var = tk.StringVar()
sales_path_var = tk.StringVar()

tk.Label(root, text="Step 1: Select Master Mapping CSV").pack(pady=5)
tk.Entry(root, textvariable=mapping_path_var, width=60).pack()
tk.Button(root, text="Browse", command=load_mapping_file).pack()

tk.Label(root, text="Step 2: Select Sales Data CSV").pack(pady=5)
tk.Entry(root, textvariable=sales_path_var, width=60).pack()
tk.Button(root, text="Browse", command=load_sales_file).pack()

tk.Label(root, text="Step 3: Process Mapping").pack(pady=5)
tk.Button(root, text="Map SKUs → MSKUs", command=process_files, bg="green", fg="white").pack(pady=10)

root.mainloop()