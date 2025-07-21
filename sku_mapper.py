import pandas as pd

class SKUMapping:
    def __init__(self, mapping_file):
        self.mapping_df = pd.read_csv(mapping_file)
        self.mapping_dict = self._create_mapping_dict()
        self.log = []

    def _create_mapping_dict(self):
        mapping = {}
        for _, row in self.mapping_df.iterrows():
            sku = str(row['SKU']).strip().upper()
            msku = str(row['MSKU']).strip().upper()
            mapping[sku] = msku
        return mapping

    def map_sku(self, sku):
        if '+' in sku:
            parts = sku.split('+')
            mskus = []
            for part in parts:
                mapped = self.mapping_dict.get(part.strip().upper(), None)
                if mapped:
                    mskus.append(mapped)
                else:
                    self.log.append(f"Missing mapping for SKU: {part}")
                    mskus.append(f"[UNMAPPED:{part}]")
            return '+'.join(mskus)
        else:
            mapped = self.mapping_dict.get(sku.strip().upper(), None)
            if not mapped:
                self.log.append(f"Missing mapping for SKU: {sku}")
                return f"[UNMAPPED:{sku}]"
            return mapped

    def get_log(self):
        return self.log