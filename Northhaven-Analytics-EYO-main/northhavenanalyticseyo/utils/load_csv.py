
def load_csv(raw_data):
    import pandas as pd
    import io

    # Try multiple encodings common in Polish bank exports
    encodings = ['utf-8', 'cp1250', 'iso-8859-2', 'utf-8-sig']
    last_error = None

    for enc in encodings:
        try:
            df = pd.read_csv(
                io.BytesIO(raw_data),
                sep=None,
                engine='python',
                encoding=enc
            )
            if df.shape[1] > 1:  # valid parse = more than 1 column
                return df
        except Exception as e:
            last_error = e
            continue

    raise ValueError(f"Could not parse CSV with any known encoding. Last error: {last_error}")