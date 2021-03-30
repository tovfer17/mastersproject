
# Copyright 2020, Gurobi Optimization, LLC

# Read diet model data from an Excel spreadsheet (diet.xls).
# Pass the imported data into the diet model (dietmodel.py).
#
# Note that this example reads an external data file (..\data\diet.xls).
# As a result, it must be run from the Gurobi examples/python directory.
#
# This example requires Python package 'xlrd', which isn't included
# in most Python distributions.  You can obtain it from
# http://pypi.python.org/pypi/xlrd.

import os
import xlrd
import dietmodel

#loc = ("/Users/fer/Desktop/data/diet.xls")


#book = xlrd.open_workbook(loc)

book = xlrd.open_workbook(os.path.join("/Users/fer/Desktop/", "data", "diet.xls"))

sh = book.sheet_by_name("Categories")

categories = []
minNutrition = {}
maxNutrition = {}
i = 1
while True:
    try:
        c = sh.cell_value(i, 0)
        categories.append(c)
        minNutrition[c] = sh.cell_value(i, 1)
        maxNutrition[c] = sh.cell_value(i, 2)
        i = i + 1
    except IndexError:
        break
for rx in range(sh.nrows):
    print(sh.row(rx))

sh = book.sheet_by_name("Foods")
foods = []
cost = {}
i = 1
while True:
    try:
        f = sh.cell_value(i, 0)
        foods.append(f)
        cost[f] = sh.cell_value(i, 1)
        i = i + 1
    except IndexError:
        break
for rx in range(sh.nrows):
    print(sh.row(rx))


sh = book.sheet_by_name("Nutrition")
nutritionValues = {}
i = 1

for food in foods:
    j = 2
    for cat in categories:
        nutritionValues[food, cat] = sh.cell_value(i,j)
        print("TEST FOOD:",food)
        print("TEST CAT",cat)
        print("TEST:",nutritionValues[food, cat])
        i += 1
    j += 1

for rx in range(sh.nrows):
    print(sh.row(rx))

dietmodel.solve(categories, minNutrition, maxNutrition, foods, cost,
                nutritionValues)