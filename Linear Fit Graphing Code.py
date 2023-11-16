import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

# Sample data with uncertainties (x, y, x_err, y_err)
x_data = np.array([0.006086427267, 0.005305039788, 0.004775549188, 0.004570383912, 0.003280839895, 0.002597402597, 0.007849293564, 0.006613756614, 0.004918839154, 0.002677376171])
y_data = np.array([14.15, 12.57, 11.49, 11.12, 8.42, 6.11, 17.64, 15.21, 11.81, 7.18])
y_err = np.array([0.0005, 0.0005, 0.0005, 0.0005, 0.0005, 0.0005, 0, 0, 0, 0])
x_err = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# Define the linear function for the line of best fit
def linear_fit(x, m, b):
    return m * x + b

# Perform the curve fit to find the best-fit parameters (m and b)
params, covariance = curve_fit(linear_fit, x_data, y_data)

# Extract the best-fit parameters and their uncertainties
m, b = params
m_err, b_err = np.sqrt(np.diag(covariance))

correlation, pvalue = pearsonr(x_data, y_data)

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot the data points with error bars and the line of best fit with uncertainty on the first subplot
ax1.errorbar(x_data, y_data, xerr=x_err, yerr=y_err, fmt='o', label='Data with Uncertainties')
x_fit = np.linspace(min(x_data), max(x_data), 100)
line_of_best_fit = lambda x: m * x + b
ax1.plot(x_fit, line_of_best_fit(x_fit), '--', label=f'Best Fit: y = ({m:.2f} ± {m_err:.2f})x + ({b:.2f} ± {b_err:.2f})')
ax1.set_xlabel('Number of LC Units Travelled')
ax1.set_ylabel('Pulse Delay (µs)')
ax1.legend()
ax1.set_title('Pulse Delay Measured After Number of LC Units Travelled')
ax1.grid(True)

# Create the residual plot on the second subplot
residuals = y_data - linear_fit(x_data, m, b)
ax2.errorbar(x_data, residuals, yerr=y_err, xerr=x_err, linestyle='', marker='o', markersize=5, color='b')
ax2.axhline(0, color='r', linestyle='--', linewidth=1)
ax2.set_xlabel('(λ-λ₀)⁻¹ [nm⁻¹]')
ax2.set_ylabel('Pulse Delay Measured After Number of LC Units Travelled')
ax2.set_title('Residual Plot')
ax2.grid(True)

# Set the aspect ratio for the second subplot to be the same as the first subplot
ax2.set_aspect('equal')

# Show the combined figure
plt.tight_layout()
plt.show()

# Print the best-fit parameters and their uncertainties
print(f'Best-Fit Parameters:')
print(f'Slope (m) = {m:.2f} ± {m_err:.2f}')
print(f'Intercept (b) = {b:.2f} ± {b_err:.2f}')
