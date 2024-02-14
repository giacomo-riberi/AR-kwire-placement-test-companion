import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass, fields
import re

@dataclass
class analysis:
    table: str
    filter: str
    predictor: str
    outcome: str

aaa: list[analysis] = [
    # analysis(
    #     "PA",
    #     "ECP_number = 1",
    #     "phase",
    #     "ulnar_nerve",
    # ),
    # analysis(
    #     "PA",
    #     "ECP_number = 2",
    #     "phase",
    #     "ulnar_nerve",
    # ),
    # analysis(
    #     "PA",
    #     "ECP_number = 3",
    #     "phase",
    #     "ulnar_nerve",
    # ),
    analysis(
        "PA",
        "ECP_number = 3 and phase <> -1",
        "phase",
        "PA_D",
    ),
    analysis(
        "PHASE",
        "phase <> -1",
        "phase",
        "hit_count",
    ),
    # analysis(
    #     "ECP",
    #     "phase <> -1",
    #     "phase",
    #     "hit_count",
    # ),
    # analysis(
    #     "PA",
    #     "phase <> -1",
    #     "phase",
    #     "hit_count",
    # ),
]

script_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    for a in aaa:
        conn = sqlite3.connect(os.path.join(script_dir, f"..\positioning_test_data-(v1.27).db"))
        query = f"SELECT {a.outcome}, {a.predictor} FROM {a.table}"
        if a.filter != "":
            query += f" WHERE {a.filter}"
        print(query)
        data = pd.read_sql_query(query, conn)
        conn.close()

        predictor_counts = data[a.predictor].value_counts().reset_index()
        predictor_counts.columns = [a.predictor, 'count']
        summary_stats = data.groupby(a.predictor)[a.outcome].agg(['mean', 'std']).reset_index()
        summary_stats = pd.merge(summary_stats, predictor_counts, on='phase')


        # PLOT        
        plt.figure(figsize=(15, 9))
        plt.rcParams['font.family'] = 'Courier New'
        width = 0.1 * (summary_stats[a.predictor].max() - summary_stats[a.predictor].min())

        # Get the current figure manager and extract the window size
        fig_mgr = plt.get_current_fig_manager()
        window_width, window_height = fig_mgr.window.winfo_width(), fig_mgr.window.winfo_height()
        font_size = min(window_width, window_height) * 0.06  # Adjust the multiplier as needed
        plt.rcParams.update({'font.size': font_size})
                

        plt.scatter(data[a.predictor] + np.random.normal(scale=0.04, size=len(data)), data[a.outcome], color='black', label=f'{a.outcome} data points', alpha=0.5, s=10)

        plt.errorbar(summary_stats[a.predictor], summary_stats['mean'], yerr=summary_stats['std'], fmt='o', color='darkred', label=f'{a.outcome} mean and std', markersize=6, capsize=6, linewidth=3)
        for i, mean, std, count in zip(range(len(summary_stats)), summary_stats['mean'], summary_stats['std'], summary_stats['count']):
            plt.text(summary_stats[a.predictor][i]-(width/2+0.02), mean, f'Mean:   {mean:6.2f}\nStddev: {std:6.2f}\nCount: {count:4.0f}   ', ha='right', va='center', color='darkred')
        

        boxplot_data = data.groupby(a.predictor)[a.outcome].apply(list)
        plt.boxplot(boxplot_data, positions=summary_stats[a.predictor], widths=width, showfliers=False, boxprops=dict(color='darkblue'), whiskerprops=dict(color='darkblue'), capprops=dict(color='darkblue'), medianprops=dict(color='aquamarine'))
        for i, (q0, q1, median, q3, q4) in enumerate(zip(boxplot_data.apply(np.percentile, args=(0,)), boxplot_data.apply(np.percentile, args=(25,)), boxplot_data.apply(np.median), boxplot_data.apply(np.percentile, args=(75,)), boxplot_data.apply(np.percentile, args=(100,)))):
            plt.text(summary_stats[a.predictor][i]+(width/2+0.02), median, f'Q3:     {q3:6.2f}\nMedian: {median:6.2f}\nQ1:     {q1:6.2f}', ha='left', va='center', color='darkblue')

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
        plt.savefig(os.path.join(script_dir, sanitize_filename(f"{a.table} {a.filter} - {a.outcome} ({a.predictor}).png")))
        plt.show()
    
def sanitize_filename(filename):
    # Define a regular expression pattern to match characters not allowed in file names
    illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'  # Control characters are also not allowed
    
    # Replace illegal characters with underscores
    return re.sub(illegal_chars, '_', filename)

if __name__ == "__main__":
    main()