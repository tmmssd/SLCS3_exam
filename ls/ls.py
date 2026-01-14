import random
import time
    

def solve_n_queens(n, max_restarts=10, max_steps=100000):
    start_time = time.time()

    for _ in range(max_restarts):
        state = list(range(n))
        random.shuffle(state)
        
        pos_diag = [0] * (2 * n)
        neg_diag = [0] * (2 * n)

        for r, c in enumerate(state):
            pos_diag[r + c] += 1
            neg_diag[r - c + n] += 1

        for _ in range(max_steps):
            conflicted_queens = [r for r in range(n) if pos_diag[r + state[r]] > 1 or neg_diag[r - state[r] + n] > 1]

            if not conflicted_queens:
                return state, time.time() - start_time

            i = random.choice(conflicted_queens)
            
            best_j = -1
            max_improvement = -1
            
            search_space = random.sample(range(n), min(n, 100)) 
            
            for j in search_space:
                if i == j: continue
                
                improvement = calculate_swap_improvement(i, j, state, pos_diag, neg_diag, n)
                
                if improvement > max_improvement:
                    max_improvement = improvement
                    best_j = j
                elif improvement == max_improvement and improvement > 0:
                    if random.random() > 0.5:
                        best_j = j

            if best_j != -1 and max_improvement >= 0:
                perform_swap(i, best_j, state, pos_diag, neg_diag, n)
            else:
                break 
        

def calculate_swap_improvement(i, j, state, pos_diag, neg_diag, n):
    c_i, c_j = state[i], state[j]
    
    # Calculate diagonal indices for both queens
    p1, n1 = i + c_i, i - c_i + n
    p2, n2 = j + c_j, j - c_j + n
    p3, n3 = i + c_j, i - c_j + n
    p4, n4 = j + c_i, j - c_i + n

    # Current diagonal conflicts for rows i and j
    old_c = (pos_diag[p1] - 1) + (neg_diag[n1] - 1) + (pos_diag[p2] - 1) + (neg_diag[n2] - 1)
    
    # Simulate swap
    pos_diag[p1] -= 1; neg_diag[n1] -= 1
    pos_diag[p2] -= 1; neg_diag[n2] -= 1
    pos_diag[p3] += 1; neg_diag[n3] += 1
    pos_diag[p4] += 1; neg_diag[n4] += 1
    
    new_c = (pos_diag[p3] - 1) + (neg_diag[n3] - 1) + (pos_diag[p4] - 1) + (neg_diag[n4] - 1)
    
    # Revert trackers
    pos_diag[p3] -= 1; neg_diag[n3] -= 1
    pos_diag[p4] -= 1; neg_diag[n4] -= 1
    pos_diag[p1] += 1; neg_diag[n1] += 1
    pos_diag[p2] += 1; neg_diag[n2] += 1
    
    return old_c - new_c

def perform_swap(i, j, state, pos_diag, neg_diag, n):
    c_i, c_j = state[i], state[j]
    pos_diag[i + c_i] -= 1; neg_diag[i - c_i + n] -= 1
    pos_diag[j + c_j] -= 1; neg_diag[j - c_j + n] -= 1
    
    state[i], state[j] = c_j, c_i
    
    pos_diag[i + state[i]] += 1; neg_diag[i - state[i] + n] += 1
    pos_diag[j + state[j]] += 1; neg_diag[j - state[j] + n] += 1


if __name__ == "__main__":
    n_values = [8, 10, 12, 15, 20, 30, 40, 50]
    results = []
    
    for n in n_values:
        solution, duration = solve_n_queens(n)
        
        if solution:
            print(f"Solved for N={n} in {duration:.6f} seconds!")
        else:
            print("Could not find a solution within the step limit.")
        results.append(duration)
    
    output_file = "solve_times.txt"

    with open(output_file, 'w') as f:
        f.write("N,SolveTime(s)\n")
        
        for n, solve_time in zip(n_values, results):
            f.write(f"{n},{solve_time}\n")