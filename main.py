from sklearn.svm import SVC
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import data_processing
import warnings
warnings.filterwarnings("ignore")

url = "https://raw.githubusercontent.com/ITrickStar/ML-practice/master/new_train.csv"
if ('')
df = pd.read_excel('данные_квартиры.xlsx',
                   usecols=lambda x: 'Unnamed' not in x, skiprows=1)

dataset = data_processing.clean_dataset(df)
data = data_processing.procesing_data(dataset)

# Разбиение на тестовую и предсказываемую сборку
X = data.drop('Удельная цена, руб./кв.м', axis=1)
y = data['Удельная цена, руб./кв.м']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=40)

# Линейная регрессия
degree = 1
regressor = LinearRegression()
regressor.fit(X_train, y_train)
X = X_train
y = y_train

coeff_linear = pd.DataFrame(
    regressor.coef_, X.columns, columns=['Coefficient'])

y_pred = regressor.predict(X_test)
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

print('Linear Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Медиана абсолютной модели:',
      metrics.mean_absolute_error(y_test, y_pred)/y.mean())
print('Adjusted R-squared:', 1 - (1-regressor.score(X, y))
      * (len(y)-1)/(len(y)-X.shape[1]-1))
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
# print('Root Mean Squared Error:', np.sqrt(
#     metrics.mean_squared_error(y_test, y_pred)))
print(coeff_linear)

# Полиномиальная регрессия
degree = 3
poly = PolynomialFeatures(degree)
pf_train = poly.fit_transform(X_train)
pf_test = poly.fit_transform(X_test)
X = pf_train
y = y_train
pfregressor = LinearRegression()
pfregressor.fit(X, y)

coeff_polynomial = pd.DataFrame(
    [pfregressor.coef_], X_train.columns)

y_pred = pfregressor.predict(pf_test)
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

print('Poly Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Медиана абсолютной модели:',
      metrics.mean_absolute_error(y_test, y_pred)/y.mean())
print('Adjusted R-squared:', 1 - (1-pfregressor.score(X, y))
      * (len(y)-1)/(len(y)-X.shape[1]-1))
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, pf_y_pred))
# print('Root Mean Squared Error:', np.sqrt(
#     metrics.mean_squared_error(y_test, pf_y_pred)))
print(coeff_polynomial)

f, ax = plt.subplots(figsize=(14, 7))
sns.regplot(y=y_test, x=X_test, order=degree)
plt.scatter(X_test, y_test, color="orange")
plt.grid(True)
plt.show()

# SVC
# svc = SVC(gamma='auto')
# svc.fit(X_train, y_train)

# err_train = np.mean(y_train != svc.predict(X_train))
# err_test = np.mean(y_test != svc.predict(X_test))
# print('Ошибка на обучающей выборке: ', err_train)
# print('Ошибка на тестовой выборке: ', err_test)
