import arviz as az
import numpy as np
import pandas as pd
import pylab as plt
import pymc as pm
from sklearn.linear_model import Ridge

df = pd.read_csv("weight_height.csv").sample(30, random_state=42)

X = df["Height"].values
Y = df["Weight"].values

X = (X - X.mean()) / X.std()

ridge = Ridge()
ridge.fit(X.reshape(-1, 1), Y)

with pm.Model() as model:
    alpha = pm.Normal("alpha", mu=160, sigma=50)
    beta = pm.Normal("beta", mu=0, sigma=50)
    sigma = pm.HalfNormal("sigma", sigma=25)

    mu = alpha + beta * X
    scores = pm.Normal("scores", mu=mu, sigma=sigma, observed=Y)
    idata = pm.sample(500, tune=500, random_seed=42)

posterior_samples = az.extract(idata)
alphas = posterior_samples["alpha"].values
betas = posterior_samples["beta"].values

x_line = np.linspace(X.min() - 0.5, X.max() + 0.5, 100)
y_ridge = ridge.intercept_ + ridge.coef_[0] * x_line

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

for i in range(100):
    y_post = alphas[i] + betas[i] * x_line
    ax.plot(x_line, y_post, "b-", linewidth=1, alpha=0.05)

ax.plot(x_line, y_ridge, "r--", linewidth=2)
ax.scatter(X, Y, c="k", s=50)

ax.set_xlabel("Height")
ax.set_ylabel("Weight")
plt.show()