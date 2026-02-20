
def load_csv(raw_data):
    import pandas as pd
    import io

    df = pd.read_csv(io.BytesIO(raw_data), sep=None, engine='python')
    return df