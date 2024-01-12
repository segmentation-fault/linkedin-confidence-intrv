from scipy.stats import poisson
from runstats import Statistics


def calc_under_analytical():
    p_under_analytical = poisson.cdf(1.5, 0.85)
    print("Under probability (analytical): " + "%.2f" % p_under_analytical)
    print("Over probability (analytical): " + "%.2f" % (1 - p_under_analytical))


def calc_under_mc(n_tries: int, n_runs: int):
    out_stats = Statistics()  # To calculate mean and standard deviation

    for i in range(n_tries):
        samples = poisson.rvs(0.85, size=n_runs)
        out_stats.push(sum(map(lambda x: int(x < 1.5), samples)) / len(samples))

    print("Under probability (MC): " + "%.2f" % out_stats.mean() +
          " +/- " + "%.2f" % (1.96 * out_stats.stddev() / len(out_stats)))


if __name__ == '__main__':
    calc_under_analytical()

    print("=" * 20)
    n_tries = 5  # number of tries, the higher the better!
    n_runs = 50  # number of runs per try
    print("# runs: " + str(n_runs) + " # tries: " + str(n_tries))
    calc_under_mc(n_tries, n_runs)

    print("=" * 20)
    n_tries = 10  # number of tries, the higher the better!
    n_runs = 50  # number of runs per try
    print("# runs: " + str(n_runs) + " # tries: " + str(n_tries))
    calc_under_mc(n_tries, n_runs)

    print("=" * 20)
    n_tries = 10  # number of tries, the higher the better!
    n_runs = 100  # number of runs per try
    print("# runs: " + str(n_runs) + " # tries: " + str(n_tries))
    calc_under_mc(n_tries, n_runs)

    print("=" * 20)
    n_tries = 20  # number of tries, the higher the better!
    n_runs = 100  # number of runs per try
    print("# runs: " + str(n_runs) + " # tries: " + str(n_tries))
    calc_under_mc(n_tries, n_runs)
