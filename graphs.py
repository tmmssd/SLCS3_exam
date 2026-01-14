import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists('analysis'):
    os.makedirs('analysis')

folders = ['cp_boolean', 'cp_integer', 'ls', 'qubo']
model_names = ['CP Boolean', 'CP Integer', 'Local Search', 'QUBO']
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']

data = {}
for folder, name in zip(folders, model_names):
    file_path = os.path.join(folder, 'solve_times.txt')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['SolveTime(s)'] = pd.to_numeric(df['SolveTime(s)'], errors='coerce')
        # Replace 0.0 with a very small value to avoid division by zero
        df['SolveTime(s)'] = df['SolveTime(s)'].replace(0.0, 0.0001)
        data[name] = df

# Load QUBO best solve times
qubo_best_data = None
best_file_path = os.path.join('qubo', 'best_solve_times.txt')
if os.path.exists(best_file_path):
    qubo_best_data = pd.read_csv(best_file_path)
    qubo_best_data['SolveTime(s)'] = pd.to_numeric(qubo_best_data['SolveTime(s)'], errors='coerce')
    qubo_best_data['SolveTime(s)'] = qubo_best_data['SolveTime(s)'].replace(0.0, 0.0001)

# MAIN COMPARISON GRAPHS
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
# fig.suptitle('Model Performance Comparison', fontsize=18, fontweight='bold')

# Log-scale plot
ax1 = fig.add_subplot(gs[0, :])
for (name, df), color in zip(data.items(), colors):
    ax1.plot(df['N'], df['SolveTime(s)'], marker='o', label=name, 
             linewidth=2.5, markersize=8, color=color)
# Add QUBO best times if available
if qubo_best_data is not None:
    ax1.plot(qubo_best_data['N'], qubo_best_data['SolveTime(s)'], 
             marker='s', label='QUBO (Best Found)', linewidth=2.5, 
             markersize=8, color='#9b59b6', linestyle='--')
ax1.set_xlabel('Problem Size (N)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Solve Time (seconds, log scale)', fontsize=13, fontweight='bold')
ax1.set_title('Solve Time vs Problem Size - All Models (Log Scale)', fontsize=15)
ax1.set_yscale('log')
ax1.legend(fontsize=11, loc='upper left')
ax1.grid(True, alpha=0.3, which='both', linestyle='--')

# Linear plot - Fast models
ax2 = fig.add_subplot(gs[1, 0])
fast_models = ['Local Search', 'CP Integer']
for name, df in data.items():
    if name in fast_models:
        color = colors[model_names.index(name)]
        ax2.plot(df['N'], df['SolveTime(s)'], marker='o', label=name, 
                 linewidth=2.5, markersize=8, color=color)
ax2.set_xlabel('Problem Size (N)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Solve Time (seconds)', fontsize=12, fontweight='bold')
ax2.set_title('Fast Models: LS vs CP Integer', fontsize=14)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3, linestyle='--')

# Linear plot - Slow models
ax3 = fig.add_subplot(gs[1, 1])
slow_models = ['CP Boolean', 'QUBO']
for name, df in data.items():
    if name in slow_models:
        color = colors[model_names.index(name)]
        ax3.plot(df['N'], df['SolveTime(s)'], marker='o', label=name, 
                 linewidth=2.5, markersize=8, color=color)
# Add QUBO best times
if qubo_best_data is not None:
    ax3.plot(qubo_best_data['N'], qubo_best_data['SolveTime(s)'], 
             marker='s', label='QUBO (Best)', linewidth=2.5, 
             markersize=8, color='#9b59b6', linestyle='--')
ax3.set_xlabel('Problem Size (N)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Solve Time (seconds)', fontsize=12, fontweight='bold')
ax3.set_title('Slow Models + QUBO Best Time', fontsize=14)
ax3.legend(fontsize=11)
ax3.grid(True, alpha=0.3, linestyle='--')

# Performance largest N
ax4 = fig.add_subplot(gs[2, :])
if data:
    largest_n_times = []
    names_list = []
    for name, df in data.items():
        largest_n_times.append(df['SolveTime(s)'].iloc[-1])
        names_list.append(name)
    
    # Add QUBO best time
    if qubo_best_data is not None:
        largest_n_times.append(qubo_best_data['SolveTime(s)'].iloc[-1])
        names_list.append('QUBO (Best)')
    
    sorted_indices = sorted(range(len(largest_n_times)), key=lambda i: largest_n_times[i])
    sorted_names = [names_list[i] for i in sorted_indices]
    sorted_times = [largest_n_times[i] for i in sorted_indices]
    
    # Assign colors
    sorted_colors = []
    for name in sorted_names:
        if name == 'QUBO (Best)':
            sorted_colors.append('#9b59b6')
        else:
            sorted_colors.append(colors[model_names.index(name)])
    
    bars = ax4.barh(sorted_names, sorted_times, color=sorted_colors, alpha=0.8, edgecolor='black')
    ax4.set_xlabel('Solve Time (seconds)', fontsize=12, fontweight='bold')
    ax4.set_title(f'Performance at Largest Problem Size (N={df["N"].iloc[-1]})', fontsize=14)
    ax4.grid(True, alpha=0.3, axis='x', linestyle='--')
    
    for bar, time in zip(bars, sorted_times):
        ax4.text(time, bar.get_y() + bar.get_height()/2, f' {time:.3f}s', 
                va='center', fontsize=10, fontweight='bold')

plt.savefig('analysis/model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# INDIVIDUAL MODEL ANALYSIS
for name, df in data.items():
    color = colors[model_names.index(name)]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    # fig.suptitle(f'{name} - Detailed Analysis', fontsize=16, fontweight='bold')
    
    # Solve time vs N (Linear scale)
    ax1 = axes[0]
    ax1.plot(df['N'], df['SolveTime(s)'], marker='o', color=color, linewidth=2.5, markersize=8)
    ax1.fill_between(df['N'], df['SolveTime(s)'], alpha=0.3, color=color)
    ax1.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Solve Time (seconds)', fontsize=11, fontweight='bold')
    ax1.set_title('Solve Time vs Problem Size', fontsize=13)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Solve time vs N (Log scale)
    ax2 = axes[1]
    ax2.plot(df['N'], df['SolveTime(s)'], marker='o', color=color, linewidth=2.5, markersize=8)
    ax2.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Solve Time (seconds, log scale)', fontsize=11, fontweight='bold')
    ax2.set_title('Solve Time vs Problem Size (Log Scale)', fontsize=13)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, which='both', linestyle='--')
    
    # Growth rate
    ax3 = axes[2]
    if len(df) > 1:
        growth_rate = df['SolveTime(s)'].diff() / df['N'].diff()
        growth_rate = growth_rate.replace([float('inf'), -float('inf')], float('nan'))
        ax3.plot(df['N'].iloc[1:], growth_rate.iloc[1:], marker='o', color=color, 
                linewidth=2.5, markersize=8)
        ax3.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Time Increase per Unit N', fontsize=11, fontweight='bold')
        ax3.set_title('Growth Rate Analysis', fontsize=13)
        ax3.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    safe_name = name.lower().replace(' ', '_')
    plt.savefig(f'analysis/{safe_name}_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# DEDICATED QUBO BEST TIME ANALYSIS
if 'QUBO' in data and qubo_best_data is not None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    # fig.suptitle('QUBO: Full Runtime vs Best Solution', fontsize=16, fontweight='bold')
    
    qubo_full = data['QUBO']
    
    # Plot 1: QUBO Full Runtime vs Best Solution Time
    ax1 = axes[0]
    ax1.plot(qubo_full['N'], qubo_full['SolveTime(s)'], marker='o', 
             label='Full Runtime', linewidth=2.5, markersize=8, color='#f39c12')
    ax1.plot(qubo_best_data['N'], qubo_best_data['SolveTime(s)'], marker='s', 
             label='Time to Best Solution', linewidth=2.5, markersize=8, 
             color='#9b59b6', linestyle='--')
    ax1.fill_between(qubo_best_data['N'], qubo_best_data['SolveTime(s)'], 
                      qubo_full['SolveTime(s)'], alpha=0.2, color='#e74c3c', 
                      label='Wasted Time')
    ax1.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
    ax1.set_title('QUBO: Full Runtime vs Time to Find Best Solution', fontsize=13)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Plot 2: QUBO Efficiency: Percentage of time wasted
    ax2 = axes[1]
    efficiency = (qubo_best_data['SolveTime(s)'] / qubo_full['SolveTime(s)']) * 100
    wasted = 100 - efficiency
    
    ax2.plot(qubo_best_data['N'], efficiency, marker='o', linewidth=2.5, 
             markersize=8, color='#2ecc71', label='Useful Time %')
    ax2.plot(qubo_best_data['N'], wasted, marker='s', linewidth=2.5, 
             markersize=8, color='#e74c3c', label='Wasted Time %')
    ax2.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Percentage of Runtime (%)', fontsize=11, fontweight='bold')
    ax2.set_title('QUBO: Time Efficiency Analysis', fontsize=13)
    ax2.set_ylim([0, 105])
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # Plot 3: Speedup if QUBO stopped at best solution
    ax3 = axes[2]
    speedup = qubo_full['SolveTime(s)'] / qubo_best_data['SolveTime(s)']
    ax3.plot(qubo_best_data['N'], speedup, marker='o', linewidth=2.5, 
             markersize=8, color='#3498db')
    ax3.axhline(y=1, color='gray', linestyle='--', linewidth=2, alpha=0.7, 
                label='No improvement')
    ax3.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Speedup Factor', fontsize=11, fontweight='bold')
    ax3.set_title('Potential Speedup if QUBO Stopped at Best Solution', fontsize=13)
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('analysis/qubo_runtime_vs_best.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    
    
    
    
    
    
    
    # INDIVIDUAL MODEL ANALYSIS
    name = 'QUBO Best'
    color = '#9b59b6'
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    # fig.suptitle(f'{name} - Detailed Analysis', fontsize=16, fontweight='bold')
    
    # Solve time vs N (Linear scale)
    ax1 = axes[0]
    ax1.plot(qubo_best_data['N'], qubo_best_data['SolveTime(s)'], marker='o', color=color, linewidth=2.5, markersize=8)
    ax1.fill_between(qubo_best_data['N'], qubo_best_data['SolveTime(s)'], alpha=0.3, color=color)
    ax1.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Solve Time (seconds)', fontsize=11, fontweight='bold')
    ax1.set_title('Solve Time vs Problem Size', fontsize=13)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Solve time vs N (Log scale)
    ax2 = axes[1]
    ax2.plot(qubo_best_data['N'], qubo_best_data['SolveTime(s)'], marker='o', color=color, linewidth=2.5, markersize=8)
    ax2.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Solve Time (seconds, log scale)', fontsize=11, fontweight='bold')
    ax2.set_title('Solve Time vs Problem Size (Log Scale)', fontsize=13)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, which='both', linestyle='--')
    
    # Growth rate
    ax3 = axes[2]
    if len(qubo_best_data) > 1:
        growth_rate = qubo_best_data['SolveTime(s)'].diff() / qubo_best_data['N'].diff()
        growth_rate = growth_rate.replace([float('inf'), -float('inf')], float('nan'))
        ax3.plot(qubo_best_data['N'].iloc[1:], growth_rate.iloc[1:], marker='o', color=color, 
                linewidth=2.5, markersize=8)
        ax3.set_xlabel('Problem Size (N)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Time Increase per Unit N', fontsize=11, fontweight='bold')
        ax3.set_title('Growth Rate Analysis', fontsize=13)
        ax3.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    safe_name = name.lower().replace(' ', '_')
    plt.savefig(f'analysis/{safe_name}_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    


print("Analysis complete! Graphs saved to 'analysis/' directory.")