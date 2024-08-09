import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Parameters of the Gaussian distribution
mu = 18     # Mean
sigma = 294    # Standard deviation

# Values for 2σ and 3σ
lower_bound = 2 * sigma
upper_bound = 3 * sigma

# Compute CDF values
cdf_lower = norm.cdf(lower_bound, loc=mu, scale=sigma)
cdf_upper = norm.cdf(upper_bound, loc=mu, scale=sigma)

# Calculate the proportion of values between 2σ and 3σ
proportion_between = cdf_upper - cdf_lower

print(f"Proportion of values between 2σ and 3σ: {100*proportion_between:.4f} [%]")

# Plotting the Gaussian distribution
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
pdf = norm.pdf(x, loc=mu, scale=sigma)

plt.figure(figsize=(10, 6))
plt.plot(x, pdf, label='Normal Distribution')

# Highlight the area between 2σ and 3σ
x_fill = np.linspace(lower_bound, upper_bound, 1000)
pdf_fill = norm.pdf(x_fill, loc=mu, scale=sigma)
plt.fill_between(x_fill, 0, pdf_fill, color='orange', alpha=0.5, label='Area between 2σ and 3σ')

plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.title('Gaussian Distribution with Area between 2σ and 3σ Highlighted')
plt.legend()
plt.grid(True)
plt.show()


# Signal-to-noise ratio

sigma = [2.87, 1.34, 10.29, 1.1, 5.25, 7, 4.85, 1.91, 2.78]
dist = [7.03, 4.22, 36.72, 4.25, 14.1, 29.03, 7.37, 2.6, 14.1]
coefficients = np.polyfit(dist, sigma, 1)
linear_fit = np.poly1d(coefficients)

# Generate points for the regression line
dist_fit = np.linspace(min(dist), max(dist), 100)
sigma_fit = linear_fit(dist_fit)


plt.figure()
plt.plot(dist, sigma, 'ro', label="Measurements")
plt.plot(dist_fit, sigma_fit, 'b-', label=f'Linear fit: $y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}$')
plt.xlabel('Distance to the plane [m]')
plt.ylabel('Standard deviation [cm]')
plt.title('Distance x STD \n Signal-to-noise ratio analysis.')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()


