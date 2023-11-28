import pandas as pd

def insertCommonColumns(src_df, dest_df, mapping=None):
    src_cols = set(src_df.columns)
    dst_cols = set(dest_df.columns)
    common_cols = src_cols.intersection(dst_cols)
    return src_df[list(common_cols)] 
