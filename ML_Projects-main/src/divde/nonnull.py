import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor


df = pd.read_csv('data/cleaned_data.csv')
df['car_sub_title'] = df['car_sub_title'].fillna('')
df= df.assign(title = df['car_title'] + " " + df['car_sub_title'] if not df['car_sub_title'].empty else df['car_title'])
df.drop(['car_sub_title'], axis=1, inplace=True)

df['year'] = df.groupby('car_title')['year'].transform(lambda x: x.fillna(int(x.mode()[0])) if not x.mode().empty else None)
df['reg'] = df.groupby('car_title')['reg'].transform(lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else None)
df['car_attention_grabber'] = df.groupby('car_title')['car_attention_grabber'].transform(lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else None)
df['engine_size'] = df.groupby('car_title')['engine_size'].transform(lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else None)
df['car_seller_rating'] = df.groupby('title')['car_seller_rating'].transform(lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else None)

df.dropna(subset=['miles_traveled', 'car_seller_rating', 'engine_size', 'power', 'car_seller_location',
                  'year', 'reg', 'car_type', 'car_attention_grabber', 'fuel_type', 'transmission', 'car_seller'],
          inplace=True)

label_encoder = LabelEncoder()

df['car_seller_location_encoded'] = label_encoder.fit_transform(df['car_seller_location'])
df['car_seller_encoded'] = label_encoder.fit_transform(df['car_seller'])
df['car_attention_grabber_encoded'] = label_encoder.fit_transform(df['car_attention_grabber'])
df['reg_encoded'] = label_encoder.fit_transform(df['reg'])
features = ['miles_traveled', 'car_seller_rating', 'year', 'car_price', 'car_seller_location_encoded',
            'car_seller_encoded', 'car_attention_grabber_encoded', 'reg_encoded']

df_train = df.dropna(subset=['num_owners'])


# Tạo X_train và y_train từ các mẫu không bị thiếu dữ liệu
X_train = df_train[features]
y_train = df_train['num_owners']

# Tạo mô hình Random Forest Regression
rf_model = RandomForestRegressor(n_estimators=100, random_state=0)

# Đào tạo mô hình trên tập huấn luyện
rf_model.fit(X_train, y_train)

# Sử dụng mô hình để dự đoán giá trị "num_owners" cho các mẫu bị thiếu dữ liệu
X_null = df[df['num_owners'].isnull()][features]
predicted_values = rf_model.predict(X_null)

# Gán giá trị dự đoán vào các mẫu bị thiếu dữ liệu
df.loc[df['num_owners'].isnull(), 'num_owners'] = predicted_values

df['num_owners'] = df['num_owners'].astype(int)
df['year'] = df['year'].astype(int)

df.drop(['car_seller_location_encoded', 'car_seller_encoded', 'car_attention_grabber_encoded', 'reg_encoded', 'car_title'], axis=1, inplace=True)
df.to_csv('nonnull_data.csv', index=False)
