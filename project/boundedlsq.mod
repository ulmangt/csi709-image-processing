model;

# number of constraints
param l;

# number of pixels in high definition image
param n;

# output vector (0 to 255 pixel intensities from low resolution image)
param y { 1..l };

# input data
param x { 1..l, 1..n };

# problem variables and simple constraints (high definition pixel intensities
var a {1..n} >= 0, <= 255;

minimize obj: sum { i in 1..l } ( ( y[i] - sum { j in 1..n } ( x[i,j] * a[j] ) )^2 );

option solver loqo;
