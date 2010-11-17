function plot_run(filename)
  % Plots the fitness over a run from a log file

  [N,iteration,parameters,fitness,best] = load_run_data(filename);

  % Plot
  figure(1); clf; hold on;
  plot(iteration, fitness, '-o', 'MarkerSize', 5);
  plot(best(:,1), 'r');
  idx = find(fitness == best);
  plot(idx, best(idx), 'ro', 'MarkerSize', 5);
  for ii = 1:length(idx)
    disp(sprintf('ii = %3d, fitness = %g', idx(ii), best(idx(ii))));
  end
  title(filename, 'Interpreter', 'none');
  legend(filename);

  % Save
  print('-dpng', strcat(filename, '.png'));
  print('-depsc', strcat(filename, '.eps'));

end

