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
sigma_haut = [7.96, 6.86, 4.85, 5.25]
lux_haut = [0, 76, 72.2, 73.5]
dist_haut = [19.95, 17.64, 7.37,  14.1 ]
dist_haut_aprox_measured = [21.952, 20.075, 0, 0,  ]


sigma_devant = [4.95, 4.81, 12.26, 9.74, 7, 2.78, 1.91, 10.29, 2.87]
lux_devant = [1.7, 11.4, 9.8, 8, 71.6, 73.3, 70.6, 71.90, 71.9]
dist_devant = [17.17, 19.85, 34.81, 37.40, 29.03, 14.1,  2.6, 36.72, 7.03]
dist_devant_aprox_measured = [18.707, 21.724, 40, 42.541, 0, 0, 0, 0, 0]
# solei branche devant 4.25 m 1.1,devant 4.22m 1.34,

######## # Measures 21
# sigma_haut = [7.96, 6.86]
# lux_haut = [0, 76]
# dist_haut = [19.95, 17.64]
# dist_haut_aprox_measured = [21.952, 20.075]


# sigma_devant = [4.95, 4.81, 12.26, 9.74]
# lux_devant = [1.7, 11.4, 9.8, 8 ]
# dist_devant = [17.17, 19.85, 34.81, 37.40 ]
# dist_devant_aprox_measured = [18.707, 21.724, 40, 42.541, ]

coefficient_devant = np.polyfit(dist_devant, sigma_devant, 1)
coefficients_haut = np.polyfit(dist_haut, sigma_haut, 1)
linear_fit_devant =  np.poly1d(coefficient_devant)
linear_fit_haut =  np.poly1d(coefficients_haut)

# Generate points for the regression line
dist_fit_devant = np.linspace(min(dist_devant), max(dist_devant), 100)
dist_fit_haut= np.linspace(min(dist_haut), max(dist_haut), 100)
sigma_fit_devant = linear_fit_devant(dist_fit_devant)
sigma_fit_haut = linear_fit_haut(dist_fit_haut)


plt.figure()
plt.plot(dist_devant, sigma_devant, 'ro', label="Measurements devant")
plt.plot(dist_haut, sigma_haut, 'bo', label="Measurements haut")
plt.plot(dist_fit_devant, sigma_fit_devant, 'r-', label=f'Linear fit devant : $y = {coefficient_devant[0]:.2f}x + {coefficient_devant[1]:.2f}$')
plt.plot(dist_fit_haut, sigma_fit_haut, 'b-', label=f'Linear fit haut : $y = {coefficients_haut[0]:.2f}x + {coefficients_haut[1]:.2f}$')

plt.xlabel('Distance to the plane [m]')
plt.ylabel('Standard deviation [cm]')
plt.title('Distance x STD \n Signal-to-noise ratio analysis.')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()


