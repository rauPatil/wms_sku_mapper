from baserow_client import post_to_baserow
from sku_mapper import SKUMapper
from inventory_updater import update_inventory
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="WMS Dashboard", layout="wide")

st.title("📦 Warehouse Management Dashboard")

# Sidebar for page selection
page = st.sidebar.radio("Go to", ["Upload Sales File", "Outbound Report", "Inventory", "Charts"])

# Load files
outbound_path = "data/outbound.csv"
inventory_path = "data/updated_inventory.csv"

@st.cache_data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

outbound_df = load_data(outbound_path)
inventory_df = load_data(inventory_path)


if page == "Upload Sales File":
    st.subheader("📤 Upload Sales File")
    uploaded_file = st.file_uploader("Choose a sales CSV file", type="csv")

    if uploaded_file is not None:
        df_uploaded = pd.read_csv(uploaded_file)
        st.write("Uploaded Sales Data Preview")
        st.dataframe(df_uploaded)

        os.makedirs("data", exist_ok=True)
        df_uploaded.to_csv("data/temp_sales.csv", index=False)

        # Automatically run mapping and inventory update after saving sales file
        try:
            mapper = SKUMapper("data/msku_mapping.csv", "data/combo_sheet.csv")
            sales_df = pd.read_csv("data/temp_sales.csv")
            outbound = []

            for _, row in sales_df.iterrows():
                sku = str(row["SKU"]).strip()
                qty = int(row["Quantity"])
                if mapper.is_combo(sku):
                    for part_sku, part_qty in mapper.explode_combo(sku):
                        msku = mapper.map_sku(part_sku)
                        if msku:
                            outbound.append([msku, part_qty * qty])
                else:
                    msku = mapper.map_sku(sku)
                    if msku:
                        outbound.append([msku, qty])

            outbound_df = pd.DataFrame(outbound, columns=["MSKU", "Quantity"])
            outbound_df = outbound_df.groupby("MSKU").sum().reset_index()
            outbound_df.to_csv("data/outbound.csv", index=False)

            # Post outbound data to Baserow
            from baserow_client import post_to_baserow
            for _, row in outbound_df.iterrows():
                post_to_baserow(table_id="615322", data={"SKU": row["MSKU"], "Qty": int(row["Quantity"])})

            # Update inventory
            update_inventory("data/current_inven.csv", "data/outbound.csv", "data/updated_inventory.csv")
            st.success("Outbound and Inventory updated successfully!")

        except Exception as e:
            st.error(f"Failed to process sales file: {e}")

# Page: Outbound Report
elif page == "Outbound Report":
    st.header("Outbound MSKUs")
    if outbound_df.empty:
        st.warning("No outbound data found.")
    else:
        st.dataframe(outbound_df)

# Page: Inventory
elif page == "Inventory":
    st.header("📦Current Inventory")
    if inventory_df.empty:
        st.warning("No inventory data found.")
    else:
        st.dataframe(inventory_df)

# Page: Charts
elif page == "Charts":
    st.header("📊 Inventory & Sales Charts")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 MSKUs Sold")
        if not outbound_df.empty:
            top_sold = outbound_df.groupby("MSKU")["Quantity"].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_sold)

    with col2:
        st.subheader("Remaining Stock")
        if not inventory_df.empty:
            top_stock = inventory_df.set_index("MSKU")["Updated Stock"].sort_values(ascending=False).head(10)
            st.bar_chart(top_stock)