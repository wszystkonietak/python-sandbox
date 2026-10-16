import arviz as az
import numpy as np
import pandas as pd
import pylab as plt
import pymc as pm

df = pd.read_csv("weight_height.csv").sample(80, random_state=42)

X = df[["Height", "Weight"]].values
Y = (df["Gender"] == "Male").astype(int).values

X = (X - X.mean(axis=0)) / X.std(axis=0)

with pm.Model() as model:
    alpha = pm.Normal("alpha", mu=0, sigma=5)
    beta = pm.Normal("beta", mu=0, sigma=5, shape=2)

    logits = alpha + beta[0] * X[:, 0] + beta[1] * X[:, 1]
    p = pm.math.sigmoid(logits)
    Y_obs = pm.Bernoulli("Y_obs", p=p, observed=Y)
    idata = pm.sample(500, tune=500, random_seed=42)

posterior_samples = az.extract(idata)
alphas = posterior_samples["alpha"].values
betas = posterior_samples["beta"].values

nn = 200
xx1, xx2 = np.meshgrid(np.linspace(-2.5, 2.5, nn), np.linspace(-2.5, 2.5, nn))
xx = np.array([xx1.flatten(), xx2.flatten()]).T

logits_grid = alphas + xx.dot(betas)
probs_grid = 1.0 / (1.0 + np.exp(-logits_grid))
yy_mean = np.mean(probs_grid, axis=1).reshape((nn, nn))

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

ax.contourf(xx1, xx2, yy_mean, levels=20, cmap="bwr", alpha=0.4)

for i in range(30):
    yy_sample = logits_grid[:, i].reshape((nn, nn))
    ax.contour(xx1, xx2, yy_sample, levels=[0.0], colors="k", linewidths=1, alpha=0.15)

ax.scatter(X[:, 0], X[:, 1], c=Y, cmap="bwr", s=80, edgecolors="black")

ax.set_xlabel("Height")
ax.set_ylabel("Weight")
plt.show()