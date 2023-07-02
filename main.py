from config import DATA_DIR,CSV_PATH
from interpolate_csv_file import interpolate_df
from well_production import well_production
# TODO: good prints
# 1- Interpolate six files
# ---- interpolate df (data from csv file , 10 rows of data in this example) ----
# df = pd.read_csv(CSV_PATH)
# print(df)
# RGI_WELLs_dict = interpolate_all_wells(DATA_DIR, df)

# 2- well production
# ----
well_production()
# fields parameters
