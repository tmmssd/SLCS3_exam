include "alldifferent.mzn";

int: n; % n of queens

array[1..n] of var 1..n: q;


% column constraint
constraint alldifferent(q);

% (/) anti-diagonals constraint
constraint alldifferent([ q[i] + i | i in 1..n ]);

% (\) main diagonals constraint
constraint alldifferent([ q[i] - i | i in 1..n ]);

% --- Solve Goal ---
% ":: domain" annotation encourages the solver to branch on the variable domain
% When you are guessing where to put queens, look at the array q. Always pick the row that has the fewest legal spots left (first_fail). When you pick a spot for that row, try the left-most column first (indomain_min).
solve :: int_search(q, first_fail, indomain_min) satisfy;

output [
  if j = 1 then "\n" else " " endif ++
  if fix(q[i]) = j then "Q" else "." endif
  | i, j in 1..n
];