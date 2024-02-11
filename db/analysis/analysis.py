import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Connect to your SQLite database
script_dir = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(os.path.join(script_dir, f"..\positioning_test_data-(v1.26).db"))

# Query data from the database
query = "SELECT phase, brachial_artery FROM PA WHERE ECP_number = 1"
data = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

##########################################################

# Calculating mean and standard deviation for each phase
summary_stats = data.groupby('phase')['brachial_artery'].agg(['mean', 'std']).reset_index()

# Plotting
plt.figure(figsize=(10, 6))

# Plot mean values as a line with dots
plt.errorbar(summary_stats['phase'], summary_stats['mean'], yerr=summary_stats['std'], fmt='o', color='blue', label='Mean', markersize=8, capsize=5)

# Adding labels and title
plt.xlabel('Phase')
plt.ylabel('Value')
plt.title('Mean Value with Standard Deviation')
plt.legend()
plt.grid(False)

plt.show()