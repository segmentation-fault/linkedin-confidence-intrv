# Confidence Intervals, or how to be sure I run enough simulations

(This is the companion code to my linkedIn article)

## Intro
The objective of an odds pricing algorithm for a sport, is to produce market odds from some initial parameters. Odds are, essentially, the probability of a certain outcome with a margin (or a vig) added. When writing the algorithm you have, essentially two ways to proceed:

* Writing a statistical model that outputs market probabilities (e.g. probabilities for Over/Under 1.5 goals for a soccer match at Final Time) given some initial parameters (e.g. goal expectations, supremacy etc.)
* Writing a MonteCarlo (MC) simulation, doing the same stuff as the previous.
	
Both have pros and cons. A statistical model is harder to develop, and often entails major code re-factorings in the test phase; additionally, adapting it from a pre-match modelling to a live modelling is not straightforward. On the other hand, it is usually faster to run and optimize. A MonteCarlo simulation is easier to develop, easier to adapt to a live competition, but is usually heavier on the hardware (especially if accurate results are needed, as we will see in the following); parallelization and optimization efforts are thus often needed. 

Given the popularity of MonteCarlo simulations (e.g. [DraftKings prefers them](https://medium.com/draftkings-engineering/building-a-tennis-simulation-d6afdaa97d19)) today I want to talk about an often overlooked tool to understand whether our MonteCarlo simulation is consistent: Confidence Intervals.

## What is a Confidence Interval?
In this article, we will use confidence intervals as a measure to answer the question: how far is my result from the _true_ result? But first, let's introduce what a confidence interval actually is.

A confidence interval at X%, is an interval around a point, where we have X% probability of finding the true mean. What it means, is that we have a measure (granted certain hypotheses) of how our result fares against the true average of a certain quantity. Ideally, we would like X to be as close to 100% as possible, and the bounds of our interval, as close as possible.

First hypothesis: we assume the outputs of our MC simulation to be normally distributed around the true mean. Unless you are exploring some statistical niche corner (e.g. rare events, infinite variance distributed outcomes) the law of big numbers cover us. This gives us a very nice formula for our confidence interval. Specifically, the formula for a 95% confidence interval, i.e. the interval in which we have 95% of probability of finding the true mean m, given our estimated mean m', our estimated standard deviation s' and having performed n tries is:

m' - 1.96 s'/sqrt(n) < m < m' + 1.96 s'/sqrt(n)

notice how the interval thins the higher is n (i.e. the number of tries of our MC simulation); thus, the more tries we make (and the more computational power we use) the more accurate our result will be. I will leave the nitty gritty mathematical details out of this simple article. 

## Let's put it to good use!
Let's write a python script to calculate the Over/Under 1.5 goals for a soccer match. I will assume the total goals in the match are Poisson distributed, with expectation 0.85 goals. Notice, we can easily calculate the under analytically as the Cumulative Distribution Function (CDF) of the Poisson distribution; I will use the `poisson` facilities in `scipy`:
```
from scipy.stats import poisson

p_under_analytical = poisson.cdf(1.5, 0.85)
print("Under probability (analytical): " + "%.2f" % p_under_analytical)
print("Over probability (analytical): " + "%.2f" % (1 - p_under_analytical))
```
which will output:
```
Under probability (analytical): 0.79
Over probability (analytical): 0.21
```

Now let's build a simple MC tallying when we are under 1.5, and using the `runningstats` package to calculate mean and standard deviation of our samples; to keep it simple I will use a simple for loop without workers pools and parallelization.
```
def calc_under_mc(n_tries: int, n_runs: int):
    out_stats = Statistics()  # To calculate mean and standard deviation

    for i in range(n_tries):
        samples = poisson.rvs(0.85, size=n_runs)
        out_stats.push(sum(map(lambda x: int(x < 1.5), samples)) / len(samples))

    print("Under probability (MC): " + "%.2f" % out_stats.mean() +
          " +/- " + "%.2f" % (1.96 * out_stats.stddev() / len(out_stats)))
```
If we run the MC simulation with an increasing number of tries and runs we will see something like:

```
====================
# runs: 50 # tries: 5
Under probability (MC): 0.82 +/- 0.02
====================
# runs: 50 # tries: 10
Under probability (MC): 0.82 +/- 0.01
====================
# runs: 100 # tries: 10
Under probability (MC): 0.82 +/- 0.01
====================
# runs: 100 # tries: 20
Under probability (MC): 0.79 +/- 0.00
```
as you can see, the more the runs, the more accurate the mean, the more the tries, the tighter the confidence interval! You can find the code in my [github](https://github.com/segmentation-fault/linkedin-confidence-intrv).

## Conclusion
In this article I have shown you what is a Confidence Interval, how it is a useful tool to assess the performances of our MonteCarlo simulations, and how to use it. I hope this little tutorial helps pricing modellers out there to create better and more precise tools to price sport events!

# About me
I have 10+ years experience in statistical modelling and simulations. I first applied my skills in telecommunications systems, then I switched to sport betting. I also implement and integrate my models, so if you need any consultation, just drop me a DM!
