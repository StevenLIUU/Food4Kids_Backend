import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def extract_unit(content):
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
    val = ''
    unit = ''
    read_val = True
    for c in content.strip():
        if read_val and c in digits:
            val += c
        elif read_val:
            read_val = False
            unit += c
        else:
            unit += c
    return (float(val), unit)


def extract_content(input):
    if pd.isna(input): return ('NA', 'NA')
    splits = input.strip().split('/')
    content = extract_unit(splits[0])
    per = extract_unit(splits[1])
    return (content, per)


def read_vitamin(input):
    if pd.isna(input): return 'NA'
    splits = input.split(';')
    types = {}
    for i in splits:
        key = i.strip()[0]
        (content, per) = extract_content(i.strip()[3:])
        if key in types.keys(): print('Duplicate vitamin type')
        types[key] = (content, per)
    return types


def read_price(price):
    return float(price.strip()[1:])


def read_food_type(input):
    if pd.isna(input): return []
    types = list(map(lambda x: x.strip(), input.split(',')))
    return types


def calc_min_pack_stat(min_pack_weight, nutri):
    (content, per) = extract_content(nutri)
    if content == 'NA': return 'NA'
    nutri_amount = min_pack_weight / per[0] * content[0]
    return nutri_amount


def data_process(df):
    df['Unit'] = list(map(lambda x: extract_unit(x)[1], df['Package Weight']))
    df['Package Weight'] = list(map(lambda x: extract_unit(x)[0], df['Package Weight']))
    df['Minimum Package Weight'] = list(map(lambda x: extract_unit(x)[0], df['Minimum Package Weight']))
    df['Price'] = list(map(lambda x: read_price(x), df['Price']))
    df['Minimum Package Price'] = df['Price'] / df['Package Weight'] * df['Minimum Package Weight']
    df['Minimum Package Protein'] = list(map(lambda row: calc_min_pack_stat(row[1]['Minimum Package Weight'], row[1]['Protein']), df[['Minimum Package Weight', 'Protein']].iterrows()))
    df['Protein Unit'] = list(map(lambda x: extract_content(x)[0][1], df['Protein']))
    df['Minimum Package Carbohydrate'] = list(map(lambda row: calc_min_pack_stat(row[1]['Minimum Package Weight'], row[1]['Carbohydrate']), df[['Minimum Package Weight', 'Carbohydrate']].iterrows()))
    df['Carbohydrate Unit'] = list(map(lambda x: extract_content(x)[0][1], df['Carbohydrate']))
    df['Minimum Package Fiber'] = list(map(lambda row: calc_min_pack_stat(row[1]['Minimum Package Weight'], row[1]['Fiber']), df[['Minimum Package Weight', 'Fiber']].iterrows()))
    df['Fiber Unit'] = list(map(lambda x: extract_content(x)[0][1], df['Fiber']))
    df['Minimum Package Fat'] = list(map(lambda row: calc_min_pack_stat(row[1]['Minimum Package Weight'], row[1]['Fat']), df[['Minimum Package Weight', 'Fat']].iterrows()))
    df['Fat Unit'] = list(map(lambda x: extract_content(x)[0][1], df['Fat']))
    df['Minimum Package Sodium'] = list(map(lambda row: calc_min_pack_stat(row[1]['Minimum Package Weight'], row[1]['Sodium']), df[['Minimum Package Weight', 'Sodium']].iterrows()))
    df['Sodium Unit'] = list(map(lambda x: extract_content(x)[0][1], df['Sodium']))
    df['Allergic'] = list(map(lambda x: read_food_type(x), df['Allergic']))
    df['Vegetables'] = list(map(lambda x: 'Vegetables' in read_food_type(x), df['Food type']))
    df['Liquid'] = list(map(lambda x: 'Liquid' in read_food_type(x), df['Food type']))
    df['Snacks'] = list(map(lambda x: 'Snacks' in read_food_type(x) or 'Cookies' in read_food_type(x), df['Food type']))
    df['Fruit'] = list(map(lambda x: 'Fruit' in read_food_type(x), df['Food type']))
    df['Meat'] = list(map(lambda x: 'Meat' in read_food_type(x), df['Food type']))
    df['Grain'] = list(map(lambda x: 'Cereals' in read_food_type(x) or 'Bread' in read_food_type(x) or 'Noodles' in read_food_type(x), df['Food type']))
    new_df = df[['Item name', 'Package Weight', 'Minimum Package Weight', 'Unit', 'Price',
                 'Minimum Package Protein', 'Protein Unit', 'Minimum Package Carbohydrate', 'Carbohydrate Unit', 'Minimum Package Fiber',
                 'Fiber Unit', 'Minimum Package Fat', 'Fat Unit', 'Minimum Package Sodium', 'Sodium Unit',
                 'Allergic',
                 'Vegetables', 'Liquid', 'Snacks', 'Fruit', 'Meat', 'Grain',
                 'Brand', 'Source']]
    return new_df

# print(pd.read_csv('C:/Users/nliu/Desktop/work/Food4Kids/food_data.csv'))
def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return data_process(df)

df = read_csv_data('C:/Users/nliu/Desktop/work/Food4Kids/food_data.csv')
print(df)