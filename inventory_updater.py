import pandas as pd

def update_inventory(inventory_path, outbound_path, output_path="current_inven.csv"):

    # Load inventory data
    inventory_df = pd.read_csv(inventory_path)
    inventory_df.columns = inventory_df.columns.str.strip()
    inventory_df["MSKU"] = inventory_df["MSKU"].astype(str).str.strip()

    if "MSKU" not in inventory_df.columns or "Opening Stock" not in inventory_df.columns:
        raise ValueError("Inventory file must have 'MSKU' and 'Opening Stock' columns")

    outbound_df = pd.read_csv(outbound_path)
    outbound_df.columns = outbound_df.columns.str.strip()
    outbound_df["MSKU"] = outbound_df["MSKU"].astype(str).str.strip()

    outbound_summary = outbound_df.groupby("MSKU")["Quantity"].sum().reset_index()

    updated_df = pd.merge(inventory_df, outbound_summary, on="MSKU", how="left")
    updated_df["Quantity"] = updated_df["Quantity"].fillna(0).astype(int)
    updated_df["Updated Stock"] = updated_df["Opening Stock"] - updated_df["Quantity"]

    # Save result
    updated_df.to_csv(output_path, index=False)
    print(f"Updated inventory saved to {output_path}")
