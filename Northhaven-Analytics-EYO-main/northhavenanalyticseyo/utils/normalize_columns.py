from ..constants import COLUMN_MAP
import re


def normalize_columns(df):
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    new_columns = {}

    for standard_name, synonyms in COLUMN_MAP.items():
        synonyms_normalized = [
            s.strip().lower()
            for s in synonyms
        ]

        for col in df.columns:
            if col in new_columns:
                continue  # already mapped, skip
            for syn in synonyms_normalized:
                # exact match OR synonym is a whole word within col name
                if col == syn or re.search(r'(?<![a-z0-9])' + re.escape(syn) + r'(?![a-z0-9])', col):
                    new_columns[col] = standard_name
                    break

    df = df.rename(columns=new_columns)

    return df
