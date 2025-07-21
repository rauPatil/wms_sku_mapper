# gui_app.py

import tkinter as tk
from tkinter import filedialog, messagebox
from inventory_updater import update_inventory
import pandas as pd
from sku_mapper import SKUMapper

def process_file(file_path, mapper):
    sales_df = pd.read_csv(file_path)
    outbound = []

    for _, row in sales_df.iterrows():
        sku = str(row["SKU"]).strip()
        qty = int(row["Quantity"])

        print(f">>> Processing: SKU={sku}, Quantity={qty}")

        if mapper.is_combo(sku):
            print(f"   Combo Detected: {sku}")
            for part_sku, part_qty in mapper.explode_combo(sku):
                msku = mapper.map_sku(part_sku)
                print(f"     -> {part_sku} → {msku} x {part_qty * qty}")
                if msku:
                    outbound.append([msku, part_qty * qty])
        else:
            msku = mapper.map_sku(sku)
            print(f"   Regular SKU: {sku} → {msku}")
            if msku:
                outbound.append([msku, qty])

    if not outbound:
        print("No outbound data generated. Check your input files.")
    else:
        outbound_df = pd.DataFrame(outbound, columns=["MSKU", "Quantity"])
        outbound_df = outbound_df.groupby("MSKU").sum().reset_index()
        outbound_df.to_csv("outbound.csv", index=False)
        print("outbound.csv created!")
    sales_df = pd.read_csv(file_path)
    outbound = []

    for _, row in sales_df.iterrows():
        sku = str(row["SKU"]).strip()
        qty = int(row["Quantity"])

        print(f">>> Processing: SKU={sku}, Quantity={qty}")

        if mapper.is_combo(sku):
            print(f"   Combo Detected: {sku}")
            for part_sku, part_qty in mapper.explode_combo(sku):
                msku = mapper.map_sku(part_sku)
                print(f"     -> {part_sku} → {msku} x {part_qty * qty}")
                if msku:
                    outbound.append([msku, part_qty * qty])
        else:
            msku = mapper.map_sku(sku)
            print(f"   Regular SKU: {sku} → {msku}")
            if msku:
                outbound.append([msku, qty])
        if not outbound:
            print("No outbound data generated. Check your input files.")
        else:
            outbound_df = pd.DataFrame(outbound, columns=["MSKU", "Quantity"])
            outbound_df = outbound_df.groupby("MSKU").sum().reset_index()
            outbound_df.to_csv("outbound.csv", index=False)
            print("outbound.csv created!")

    messagebox.showinfo("Done", "Outbound file created: outbound.csv")

    outbound_df = pd.DataFrame(outbound, columns=["MSKU", "Quantity"])
    outbound_df = outbound_df.groupby("MSKU").sum().reset_index()
    outbound_df.to_csv("outbound.csv", index=False)
    messagebox.showinfo("Done", "Outbound file created: outbound.csv")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        process_file(file_path, mapper)

# Load mappings
mapper = SKUMapper("data/msku_mapping.csv", "data/combo_sheet.csv")

# GUI
root = tk.Tk()
root.title("WMS - SKU to MSKU Mapper")


btn = tk.Button(root, text="Upload Sales CSV", command=select_file, padx=20, pady=10)
btn.pack(pady=20)


def update_inventory_from_gui():
    try:
        update_inventory("data/current_inven.csv", "outbound.csv")
        messagebox.showinfo("Success", "Inventory updated and saved to updated_inventory.csv")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update inventory:\n{e}")

inv_btn = tk.Button(root, text="Update Inventory", command=update_inventory_from_gui, padx=20, pady=10)
inv_btn.pack(pady=10)

root.mainloop()