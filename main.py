import scipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    df.drop(columns=["day", "24_hr", "datetime"], inplace=True)  #  "minutes"
    df = df[["minutes", "tide_height"]]

    df.to_csv("cleaned_data.csv", index=False)


# formula from TA
# A * sin(B * t + C) + D
def oscillatory_func(t, A, B, C, D):
    return A * np.sin(B * t + C) + D


def fit_and_plot(df, x_axis, y_axis="tide_height"):
    # initial guess
    initial_guess = [-4.4, 0.005, -3.6, 2.4]

    rmse = 0.25

    weights = 1 / rmse

    params, covariance = scipy.optimize.curve_fit(
        oscillatory_func,
        df[x_axis],
        df[y_axis],
        p0=initial_guess,
        sigma=np.full(len(df), weights),
    )

    # plotting Part 2
    A, B, C, D = params

    fitted_curve = oscillatory_func(df[x_axis], A, B, C, D)

    plt.figure(1)
    plt.scatter(df[x_axis], df[y_axis], label="Original Data")
    plt.plot(df[x_axis], fitted_curve, "r-", label="Fitted Curve")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Height")
    plt.legend()
    plt.savefig("Part2.pdf", bbox_inches="tight", dpi=400)
    plt.show()
    return np.array(fitted_curve)


def array_to_hist(arr):
    plt.figure(2)
    w = 0.5
    plt.hist(arr, bins=np.arange(min(arr), max(arr) + w, w),edgecolor="black",)
    plt.xlabel("Residuals")
    plt.ylabel("Frequency")
    plt.title("Histogram of Residuals")
    plt.savefig("Part3.pdf", bbox_inches="tight", dpi=400)
    plt.show()


def main():
    # read_and_clean_data()
    df = pd.read_csv("cleaned_data.csv")
    df.sort_values(by="minutes", inplace=True)

    best_fit_curve_vals = fit_and_plot(df, "minutes", "tide_height")
    residuals = np.abs(df["tide_height"] - best_fit_curve_vals)

    array_to_hist(residuals)


if __name__ == "__main__":
    main()
