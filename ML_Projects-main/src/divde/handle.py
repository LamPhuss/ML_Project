import pandas as pd

df = pd.read_csv('C:\\Users\\LamPhuss\\Code\\Python\\ML_Projects-main\\ML_Projects-main\\src\\all_car_adverts.csv', index_col=0)
import re


# regex expressions
fuel_type = r'Electric|Diesel Hybrid|Petrol|Diesel Plug-in Hybrid|Bi Fuel|Petrol Plug-in Hybrid|Petrol ' \
            r'Hybrid|Hydrogen|Diesel'
car_type = r'Hatchback|Hearse|Saloon|Convertible|Limousine|Minibus|Panel Van|Estate|Camper|Combi Van|Pickup Double ' \
           r'Cab Car|Coupe|Pickup|SUV|MPV|Window Van|Car Derived Van|Cabriolet'
service = r'First service is not due|Full Service History|No service history|Part service history|Full dealership ' \
          r'history|Full service history partially by franchise|Full franchise service history|Full - Main ' \
          r'Retailer|Full service history|Part Service History|Full Dealership History|No Service History'
transmission = r'Automatic|Manual'
miles_traveled = r'\d+\,?\d*\s?miles?'
power = r'\d+PS|\d+BHP|\d+HP|\d+KILOWATT'
pev_owners = r'\d+\sowners?'
ulez = r'ULEZ'
year = r'\b\d{4}\s'
reg = r'\(.+reg\)'
engine_size = r'\d+\.\d+L|\d+L'
warranty = r'Full manufacturer warranty'
first_year_tax = r'First year road tax included'


# regex functions
def extract_fuel_type(text):
    match = re.search(fuel_type, text)
    if match:
        return match.group().split()[0]
    else:
        return None


def extract_car_type(text):
    match = re.search(car_type, text)
    if match:
        return match.group().split()[0]
    else:
        return None


def extract_transmission(text):
    match = re.search(transmission, text)
    if match:
        return match.group().split()[0]
    else:
        return None


def extract_num_owners(text):
    match = re.search(pev_owners, text)
    if match:
        return int(match.group().split()[0])
    else:
        return None


def extract_miles_traveled(text):
    match = re.search(miles_traveled, text)
    if match:
        return float(match.group().replace(',', '').split()[0])
    else:
        return None


def extract_power(text):
    match = re.search(power, text)
    if match:
        x = match.group().split()[0]
        if x[-2:] == 'PS':
            return float(x[:-2]) * 0.7355
        elif x[-3:] == 'BHP':
            return float(x[:-3]) * 0.7457
        elif x[-2:] == 'HP':
            return float(x[:-2]) * 0.7457
        elif x[-8:] == 'KILOWATT':
            return float(x[:-8])
        else:
            return None
    else:
        return None


def extract_year(text):
    match = re.search(year, text)
    if match:
        return match.group().split()[0]
    else:
        return None


def extract_reg(text):
    match = re.search(reg, text)
    if match:
        x = match.group().split()[0]
        return x[1:]
    else:
        return None

def extract_engine_size(text):
    match = re.search(engine_size, text)
    if match:
        x = match.group().split()[0]
        x = x.replace('L', '')
        return float(x)
    else:
        return None


def extract_ulez(text):
    match = re.search(ulez, text)
    if match:
        return 1
    else:
        return 0


df['fuel_type'] = df['car_specs'].apply(extract_fuel_type)
df['car_type'] = df['car_specs'].apply(extract_car_type)
df['transmission'] = df['car_specs'].apply(extract_transmission)
df['num_owners'] = df['car_specs'].apply(extract_num_owners)
df['miles_traveled'] = df['car_specs'].apply(extract_miles_traveled)
df['power'] = df['car_specs'].apply(extract_power)
df['year'] = df['car_specs'].apply(extract_year)
df['engine_size'] = df['car_specs'].apply(extract_engine_size)
df['ulez'] = df['car_specs'].apply(extract_ulez)
df['reg'] = df['car_specs'].apply(extract_reg)
df['service'] = df['car_specs'].apply(lambda x: re.findall(service, x) if re.findall(service, x) else "UnKnown")
df['warranty'] = df['car_specs'].apply(lambda x: 1 if re.findall(warranty, x) else 0)
df['first_year_tax'] = df['car_specs'].apply(lambda x: 1 if re.findall(first_year_tax, x) else 0)


accident = r'Cat\s\w'
new_brand = r'Brand new'
approve_used = r'Approved used'
finance = r'Finance available'
discounted = r'Save £\d{1,4}[,\d{3}]?'


def extract_discounted(text):
    match = re.search(discounted, text)
    if match:
        return float(match.group().split('Save £')[1].replace(',', ''))
    else:
        return 0


def accident_type(text):
    match = re.search(accident, text)
    if match:
        return match.group().split()[1]
    else:
        return "UnKnown"


df['car_badges'] = df['car_badges'].astype(str)
df['accident_type'] = df['car_badges'].apply(lambda x: accident_type(x))
df['new_brand'] = df['car_badges'].apply(lambda x: 1 if re.findall(new_brand, x) else 0)
df['approve_used'] = df['car_badges'].apply(lambda x: 1 if re.findall(approve_used, x) else 0)
df['finance'] = df['car_badges'].apply(lambda x: 1 if re.findall(finance, x) else 0)
df['discounted'] = df['car_badges'].apply(extract_discounted)

df.drop(['car_specs', 'engine_vol', 'engine_size_unit', 'full_service', 'part_service', 'first_year_road_tax', 'part_service', 'part_warranty', 'miles', 'engine_vol', 'engine_size_unit', 'miles', 'feul_type', 'num_owner', 'body_type', 'make', 'model', 'variant', 'make', 'model', 'variant','car_badges', 'finance_available', 'brand_new'], axis=1, inplace=True)

df= df.assign(title = df['car_title'] + " " + df['car_sub_title'])
#df.drop(['car_title', 'car_sub_title'], axis=1, inplace=True)

df.to_csv('cleaned_data.csv', index=False)