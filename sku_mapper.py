# sku_mapper.py

import pandas as pd

class SKUMapper:
    def __init__(self, mapping_path, combo_path):
        self.mapping_df = pd.read_csv(mapping_path)
        self.combo_df = pd.read_csv(combo_path)
        self.combo_df.columns = self.combo_df.columns.str.strip()
        self.msku_map = self._build_mapping()

    def _build_mapping(self):
        self.mapping_df.columns = self.mapping_df.columns.str.strip()
        mapping = {}
        for _, row in self.mapping_df.iterrows():
            sku = str(row["SKU"]).strip()
            msku = str(row["MSKU"]).strip()
            mapping[sku] = msku
        return mapping

    def is_combo(self, sku):
        return sku in self.combo_df["Combo"].values

    def explode_combo(self, sku):
        """Returns list of tuples: [(sku1, qty), (sku2, qty)]"""
        row = self.combo_df[self.combo_df["Combo"] == sku]
        if row.empty:
            return []
        skus = []
        for col in row.columns:
            if col.startswith("SKU") and not pd.isna(row.iloc[0][col]):
                skus.append((row.iloc[0][col], 1))  # qty=1 for now
        print(f"[explode_combo] {sku} exploded into: {skus}")
        return skus

    def map_sku(self, sku):
        sku = str(sku).strip()
        mapped = self.msku_map.get(sku, None)
        print(f"[map_sku] {sku} -> {mapped}")
        return mapped

    def get_all_mapped_mskus(self):
        return list(set(self.msku_map.values()))