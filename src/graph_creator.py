import numpy as np
import matplotlib.pyplot as plt


# Generates a bar chart of the amount of characters per query.
def gen_char_bar(query_characters):
    data = []
    labels = []
    for query, count in query_characters.items():
        data.append(count)
        labels.append(query)

    plt.title('The amount of characters (excl. spaces) per query.')
    plt.xlabel('Character count')
    plt.ylabel('Query')
    bars = plt.barh(labels, data, color='royalblue', alpha=0.7)
    plt.bar_label(bars, padding=10)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='x', alpha=0.7)
    plt.margins(0.1, 0)
    plt.gca().invert_yaxis()
    plt.savefig('results/graphs/QM_graph_character_count', bbox_inches='tight')
    plt.close()


# Generates a bar chart of the runtime per query.
def gen_time_bar(runtime, planning_time, execution_time):
    if runtime:  # MayBMS returns runtime, DuBio returns planning and execution time.
        data = []
        labels = []
        for query, time in runtime.items():
            data.append(time)
            labels.append(query)

        plt.title('The total runtime per query')
        plt.xlabel('Runtime in ms.')
        plt.ylabel('Query')
        bars = plt.barh(labels, data, color='royalblue', alpha=0.7)
        plt.bar_label(bars, padding=10)
        plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='x', alpha=0.7)
        plt.margins(0.1, 0)
        plt.gca().invert_yaxis()
        plt.savefig('results/graphs/QM_graph_runtime', bbox_inches='tight')
        plt.close()

    else:
        plan_data = []
        exec_data = []
        labels = []
        for query, time in planning_time.items():
            labels.append(query)
            plan_data.append(time)
            exec_data.append(execution_time.get(query))

        y_axis = np.arange(len(labels))
        bars = plt.barh(y_axis - 0.2, exec_data, 0.4, label='execution time')
        plt.bar_label(bars, padding=6)
        bars = plt.barh(y_axis + 0.2, plan_data, 0.4, label='planning time')
        plt.bar_label(bars, padding=6)

        plt.yticks(y_axis, labels)
        plt.title('The total planning time and execution time per query')
        plt.xlabel('Runtime in ms.')
        plt.ylabel('Query')
        plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='x', alpha=0.7)
        plt.legend()
        plt.margins(0.15, 0)
        plt.gca().invert_yaxis()
        plt.savefig('results/graphs/QM_graph_runtime', bbox_inches='tight')
        plt.close()


