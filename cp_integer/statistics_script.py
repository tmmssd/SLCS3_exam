import subprocess
import os
import re

# Values of N
n_values = [8, 10, 12, 15, 20, 30, 40, 50]

# Output files
full_output_file = "results.txt"
summary_file = "solve_times.txt"

# Remove existing output files if they exist
if os.path.exists(full_output_file):
    os.remove(full_output_file)
if os.path.exists(summary_file):
    os.remove(summary_file)

# Write header for summary file
with open(summary_file, 'w') as f:
    f.write("N,SolveTime(s)\n")

# Run MiniZinc for each N value
for n in n_values:
    # Write to full results file
    with open(full_output_file, 'a') as f:
        f.write("=" * 30 + "\n")
        f.write(f"N = {n}\n")
        f.write("=" * 30 + "\n")
        
        # Run minizinc command
        result = subprocess.run(
            [
                'C:\\Program Files\\MiniZinc\\minizinc.exe',
                '--solver', 'gecode',
                '--statistics',
                'cp_integer.mzn',
                '-D', f'n={n}'
            ],
            capture_output=True,
            text=True
        )
        
        # Write full output to file
        f.write(result.stdout)
        if result.stderr:
            f.write(result.stderr)
    
    # Extract solve time from output
    solve_time = None
    # Look for patterns like "solveTime=0.123" or "time: 0.123"
    time_patterns = [
        r'solveTime[=:]\s*([\d.]+)',
        r'time[=:]\s*([\d.]+)',
        r'solving time[=:]\s*([\d.]+)'
    ]
    
    output_text = result.stdout + result.stderr
    for pattern in time_patterns:
        match = re.search(pattern, output_text, re.IGNORECASE)
        if match:
            solve_time = match.group(1)
            break
    
    # Write to summary file
    with open(summary_file, 'a') as f:
        if solve_time:
            f.write(f"{n},{solve_time}\n")
        else:
            f.write(f"{n},N/A\n")