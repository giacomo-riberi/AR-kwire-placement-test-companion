import os, io, re, subprocess

import sqlite3
from dataclasses import dataclass
from tabulate import tabulate

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from itertools import combinations
import statistics

from PIL import Image, ImageDraw, ImageFont

# https://www.practicalpythonfordatascience.com/ap_seaborn_palette
script_dir = os.path.dirname(os.path.realpath(__file__))

# palette (mi paice la RdYlBu)
color1      = 'crimson'
color2      = 'royalblue'
color3      = 'aquamarine'
color_text  = 'indigo'
colors = ['crimson', 'royalblue', 'forestgreen', 'darkorange', 'darkslategray']
# ['darkred', 'darkblue', 'purple', 'darkgreen', 'red']
# ['crimson', 'maroon', 'firebrick', 'blue', 'navy']
# ['royalblue', 'steelblue', 'purple', 'indigo', 'darkorchid']
# ['mediumpurple', 'green', 'forestgreen', 'olive', 'teal']
# ['darkorange', 'saddlebrown', 'darkslategray', 'darkcyan', 'darkgoldenrod']
# ['mediumvioletred', 'coral', 'darkkhaki', 'mediumseagreen', 'mediumslateblue']



@dataclass
class analysis:
    title: str
    category: str
    type: str
    size: tuple
    query: str
    predictor: str
    outcome: str
    outcomeY: str = None

@dataclass
class multianalysis:
    title: str
    category: str
    aaa: list[analysis]

        
# !!! Tabella angolo deviazione e distanza da nervo ???
    
aaa: list[analysis] = [

    # -------------------------- STATISTICAL -------------------------- #
    analysis(
        "ECP PACF by phase",
        "statistical",
        "barplot chi-square",
        (6, 8),
        "SELECT phase, ECP_PACF FROM ECP WHERE phase <> -1",
        "phase",
        "ECP_PACF",
        "ECP PACF",
    ),
    analysis(
        "ECP PACF by ECP",
        "statistical",
        "barplot chi-square",
        (6, 8),
        "SELECT ECP_number, ECP_PACF FROM ECP WHERE phase <> -1",
        "ECP_number",
        "ECP_PACF",
        "ECP PACF",
    ),
    analysis(
        "ECP ease of placement by phase",
        "statistical",
        "errorbox anova dunnett",
        (8, 8),
        "SELECT phase, ease_of_placement FROM ECP WHERE phase <> -1",
        "phase",
        "ease_of_placement",
        "ease of placement",
    ),
    analysis(
        "ECP ease of placement by duration",
        "statistical",
        "linregress",
        (8, 8),
        "SELECT ease_of_placement, ECP_D FROM ECP WHERE phase <> -1",
        "ECP_D",
        "ease_of_placement",
        "ease of placement",
    ),
    analysis(
        "ECP ease of placement by RPC",
        "statistical",
        "linregress",
        (8, 8),
        "SELECT ease_of_placement, ECP_RPC FROM ECP WHERE phase <> -1",
        "ECP_RPC",
        "ease_of_placement",
        "ease of placement",
    ),
    analysis(
        "PA success by phase",
        "statistical",
        "barplot chi-square",
        (6, 8),
        "SELECT phase, success FROM PA WHERE phase <> -1;",
        "phase",
        "success",
    ),

    # --------------------------- POSITIONAL -------------------------- #
    analysis(
        "PA delta insertion depth by phase",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, delta_id_PA_target FROM PA WHERE phase <> -1;",
        "phase",
        "delta_id_PA_target",
        "delta insertion depth PA target (mm)",
    ),
    analysis(
        "PA delta insertion depth by phase\n(only success)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, delta_id_PA_target FROM PA WHERE phase <> -1 AND success == 1;",
        "phase",
        "delta_id_PA_target",
        "delta insertion depth PA target (mm)",
    ),
    analysis(
        "PA delta insertion depth by phase\n(Student)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.delta_id_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'st';",
        "phase",
        "delta_id_PA_target",
        "delta insertion depth PA target (mm)",
    ),
    analysis(
        "PA delta insertion depth by phase\n(Resident)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.delta_id_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'sp' ;",
        "phase",
        "delta_id_PA_target",
        "delta insertion depth PA target (mm)",
    ),

    analysis(
        "PA angle to target by phase\n(only success)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, angle_PA_target FROM PA WHERE phase <> -1 AND success == 1;",
        "phase",
        "angle_PA_target",
        "angle PA from target (deg)",
    ),
    analysis(
        "PA angle to target by phase",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, angle_PA_target FROM PA WHERE phase <> -1;",
        "phase",
        "angle_PA_target",
        "angle PA from target (deg)",
    ),
    analysis(
        "PA angle to target by phase\n(Student)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.angle_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'st' ;",
        "phase",
        "angle_PA_target",
        "angle PA from target (deg)",
    ),
    analysis(
        "PA angle to target by phase\n(Resident)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.angle_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND career == 'sp' ;",
        "phase",
        "angle_PA_target",
        "angle PA from target (deg)",
    ),
    analysis(
        "PA angle to target confidence by phase",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, confidence_angle, angle_PA_target FROM PA WHERE phase <> -1;",
        "phase",
        "confidence_angle",
        "confidence angle (deg)",
    ),
    analysis(
        "PA angle to target by confidence\n(phase 0)",
        "positional",
        "linregress idealline",
        (8, 8),
        "SELECT phase, confidence_angle, angle_PA_target FROM PA WHERE phase == 0;",
        "confidence_angle",
        "angle_PA_target",
        "angle PA from target (deg)",
    ),
    analysis(
        "PA angle to target by confidence\n(phase 1)",
        "positional",
        "linregress idealline",
        (8, 8),
        "SELECT phase, confidence_angle, angle_PA_target FROM PA WHERE phase == 1;",
        "confidence_angle",
        "angle_PA_target",
        "angle PA from target (deg)",
    ),
    analysis(
        "PA angle to target by confidence\n(phase 2)",
        "positional",
        "linregress idealline",
        (8, 8),
        "SELECT phase, confidence_angle, angle_PA_target FROM PA WHERE phase == 2;",
        "confidence_angle",
        "angle_PA_target",
        "angle PA from target (deg)",
    ),

    analysis(
        "PA P2e from target by phase\n(only success)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, distance_P2e_PA_target FROM PA WHERE phase <> -1 AND success == 1;",
        "phase",
        "distance_P2e_PA_target",
        "distance of skin entrance point from target (mm)",
    ),
    analysis(
        "PA P2e from target by phase",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, distance_P2e_PA_target FROM PA WHERE phase <> -1;",
        "phase",
        "distance_P2e_PA_target",
        "distance of skin entrance point from target (mm)",
    ),
    analysis(
        "PA P2e from target by phase\n(Student)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.distance_P2e_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND PHASE.career == 'st';",
        "phase",
        "distance_P2e_PA_target",
        "distance of skin entrance point from target (mm)",
    ),
    analysis(
        "PA P2e from target by phase\n(Resident)",
        "positional",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.distance_P2e_PA_target FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1 AND PHASE.career == 'sp';",
        "phase",
        "distance_P2e_PA_target",
        "distance of skin entrance point from target (mm)",
    ),
    analysis(
        "PA P2e by confidence\n(phase 0)",
        "positional",
        "linregress idealline",
        (8, 8),
        "SELECT phase, confidence_position, distance_P2e_PA_target FROM PA WHERE phase == 0;",
        "confidence_position",
        "distance_P2e_PA_target",
        "distance of skin entrance point from target (mm)",
    ),
    analysis(
        "PA P2e by confidence\n(phase 1)",
        "positional",
        "linregress idealline",
        (8, 8),
        "SELECT phase, confidence_position, distance_P2e_PA_target FROM PA WHERE phase == 1;",
        "confidence_position",
        "distance_P2e_PA_target",
        "distance of skin entrance point from target (mm)",
    ),
    analysis(
        "PA P2e by confidence\n(phase 2)",
        "positional",
        "linregress idealline",
        (8, 8),
        "SELECT phase, confidence_position, distance_P2e_PA_target FROM PA WHERE phase == 2;",
        "confidence_position",
        "distance_P2e_PA_target",
        "distance of skin entrance point from target (mm)",
    ),
    


    # ---------------------------- DURATION --------------------------- #
    analysis(
        "ECP duration by phase",
        "duration",
        "errorbox anova dunnett",
        (8, 8),
        "SELECT PHASE.phase, ECP.ECP_D FROM PHASE LEFT JOIN ECP ON PHASE.id = ECP.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "ECP_D",
        "duration (s)"
    ),
    analysis(
        "PA duration by phase",
        "duration",
        "errorbox anova dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.PA_D FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "PA_D",
        "duration (s)"
    ),

    # ------------------------------ RPC ------------------------------ #
    analysis(
        "ECP RPC by phase",
        "RPC",
        "errorbox anova dunnett",
        (8, 8),
        "SELECT PHASE.phase, ECP.ECP_RPC FROM PHASE LEFT JOIN ECP ON PHASE.id = ECP.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "ECP_RPC",
        "RPC",
    ),
    analysis(
        "ECP RPC by phase\n(Student)",
        "RPC",
        "errorbox anova dunnett",
        (8, 8),
        "SELECT PHASE.phase, ECP.ECP_RPC FROM PHASE LEFT JOIN ECP ON PHASE.id = ECP.PHASE_id WHERE PHASE.phase <> -1 AND career == 'st';",
        "phase",
        "ECP_RPC",
        "RPC",
    ),
    analysis(
        "ECP RPC by phase\n(Resident)",
        "RPC",
        "errorbox anova dunnett",
        (8, 8),
        "SELECT PHASE.phase, ECP.ECP_RPC FROM PHASE LEFT JOIN ECP ON PHASE.id = ECP.PHASE_id WHERE PHASE.phase <> -1 AND career == 'sp';",
        "phase",
        "ECP_RPC",
        "RPC",
    ),
    analysis(
        "PA RPC by phase",
        "RPC",
        "errorbox anova dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.PA_RPC FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PHASE.phase <> -1;",
        "phase",
        "PA_RPC",
        "RPC",
    ),


    # --------------------------- ANATOMICAL -------------------------- #
    analysis(
        "PA entered articulation by phase",
        "anatomical",
        "barplot chi-square",
        (6, 8),
        "SELECT phase, entered_articulation FROM PA WHERE phase <> -1;",
        "phase",
        "entered_articulation",
        "entered articulation",
    ),

    analysis(
        "ECP hit count by phase",
        "anatomical",
        "barplot chi-square",
        (6, 8),
        "SELECT phase, hit_count FROM ECP WHERE phase <> -1;",
        "phase",
        "hit_count",
        "hit count",
    ),
    analysis(
        "PA hit count by phase",
        "anatomical",
        "barplot chi-square",
        (6, 8),
        "SELECT phase, hit_count FROM PA WHERE phase <> -1;",
        "phase",
        "hit_count",
        "hit count",
    ),
    
    analysis(
        "ECP has hit by phase",
        "anatomical",
        "barplot chi-square",
        (6, 8),
        "SELECT phase, CASE WHEN hit_count >= 1 THEN 1 ELSE 0 END AS ECP_has_hit FROM ECP WHERE phase <> -1;",
        "phase",
        "ECP_has_hit",
        "ECP has hit",
    ),
    analysis(
        "PA has hit vs estimate\n(phase 0)",
        "anatomical",
        "barplot chi-square",
        (4.5, 8),
        "SELECT hit_count, estimate_hit FROM PA WHERE phase == 0;",
        "estimate_hit",
        "hit_count",
        "hit count",
    ),
    analysis(
        "PA has hit vs estimate\n(phase 1)",
        "anatomical",
        "barplot chi-square",
        (4.5, 8),
        "SELECT hit_count, estimate_hit FROM PA WHERE phase == 1;",
        "estimate_hit",
        "hit_count",
        "hit count",
    ),
    analysis(
        "PA has hit vs estimate\n(phase 2)",
        "anatomical",
        "barplot chi-square",
        (4.5, 8),
        "SELECT hit_count, estimate_hit FROM PA WHERE phase == 2;",
        "estimate_hit",
        "hit_count",
        "hit count",
    ),

    analysis(
        "PA distance from ulnar nerve by phase\n(ECP 1)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, ulnar_nerve FROM PA WHERE ECP_number == 1",
        "phase",
        "ulnar_nerve",
        "distance from ulnar nerve (mm)",
    ),
    analysis(
        "PA distance from ulnar nerve by phase\n(ECP 2)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, ulnar_nerve FROM PA WHERE ECP_number == 2",
        "phase",
        "ulnar_nerve",
        "distance from ulnar nerve (mm)",
    ),
    analysis(
        "PA distance from ulnar nerve by phase\n(ECP 2) - Student",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.ulnar_nerve FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PA.ECP_number == 2 AND (PHASE.career == 'st' OR PHASE.phase == -1);",
        "phase",
        "ulnar_nerve",
        "distance from ulnar nerve (mm)",
    ),
    analysis(
        "PA distance from ulnar nerve by phase\n(ECP 2) - Resident",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT PHASE.phase, PA.ulnar_nerve FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PA.ECP_number == 2 AND (PHASE.career == 'sp' OR PHASE.phase == -1);",
        "phase",
        "ulnar_nerve",
        "distance from ulnar nerve (mm)",
    ),
    analysis(
        "PA distance from ulnar nerve by phase\n(ECP 3)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, ulnar_nerve FROM PA WHERE ECP_number == 3",
        "phase",
        "ulnar_nerve",
        "distance from ulnar nerve (mm)",
    ),
    analysis(
        "PA has hit ulnar nerve by phase\n(ECP 1)",
        "anatomical",
        "barplot chi-square",
        (8, 8),
        "SELECT phase, CASE WHEN ulnar_nerve = 0 THEN 1 ELSE 0 END AS ulnar_nerve_hit FROM PA WHERE ECP_number = 1 AND phase <> -1;",
        "phase",
        "ulnar_nerve_hit",
        "ulnar nerve was hit",
    ),
    analysis(
        "PA has hit ulnar nerve by phase\n(ECP 1) - Student",
        "anatomical",
        "barplot chi-square",
        (8, 8),
        "SELECT PHASE.phase, CASE WHEN PA.ulnar_nerve = 0 THEN 1 ELSE 0 END AS ulnar_nerve_hit FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PA.ECP_number = 1 AND PHASE.career = 'st' AND PHASE.phase <> -1;",
        "phase",
        "ulnar_nerve_hit",
        "ulnar nerve was hit",
    ),
    analysis(
        "PA has hit ulnar nerve by phase\n(ECP 1) - Resident",
        "anatomical",
        "barplot chi-square",
        (8, 8),
        "SELECT PHASE.phase, CASE WHEN PA.ulnar_nerve = 0 THEN 1 ELSE 0 END AS ulnar_nerve_hit FROM PHASE LEFT JOIN PA ON PHASE.id = PA.PHASE_id WHERE PA.ECP_number = 1 AND PHASE.career = 'sp' AND PHASE.phase <> -1;",
        "phase",
        "ulnar_nerve_hit",
        "ulnar nerve was hit",
    ),


    analysis(
        "PA distance from median nerve by phase\n(ECP 1)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, median_nerve FROM PA WHERE ECP_number == 1",
        "phase",
        "median_nerve",
        "distance from median nerve (mm)",
    ),
    analysis(
        "PA distance from median nerve by phase\n(ECP 2)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, median_nerve FROM PA WHERE ECP_number == 2",
        "phase",
        "median_nerve",
        "distance from median nerve (mm)",
    ),
    analysis(
        "PA distance from median nerve by phase\n(ECP 3)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, median_nerve FROM PA WHERE ECP_number == 3",
        "phase",
        "median_nerve",
        "distance from median nerve (mm)",
    ),

    analysis(
        "PA distance from brachial artery by phase\n(ECP 1)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, brachial_artery FROM PA WHERE ECP_number == 1",
        "phase",
        "brachial_artery",
        "distance from brachial artery (mm)",
    ),
    analysis(
        "PA distance from brachial artery by phase\n(ECP 2)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, brachial_artery FROM PA WHERE ECP_number == 2",
        "phase",
        "brachial_artery",
        "distance from brachial artery (mm)",
    ),
    analysis(
        "PA distance from brachial artery by phase\n(ECP 3)",
        "anatomical",
        "errorbox levene dunnett",
        (8, 8),
        "SELECT phase, brachial_artery FROM PA WHERE ECP_number == 3",
        "phase",
        "brachial_artery",
        "distance from brachial artery (mm)",
    ),

]

mmm: list[multianalysis] = [

]

def main():
    liveshow = False

    process = subprocess.Popen(["git", "checkout", "master"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    quit()

    with sqlite3.connect(os.path.join(script_dir, f"..\\positioning_test_data-(v1.27).db")) as conn:
        for a in aaa:
            dataframe, dataserie, summary = get_data_summary(conn, a)

            if "errorbox" in a.type:
                _ = errorbox(dataframe, dataserie, summary, a, save=True, show=liveshow)
            
            elif "linregress" in a.type:
                _ = linregress(dataframe, dataserie, summary, a, save=True, show=liveshow)
            
            elif "barplot" in a.type:
                _ = barplot(dataframe, dataserie, summary, a, save=True, show=liveshow)
            
            else:
                print("unknown analysis type")
                quit()

        for m in mmm:
            imgsBytes = []
            for a in m.aaa:
                dataframe, dataserie, summary = get_data_summary(conn, a)
                if a.type == "errorbox":
                    imgsBytes.append(errorbox(dataframe, dataserie, summary, a, save=False, show=False))    # saving at the end
                
                elif a.type == "linregress":
                    imgsBytes.append(linregress(dataframe, dataserie, summary, a, save=False, show=False)) # saving at the end
                
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

            save_path = os.path.join(script_dir, a.category, sanitize_filename(f"{m.title}.png"))
            if not os.path.exists(save_path):
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            img_out.save(save_path)

            if liveshow:
                img_out.show()
            img_out.close()

def get_data_summary(conn: sqlite3.Connection, a: analysis) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    dataframe = pd.read_sql_query(a.query, conn)
    # print(data) #debug

    # mean, std
    summary = dataframe.groupby(a.predictor)[a.outcome].agg(['mean', 'std']).reset_index()

    # count
    predictor_counts = dataframe[a.predictor].value_counts().reset_index()
    summary = pd.merge(summary, predictor_counts, on=a.predictor)
    
    # stderr
    summary['stderr'] = summary['std'] / np.sqrt(summary['count'])

    # outcome values as lists for each predictor level
    dataserie = dataframe.groupby(a.predictor)[a.outcome].apply(list)

    return dataframe.sort_index(), dataserie.sort_index(), summary.sort_index()

def barplot(dataframe: pd.DataFrame, dataserie: pd.Series, summary: pd.DataFrame, a: analysis, save: bool = True, show: bool = True):
    plt.figure(figsize=a.size)
    plt.rcParams['font.family'] = 'Courier New'

    font_size_title = min(plt.get_current_fig_manager().window.winfo_width(), plt.get_current_fig_manager().window.winfo_height()) * 0.08
    # plt.rcParams.update({'font.size': font_size_title}) # set default dimension
    font_size_legend    = 0.6 * font_size_title
    font_size_text      = 0.6 * font_size_title
    font_size_analysis  = 0.6 * font_size_title

    # Creating cross-tabulation of predictor and outcome
    cross_tab = pd.crosstab(dataframe[a.predictor], dataframe[a.outcome])
    # cross_tab.plot.bar()

    min_x_preplot, max_x_preplot = cross_tab.index.min(), cross_tab.index.max()
    min_y_preplot, max_y_preplot = cross_tab.min().min(), cross_tab.max().max()
    width = 0.06 * (max_x_preplot-min_x_preplot)

    # Get the number of phases and items
    predictor_count = cross_tab.shape[0]
    outcome_count = cross_tab.shape[1]

    # Set width of bar
    bar_width = 0.6/outcome_count

    # !!! mettere a posto (non urgente)
    for i, sub_bar in enumerate(cross_tab):
        bar_Xs = [p - (outcome_count * bar_width) / 2 + (bar_width / 2) + i * bar_width for p in cross_tab.index]
        bar_Ys = cross_tab[sub_bar]
        plt.bar(bar_Xs, bar_Ys,
                bar_width, label=sub_bar,
                color=colors[i % len(colors)])

        for i, y in enumerate(bar_Ys):
            total = sum(cross_tab.iloc[i])  # Sum of counts for the current phase
            percentage = y / total * 100 if total != 0 else 0  # Calculate percentage, handle division by zero
            plt.text(bar_Xs[i], y,
                        f'{y} ({percentage:.1f}%)',
                        ha='center', va=('top' if y>(max_y_preplot-min_y_preplot)/2 else 'bottom'), rotation='vertical',
                        color=('white' if y>(max_y_preplot-min_y_preplot)/2 else 'black'), fontsize=font_size_text)
        
    # get actual plot dimensions
    min_x, max_x = plt.xlim()
    min_y, max_y = plt.ylim()

    for i, predictor in enumerate(cross_tab.index):
        total = sum(cross_tab.iloc[i])
        y = cross_tab.iloc[i].max()
        plt.text(predictor, (y if y>(max_y-min_y)/2 else y+0.15*(max_y-min_y)),
                    f'n={total}',
                    ha='center', va='bottom',
                    color='black', fontsize=font_size_text)

    # Chi-square test
    if "chi-square" in a.type:
        plt.subplots_adjust(bottom=0.25)

        # omnibus test
        chi2, p, dof, expected = stats.chi2_contingency(cross_tab)
        plt.text(min_x, min_y-0.1*(max_y-min_y),
                    f"Chi-square ({'-'.join([str(i) for i in cross_tab.index])}): {chi2:5.2f}\n └ p:               {p:7.4f}",
                    ha='left', va='top',
                    color=color_text, fontsize=font_size_analysis)

        # post hoc test
        # https://www.researchgate.net/post/How_Bonferroni_correction_be_applied_for_chi_square_test_on_comparison_of_three_groups
        bonferroni_correction = predictor_count*outcome_count
        for i, (g1, g2) in enumerate(combinations(cross_tab.index, 2)):
            if min(cross_tab.loc[g1]) == 0 and min(cross_tab.loc[g2]) == 0:
                continue
            chi2, p, dof, expected = stats.chi2_contingency(cross_tab.loc[[g1, g2]])
            plt.text(min_x, min_y-0.16*(max_y-min_y)-0.06*(max_y-min_y)*i,
                    f"Chi-Square ({g1}-{g2}):   {chi2:5.2f}\n └ p (Bonferroni):  {p*bonferroni_correction:7.4f}",
                    ha='left', va='top',
                    color=color_text, fontsize=font_size_analysis)

    # Adding labels and title
    plt.xlabel(a.predictor, fontsize=font_size_title)
    plt.ylabel((a.outcomeY if a.outcomeY != None else a.outcome),   fontsize=font_size_title)
    plt.title (a.title,     fontsize=font_size_title)
    plt.legend(             fontsize=font_size_legend)

    # Set axis ticks
    if all(isinstance(x, int) for x in dataframe):
        plt.yticks(np.arange(min(dataframe), max(dataframe)+1, 1))  # Set y-axis ticks to integers if all data is integer
    plt.xticks(summary[a.predictor])                                # Set x-axis ticks to follow a.predictor

    plt.grid(True, axis='y', alpha=0.5)

    # save graph to file
    if save:
        save_path = os.path.join(script_dir, a.category, sanitize_filename(f"{a.title}.png"))
        if not os.path.exists(save_path):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)

    # save graph to variable
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')

    # show graph
    if show:
        plt.show()
    
    plt.close()

    return img_data

def linregress(dataframe: pd.DataFrame, dataserie: pd.Series, summary: pd.DataFrame, a: analysis, save: bool = True, show: bool = True):
    plt.figure(figsize=a.size)
    plt.rcParams['font.family'] = 'Courier New'
    min_x_preplot, max_x_preplot = dataframe[a.predictor].min(), dataframe[a.predictor].max()
    min_y_preplot, max_y_preplot = dataframe[a.outcome].min(), dataframe[a.outcome].max()
    width = 0.06 * (max_x_preplot-min_x_preplot)

    font_size_title = min(plt.get_current_fig_manager().window.winfo_width(), plt.get_current_fig_manager().window.winfo_height()) * 0.08
    # plt.rcParams.update({'font.size': font_size_title}) # set default dimension
    font_size_legend    = 0.6 * font_size_title
    font_size_text      = 0.6 * font_size_title
    font_size_analysis  = 0.6 * font_size_title

    # LINEAR REGRESSION
    res = stats.linregress(dataframe[a.predictor], dataframe[a.outcome])

    result_str  = f"Count               : {dataframe[a.outcome].count():3.0f}\n"
    result_str += f"Pearson corr. coeff.:   {res.rvalue:3.2f}\n"
    result_str += f"R-squared:              {res.rvalue**2:4.2f}\n" # Coefficient of determination (R-squared):

    # calculate 95% confidence interval on slope and intercept
    tinv = lambda p, df: abs(stats.t.ppf(p/2, df)) # Two-sided inverse Students t-distribution (p: probability, df: degrees of freedom)
    ts = tinv(0.05, len(dataframe[a.predictor])-2)
    result_str += f"Slope     (95%):        {res.slope:4.2f} +/- {ts*res.stderr:4.2f}\n"
    result_str += f"Intercept (95%):        {res.intercept:4.2f} +/- {ts*res.intercept_stderr:4.2f}\n"
    result_str += f"p:                      {res.pvalue:6.4f}\n"

    if "idealline" in a.type:
        # Calculate the intersect point
        x_intersect = (res.intercept) / (1 - res.slope)
        y_intersect = res.intercept + res.slope * x_intersect
        result_str += (f"Intersect (x, y):       {float(x_intersect):.2f}, {y_intersect:.2f}\n")
    
    # PLOT
    sc = plt.scatter(dataframe[a.predictor], dataframe[a.outcome],
                label=f'{a.outcome} Data Points', 
                color='black', alpha=0.5,
                s=10)
    
    plt.plot(dataframe[a.predictor], res.intercept + res.slope * dataframe[a.predictor], color=color1, label='Fitted line')
    
    if "idealline" in a.type:
        plt.plot([min(dataframe[a.predictor]), max(dataframe[a.predictor])], [0, max(dataframe[a.predictor])-min(dataframe[a.predictor])], color=color2, label='Ideal line', linestyle='dashed')

    # get actual plot dimensions
    min_x, max_x = plt.xlim()
    min_y, max_y = plt.ylim()    
    
    plt.subplots_adjust(bottom=0.2)
    plt.text(min_x, min_y-0.2*(max_y-min_y),
                    result_str,
                    ha='left', va='center', color=color_text, fontsize=font_size_analysis)
    
    # Adding labels and title
    plt.xlabel(a.predictor, fontsize=font_size_title)
    plt.ylabel((a.outcomeY if a.outcomeY != None else a.outcome),   fontsize=font_size_title)
    plt.title (a.title,     fontsize=font_size_title)
    plt.legend(             fontsize=font_size_legend)

    # Set axis ticks
    if all(isinstance(x, int) for x in dataframe):
        plt.yticks(np.arange(min(dataframe), max(dataframe)+1, 1))    # Set y-axis ticks to integers if all data is integer
    
    xticks = []
    if len(dataframe[a.predictor].value_counts()) <= 8:
        xticks = dataframe[a.predictor]
    else:
        max_val = max(dataframe[a.predictor])
        if max_val <= 10:
            xticks = np.arange(0, max_val + 1, step=1, dtype=int)
        if max_val <= 20:
            xticks = np.arange(0, max_val + 1, step=2, dtype=int)
        elif max_val <= 40:
            xticks = np.arange(0, max_val + 1, step=5, dtype=int)
        elif max_val <= 100:
            xticks = np.arange(0, max_val + 1, step=10, dtype=int)
        elif max_val <= 200:
            xticks = np.arange(0, max_val + 1, step=20, dtype=int)
        elif max_val <= 500:
            xticks = np.arange(0, max_val + 1, step=50, dtype=int)
        else:
            xticks = np.arange(0, max_val + 1, step=100, dtype=int)
    
    if "idealline" in a.type:
        if x_intersect > min_x and x_intersect < max_x:
            xticks = np.concatenate([xticks, [x_intersect]])
    plt.xticks(xticks)

    plt.grid(True, alpha=0.5)

    # save graph to file
    if save:
        save_path = os.path.join(script_dir, a.category, sanitize_filename(f"{a.title}.png"))
        if not os.path.exists(save_path):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
    
    # save graph to variable
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')

    # show graph
    if show:
        plt.show()

    plt.close()

    return img_data

def errorbox(dataframe: pd.DataFrame, dataserie: pd.Series, summary: pd.DataFrame, a: analysis, save: bool = True, show: bool = True) -> io.BytesIO:
    plt.figure(figsize=a.size)
    plt.rcParams['font.family'] = 'Courier New'
    min_x_preplot, max_x_preplot = dataframe[a.predictor].min(), dataframe[a.predictor].max()
    min_y_preplot, max_y_preplot = dataframe[a.outcome].min(), dataframe[a.outcome].max()
    width = 0.06 * (max_x_preplot-min_x_preplot)

    font_size_title = min(plt.get_current_fig_manager().window.winfo_width(), plt.get_current_fig_manager().window.winfo_height()) * 0.08
    # plt.rcParams.update({'font.size': font_size_title}) # set default dimension
    font_size_legend    = 0.6 * font_size_title
    font_size_text      = 0.5 * font_size_title
    font_size_analysis  = 0.6 * font_size_title

    # PLOT
    sc = plt.scatter(dataframe[a.predictor] + np.random.normal(scale=width/6, size=len(dataframe)), dataframe[a.outcome],
                label=f'{a.outcome} Data Points', 
                color='black', alpha=0.5,
                s=10)

    eb = plt.errorbar(summary[a.predictor], summary['mean'], yerr=summary['std'],
                    label=f'{a.outcome} Mean and Stddev', 
                    color=color1,
                    fmt='o', markersize=6, capsize=6, linewidth=3)
    
    bp  = plt.boxplot(dataserie, positions=summary[a.predictor], widths=width,
                boxprops=dict(color=color2), whiskerprops=dict(color=color2), capprops=dict(color=color2), medianprops=dict(color=color3),
                showfliers=False, notch=False,)

    # get actual plot dimensions
    min_x, max_x = plt.xlim()
    min_y, max_y = plt.ylim()

    # Mean and Median tests
    mean_control = None
    std_control  = None
    for i, (index, mean, std, stderr, count, q1, median, q3) in enumerate(zip(dataserie.index, summary['mean'], summary['std'], summary['stderr'], summary['count'], dataserie.apply(np.percentile, args=(25,)), dataserie.apply(np.median), dataserie.apply(np.percentile, args=(75,)))):
        if mean_control == None and not math.isnan(mean):
            mean_control = mean
        if std_control == None and not math.isnan(std):
            std_control = std

        mean_diff_str, mean_diff_perc_str = "", ""
        if mean_control != mean and not math.isnan(mean):
            mean_diff_str       = f"{mean-mean_control:+6.2f}"
            mean_diff_perc_str  = f"{(mean-mean_control)/mean_control*100:+6.0f}%"

        std_diff_str, std_diff_perc_str = "", ""
        if std_control != std and not math.isnan(std):
            std_diff_str        = f"{std-std_control:+6.2f}"
            std_diff_perc_str   = f"{(std-std_control)/std_control*100:+6.0f}%"

        # !!! tmp remove for thesis
        # plt.text(summary[a.predictor][i]-width/1.9, min_y+0.80*(max_y-min_y),
        #             f'Count:\nMean:\n\n\nStddev:\n\n\nStderr:\n',
        #             ha='right', va='top', color=color1, fontsize=font_size_text)
        # plt.text(summary[a.predictor][i]+width/1.9, 0.80*(max_y-min_y)+min_y,
        #             f'{count:3.0f}\n{mean:6.2f}\n{mean_diff_str}\n{mean_diff_perc_str}\n{std:6.2f}\n{std_diff_str}\n{std_diff_perc_str}\n{stderr:6.2f}',
        #             ha='left', va='top', color=color1, fontsize=font_size_text)
        
        # plt.text(summary[a.predictor][i]-width/1.9, 0.20*(max_y-min_y)+min_y,
        #             f'Q3:\nMedian:\nQ1:',
        #             ha='right', va='bottom', color=color2, fontsize=font_size_text)
        # plt.text(summary[a.predictor][i]+width/1.9, 0.20*(max_y-min_y)+min_y,
        #             f'{q3:6.2f}\n{median:6.2f}\n{q1:6.2f}',
        #             ha='left', va='bottom', color=color2, fontsize=font_size_text)

    # ANOVA test
    if "anova" in a.type.lower():
        plt.subplots_adjust(bottom=0.2)
        if all(len(lst) <= 1 for lst in dataserie):
            plt.text(min_x, min_y-0.1*(max_y-min_y),
                    f"ANOVA (Fisher's)\nwarning:\nnot enough data!",
                    ha='left', va='top', color=color_text, fontsize=font_size_analysis)
        else:
            anova_f, anova_p = stats.f_oneway(*dataserie)
            plt.text(min_x, min_y-0.1*(max_y-min_y),
                    f"ANOVA (Fisher's)\nf: {anova_f:5.2f}\np: {anova_p:7.4f}",
                    ha='left', va='top', color=color_text, fontsize=font_size_analysis)

    # DUNNETT test
    if "dunnett" in a.type.lower():
        plt.subplots_adjust(bottom=0.2)
        if len(dataserie[0]) <= 1:
            plt.text(max_x, min_y-0.1*(max_y-min_y),
                    f"DUNNETT (control: {0})\nwarning:\nnot enough data in control!",
                    ha='right', va='top', color=color_text, fontsize=font_size_analysis)
        else:
            dunnett_stat = stats.dunnett(*dataserie[1:], control=dataserie[0])
            dunnett_f, dunnett_p, dunnett_ci = dunnett_stat.statistic, dunnett_stat.pvalue, dunnett_stat.confidence_interval()
            
            dunnett_table_rows = [[f"{i}", f"{stat:4.2f}", f"{p_val:6.4f}", f"{ci_low:7.2f}<>{ci_high:7.2f}"] for i, stat, p_val, ci_low, ci_high in zip(dataserie[1:].index, dunnett_f, dunnett_p, dunnett_ci[0], dunnett_ci[1])]
            dunnett_table_str = tabulate(dunnett_table_rows, headers=['i', 'stat', 'p', 'CI'], colalign=('center', 'center', 'center', 'center'),)
            dunnett_table_pad = "\n".join([l.ljust(max(len(s) for s in dunnett_table_str.splitlines())) for l in dunnett_table_str.splitlines()])
            plt.text(max_x, min_y-0.1*(max_y-min_y),
                    f"DUNNETT (control: {0})\n{dunnett_table_pad}",
                    ha='right', va='top', color=color_text, fontsize=font_size_analysis)

    # LEVENE test su due code
    if "levene" in a.type.lower():
        plt.subplots_adjust(bottom=0.25)

        # omnibus test (tra questi 3 gruppi ce differenza)
        dataserie_analysis_index = [idx for idx in dataserie.index if idx != -1] # exclude phase -1
        statistic, p_value = stats.levene(*dataserie.iloc[dataserie_analysis_index])
        plt.text(min_x, min_y-0.1*(max_y-min_y),
                f"LEVENE ({'-'.join([str(i) for i in dataserie_analysis_index])}):    {statistic:4.2f}\n └ p:              {p_value:6.4f}",
                ha='left', va='top', color=color_text, fontsize=font_size_analysis)

        # post hoc test 
        bonferroni_correction = 2 # p x 2 (due test complessivi)     
        for i, (g1, g2) in enumerate(combinations(dataserie_analysis_index, 2)):
            statistic, p_value = stats.levene(dataserie[g1], dataserie[g2])
            plt.text(min_x, min_y-0.16*(max_y-min_y)-0.06*(max_y-min_y)*i,
                    f"LEVENE ({g1}-{g2}):      {statistic:4.2f}\n └ p (Bonferroni): {p_value*bonferroni_correction:6.4f}",
                    ha='left', va='top', color=color_text, fontsize=font_size_analysis)
        
    # F test
    if "f-test" in a.type.lower():
        plt.subplots_adjust(bottom=0.2)

        # F di snedeco = tabulare
        # critical_value = stats.f.ppf(1 - 0.05 / 2, df1, df2)
        # if F > critical_value or F < 1 / critical_value:
        #     print("F: Reject the null hypothesis: The groups have significantly different standard deviations.")
        
        dataserie_analysis_index = [idx for idx in dataserie.index if idx != -1] # exclude phase -1
        bonferroni_correction = 2 # moltiplicato per 2 perche stiamo analizzando solo 2 fasi su tre alla volta
        for i, (g1, g2) in enumerate(combinations(dataserie[dataserie_analysis_index].index, 2)):
            F = np.var(dataserie[g1]) / np.var(dataserie[g2])
            df1 = len(dataserie[g1])-1
            df2 = len(dataserie[g2])-1
            coda_destra = 1-stats.f.cdf(F, df1, df2)
            # coda_sinistra = 1/stats.f.cdf(F, df1, df2)    # da berchialla
            coda_sinistra = 1-stats.f.cdf(F, df1, df2)      #!!! tmp
            p_value = coda_destra + coda_sinistra
            # print(f"F p (coda destra):     {coda_destra:7.10f}")
            # print(f"F p (coda sinistra):   {coda_sinistra:7.10f}")
            # print(f"F-test P totale ({g1}-{g2}): {p_value:7.10f}")
            # F p (coda destra):     0.0065897445
            # F p (coda sinistra):   1.0066334573
            # F-test P totale (0-1): 1.0132232018
            # F p (coda destra):     0.0000003322
            # F p (coda sinistra):   1.0000003322
            # F-test P totale (0-2): 1.0000006643
            # F p (coda destra):     0.0001874040
            # F p (coda sinistra):   1.0001874392
            # F-test P totale (1-2): 1.0003748432
            plt.text(min_x, min_y-0.1*(max_y-min_y)-0.06*(max_y-min_y)*i,
                    f"f-test ({g1}-{g2}):      {F:6.4f}\n └ p (Bonferroni): {p_value*bonferroni_correction:6.4f}",
                    ha='left', va='top', color=color_text, fontsize=font_size_analysis)
    
    # Adding labels and title
    plt.xlabel(a.predictor, fontsize=font_size_title)
    plt.ylabel((a.outcomeY if a.outcomeY != None else a.outcome),   fontsize=font_size_title)
    plt.title (a.title,     fontsize=font_size_title)
    plt.legend(             fontsize=font_size_legend)

    # Set axis ticks
    if all(isinstance(x, int) for x in dataframe):
        plt.yticks(np.arange(min(dataframe), max(dataframe)+1, 1))    # Set y-axis ticks to integers if all data is integer
    plt.xticks(summary[a.predictor])                        # Set x-axis ticks to follow a.predictor

    plt.grid(True, alpha=0.5)

    # save graph to file
    if save:
        save_path = os.path.join(script_dir, a.category, sanitize_filename(f"{a.title}.png"))
        if not os.path.exists(save_path):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)

    # save graph to variable
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')

    # show graph
    if show:
        plt.show()
    
    plt.close()

    return img_data
    
def sanitize_filename(filename):
    # Define a regular expression pattern to match characters not allowed in file names
    illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'  # Control characters are also not allowed
    
    # Replace illegal characters with underscores
    return re.sub(illegal_chars, '_', filename)

if __name__ == "__main__":
    main()