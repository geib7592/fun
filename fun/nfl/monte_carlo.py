import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def single_run(win_prob_pct: list[float], points: list[int]) -> int:
    r = np.random.uniform(size=len(win_prob_pct))
    win_prob = 0.01 * np.array(win_prob_pct)
    wins = r < win_prob
    point_total = sum(np.array(points) * wins)
    return point_total


def many_runs(win_prob_pct: list[float], points: list[int], N: int) -> int:
    r = np.random.uniform(size=(N, len(win_prob_pct)))
    win_prob = 0.01 * np.array(win_prob_pct)
    win_prob_tiled = np.tile(win_prob, (N, 1))
    wins = r < win_prob_tiled
    points_tiled = np.tile(points, (N, 1))
    point_total = np.sum(points_tiled * wins, axis=1)
    return point_total


def get_points_from_win_prob(win_prob_pct: list[float]):
    df = pd.DataFrame(data={"prob": win_prob_pct})
    df2 = df.sort_values('prob')
    df2['points'] = range(1, len(win_prob_pct)+1)
    points = df2.sort_index()['points'].values
    return points


def cdf_plot(y):
    x = sorted(y)
    cdf = np.cumsum(x) / sum(x)
    plt.plot(x, 100 - 100 * cdf)
    plt.xlabel("Score")
    plt.ylabel("Probability of beating this score")


if __name__ == "__main__":
    win_prob_pct = [59, 83, 73, 76, 67, 74, 60, 71, 51, 80, 77, 55, 59, 69]
    points = [3, 14, 9, 11, 6, 10, 5, 8, 1, 13, 12, 2, 4, 7]
    y = many_runs(win_prob_pct, points, int(1e5))

    win_prob_pct = [59, 83, 73, 76, 67, 74, 60, 71, 51, 80, 77, 55, 59, 59]
    points = [3, 14, 9, 11, 6, 10, 5, 8, 1, 13, 12, 2, 4, 7]
    y2 = many_runs(win_prob_pct, points, int(1e5))

    win_prob_pct = [67] * 14
    points = list(range(1, 15))
    y0 = many_runs(win_prob_pct, points, int(1e5))
    
    win_prob_pct = [50] * 14
    points = list(range(1, 15))
    y1 = many_runs(win_prob_pct, points, int(1e5))

    cdf_plot(y2)
    cdf_plot(y0)
    cdf_plot(y1)


    ml = np.array([174,132,168,174,148,800,142,235,132,144,255,2500,132,390])
    win_prob_pct = 100*ml/(ml+100)
    y10 = many_runs(win_prob_pct, get_points_from_win_prob(win_prob_pct), int(1e5))

    ...




