import pandas as pd
import json
from ast import literal_eval


def insertCommonColumns(src_df, dest_df, mapping=None):
    src_cols = set(src_df.columns)
    dst_cols = set(dest_df.columns)
    common_cols = src_cols.intersection(dst_cols)
    return src_df[list(common_cols)] 


def cols2json(df):
    for series_name, series in df.items():
        try:
            df[series_name] = series.apply(lambda x: literal_eval(x))
        except Exception as e:
            print(f"Couldn't convert {series_name}: {e}")

    return df