import pandas as pd
"""
# Đọc file Excel ban đầu
df = pd.read_csv('C:/Users/LamPhuss/Code/Python/ML_Projects-main/ML_Projects-main/src/all_car_adverts.csv' ,usecols=['col1', 'col2', 'col3', 'col4'])

# Tính toán số dòng trong mỗi phần
num_rows = len(df.index)
chunk_size = num_rows // 4

# Lưu mỗi phần vào một file Excel mới
for i, chunk_start in enumerate(range(0, num_rows, chunk_size)):
    chunk_end = min(chunk_start + chunk_size, num_rows)
    chunk = df.iloc[chunk_start:chunk_end]
    chunk.to_csv(f'C:/Users/LamPhuss/Code/Python/ML_Projects-main/ML_Projects-main/src/divde/output_file_{i}.csv', index=False) """
"""['car_price', 'car_specs', 'year', 'engine_size', 'engine_vol', 'car_sub_title', 'reg', 'car_title', 'model', 'car_attention_grabber']
['car_title' ,'year' ,'body_type' ,'miles' ,'engine_vol' ,'engine_size' ,'transmission' ,'num_owner' , 'ulez', 'finance_available' ,'car_price']"""
dataframe = pd.read_csv('C:\\Users\\LamPhuss\\Code\\Python\\ML_Projects-main\\ML_Projects-main\\src\\all_car_adverts.csv' ,usecols=['car_title' ,'year' ,'body_type' ,'miles' ,'engine_vol' ,'engine_size' ,'transmission' ,'num_owner' , 'ulez', 'finance_available' ,'car_price'])

num_rows = len(dataframe.index)
#dataframe.dropna(subset=[''])
chunk_size = num_rows // 2
for i, chunk_start in enumerate(range(0, num_rows, chunk_size)):
    dataframe['year'] = pd.to_numeric(dataframe['year'], errors='coerce')
    chunk_end = min(chunk_start + chunk_size, num_rows)
    chunk = dataframe.iloc[chunk_start:chunk_end]
    chunk.to_csv(f'C:/Users/LamPhuss/Code/Python/ML_Projects-main/ML_Projects-main/src/divde/output_files_{i}.csv', index=False) 