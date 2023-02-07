import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Очистка датасета из предыдущего отчета
def clean_dataset(dataset):
    for i in range(dataset.columns.size):
        if (dataset[dataset.columns[i]].isnull().sum() and float(dataset[dataset.columns[i]].isnull().sum()) < dataset.shape[0]/90):
            dataset.dropna(subset=[dataset.columns[i]], inplace=True)

    dataset['Высота потолков, м'].fillna(2.65, inplace=True)
    dataset['Тип этажа'].fillna(
        dataset['Тип этажа'].mode().iloc[0], inplace=True)
    dataset['Состояние ремонта'].fillna('Нет', inplace=True)
    dataset.loc[dataset['Количество комнат']
                == 'Студия', 'Количество комнат'] = 0
    dataset['Дата снятия (продажи)'].fillna(np.nan, inplace=True)
    dataset['Школа\nм'].fillna(
        dataset['Школа\nм'].median(axis=0), inplace=True)
    dataset['Детский сад\nм'].fillna(
        dataset['Детский сад\nм'].median(axis=0), inplace=True)

    return dataset

# Преобразование DataFrame


def procesing_data(dataset):
    for i in dataset.select_dtypes(include=[object]):
        if (dataset[i].unique().size > 2):
            dataset[i] = dataset[i].astype('category')
    dataset['Количество комнат'] = dataset['Количество комнат'].astype('int64')
    binary_columns = [
        i for i in dataset.columns if dataset[i].dtype.name == 'object']
    categorical_columns = [
        i for i in dataset.columns if dataset[i].dtype.name == 'category']
    numerical_columns = [i for i in dataset.columns if (
        dataset[i].dtype.name != 'category' and dataset[i].dtype.name != 'object')]

    binary_columns = ['Тип рынка', 'Парковка',
                      'Актуальность на дату послед. проверки']
    include_binary_columns = ['Тип рынка', 'Парковка']
    binary_columns = include_binary_columns
    data_binary = dataset[binary_columns]
    data_binary = data_binary.apply(lambda x: pd.factorize(x)[0])

    numerical_columns = ['Общая площадь,\nкв.м', 'Жилая площадь,\nкв.м', 'Площадь кухни,\nкв.м', 'Высота потолков, м', 'Год постройки', 'Этаж', 'Этажность', 'Количество комнат', 'Цена предложения,\nруб.',
                         'Удельная цена, руб./кв.м', 'Колич.  Просмотр.', 'Колич.  Просм. в день', 'Остановка\nм', 'Парк\nм', 'Центр\nкм', 'Станция метро\nм', 'Школа\nм', 'Детский сад\nм']
    include_numerical_columns = ['Общая площадь,\nкв.м', 'Высота потолков, м', 'Этаж',
                                 'Остановка\nм', 'Парк\nм', 'Центр\nкм', 'Станция метро\nм', 'Школа\nм', 'Детский сад\nм']
    include_numerical_columns = ['Общая площадь,\nкв.м']
    numerical_columns = include_numerical_columns
    data_numerical = dataset[numerical_columns]

    categorical_columns = ['Функциональная зона', 'Тип дома', 'Класс', 'Тип этажа', 'Состояние ремонта',
                           'Материал стен', 'Дата создания', 'Дата парсинга', 'Дата послед. проверки', 'Дата снятия (продажи)']
    include_categorical_columns = ['Тип дома',
                                   'Класс', 'Тип этажа', 'Материал стен']
    categorical_columns = include_categorical_columns
    data_categorical = pd.get_dummies(
        dataset[categorical_columns], drop_first=True)

    data = pd.concat((data_numerical,
                     dataset['Удельная цена, руб./кв.м']), axis=1)
    return data


# логарифмическая гистограмма
def hist(dataset):
    dataset['Удельная цена, руб./кв.м'].hist(bins=20)
    plt.show()
    dataset['Удельная цена, руб./кв.м'].apply(np.log).hist(bins=20)
    plt.show()
