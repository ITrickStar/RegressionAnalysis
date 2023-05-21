import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Очистка dataset


def clean_data(df: pd.DataFrame):
    for i in df.columns:
        if (float(df[i].isnull().sum()) > df.shape[0]/4):
            print(df[i].isnull().sum())
            df.drop(columns=i, inplace=True)

    for i in df.columns:
        if (df[i].isnull().sum() < df.shape[0]/50):
            df.dropna(subset=[i], inplace=True)

    for i in df.columns:
        if (df[i].unique().size == 2):
            df[i] = df[i].astype(bool)
    for i in df.select_dtypes(exclude=['number', 'bool', 'object']):
        df[i] = df[i].astype('category')

    for i in df.select_dtypes(include=['bool', 'number']):
        df[i].fillna(df[i].median(), inplace=True)
    for i in df.select_dtypes(include=['category', 'object']):
        df[i].fillna(df[i].mode().iat[0], inplace=True)

    for i in df.select_dtypes(include=['number']):
        df = df[(df[i] >= df[i].quantile(0.005)) &
                (df[i] <= df[i].quantile(0.995))]

    return df


# Преобразование dataset
def reform_data(dataset: pd.DataFrame) -> pd.DataFrame:
    binary_columns = [
        i for i in dataset.columns if dataset[i].dtype.name == 'bool']
    numerical_columns = [i for i in dataset.columns if (
        dataset[i].dtype.name != 'category' and dataset[i].dtype.name != 'object')]
    categorical_columns = [
        i for i in dataset.columns if dataset[i].dtype.name == 'category']

    data_binary = dataset[binary_columns]
    data_binary = dataset.select_dtypes(
        include=[object]).apply(lambda x: pd.factorize(x)[0])

    data_numerical = dataset[numerical_columns]

    data_categorical = pd.get_dummies(
        dataset[categorical_columns], drop_first=True)

    target = dataset[[df for df in dataset.columns.to_list()
                      if df.find('Удельная цена') != -1]]

    types = [data_binary, data_numerical, data_categorical, target]
    non_empty_types = [df for df in types if not df.empty]

    data = pd.concat(non_empty_types, axis=1)
    return data


# логарифмическая гистограмма
def hist(dataset):
    dataset['Удельная цена, руб./кв.м'].hist(bins=20)
    plt.show()
    dataset['Удельная цена, руб./кв.м'].apply(np.log).hist(bins=20)
    plt.show()
