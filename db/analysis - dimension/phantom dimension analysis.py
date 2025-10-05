import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
from tabulate import tabulate

# Setup
script_dir = os.path.dirname(os.path.realpath(__file__))
plt.rcParams['font.family'] = 'Courier New'

# Color palette function from your original script
def palette_hsv(num_colors, saturation=0.5, brightness=0.9):
    """
    Generate a pastel-like color palette based on the HSV colormap.
    """
    num_colors += 1
    cmap = plt.get_cmap('hsv', num_colors) 
    palette = []
    for i in range(num_colors):
        rgb = cmap(i)[:3]
        hsv = mcolors.rgb_to_hsv(rgb)
        hsv[1] = saturation
        hsv[2] = brightness
        pastel_rgb = mcolors.hsv_to_rgb(hsv)
        pastel_hex = mcolors.rgb2hex(pastel_rgb)
        palette.append(pastel_hex)
    return palette[:-1]

# Generate palette
palette = palette_hsv(7)
print("palette:", palette)

# Connect to database and get data
db_path = os.path.join(script_dir, "..\\positioning_test_data-(v1.27).db")

try:
    conn = sqlite3.connect(db_path)
    
    # First, check what tables exist
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\n" + "="*70)
    print("AVAILABLE TABLES IN DATABASE:")
    print("-"*70)
    for table in tables:
        print(f"  - {table[0]}")
    
    # Try to find the phantom table or similar
    phantom_table = None
    for table in tables:
        if 'phantom' in table[0].lower():
            phantom_table = table[0]
            break
    
    if phantom_table:
        print(f"\nFound phantom table: {phantom_table}")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({phantom_table})")
        columns = cursor.fetchall()
        print(f"\nColumns in {phantom_table}:")
        for col in columns:
            print(f"  - '{col[1]}' ({col[2]})")  # Added quotes to see spaces
        
        # Try to get the data
        query = f"SELECT * FROM {phantom_table}"
        df = pd.read_sql_query(query, conn)
        
        # Print actual column names from dataframe
        print("\nActual DataFrame columns:")
        for col in df.columns:
            print(f"  - '{col}' (length: {len(col)})")
    else:
        print("\nNo phantom table found")
    
    conn.close()
    
except sqlite3.Error as e:
    print(f"\nDatabase error: {e}")
    quit()

# Print the data for manual confirmation
print("\n" + "="*70)
print("DATA CONFIRMATION")
print("="*70)

# Define the measurement columns we want
measurement_cols = ["M:2-M:3", "M:3-M:4", "M:7-M:8", "M:8-M:9", 
                   "M:2-M:7", "M:3-M:8", "M:4-M:9"]

# Create a mapping to handle column name variations (with/without spaces)
column_mapping = {}
for desired_col in measurement_cols:
    for actual_col in df.columns:
        # Strip spaces and compare
        if desired_col.replace(" ", "") == actual_col.replace(" ", "").replace(":", ":"):
            column_mapping[desired_col] = actual_col
            break
        # Also try exact match
        elif desired_col == actual_col.strip():
            column_mapping[desired_col] = actual_col
            break

print(f"\nColumn mapping:")
for desired, actual in column_mapping.items():
    print(f"  '{desired}' -> '{actual}'")

# Rename columns to standardized names
for desired, actual in column_mapping.items():
    if actual in df.columns and desired != actual:
        df[desired] = df[actual]
        if actual != desired:  # Don't drop if they're the same
            df = df.drop(columns=[actual])

# Now check available columns
available_cols = [col for col in measurement_cols if col in df.columns]
print(f"\nAvailable measurement columns after mapping: {available_cols}")

# Display the data in a nice table format
if available_cols:
    display_cols = ['id'] + available_cols if 'id' in df.columns else available_cols
    print("\nData Table:")
    print(tabulate(df[display_cols], headers='keys', tablefmt='grid', floatfmt=".3f"))

# Define short and long distance groups
short_distances = ["M:2-M:3", "M:3-M:4", "M:7-M:8", "M:8-M:9"]
long_distances = ["M:2-M:7", "M:3-M:8", "M:4-M:9"]

# Function to create a plot for a group of measurements
def create_measurement_plot(df, measurement_list, title, filename, palette):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Font sizes
    font_size_title = 18
    font_size_label = 14
    font_size_tick = 11
    font_size_text = 10
    
    # Prepare data
    all_data = []
    all_positions = []
    all_labels = []
    
    for idx, col in enumerate(measurement_list):
        if col in df.columns:
            values = df[col].dropna().values
            if len(values) > 0:  # Only add if we have data
                all_data.append(values)
                all_positions.append(idx)
                all_labels.append(col)
            else:
                print(f"  Warning: Column '{col}' has no data")
        else:
            print(f"  Warning: Column '{col}' not found in dataframe")
    
    if not all_data:
        print(f"No data available for {title}")
        return
    
    print(f"\nCreating plot for {title} with {len(all_data)} measurements")
    
    # Create violin plots
    parts = ax.violinplot(all_data, positions=all_positions, widths=0.7,
                          showmeans=False, showmedians=False, showextrema=False)
    
    for pc, color in zip(parts['bodies'], palette[:len(parts['bodies'])]):
        pc.set_facecolor(color)
        pc.set_alpha(0.3)
        pc.set_edgecolor('black')
        pc.set_linewidth(0.5)
    
    # Create box plots
    bp = ax.boxplot(all_data, positions=all_positions, widths=0.35,
                   patch_artist=True, notch=False,
                   boxprops=dict(alpha=0.6),
                   whiskerprops=dict(color='black', linewidth=1.2),
                   capprops=dict(color='black', linewidth=1.2),
                   medianprops=dict(color=palette[2], linewidth=2.5),
                   flierprops=dict(marker='o', markersize=4, alpha=0.5))
    
    # Color each box
    for patch, color in zip(bp['boxes'], palette[:len(bp['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    # Add scattered points with jitter
    np.random.seed(42)
    for idx, data in enumerate(all_data):
        jitter = np.random.normal(0, 0.08, size=len(data))
        x_positions = np.full(len(data), all_positions[idx]) + jitter
        ax.scatter(x_positions, data, alpha=0.7, s=30, color='black', zorder=3)
    
    # Add mean markers
    means = [np.mean(data) for data in all_data]
    ax.scatter(all_positions, means, color=palette[0], s=150, marker='D', 
              zorder=4, edgecolor='black', linewidth=1.5)
    
    # Formatting
    ax.set_xticks(all_positions)
    ax.set_xticklabels(all_labels, fontsize=font_size_tick, rotation=0)
    ax.set_xlabel('Measurement Type', fontsize=font_size_label, fontweight='bold')
    ax.set_ylabel('Distance (mm)', fontsize=font_size_label, fontweight='bold')
    ax.set_title(title, fontsize=font_size_title, fontweight='bold', pad=20)
    
    # Add grid
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)
    
    # Add statistics annotations
    for i, (pos, data) in enumerate(zip(all_positions, all_data)):
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        
        # Add n at the bottom
        ax.text(pos, ax.get_ylim()[0] + 0.01 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
               f'n={n}', ha='center', va='bottom', fontsize=font_size_text)
        
        # Add mean and std at the top
        ax.text(pos, ax.get_ylim()[1] - 0.02 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
               f'μ={mean:.1f}\nσ={std:.2f}', ha='center', va='top', 
               fontsize=font_size_text-1,
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Create legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
               markersize=6, alpha=0.7, label='Data points'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor=palette[0], 
               markeredgecolor='black', markersize=10, label='Mean'),
        Line2D([0], [0], color=palette[2], linewidth=2.5, label='Median'),
        Line2D([0], [0], color=palette[3], linewidth=10, alpha=0.6, label='IQR (Box)'),
        Line2D([0], [0], color='black', linewidth=1.2, label='Whiskers'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=font_size_text)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    save_path = os.path.join(script_dir, filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.2)
    print(f"Saved: {filename}")
    plt.show()

# Create the two plots
print("\n" + "="*70)
print("CREATING PLOTS")
print("="*70)

# Plot 1: Short distances
create_measurement_plot(df, short_distances, 
                       'Phantom Marker Measurements', 
                       'phantom_measurements_2.png',
                       palette)

# Plot 2: Long distances
create_measurement_plot(df, long_distances,
                       'Phantom Marker Measurements',
                       'phantom_measurements_1.png',
                       palette)

# Print summary statistics for both groups
print("\n" + "="*70)
print("SUMMARY STATISTICS BY GROUP")
print("="*70)

print("\nShort Distances (Pin-to-Pin):")
print("-"*40)
print(f"{'Measurement':<12} {'Mean':<10} {'Std':<10} {'Min':<10} {'Max':<10}")
for col in short_distances:
    if col in df.columns:
        data = df[col].dropna()
        if len(data) > 0:
            print(f"{col:<12} {data.mean():<10.3f} {data.std():<10.3f} {data.min():<10.3f} {data.max():<10.3f}")
    else:
        print(f"{col:<12} NOT FOUND")

print("\nLong Distances (Diagonal):")
print("-"*40)
print(f"{'Measurement':<12} {'Mean':<10} {'Std':<10} {'Min':<10} {'Max':<10}")
for col in long_distances:
    if col in df.columns:
        data = df[col].dropna()
        if len(data) > 0:
            print(f"{col:<12} {data.mean():<10.3f} {data.std():<10.3f} {data.min():<10.3f} {data.max():<10.3f}")
    else:
        print(f"{col:<12} NOT FOUND")