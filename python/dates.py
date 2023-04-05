"""File for obtaining the dates of the 2023 year."""

import numpy as np

DATES = []

for i in range(1, 13):
    if i < 8:
        if i % 2 == 0:
            if i != 2:
                for j in range(1, 31):
                    DATES.append(f'{j}.0{i}.2023')
            else:
                for j in range(1, 29):
                    DATES.append(f'{j}.0{i}.2023')
        else:
            for j in range(1, 32):
                DATES.append(f'{j}.0{i}.2023')
    else:
        if i % 2 == 0:
            for j in range(1, 32):
                if i < 10:
                    DATES.append(f'{j}.0{i}.2023')
                else:
                    DATES.append(f'{j}.{i}.2023')
        else:
            for j in range(1, 31):
                if i < 10:
                    DATES.append(f'{j}.0{i}.2023')
                else:
                    DATES.append(f'{j}.{i}.2023')

DATES = np.array(DATES)
