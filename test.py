import matplotlib.pyplot as plt

fig = plt.figure()

# Adding the second subplot in a 2x2 grid
ax1 = fig.add_subplot(222)
ax1.plot([1, 2, 3], [1, 4, 9])
ax1.set_title('Second Subplot')

# Optionally, add more subplots for complete visualization
ax2 = fig.add_subplot(221)
ax2.plot([1, 2, 3], [9, 4, 1])
ax2.set_title('First Subplot')

ax3 = fig.add_subplot(223)
ax3.plot([1, 2, 3], [2, 3, 5])
ax3.set_title('Third Subplot')

ax4 = fig.add_subplot(224)
ax4.plot([1, 2, 3], [5, 6, 7])
ax4.set_title('Fourth Subplot')

# Automatically adjust subplot params so that the subplot(s) fits into the figure area.
plt.tight_layout()
plt.show()
