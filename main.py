import scipy
import pandas as pd
import numpy as np
import datetime

# read in data from ASTR19_S22_group_project_data.txt
# define an oscillatory function in Python to describe intra- and inter-day variations in the tide
# use scipy library to fit the oscillatory function to the data assuming the root mean squared experimental error on the height of the tide is 0.25 feet
# graph both the model and the data on the same plot (label the data, provide sufficient labeling of the axes to provide clarity, save the figure to PDF)
# subtract off the best fit function from the data and plot the residuals
# ~more that I will add a bit later~


def read_and_clean_data():
    df = pd.read_csv("data.csv")

    new_col_names = {
        "Day of the year": "day",
        "Time in hours:minutes": "24_hr",
        "Tide Height in feet": "tide_height",
    }

    df.rename(columns=new_col_names, inplace=True)

    df["datetime"] = pd.to_datetime(df["24_hr"], format="%H:%M")
    df["minutes"] = df["datetime"].dt.hour * 60 + df["datetime"].dt.minute
    df["time"] = ((df["day"] - 1) * 24 * 60) + df["minutes"]

    df.drop(columns=["day", "24_hr", "datetime", "minutes"], inplace=True)
    df = df[["time", "tide_height"]]

    df.to_csv("cleaned_data.csv", index=False)


df = pd.read_csv("cleaned_data.csv")

print(df)


# formula from TA
# A * sin(B * t + C) + D
def oscillatory_func(t, A, B, C, D):
    return A * np.sin(B * t + C) + D
