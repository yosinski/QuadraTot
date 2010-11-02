function plot_several_runs(files)
  % Plots the fitness of two runs together

  clr = {};
  clr{end+1} = 'b';
  clr{end+1} = 'r';
  clr{end+1} = 'g';
  clr{end+1} = 'm';
  clr{end+1} = 'r';

  figure(1); clf; hold on;

  titl = '';
  for ii = 1:length(files)
    file = files{ii};
    if ii ~= 1
      titl = strcat(titl, ' ');
    end
    titl = strcat(titl, file);

    [N,iteration,parameters,fitness,best] = load_run_data(file);

    % Plot
    %plot(iteration, fitness, '-o', 'MarkerSize', 5);
    plot(iteration, best, '-', 'color', clr{ii});
    %idx = find(fitness == best);
    %plot(idx, best(idx), 'o', 'Color', clr{ii}, 'MarkerSize', 5);
  end

  title(titl, 'Interpreter', 'none');
  legend(files);

  for ii = 1:length(files)
    file = files{ii};
    [N,iteration,parameters,fitness,best] = load_run_data(file);
    idx = find(fitness == best);
    plot(idx, best(idx), 'o', 'Color', clr{ii}, 'MarkerSize', 5);
  end


  % Save
  print('-dpng', strcat(titl, '.png'));
  print('-depsc', strcat(titl, '.eps'));

end
