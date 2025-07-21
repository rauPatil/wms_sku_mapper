# 📦 Warehouse Management System (WMS) MVP

A Python-based MVP for automating SKU-to-MSKU mapping, outbound generation, inventory subtraction, and database integration with Baserow — all wrapped in a user-friendly Streamlit web interface.

---

## 🚀 Features

- ✅ Drag-and-drop upload of marketplace sales data (CSV)
- 🔄 SKU-to-MSKU mapping with combo support
- 📤 Auto-generation of outbound report (`outbound.csv`)
- 🧮 Live inventory update (`updated_inventory.csv`)
- 🌐 Integration with [Baserow.io](https://baserow.io) — inventory + outbound synced
- 📊 Dashboards: Top MSKUs sold and current stock
- ❌ AI Assistant (PandasAI) removed due to compatibility issues

---

## 🧠 Tech Stack

- Python 3.11
- Streamlit
- Pandas
- Baserow API
- dotenv (for secure credentials)

---

## 📁 Folder Structure

wms_sku_mapper/
├── data/                    # CSVs (input/output)
├── baserow_client.py        # Baserow uploader
├── sku_mapper.py            # SKU-to-MSKU logic
├── inventory_updater.py     # Subtract outbound from current inventory
├── streamlit_app.py         # Main GUI app
└── .env                     # Baserow API credentials
# 📦 Warehouse Management System (WMS) MVP

A Python-based MVP for automating SKU-to-MSKU mapping, outbound generation, inventory subtraction, and database integration with Baserow — all wrapped in a user-friendly Streamlit web interface.

---

## 🚀 Features

- ✅ Drag-and-drop upload of marketplace sales data (CSV)
- 🔄 SKU-to-MSKU mapping with combo support
- 📤 Auto-generation of outbound report (`outbound.csv`)
- 🧮 Live inventory update (`updated_inventory.csv`)
- 🌐 Integration with [Baserow.io](https://baserow.io) — inventory + outbound synced
- 📊 Dashboards: Top MSKUs sold and current stock
- ❌ AI Assistant (PandasAI) removed due to compatibility issues

---

## 🧠 Tech Stack

- Python 3.11
- Streamlit
- Pandas
- Baserow API
- dotenv (for secure credentials)

---

## 📁 Folder Structure

```
wms_sku_mapper/
├── data/                    # CSVs (input/output)
├── baserow_client.py        # Baserow uploader
├── sku_mapper.py            # SKU-to-MSKU logic
├── inventory_updater.py     # Subtract outbound from current inventory
├── streamlit_app.py         # Main GUI app
└── .env                     # Baserow API credentials
```

---

## ⚙️ Setup Instructions

### 1. Clone Repo & Set Up Environment

```bash
git clone https://github.com/your-username/wms_sku_mapper.git
cd wms_sku_mapper
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create `.env` file

```ini
BASEROW_API_TOKEN=your_actual_token_here
BASEROW_DB_ID=261210
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

---

## 📥 How It Works

### Step 1: Upload Marketplace Sales File
- Drag and drop your `sales.csv` (with columns `SKU`, `Quantity`).
- Sales data is mapped to `MSKU`, combos are handled.

### Step 2: Auto-Generate Outbound
- Output saved to `data/outbound.csv`
- Posted to Baserow Outbound table (ID: 615322)

### Step 3: Inventory Update
- Subtracts outbound quantities from `data/current_inven.csv`
- Saves updated inventory to `data/updated_inventory.csv`

### Step 4: Dashboard View
- View top MSKUs sold and available stock on the Charts page

---

## 🎥 Loom Video Walkthrough

👉 [Click here to view Loom video walkthrough](#)  
(*replace `#` with your Loom link after recording*)

---

## 📧 Submission

Email to: `vaibhav@cste.international`  
Subject: **WMS Assignment – Neel Patil**

---

## ✅ Status

- ✅ SKU-MSKU Mapping
- ✅ Outbound Generation
- ✅ Inventory Subtraction
- ✅ GUI with Streamlit
- ✅ Baserow Integration
- 🚫 AI Assistant (excluded)

---

## 🙏 Credits

Developed by **Neel Patil**  
For CSTE WMS Evaluation Assignment – July 2025