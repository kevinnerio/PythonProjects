#practice course material here
import pandas as pd

#this is the entire list of cars
used_cars_list = pd.read_csv('used_car_dataset.csv')

#cars from 2023
used_cars_from_2023 = used_cars_list[used_cars_list['Year']>2023].head(5)

print(used_cars_from_2023)