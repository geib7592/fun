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
    N = int(N)
    r = np.random.uniform(size=(N, len(win_prob_pct)))
    win_prob = 0.01 * np.array(win_prob_pct)
    win_prob_tiled = np.tile(win_prob, (N, 1))
    wins = r < win_prob_tiled
    points_tiled = np.tile(points, (N, 1))
    point_total = np.sum(points_tiled * wins, axis=1)
    return point_total


def get_points_from_win_prob(win_prob_pct: list[float]):
    df = pd.DataFrame(data={"prob": win_prob_pct})
    df2 = df.sort_values("prob")
    df2["points"] = range(1, len(win_prob_pct) + 1)
    points = df2.sort_index()["points"].values
    return points


def cdf_plot(y):
    x = sorted(y)
    cdf = np.cumsum(x) / sum(x)
    plt.plot(x, 100 - 100 * cdf)
    plt.xlabel("Score")
    plt.ylabel("Probability of beating this score")


def play_around():
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

    ml = np.array(
        [174, 132, 168, 174, 148, 800, 142, 235, 132, 144, 255, 2500, 132, 390]
    )
    win_prob_pct = 100 * ml / (ml + 100)
    y10 = many_runs(win_prob_pct, get_points_from_win_prob(win_prob_pct), int(1e5))


def bet_against_the_toss_ups():
    win_prob_pct = np.array([59, 83, 73, 76, 67, 74, 60, 71, 51, 80, 77, 55, 59, 59])
    points = get_points_from_win_prob(win_prob_pct)
    y1 = many_runs(win_prob_pct, points, int(1e5))
    y2 = many_runs(get_flipped_win_probs(win_prob_pct, 60), points, int(1e5))
    y3 = many_runs(get_flipped_win_probs(win_prob_pct, 70), points, int(1e5))

    cdf_plot(y1)
    cdf_plot(y2)
    cdf_plot(y3)

    ...


def get_flipped_win_probs(win_prob_pct, threshold):
    """flip win probs that are below threshold"""
    win_prob_pct_flip = []
    for i in win_prob_pct:
        win_prob_pct_flip.append(i if i > threshold else 100 - i)
    return win_prob_pct_flip


def get_flipped_win_probs_choice(win_prob_pct=list[float], choices=list[bool]):
    """flip win probs betted against"""
    win_prob_pct_flip = []
    for i, p in enumerate(win_prob_pct):
        win_prob_pct_flip.append(p if choices[i] else 100 - p)
    return win_prob_pct_flip


def get_randomized_picks(win_prob_pct: list[float], shift_pct: float = 0):
    choices = np.random.uniform(size=len(win_prob_pct)) * 100 < (
        shift_pct + win_prob_pct
    )
    N_underdogs = len(choices) - sum(choices)
    print(f"Betting for {N_underdogs} underdogs")
    return choices


def odds_of_winning():
    probs = [
        0.792,
        0.846,
        0.762,
        0.783,
        0.556,
        0.655,
        0.545,
        0.661,
        0.535,
        0.512,
        0.524,
        0.545,
        0.636,
        0.810,
        0.661,
        0.630,
    ]
    choices1 = [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1]
    ranks1 = [3, 1, 5, 4, 11, 9, 16, 8, 15, 13, 14, 12, 10, 2, 7, 6]
    choices2 = [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1]
    ranks2 = [3, 2, 10, 11, 13, 8, 7, 6, 9, 12, 16, 15, 4, 5, 14, 1]
    winpct = [
        100 * p * choices1[i] + 100 * (1 - p) * (1 - choices1[i])
        for i, p in enumerate(probs)
    ]
    points = [len(ranks1) - i + 1 for i in ranks1]
    y1 = many_runs(winpct, points, 1e4)

    winpct = [
        100 * p * choices2[i] + 100 * (1 - p) * (1 - choices2[i])
        for i, p in enumerate(probs)
    ]
    points = [len(ranks2) - i + 1 for i in ranks2]
    y2 = many_runs(winpct, points, 1e4)

    prob_2_wins = sum((y2 - y1) > 0) / len(y1)
    return prob_2_wins


if __name__ == "__main__":
    odds_of_winning()
    ...
