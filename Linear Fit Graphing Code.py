import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

# Sample data with uncertainties (x, y, x_err, y_err)
x_data = np.array([41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0])
y_data = np.array([146,142,139,134,130,126,122,118,115,112,107,102,97,91,88,85,81,77,74,71,67,65,61,57,54,50,47,43,38,34,31,28,25,22,18,13,11,7,4,0,0,0])
y_err = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
x_err = np.array([0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5])

# Define the linear function for the line of best fit
def linear_fit(x, m, b):
    return m * x + b

# Perform the curve fit to find the best-fit parameters (m and b)
params, covariance = curve_fit(linear_fit, x_data, y_data)

# Extract the best-fit parameters and their uncertainties
m, b = params
m_err, b_err = np.sqrt(np.diag(covariance))
correlation, pvalue = pearsonr(x_data, y_data)

# Reduced Chi Squared 
residuals = y_data - linear_fit(x_data, m, b)
chi_squared = np.sum((residuals / y_err) ** 2)
degrees_of_freedom = len(x_data) - len(params)
reduced_chi_squared = chi_squared / degrees_of_freedom

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
print(f'Chi Squared = {reduced_chi_squared:.2f}')
