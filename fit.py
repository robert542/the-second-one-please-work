import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the model function using f1 from the n=1 data point
def model(n, B):
    f1 = y_data[0]  # Assuming the first element in y_data corresponds to n=1
    return f1 * n * np.sqrt(1 + B * n**2)

# Example data
x_data = np.array([1, 3, 5, 7, 9, 11])  # This represents the 'n' in your function
y_data = np.array([110.15, 334.4, 581.1, 825.0, 1079.72, 1348.65])  # Observed data

# Curve fitting
params, params_covariance = curve_fit(lambda n, B: model(n, B), x_data, y_data, p0=[0.01])

# Generate fitted y-values
fitted_y = model(x_data, *params)

# Calculate residuals
residuals = y_data - fitted_y

# Calculate total sum of squares (SST)
sst = np.sum((y_data - np.mean(y_data))**2)

# Calculate residual sum of squares (SSR)
ssr = np.sum(residuals**2)

# Calculate R^2
r_squared = 1 - (ssr / sst)

# Print residuals, R^2, and B
print("Fitted B value:", params[0])
print("Residuals:", residuals)
print("R^2:", r_squared)

# Plotting the results
plt.figure(figsize=(6, 4))
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, fitted_y, label='Fitted function', color='red')
plt.xlabel('n')
plt.ylabel('y')
plt.title('Non-linear Fit with B as the Only Fitting Parameter')
plt.legend()
plt.show()

# Plot residuals
plt.figure(figsize=(6, 4))
plt.stem(x_data, residuals)  # Removed the use_line_collection argument
plt.xlabel('n')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()
