from config import DATA_DIR
from interpolate_six_files import interpolate_all_wells, CSV_PATH

# TODO: good prints
# 1- Interpolate six files
# run function to interpolate df (data from csv file , 10 rows of data in this example)
df = pd.read_csv(CSV_PATH)
print(df)
RGI_WELLs_dict = interpolate_all_wells(DATA_DIR, df)
# 2- well production

# fields parameters
