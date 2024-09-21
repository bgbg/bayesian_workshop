from typing import Literal

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np

MY_COLORS = ["#e4543b", "#12a2ff", "#e6d57b", "#46054e", "#ff8cec"]


def plot_data_with_predictions(count_data, expected_data=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12.5, 4))
    ax.bar(
        range(len(count_data)),
        count_data,
        color=MY_COLORS[0],
        label="observed",
    )
    if expected_data is not None:
        ax.plot(
            range(len(count_data)),
            expected_data,
            lw=4,
            color=MY_COLORS[1],
            label="expected",
        )
    ax.legend()
    return ax


def plot_time_series(
    x,
    y,
    ax=None,
    plot_type: Literal["line", "point", "bar"] = "bar",
    title=None,
    xlabel=None,
    ylabel=None,
    color=MY_COLORS[0],
):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12.5, 4))

    # Check if `x` is datetime type
    if np.issubdtype(x.dtype, np.datetime64):
        x_values = mdates.date2num(x)
        is_datetime = True
    else:
        x_values = x
        is_datetime = False

    # Plot based on the selected plot type
    if plot_type == "bar":
        ax.bar(x=x_values, height=y, width=7, color=color)
    elif plot_type == "line":
        ax.plot(x_values, y, lw=4, color=color)
    elif plot_type == "point":
        ax.scatter(x_values, y, color=color)
    else:
        raise ValueError("Invalid plot type. Use 'line', 'point', or 'bar'.")

    # Format x-axis based on x values type
    if is_datetime:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%Y"))
    else:
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    # Add labels and title if provided
    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # Format y-axis ticks
    sns.despine(ax=ax)
    tks = ax.get_yticks()
    mx = max(tks)
    md = np.round(mx / 2, -2)
    tks = [0, md, mx]
    ax.set_yticks(tks)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(False)

    return ax
