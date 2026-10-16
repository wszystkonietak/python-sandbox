import arviz as az
import numpy as np
import pylab as plt
import pymc as pm
from sklearn.linear_model import Ridge

np.random.seed(42)

alpha, sigma = 7, 1
beta = [1, 2.5]
size = 25

X1 = np.random.randn(size)
X2 = np.random.randn(size) * 0.2
Y = alpha + beta[0] * X1 + beta[1] * X2 + np.random.randn(size) * sigma

X = np.array([X1, X2]).T
ridge = Ridge()
ridge.fit(X, Y)

with pm.Model() as basic_model:
    alpha_estimated = pm.Normal("alpha_estimated", mu=0, sigma=1)
    beta_estimated = pm.Normal("beta_estimated", mu=0, sigma=1, shape=2)
    sigma_estimated = pm.HalfNormal("sigma_estimated", sigma=1)

    mu_estimated = alpha_estimated + beta_estimated[0] * X1 + beta_estimated[1] * X2
    Y_obs = pm.Normal("Y_obs", mu=mu_estimated, sigma=sigma_estimated, observed=Y)
    idata = pm.sample(500, tune=500, random_seed=42)

posterior_samples = az.extract(idata)
alphas = posterior_samples["alpha_estimated"].values
betas = posterior_samples["beta_estimated"].values

sz = 20
x1, x2 = np.meshgrid(np.linspace(X1.min(), X1.max(), sz), np.linspace(X2.min(), X2.max(), sz))
xx = np.array([x1.flatten(), x2.flatten()]).T

yy_ridge = (ridge.intercept_ + xx.dot(ridge.coef_)).reshape((sz, sz))

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection="3d")

for i in range(15):
    yy_post = (alphas[i] + xx.dot(betas[:, i])).reshape((sz, sz))
    ax.plot_surface(x1, x2, yy_post, color="g", alpha=0.1)

ax.plot_surface(x1, x2, yy_ridge, color="b", alpha=0.4)
ax.scatter(X1, X2, Y, color="r", s=40, edgecolors="black")

ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_zlabel("y")
plt.show()