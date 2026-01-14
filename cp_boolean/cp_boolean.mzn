int: n; % n of queens

array[1..n, 1..n] of var 0..1: x;


% row constraint
constraint forall(i in 1..n) (
    sum(j in 1..n)(x[i,j]) = 1
);

% column constraint
constraint forall(j in 1..n) (
    sum(i in 1..n)(x[i,j]) = 1
);

% (/) anti-diagonals constraint
constraint forall(k in 2..2*n) (
    sum(i, j in 1..n where i + j == k)(x[i,j]) <= 1
);

% (\) main diagonals constraint
constraint forall(k in (1-n)..(n-1)) (
    sum(i, j in 1..n where i - j == k)(x[i,j]) <= 1
);

solve satisfy;


output [
  if j = 1 then "\n" else " " endif ++
  if fix(x[i,j]) == 1 then "Q" else "." endif
  | i, j in 1..n
];