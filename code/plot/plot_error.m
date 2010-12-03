function plot_error(files, saveFileName)

clr = {};
  clr{end+1} = 'k';
  clr{end+1} = 'r';
  clr{end+1} = 'g';
  clr{end+1} = 'b';
  clr{end+1} = 'c';
  clr{end+1} = 'm';
%  clr{end+1} = 'y';

figure(2); clf; hold on;
ax = zeros(4, 1);
ax(1) = 0; ax(2) = 80; ax(3) = 0; ax(4) = 20;
axis(ax);
xlabel("Iteration");
ylabel("Body lengths/minute");

leg = cell(1, 6);

for ii = 0:5
  a = files{(ii * 3) + 1};
  b = files{(ii * 3) + 2};
  c = files{(ii * 3) + 3};
  [aN,aiteration,aparameters,afitness,abest] = load_run_data(a);
  [bN,biteration,bparameters,bfitness,bbest] = load_run_data(b);
  [cN,citeration,cparameters,cfitness,cbest] = load_run_data(c);
  
  leg{1, ii+1} = strrep (a, "_", "\\_");
  
  %find shortest
  N = min(aN, bN);
  N = min(N, cN);
  iteration = zeros(0, 0);
  if N == length(aiteration)
    iteration = aiteration;
  elseif N == length(biteration)
    iteration = biteration;
  else
    iteration = citeration;
  endif
  
  %find mean
  means = zeros(N, 1);
  stdev = zeros(N, 1);
  x = zeros(N, 1);
  for i = 1:N
    v = zeros(3, 1);
    v(1) = abest(i);
    v(2) = bbest(i);
    v(3) = cbest(i);
    means(i) = (abest(i) + bbest(i) + cbest(i)) / 3;
    stdev(i) = std(v) / sqrt(3);
    x(i) = i + (.03 * ii);
  end
  
  %plot(iteration, best, '-', 'color', clr{mod(ii,6)+1});
  e = errorbar(x, means, stdev);
  set(e, "color", clr{mod(ii,6)+1});

  %e = plot(x, means, 'linewidth', 2);
  %set(e, "color", clr{mod(ii,6)+1});
  %e = plot(x, means + stdev);
  %set(e, "color", clr{mod(ii,6)+1});
  %e = plot(x, means - stdev);
  %set(e, "color", clr{mod(ii,6)+1});
end

legend(leg);

% I think this causes problems...
%title('Mean and Standard Error', 'Interpreter', 'none');

% Save
print('-dpng', strcat(saveFileName, '.png'));
print('-depsc', strcat(saveFileName, '.eps'));
