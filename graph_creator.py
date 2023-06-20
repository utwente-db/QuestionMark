import matplotlib.pyplot as plt
import numpy as np


# Generates a graph to display the variability in time, precision and recall
def gen_plot_time(title, xlabel, labels, file, time):
    plt.title('Shows the variability in execution time for \n' + title)
    plt.xlabel(xlabel)
    plt.ylabel('Time')
    plt.plot(labels, time, color='royalblue', marker='o')

    # Creates the labels above each data point.
    for x, y in zip(labels, time):
        label = y
        plt.annotate(label, (x, y),
                     xycoords="data",
                     textcoords="offset points",
                     xytext=(0, 10), ha="center")

    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    plt.margins(0, 0.1)
    plt.savefig('performance/graphs/QM_graph_' + file + '_time', bbox_inches='tight')
    plt.close()


def gen_plot_prerec(title, xlabel, labels, file, precision, recall):
    plt.title('Shows the variability in precision and recall for \n' + title)
    plt.xlabel(xlabel)
    plt.ylabel('Precision / Recall')

    plt.plot(labels, recall, label='recall', marker='o')

    # Creates the labels above each data point.
    for x, y in zip(labels, recall):
        label = y
        plt.annotate(label, (x, y),
                     xycoords="data",
                     textcoords="offset points",
                     xytext=(0, 10), ha="center")

    plt.plot(labels, precision, label='precision', linestyle='-.', marker='o')

    # Creates the labels above each data point.
    for x, y in zip(labels, precision):
        label = y
        plt.annotate(label, (x, y),
                     xycoords="data",
                     textcoords="offset points",
                     xytext=(0, 10), ha="center")

    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    plt.legend()
    plt.margins(0, 0.1)
    plt.savefig('performance/graphs/QM_graph_' + file + '_prerec', bbox_inches='tight')
    plt.close()


def gen_all_graphs():
    # Generates graphs for the distance measure in ASN.
    time = [31, 22, 20, 436, 150]
    precision = [0.306, 0.392, 0.392, 0.496, 0.390]
    recall = [0.239, 0.521, 0.521, 0.148, 0.367]
    labels = ['Levenshtein', 'Jaro', 'Jaro-Winkler', 'Hamming', 'Jaccard']
    title = 'different distance measures for the ASN blocking algorithm.'
    gen_plot_time(title, 'Distance Measure', labels, 'distance_asn', time)
    gen_plot_prerec(title, 'Distance Measure', labels, 'distance_asn', precision, recall)

    # Generates graphs for the phi in ASN.
    time = [47, 34, 28, 56]
    precision = [0.553, 0.396, 0.392, 0.384]
    recall = [0.109, 0.403, 0.512, 0.512]
    labels = ['phi=0.1', 'phi=0.3', 'phi=0.4', 'phi=0.5']
    title = 'different distance thresholds for the ASN blocking algorithm.'
    gen_plot_time(title, 'Distance Threshold', labels, 'phi_asn', time)
    gen_plot_prerec(title, 'Distance Threshold', labels, 'phi_asn', precision, recall)

    # Generates graphs for the window size in ASN.
    time = [36, 25, 28, 21]
    precision = [0.388, 0.391, 0.392, 0.386]
    recall = [0.496, 0.517, 0.521, 0.519]
    labels = ['ws=1', 'ws=3', 'ws=6', 'ws=10']
    title = 'different window sizes for the ASN blocking algorithm.'
    gen_plot_time(title, 'Window Size', labels, 'ws_asn', time)
    gen_plot_prerec(title, 'Window Size', labels, 'ws_asn', precision, recall)

    # Generates graphs for the maximum block size in ASN.
    time = [33, 24, 21, 19]
    precision = [0.458, 0.400, 0.374, 0.364]
    recall = [0.329, 0.471, 0.563, 0.570]
    labels = ['mbs=6', 'mbs=20', 'mbs=50', 'mbs=80']
    title = 'different maximum block sizes for the ASN blocking algorithm.'
    gen_plot_time(title, 'Maximum Block Size', labels, 'mbs_asn', time)
    gen_plot_prerec(title, 'Maximum Block Size', labels, 'mbs_asn', precision, recall)

    # Generates graphs for the dataset size in ASN.
    time = [19, 33, 410, 7532, 42778, 2276543]
    labels = ['1 171', '2 343', '20 000', '80 000', '200 000', '999 000']
    title = 'different window sizes for the ASN blocking algorithm.'
    gen_plot_time(title, '# of Records', labels, 'size_asn', time)

    # Generates graphs for the phi in ISA.
    time = [1679, 1669, 1609, 180000]
    precision = [0.211, 0.374, 0.324, 0]
    recall = [0.425, 0.845, 0.994, 0]
    labels = ['phi=0.2', 'phi=0.3', 'phi=0.4', 'phi=0.5']
    title = 'different distance thresholds for the ISA blocking algorithm.'
    gen_plot_time(title, 'Distance Threshold', labels, 'phi_isa', time)
    gen_plot_prerec(title, 'Distance Threshold', labels, 'phi_isa', precision, recall)

    # Generates graphs for the maximum block size in ISA.
    time = [1631, 1695, 1560, 1593]
    precision = [0.331, 0.329, 0.328, 0.322]
    recall = [0.993, 0.994, 0.994, 0.994]
    labels = ['mbs=6', 'mbs=10', 'mbs=20', 'mbs=50']
    title = 'different window sizes for the ISA blocking algorithm.'
    gen_plot_time(title, 'Maximum Block Size', labels, 'mbs_isa', time)
    gen_plot_prerec(title, 'Maximum Block Size', labels, 'mbs_isa', precision, recall)

    # Generates graphs for the minimum suffix length in ISA.
    time = [1616, 1565, 1386]
    precision = [0.324, 0.324, 0.330]
    recall = [0.994, 0.994, 0.981]
    labels = ['msl=1', 'msl=5', 'msl=15']
    title = 'different minimum suffix lengths for the ISA blocking algorithm.'
    gen_plot_time(title, 'Minimum Suffix Length', labels, 'msl_isa', time)
    gen_plot_prerec(title, 'Minimum Suffix Length', labels, 'msl_isa', precision, recall)

    # Generates graphs for the lower phi in AER from ASN.
    time = [2588, 162, 115, 117, 114]
    precision = [0.073, 0.061, 0.061, 0.060, 0.060]
    recall = [0.133, 0.313, 0.349, 0.358, 0.358]
    labels = ['phi=0.08', 'phi=0.12', 'phi=0.15', 'phi=0.20', 'phi = 0.30']
    title = 'different lower distance thresholds for the AER matching algorithm on ASN.'
    gen_plot_time(title, 'Lower Phi', labels, 'lowphi_aer_asn', time)
    gen_plot_prerec(title, 'Lower Phi', labels, 'lowphi_aer_asn', precision, recall)

    # Generates graphs for the upper phi in AER from ASN.
    time = [114, 114, 114]
    precision = [0.060, 0.061, 0.061]
    recall = [0.358, 0.313, 0.302]
    labels = ['phi=0.22', 'phi=0.30', 'phi=0.70']
    title = 'different upper distance thresholds for the AER matching algorithm on ASN.'
    gen_plot_time(title, 'Upper Phi', labels, 'uppphi_aer_asn', time)
    gen_plot_prerec(title, 'Upper Phi', labels, 'uppphi_aer_asn', precision, recall)

    # Generates graphs for the upper phi and lower phi in AER from ISA.
    time = [300000, 21104, 21549]
    precision = [0.005, 0.005, 0.005]
    recall = [0.978, 0.978, 0.977]
    labels = ['phi=0.22-0.25', 'phi=0.25-0.30', 'phi=0.30-0.35']
    title = 'different distance thresholds for the AER matching algorithm on ISA.'
    gen_plot_time(title, 'Lower Phi - Upper Phi', labels, 'phi_aer_isa', time)
    gen_plot_prerec(title, 'Lower Phi - Upper Phi', labels, 'phi_aer_isa', precision, recall)


if __name__ == '__main__':
    gen_all_graphs()
