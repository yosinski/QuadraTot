function plot_explore(file)
  % Plots the fitness of an exploration run

  %clr = {};
  %clr{end+1} = 'c';
  %clr{end+1} = 'r';
  %clr{end+1} = 'g';
  %clr{end+1} = 'b';
  %clr{end+1} = 'k';
  %clr{end+1} = 'm';
  %  clr{end+1} = 'y';

  [N,iteration,dimIdx,pointIdx,dupIdx,params,fitness,best] = load_explore_data(file);

  dimensions   = length(unique(sort(dimIdx)));
  pointsPer    = length(unique(sort(pointIdx)));
  duplications = length(unique(sort(dupIdx)));

  if (dimensions * pointsPer * duplications ~= N)
    error('something wrong');
  end

  centerPoint = [];
  for ii = 1:dimensions
    centerPoint(end+1) = params(mod((ii)*(pointsPer*duplications), N) + 1, ii);
  end

  for ii = 1:dimensions
    figure(ii); clf;
    pIdx = ((ii-1)*(pointsPer*duplications)+1) : ((ii)*(pointsPer*duplications));
    thisParams  = params(pIdx,:);
    thisFitness = fitness(pIdx,:);
    fits = [thisFitness(1:2:end) thisFitness(2:2:end)];     % HACK: only works for 2 dups
    
    %mean(fits, 2)
    %std(fits, 0, 2)

    % HACK: only works for 2 dups
    errorbar(thisParams(1:2:end,ii), mean(fits, 2), std(fits, 0, 2), ">");
    title(sprintf('varying param %d', ii));

    %forplot = []
    %for jj = 1:pointsPer
    %  keyboard;
    %  first = pIdx(1) + (jj-1)*  1234;
    %  forplot(end+1) = 3
    %end

    % Save
    titl = sprintf('%s_dim_%d', file, ii);
    disp(sprintf('Saving as %s', titl));
    print('-dpng', strcat(titl, '.png'));
    print('-depsc', strcat(titl, '.eps'));

  end
  

end
