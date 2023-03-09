from matplotlib import pyplot as plt


def graph(objectives, match_percentages):
    global fig
    fig, ax = plt.subplots()
    ax.bar(objectives, match_percentages)

    max_label_len = 20
    trunc_x = [label[:max_label_len] + "..." if len(
        label) > max_label_len else label for label in objectives]
    ax.set_xticklabels(trunc_x)

    plt.title("Objectives Match Percentage")
    plt.xlabel("Objectives")
    plt.ylabel("Match Percentage")
    plt.ylim([0, 1])
    plt.tight_layout()

    fig
    return fig


# labels = ['Texbook', 'Learning Objectives', 'other', 'other2']
# sizes = [15, 45, 20, 20]

# fig, ax = plt.subplots()
# ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
# plt.title("Weighting Adjustments")
# # Equal aspect ratio ensures that pie is drawn as a circle
# ax.axis('equal')

# fig
