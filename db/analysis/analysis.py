import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass, fields

@dataclass
class analysis:
    table: str
    filter: str
    predictor: str
    outcome: str

aaa: list[analysis] = [
    analysis(
        "PA",
        "ECP_number = 2",
        "phase",
        "ulnar_nerve",
    )
]

for a in aaa:
    # Connect to your SQLite database
    script_dir = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(os.path.join(script_dir, f"..\positioning_test_data-(v1.26).db"))

    # Query data from the database
    if a.filter != "":
        query = f"SELECT {a.outcome}, {a.predictor} FROM {a.table} WHERE {a.filter}"
    else:
        query = f"SELECT {a.outcome}, {a.predictor} FROM {a.table}"
    print(query)
    data = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    # Count the number of points for each phase
    predictor_counts = data[a.predictor].value_counts().reset_index()
    predictor_counts.columns = [a.predictor, 'count']

    # Calculating mean and standard deviation for each phase
    summary_stats = data.groupby(a.predictor)[a.outcome].agg(['mean', 'std']).reset_index()

    # Merge summary statistics with counts
    summary_stats = pd.merge(summary_stats, predictor_counts, on='phase')


    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot mean values as a line with dots
    plt.errorbar(summary_stats[a.predictor], summary_stats['mean'], yerr=summary_stats['std'], fmt='o', color='darkred', label=f'{a.outcome} mean and std', markersize=6, capsize=6, linewidth=3)
    # Plot the single data point
    plt.scatter(data[a.predictor] + np.random.normal(scale=0.04, size=len(data)), data[a.outcome], color='black', label=f'{a.outcome} data points', alpha=0.5, s=10)

    # Annotate mean and standard deviation values
    for i, mean, std, count in zip(range(len(summary_stats)), summary_stats['mean'], summary_stats['std'], summary_stats['count']):
        plt.text(summary_stats[a.predictor][i], mean, f'Mean: {mean:.2f}\nStd: {std:.2f}\nCount: {count}', ha='left', va='top')
        # muovere in basso a destra la scritta
        # scrivere il numero di valori su ogni fase


    # Adding labels and title
    plt.xlabel(a.predictor)
    plt.ylabel(a.outcome)

    if a.filter != "":
        plt.title(f"\"{a.outcome}\" grouped by \"{a.predictor}\" filtered for \"{a.filter}\"")
    else:
        plt.title(f"\"{a.outcome}\" grouped by \"{a.predictor}\"")
    plt.legend()
    plt.grid(True)

    # Set x-axis ticks to integers
    plt.xticks(summary_stats[a.predictor])

    # save graph and show it
    plt.savefig(os.path.join(script_dir, f"{a.table} {a.filter} - {a.outcome} ({a.predictor}).png"))
    plt.show()
    