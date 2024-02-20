import os, io, re

import sqlite3
from dataclasses import dataclass
from tabulate import tabulate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from PIL import Image, ImageDraw, ImageFont

script_dir = os.path.dirname(os.path.realpath(__file__))


@dataclass
class analysis:
    type: str
    title: str
    size: tuple
    query: str
    predictor: str
    outcome: str

@dataclass
class multianalysis:
    title: str
    aaa: list[analysis]

#!!! make a function to automatically generate analysis structs and multianalysis (automatic generation of db queries)

aaa: list[analysis] = [
    # PA    entered_articulation            by phase !!! add multianalysis by career?
    analysis(
        "errorbox",
        "PA entered_articulation by phase",
        (6, 8),
        "SELECT phase, entered_articulation FROM PA WHERE phase <> -1;",
        "phase",
        "entered_articulation",
    ),


    # PA    success                         by phase !!! add multianalysis by career?
    analysis(
        "errorbox",
        "PA success by phase",
        (6, 8),
        "SELECT phase, success FROM PA WHERE phase <> -1;",
        "phase",
        "success",
    ),


    # PA    distance_P2e_PA_target          by phase
    analysis(
        "errorbox",
        "PA distance_P2e_PA_target by phase",
        (6, 8),
        "SELECT phase, distance_P2e_PA_target FROM PA WHERE phase <> -1;",
        "phase",
        "distance_P2e_PA_target",
    ),


    # PA    delta_id_PA_target              by phase
    analysis(
        "errorbox",
        "PA delta_id_PA_target by phase",
        (6, 8),
        "SELECT phase, delta_id_PA_target FROM PA WHERE phase <> -1;",
        "phase",
        "delta_id_PA_target",
    ),

    
    # PA                angle_PA_target     by phase
    analysis(
        "errorbox",
        "PA angle_PA_target by phase",
        (6, 8),
        "SELECT phase, angle_PA_target FROM PA WHERE phase <> -1;",
        "phase",
        "angle_PA_target",
    ),


    # PA, ECP, PHASE    duration            by phase
    analysis(
        "errorbox",
        "PA duration by phase",
        (6, 8),
        "SELECT PHASE.phase, PA.PA_D FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "PA_D",
    ),
    analysis(
        "errorbox",
        "ECP duration by phase",
        (6, 8),
        "SELECT PHASE.phase, ECP.ECP_D FROM PHASE LEFT JOIN ECP ON PHASE.id = ECP.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "ECP_D",
    ),
    analysis(
        "errorbox",
        "PHASE duration by phase",
        (6, 8),
        "SELECT phase, PHASE_D FROM PHASE WHERE phase <> -1;",
        "phase",
        "PHASE_D",
    ),


    # PA, ECP, PHASE    RPC                 by phase
    analysis(
        "errorbox",
        "PA RPC by phase",
        (6, 8),
        "SELECT PHASE.phase, PA.PA_RPC FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "PA_RPC",
    ),
    analysis(
        "errorbox",
        "ECP RPC by phase",
        (6, 8),
        "SELECT PHASE.phase, ECP.ECP_RPC FROM PHASE LEFT JOIN ECP ON PHASE.id = ECP.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "ECP_RPC",
    ),
    analysis(
        "errorbox",
        "PHASE RPC by phase",
        (6, 8),
        "SELECT phase, PHASE_RPC FROM PHASE WHERE phase <> -1;",
        "phase",
        "PHASE_RPC",
    ),


    # PA, ECP, PHASE    hit_count           by phase
    analysis(
        "errorbox",
        "PA hit count by phase",
        (6, 8),
        "SELECT phase, hit_count FROM PA WHERE phase <> -1;",
        "phase",
        "hit_count",
    ),
    analysis(
        "errorbox",
        "ECP hit count by phase",
        (6, 8),
        "SELECT phase, hit_count FROM ECP WHERE phase <> -1;",
        "phase",
        "hit_count",
    ),
    analysis(
        "errorbox",
        "Phase hit count by phase",
        (6, 8),
        "SELECT phase, hit_count FROM PHASE WHERE phase <> -1;",
        "phase",
        "hit_count",
    ),
    

    # # ECP               ease_of_placement   by phase
    analysis(
        "errorbox",
        "ECP ease of placement by phase",
        (6, 8),
        "SELECT PHASE.phase, ECP.ease_of_placement FROM PHASE LEFT JOIN ECP ON PHASE.id = ECP.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "ease_of_placement",
    ),


    # PA, ECP, PHASE    ulnar_nerve         by phase
    analysis(
        "errorbox",
        "PA target 1 distance from ulnar nerve by phase",
        (8, 8),
        "SELECT phase, ulnar_nerve FROM PA WHERE ECP_number == 1",
        "phase",
        "ulnar_nerve",
    ),
    analysis(
        "errorbox",
        "PA target 2 distance from ulnar nerve by phase",
        (8, 8),
        "SELECT phase, ulnar_nerve FROM PA WHERE ECP_number == 2",
        "phase",
        "ulnar_nerve",
    ),
    analysis(
        "errorbox",
        "PA target 3 distance from ulnar nerve by phase",
        (8, 8),
        "SELECT phase, ulnar_nerve FROM PA WHERE ECP_number == 3",
        "phase",
        "ulnar_nerve",
    ),


    # PA, ECP, PHASE    middle_collateral_artery         by phase
    analysis(
        "errorbox",
        "PA target 1 distance from middle collateral artery by phase",
        (8, 8),
        "SELECT phase, middle_collateral_artery FROM PA WHERE ECP_number == 1",
        "phase",
        "middle_collateral_artery",
    ),
    analysis(
        "errorbox",
        "PA target 2 distance from middle collateral artery by phase",
        (8, 8),
        "SELECT phase, middle_collateral_artery FROM PA WHERE ECP_number == 2",
        "phase",
        "middle_collateral_artery",
    ),
    analysis(
        "errorbox",
        "PA target 3 distance from middle collateral artery by phase",
        (8, 8),
        "SELECT phase, middle_collateral_artery FROM PA WHERE ECP_number == 3",
        "phase",
        "middle_collateral_artery",
    ),


    # PA, ECP, PHASE    median_nerve         by phase
    analysis(
        "errorbox",
        "PA target 1 distance from median by phase",
        (8, 8),
        "SELECT phase, median_nerve FROM PA WHERE ECP_number == 1",
        "phase",
        "median_nerve",
    ),
    analysis(
        "errorbox",
        "PA target 2 distance from median nerve by phase",
        (8, 8),
        "SELECT phase, median_nerve FROM PA WHERE ECP_number == 2",
        "phase",
        "median_nerve",
    ),
    analysis(
        "errorbox",
        "PA target 3 distance from median nerve by phase",
        (8, 8),
        "SELECT phase, median_nerve FROM PA WHERE ECP_number == 3",
        "phase",
        "median_nerve",
    ),


    # PA, ECP, PHASE    brachial_artery         by phase
    analysis(
        "errorbox",
        "PA target 1 distance from brachial artery by phase",
        (8, 8),
        "SELECT phase, brachial_artery FROM PA WHERE ECP_number == 1",
        "phase",
        "brachial_artery",
    ),
    analysis(
        "errorbox",
        "PA target 2 distance from brachial artery by phase",
        (8, 8),
        "SELECT phase, brachial_artery FROM PA WHERE ECP_number == 2",
        "phase",
        "brachial_artery",
    ),
    analysis(
        "errorbox",
        "PA target 3 distance from brachial artery by phase",
        (8, 8),
        "SELECT phase, brachial_artery FROM PA WHERE ECP_number == 3",
        "phase",
        "brachial_artery",
    ),
]

mmm: list[multianalysis] = [
    multianalysis(
        "PA angle by phase and career",
        [analysis(
            "errorbox",
            "confidence PA angle from target by phase",
            (6, 8),
            "SELECT phase, confidence_angle, angle_PA_target FROM PA WHERE phase <> -1;",
            "phase",
            "confidence_angle",
        ),
        analysis(
            "errorbox",
            "real PA angle from target by phase",
            (6, 8),
            "SELECT phase, confidence_angle, angle_PA_target FROM PA WHERE phase <> -1;",
            "phase",
            "angle_PA_target",
        ),
        analysis(
            "correlation",
            "confidence vs real PA angle",
            (6, 8),
            "SELECT phase, confidence_angle, angle_PA_target FROM PA WHERE phase <> -1;",
            "confidence_angle",
            "angle_PA_target",
        ),
        ]
    ),

    multianalysis(
        "PA distance_P2e_PA_target by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT PHASE.phase, PA.distance_P2e_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'st' ;",
            "phase",
            "distance_P2e_PA_target",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT PHASE.phase, PA.distance_P2e_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'sp' ;",
            "phase",
            "distance_P2e_PA_target",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT PHASE.phase, PA.distance_P2e_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'su' ;",
            "phase",
            "distance_P2e_PA_target",
        ),
        ]
    ),

    multianalysis(
        "PA delta_id_PA_target by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT PHASE.phase, PA.delta_id_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'st' ;",
            "phase",
            "delta_id_PA_target",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT PHASE.phase, PA.delta_id_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'sp' ;",
            "phase",
            "delta_id_PA_target",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT PHASE.phase, PA.delta_id_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'su' ;",
            "phase",
            "delta_id_PA_target",
        ),
        ]
    ),

    multianalysis(
        "PA angle_PA_target by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT PHASE.phase, PA.angle_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'st' ;",
            "phase",
            "angle_PA_target",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT PHASE.phase, PA.angle_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'sp' ;",
            "phase",
            "angle_PA_target",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT PHASE.phase, PA.angle_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'su' ;",
            "phase",
            "angle_PA_target",
        ),
        ]
    ),

    multianalysis(
        "PHASE duration by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT phase, PHASE_D FROM PHASE WHERE phase <> -1 AND career == 'st';",
            "phase",
            "PHASE_D",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT phase, PHASE_D FROM PHASE WHERE phase <> -1 AND career == 'sp';",
            "phase",
            "PHASE_D",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT phase, PHASE_D FROM PHASE WHERE phase <> -1 AND career == 'su';",
            "phase",
            "PHASE_D",
        ),
        ]
    ),

    multianalysis(
        "PHASE RPC by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT phase, PHASE_RPC FROM PHASE WHERE phase <> -1 AND career == 'st';",
            "phase",
            "PHASE_RPC",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT phase, PHASE_RPC FROM PHASE WHERE phase <> -1 AND career == 'sp';",
            "phase",
            "PHASE_RPC",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT phase, PHASE_RPC FROM PHASE WHERE phase <> -1 AND career == 'su';",
            "phase",
            "PHASE_RPC",
        ),
        ]
    ),

    multianalysis(
        "PHASE PAC by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT phase, PHASE_PAC FROM PHASE WHERE phase <> -1 AND career == 'st';",
            "phase",
            "PHASE_PAC",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT phase, PHASE_PAC FROM PHASE WHERE phase <> -1 AND career == 'sp';",
            "phase",
            "PHASE_PAC",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT phase, PHASE_PAC FROM PHASE WHERE phase <> -1 AND career == 'su';",
            "phase",
            "PHASE_PAC",
        ),
        ]
    ),

    multianalysis(
        "PHASE PACF by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT phase, PHASE_PACF FROM PHASE WHERE phase <> -1 AND career == 'st';",
            "phase",
            "PHASE_PACF",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT phase, PHASE_PACF FROM PHASE WHERE phase <> -1 AND career == 'sp';",
            "phase",
            "PHASE_PACF",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT phase, PHASE_PACF FROM PHASE WHERE phase <> -1 AND career == 'su';",
            "phase",
            "PHASE_PACF",
        ),
        ]
    ),

    multianalysis(
        "PHASE hit count by phase and career",
        [analysis(
            "errorbox",
            "Student",
            (6, 8),
            "SELECT phase, hit_count FROM PHASE WHERE phase <> -1 AND career == 'st';",
            "phase",
            "hit_count",
        ),
        analysis(
            "errorbox",
            "Resident",
            (6, 8),
            "SELECT phase, hit_count FROM PHASE WHERE phase <> -1 AND career == 'sp';",
            "phase",
            "hit_count",
        ),
        analysis(
            "errorbox",
            "Surgeon",
            (6, 8),
            "SELECT phase, hit_count FROM PHASE WHERE phase <> -1 AND career == 'su';",
            "phase",
            "hit_count",
        ),
        ]
    ),
]

def main():
    with sqlite3.connect(os.path.join(script_dir, f"..\\positioning_test_data-(v1.27).db")) as conn:
        for a in aaa:
            data, summary = get_data_summary(conn, a)

            _ = errorbox(data, summary, a, save=True, show=True)

        for m in mmm:
            imgsBytes = []
            for a in m.aaa:
                if a.type == "errorbox":
                    data, summary = get_data_summary(conn, a)
                    imgsBytes.append(errorbox(data, summary, a, save=False, show=False)) # saving at the end
                
                elif a.type == "correlation":
                    data, summary = get_data_summary(conn, a)
                    imgsBytes.append(correlation(data, summary, a, save=False, show=False)) # saving at the end
                
                else:
                    print("unknown analysis type")
                    quit()

            # merge multianalysis image
            imgs: list[Image.Image] = []
            for imgBytes in imgsBytes:
                imgs.append(Image.open(imgBytes))
            
            img_out = Image.new("RGB", (sum(img.width for img in imgs), max(img.height for img in imgs)))
            
            x, y = 0, 0
            for img in imgs:
                img_out.paste(img, (x, y))
                x += img.width

            # add title
            font_size = 32
            ImageDraw.Draw(img_out).text(
                xy      = (img_out.width/2, font_size),
                text    = m.title,
                font    = ImageFont.truetype("courbd.ttf", font_size), # others: cour.ttf, courbd.ttf, courbi.ttf (check https://www.wfonts.com/font/courier-new)
                anchor  = "mm",
                fill    = (0,0,0,255))

            img_out.save(os.path.join(script_dir, sanitize_filename(f"{m.title}.png")))
            img_out.show()

def get_data_summary(conn: sqlite3.Connection, a: analysis) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_sql_query(a.query, conn)
    # print(data) #debug

    predictor_counts = data[a.predictor].value_counts().reset_index()
    summary = data.groupby(a.predictor)[a.outcome].agg(['mean', 'std']).reset_index()
    summary = pd.merge(summary, predictor_counts, on=a.predictor)

    # print(f"DATA:\n{data} \nSUMMARY:\n{summary}") #debug

    return data, summary

def correlation(data: pd.DataFrame, summary: pd.DataFrame, a: analysis, save: bool = True, show: bool = True):
    plt.figure(figsize=a.size)
    plt.rcParams['font.family'] = 'Courier New'
    min_x_preplot, max_x_preplot = data[a.predictor].min(), data[a.predictor].max()
    min_y_preplot, max_y_preplot = data[a.outcome].min(), data[a.outcome].max()
    width = 0.06 * (max_x_preplot-min_x_preplot)

    font_size_title = min(plt.get_current_fig_manager().window.winfo_width(), plt.get_current_fig_manager().window.winfo_height()) * 0.08
    # plt.rcParams.update({'font.size': font_size_title}) # set default dimension
    font_size_legend    = 0.6 * font_size_title
    font_size_text      = 0.6 * font_size_title

    # Calculate line of best fit
    coefficients = np.polyfit(data[a.predictor], data[a.outcome], 1)
    poly_function = np.poly1d(coefficients)
    line_x = np.linspace(min(data[a.predictor]), max(data[a.predictor]), 100)
    line_y = poly_function(line_x)

    # PLOT
    sc = plt.scatter(data[a.predictor], data[a.outcome],
                label=f'{a.outcome} Data Points', 
                color='black', alpha=0.5,
                s=10)
    
    plt.plot(line_x, line_y, color='darkred', label='Correlation')

    # get actual plot dimensions
    min_x, max_x = plt.xlim()
    min_y, max_y = plt.ylim()
    
    correlation_coefficient = np.corrcoef(data[a.predictor], data[a.outcome])[0, 1]
    plt.text(max_x, min_y+0.90*(max_y-min_y),
                    f'Pearson corr. coeff.: {correlation_coefficient:.2f}',
                    ha='right', va='center', color='darkred', fontsize=font_size_text)

    # Adding labels and title
    plt.xlabel(a.predictor, fontsize=font_size_title)
    plt.ylabel(a.outcome,   fontsize=font_size_title)
    plt.title (a.title,     fontsize=font_size_title)
    plt.legend(             fontsize=font_size_legend)

    # Set axis ticks
    if all(isinstance(x, int) for x in data):
        plt.yticks(np.arange(min(data), max(data)+1, 1))    # Set y-axis ticks to integers if all data is integer
    
    if len(data[a.predictor]) > 8:
        predictor_values = data[a.predictor]
        num_ticks = 8
        equidistant_ticks = np.linspace(min(predictor_values), max(predictor_values), num_ticks)
        plt.xticks(equidistant_ticks)

    plt.grid(True)

    # save graph to file
    if save:
        plt.savefig(os.path.join(script_dir, sanitize_filename(f"{a.title}.png")))
    img_data = io.BytesIO()

    # save graph to variable
    plt.savefig(img_data, format='png')

    # show graph
    if show:
        plt.show()

    return img_data

def errorbox(data: pd.DataFrame, summary: pd.DataFrame, a: analysis, save: bool = True, show: bool = True) -> io.BytesIO:
    plt.figure(figsize=a.size)
    plt.subplots_adjust(bottom=0.2)
    plt.rcParams['font.family'] = 'Courier New'
    min_x_preplot, max_x_preplot = data[a.predictor].min(), data[a.predictor].max()
    min_y_preplot, max_y_preplot = data[a.outcome].min(), data[a.outcome].max()
    width = 0.06 * (max_x_preplot-min_x_preplot)

    font_size_title = min(plt.get_current_fig_manager().window.winfo_width(), plt.get_current_fig_manager().window.winfo_height()) * 0.08
    # plt.rcParams.update({'font.size': font_size_title}) # set default dimension
    font_size_legend    = 0.6 * font_size_title
    font_size_text      = 0.6 * font_size_title
    font_size_analysis  = 0.6 * font_size_title

    # PLOT
    sc = plt.scatter(data[a.predictor] + np.random.normal(scale=width/6, size=len(data)), data[a.outcome],
                label=f'{a.outcome} Data Points', 
                color='black', alpha=0.5,
                s=10)

    eb = plt.errorbar(summary[a.predictor], summary['mean'], yerr=summary['std'],
                    label=f'{a.outcome} Mean and Stddev', 
                    color='darkred',
                    fmt='o', markersize=6, capsize=6, linewidth=3)
    
    boxplot_data = data.groupby(a.predictor)[a.outcome].apply(list)
    bp  = plt.boxplot(boxplot_data, positions=summary[a.predictor], widths=width,
                boxprops=dict(color='darkblue'), whiskerprops=dict(color='darkblue'), capprops=dict(color='darkblue'), medianprops=dict(color='aquamarine'),
                showfliers=False, notch=False,)

    # get actual plot dimensions
    min_x, max_x = plt.xlim()
    min_y, max_y = plt.ylim()

    # Mean and Median tests
    for i, (index, mean, std, count, q1, median, q3) in enumerate(zip(boxplot_data.index, summary['mean'], summary['std'], summary['count'], boxplot_data.apply(np.percentile, args=(25,)), boxplot_data.apply(np.median), boxplot_data.apply(np.percentile, args=(75,)))):
        plt.text(summary[a.predictor][i]-width/1.9, min_y+0.85*(max_y-min_y),
                    f'Mean:\nStddev:\nCount:',
                    ha='right', va='center', color='darkred', fontsize=font_size_text)
        plt.text(summary[a.predictor][i]+width/1.9, 0.85*(max_y-min_y)+min_y,
                    f'{mean:6.2f}\n{std:6.2f}\n{count:6.0f}   ',
                    ha='left', va='center', color='darkred', fontsize=font_size_text)
        
        plt.text(summary[a.predictor][i]-width/1.9, 0.75*(max_y-min_y)+min_y,
                    f'Q3:\nMedian:\nQ1:',
                    ha='right', va='center', color='darkblue', fontsize=font_size_text)
        plt.text(summary[a.predictor][i]+width/1.9, 0.75*(max_y-min_y)+min_y,
                    f'{q3:6.2f}\n{median:6.2f}\n{q1:6.2f}',
                    ha='left', va='center', color='darkblue', fontsize=font_size_text)

    # ANOVA test
    if all(len(lst) <= 1 for lst in boxplot_data):
        plt.text(min_x+0.0*(max_x-min_x), min_y-0.1*(max_y-min_y),
                f"ANOVA (Fisher's)\nwarning:\nnot enough data!",
                ha='left', va='top', color='purple', fontsize=font_size_analysis)
    else:
        anova_f, anova_p = stats.f_oneway(*boxplot_data)
        plt.text(min_x+0.0*(max_x-min_x), min_y-0.1*(max_y-min_y),
                f"ANOVA (Fisher's)\nf = {anova_f:7.4f}\np = {anova_p:7.4f}",
                ha='left', va='top', color='purple', fontsize=font_size_analysis)

    # DUNNETT test
    if len(boxplot_data[0]) <= 1:
        plt.text(min_x+0.3*(max_x-min_x), min_y-0.1*(max_y-min_y),
                f"DUNNETT (control: {0})\nwarning:\nnot enough data in control!",
                ha='left', va='top', color='purple', fontsize=font_size_analysis)
    else:
        dunnett_stat = stats.dunnett(*boxplot_data[1:], control=boxplot_data[0])
        dunnett_f, dunnett_p, dunnett_ci = dunnett_stat.statistic, dunnett_stat.pvalue, dunnett_stat.confidence_interval()
        data_rows = [[f"{i}", f"{stat:7.4f}", f"{p_val:7.4f}", f"{ci_low:9.4f}<>{ci_high:9.4f}"] for i, stat, p_val, ci_low, ci_high in zip(boxplot_data[1:].index, dunnett_f, dunnett_p, dunnett_ci[0], dunnett_ci[1])]
        plt.text(min_x+0.3*(max_x-min_x), min_y-0.1*(max_y-min_y),
                f"DUNNETT (control: {0})\n{tabulate(data_rows, headers=['i', 'stat', 'p', 'CI'], colalign=('center', 'center', 'center', 'center'),)}",
                ha='left', va='top', color='purple', fontsize=font_size_analysis)
    
    
    # Adding labels and title
    plt.xlabel(a.predictor, fontsize=font_size_title)
    plt.ylabel(a.outcome,   fontsize=font_size_title)
    plt.title (a.title,     fontsize=font_size_title)
    plt.legend(             fontsize=font_size_legend)

    # Set axis ticks
    if all(isinstance(x, int) for x in data):
        plt.yticks(np.arange(min(data), max(data)+1, 1))    # Set y-axis ticks to integers if all data is integer
    plt.xticks(summary[a.predictor])                        # Set x-axis ticks to follow a.predictor

    plt.grid(True)

    # save graph to file
    if save:
        plt.savefig(os.path.join(script_dir, sanitize_filename(f"{a.title}.png")))
    img_data = io.BytesIO()

    # save graph to variable
    plt.savefig(img_data, format='png')

    # show graph
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