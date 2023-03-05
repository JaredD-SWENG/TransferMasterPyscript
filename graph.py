import matplotlib.pyplot as plt


labels = ['Texbook', 'Learning Objectives', 'other', 'other2']
sizes = [15, 45, 20, 20]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title("Weighting Adjustments")
# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

fig
