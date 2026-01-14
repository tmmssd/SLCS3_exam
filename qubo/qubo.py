from amplify import VariableGenerator, Model, solve, AmplifyAEClient
from datetime import timedelta
import amplify

def solve_n_queens(n, api_token):
    
    gen = VariableGenerator()
    q = gen.array("Binary", (n, n))
    
    H = 0.0

    # Row constraint
    for i in range(n):
        H += (amplify.sum(q[i, :]) - 1) ** 2
    
    # Column constraint
    for j in range(n):
        H += (amplify.sum(q[:, j]) - 1) ** 2

    # (\) diagonals
    for k in range(-(n - 1), n):
        
        diag_vars = []
        
        start_i = 0 if k >= 0 else -k
        end_i = n - k if k >= 0 else n
        
        for i in range(start_i, end_i):
            j = i + k
            diag_vars.append(q[i][j])
        
        # Apply penalty if diagonal has 2 or more queens
        # Formula: sum pairwise interactions = (Sum^2 - Sum) / 2
        if len(diag_vars) > 1:
            s = sum(diag_vars)
            H += (s ** 2 - s) / 2

    # (/) anti-diagonals 
    for k in range(2 * n - 1):

        anti_diag_vars = []
        
        start_i = max(0, k - (n - 1))
        end_i = min(n, k + 1)
        
        for i in range(start_i, end_i):
            j = k - i
            anti_diag_vars.append(q[i][j])

        if len(anti_diag_vars) > 1:
            s = sum(anti_diag_vars)
            H += (s ** 2 - s) / 2

    model = Model(H)

    client = AmplifyAEClient()
    client.token = api_token
    client.parameters.time_limit_ms = timedelta(milliseconds=1000)
    
    result = solve(model, client)
    
    return result


def benchmark_n_queens(token, start=8, stop=90, num=42):

    n_values = [8, 10, 12, 15, 20, 30, 40, 50]
    
    times = []
    best_times = []
    actual_n = []

    for n in n_values:        
        print(f"Solving for n={n}...")
        try:
            res = solve_n_queens(n, token)
            
            if res and res.best:
                exec_time = res.execution_time.total_seconds()
                best_time = res.best.time.total_seconds()
                times.append(exec_time)
                best_times.append(best_time)
                actual_n.append(n)
        except Exception as e:
            print(f"Failed at n={n}: {e}")
            
            
    output_file = "solve_times.txt"
    output_file2 = "best_solve_times.txt"

    with open(output_file, 'w') as f:
        f.write("N,SolveTime(s)\n")
        
        for n, solve_time in zip(n_values, times):
            f.write(f"{n},{solve_time}\n")
            
    with open(output_file2, 'w') as f:
        f.write("N,SolveTime(s)\n")
        
        for n, solve_time in zip(n_values, best_times):
            f.write(f"{n},{solve_time}\n")

TOKEN = "AE/y6cZxmt9p3y2Qk8x1jEOETCxmiO7qayF" 
benchmark_n_queens(TOKEN)

# print(solve_n_queens(8, TOKEN))