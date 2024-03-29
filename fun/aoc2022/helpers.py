from timeit import timeit


def timeit_results(*functions, n=1000):
    for func in functions:
        time = timeit(func, number=n) / n
        print(f"{func.__name__}, {time:.3e} s")


def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()
