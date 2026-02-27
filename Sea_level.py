import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # Import data
    df = pd.read_csv("epa-sea-level.csv")

    # Create scatter plot
    fig, ax = plt.subplots()
    ax.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    # First line of best fit (1880–latest)
    res1 = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    years_extended = pd.Series(range(df["Year"].min(), 2051))
    sea_level_pred1 = res1.slope * years_extended + res1.intercept
    ax.plot(years_extended, sea_level_pred1, "r")

    # Second line of best fit (2000–latest)
    df_recent = df[df["Year"] >= 2000]
    res2 = linregress(df_recent["Year"], df_recent["CSIRO Adjusted Sea Level"])
    years_recent = pd.Series(range(2000, 2051))
    sea_level_pred2 = res2.slope * years_recent + res2.intercept
    ax.plot(years_recent, sea_level_pred2, "green")

    # Labels and title
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")

    # Save and return
    fig.savefig("sea_level_plot.png")
    return fig
