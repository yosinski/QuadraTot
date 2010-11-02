function plot_run(filename)
  % Plots the fitness over a run from a log file

  data = dlmread(filename);
  best = zeros(50,1);
  for i=2:50
    best(i,1) = max(best(i-1,1), data(i,6));
  end
  idx = find(data(:,6) == best(:, 1));
  plot(data(:,6), '-o', 'MarkerSize', 5);
  hold on;
  plot(best(:,1), 'r');
  plot(idx, best(idx,1), 'ro', 'MarkerSize', 5);
  title(filename);

