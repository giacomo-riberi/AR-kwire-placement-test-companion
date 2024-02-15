import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass, fields
import re
import io
from PIL import Image

script_dir = os.path.dirname(os.path.realpath(__file__))

@dataclass
class analysis:
    title: str
    size: tuple
    query: str
    predictor: str
    outcome: str

@dataclass
class multianalysis:
    title: str
    aaa: list[analysis]

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
        "PA duration by phase",
        (6, 8),
        "SELECT PHASE.phase, PA.PA_D FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "PA_D",
    ),
    analysis(
        "Phase hit count by phase",
        (6, 8),
        "SELECT phase, hit_count FROM PHASE WHERE phase <> -1;",
        "phase",
        "hit_count",
    ),
    analysis(
        "ECP hit count by phase",
        (6, 8),
        "SELECT phase, hit_count FROM ECP WHERE phase <> -1;",
        "phase",
        "hit_count",
    ),
    analysis(
        "PA hit count by phase",
        (6, 8),
        "SELECT phase, hit_count FROM PA WHERE phase <> -1;",
        "phase",
        "hit_count",
    ),
]

mmm: list[multianalysis] = [
    multianalysis(
        "Phase hit count by phase and career",
        [analysis(
            "Student",
            (6, 8),
            "SELECT phase, hit_count FROM PHASE WHERE phase <> -1 AND career == 'st';",
            "phase",
            "hit_count",
        ),
        analysis(
            "Resident",
            (6, 8),
            "SELECT phase, hit_count FROM PHASE WHERE phase <> -1 AND career == 'sp';",
            "phase",
            "hit_count",
        ),
        analysis(
            "Surgeon",
            (6, 8),
            "SELECT phase, hit_count FROM PHASE WHERE phase <> -1 AND career == 'su';",
            "phase",
            "hit_count",
        ),
        ]
    ),
    multianalysis(
        "Phase duration by phase and career",
        [analysis(
            "Student",
            (6, 8),
            "SELECT phase, PHASE_D FROM PHASE WHERE phase <> -1 AND career == 'st';",
            "phase",
            "PHASE_D",
        ),
        analysis(
            "Resident",
            (6, 8),
            "SELECT phase, PHASE_D FROM PHASE WHERE phase <> -1 AND career == 'sp';",
            "phase",
            "PHASE_D",
        ),
        analysis(
            "Surgeon",
            (6, 8),
            "SELECT phase, PHASE_D FROM PHASE WHERE phase <> -1 AND career == 'su';",
            "phase",
            "PHASE_D",
        ),
        ]
    )
]

def main():
    for a in aaa:
        data, summary = get_data_summary(a)

        _ = plotter(data, summary, a, save=True)

    for m in mmm:
        imgsBytes = []
        for a in m.aaa:
            data, summary = get_data_summary(a)

            imgsBytes.append(plotter(data, summary, a, save=False, show=False)) # saving at the end
        
        imgs: list[Image.Image] = []
        for imgBytes in imgsBytes:
            imgs.append(Image.open(imgBytes))

        # Create the new image with calculated dimensions
        img_out = Image.new("RGB", (sum(img.width for img in imgs), max(img.height for img in imgs)))
        
        x, y = 0, 0
        for img in imgs:
            img_out.paste(img, (x, y))
            x += img.width

        # Save the result image
        img_out.save(os.path.join(script_dir, sanitize_filename(f"{m.title}.png")))
        img_out.show()

def get_data_summary(a: analysis) -> tuple[pd.DataFrame, pd.DataFrame]:
    conn = sqlite3.connect(os.path.join(script_dir, f"..\positioning_test_data-(v1.27).db")) 
    data = pd.read_sql_query(a.query, conn)
    # print(data)
    conn.close()

    predictor_counts = data[a.predictor].value_counts().reset_index()
    # predictor_counts.columns = [a.predictor, 'count']
    summary = data.groupby(a.predictor)[a.outcome].agg(['mean', 'std']).reset_index()
    # print(summary_stats)
    summary = pd.merge(summary, predictor_counts, on=a.predictor)

    return data, summary

def plotter(data: pd.DataFrame, summary: pd.DataFrame, a: analysis, save: bool = True, show: bool = True) -> io.BytesIO:
    plt.figure(figsize=a.size)
    plt.rcParams['font.family'] = 'Courier New'
    
    width = 0.1 * (summary[a.predictor].max() - summary[a.predictor].min())

    # Get the current figure manager and extract the window size
    font_size_title = min(plt.get_current_fig_manager().window.winfo_width(), plt.get_current_fig_manager().window.winfo_height()) * 0.08  # Adjust the multiplier as needed
    # plt.rcParams.update({'font.size': font_size_title}) # set default dimension
    font_size_legend    = 0.6 * font_size_title
    font_size_text      = 0.6 * font_size_title

    plt.scatter(data[a.predictor] + np.random.normal(scale=width/6, size=len(data)), data[a.outcome],
                label=f'{a.outcome} Data Points', 
                color='black', alpha=0.5,
                s=10)

    eb = plt.errorbar(summary[a.predictor], summary['mean'], yerr=summary['std'],
                    label=f'{a.outcome} Mean and Stddev', 
                    color='darkred',
                    fmt='o', markersize=6, capsize=6, linewidth=3)
    
    boxplot_data = data.groupby(a.predictor)[a.outcome].apply(list)
    bp  = plt.boxplot(boxplot_data, positions=summary[a.predictor], widths=width,
                # labels=['Label 1', 'Label 1','Label 1'], #label=f'{a.outcome} Median and Quartiles',
                boxprops=dict(color='darkblue'), whiskerprops=dict(color='darkblue'), capprops=dict(color='darkblue'), medianprops=dict(color='aquamarine'),
                showfliers=False, notch=False,)

    _, max_y = plt.ylim()
    for i, (mean, std, count, q1, median, q3) in enumerate(zip(summary['mean'], summary['std'], summary['count'], boxplot_data.apply(np.percentile, args=(25,)), boxplot_data.apply(np.median), boxplot_data.apply(np.percentile, args=(75,)))):
        plt.text(summary[a.predictor][i]-(width/2), max_y-(8*font_size_text),
                    f'Mean:\nStddev:\nCount:',
                    ha='right', va='center', color='darkred', fontsize=font_size_text)
        plt.text(summary[a.predictor][i]-(width/2), max_y-(8*font_size_text),
                    f'{mean:8.2f}\n{std:8.2f}\n{count:5.0f}   ',
                    ha='left', va='center', color='darkred', fontsize=font_size_text)
        
        plt.text(summary[a.predictor][i]-(width/2), max_y-(11*font_size_text),
                    f'Q3:\nMedian:\nQ1:',
                    ha='right', va='center', color='darkblue', fontsize=font_size_text)
        plt.text(summary[a.predictor][i]-(width/2), max_y-(11*font_size_text),
                    f'{q3:8.2f}\n{median:8.2f}\n{q1:8.2f}',
                    ha='left', va='center', color='darkblue', fontsize=font_size_text)

    # Adding labels and title
    plt.xlabel(a.predictor, fontsize=font_size_title)
    plt.ylabel(a.outcome,   fontsize=font_size_title)
    plt.title (a.title,     fontsize=font_size_title)
    plt.legend(             fontsize=font_size_legend)

    # Set x-axis ticks to integers
    plt.xticks(summary[a.predictor])

    plt.grid(True)

    # save graph and show it    
    if save:
        plt.savefig(os.path.join(script_dir, sanitize_filename(f"{a.title}.png")))
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')

    if show:
        plt.show()

    return img_data
    
def sanitize_filename(filename):
    # Define a regular expression pattern to match characters not allowed in file names
    illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'  # Control characters are also not allowed
    
    # Replace illegal characters with underscores
    return re.sub(illegal_chars, '_', filename)

if __name__ == "__main__":
    main()