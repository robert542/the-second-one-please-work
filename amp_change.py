import numpy as np
import sympy as sp
import matplotlib.pyplot as plt


x, a = sp.symbols('x a')
pi = sp.pi


f = (4 / (pi**2 * x**2)) * ((sp.sin(pi * x * a) / a) + (sp.sin(pi * x * a) / (1 - a)) - (sp.sin(pi * x) / (1 - a)))


df_da = sp.diff(f, a)


df_da_func = sp.lambdify((x, a), df_da, 'numpy')


a_values = np.linspace(0.01, 0.99, 400)


x_value = 1.0


df_da_values = df_da_func(x_value, a_values)

plt.plot(a_values, df_da_values, label=r"$\frac{d}{da}\left(\frac{4}{\pi^{2}x^{2}}\left(\frac{\sin(\pi xa)}{a} + \frac{\sin(\pi xa)}{1-a} - \frac{\sin(\pi x)}{1-a}\right)\right)$")
plt.xlabel('a')
plt.ylabel(r"$\frac{d}{da}f(a)$")
plt.title('Derivative of the function with respect to a')
plt.legend()
plt.grid(True)
plt.show()
