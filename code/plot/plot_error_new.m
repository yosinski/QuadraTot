function plot_error_new(files, saveFileName)

mark = {};
  mark{end+1} = '+';
  mark{end+1} = '+';
  mark{end+1} = '*';
  mark{end+1} = 'o';
  mark{end+1} = 'x';
  mark{end+1} = 'x';

clr = {};
  clr{end+1} = 'r';
  clr{end+1} = 'k';
  clr{end+1} = 'b';
  clr{end+1} = 'b';
  clr{end+1} = 'k';
  clr{end+1} = 'r';
  
figure(2); clf; hold on;
ax = zeros(4, 1);
ax(1) = 0; ax(2) = 80; ax(3) = 0; ax(4) = 20;
axis(ax);
fs = 30; %font size
xlabel("Iteration", "fontsize", fs);
ylabel("Body lengths/minute", "fontsize", fs);

%leg = cell(1, (((length(files))/3)-1));
leg = cell(1, (length(files)-6));

frac = 5;

for ii = 0:(((length(files))/3)-1)
  a = files{(ii * 3) + 1};
  b = files{(ii * 3) + 2};
  c = files{(ii * 3) + 3};
  [aN,aiteration,aparameters,afitness,abest] = load_run_data(a);
  [bN,biteration,bparameters,bfitness,bbest] = load_run_data(b);
  [cN,citeration,cparameters,cfitness,cbest] = load_run_data(c);
  
  legName = strrep (a, "_", "\\_");
  legName = substr(legName, 6, (length(legName) - 12));
  %leg{1, ii+1} = legName;
  leg{1, ii*2+1} = legName;
  leg{1, ii*2+2} = '';
  %leg{1, ii*2+3} = '';
  
  % find shortest
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
  % iteration now = 1:N
  
  % find mean
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
  
  
  
  % get every frac data point and the error for those points
  someMeans = zeros(N/frac, 1);
  someX = zeros(N/frac, 1);
  someSD = zeros(N/frac, 1);
  for i = 1:(N/frac)
    offset = mod(ii,3) - 1;
    someMeans(i) = means(i*frac + offset);
    someX(i) = x(i*frac + offset);
    someSD(i) = stdev(i*frac + offset);
  end
  
 % plot(someX, someMeans, mark{mod(ii,6)+1}, 'color', clr{mod(ii,6)+1});
  e = errorbar(someX, someMeans, someSD, '~');
  set(e, 'color', clr{mod(ii,6)+1});
  plot(means, 'color', clr{mod(ii,6)+1});
  
  %plot(iteration, best, '-', 'color', clr{mod(ii,6)+1});
  %e = errorbar(x, means, stdev);
  %set(e, "color", clr{mod(ii,6)+1});
  %plot(means, '@');

  %e = plot(x, means, 'linewidth', 2);
  %set(e, "color", clr{mod(ii,6)+1});
  %e = plot(x, means + stdev);
  %set(e, "color", clr{mod(ii,6)+1});
  %e = plot(x, means - stdev);
  %set(e, "color", clr{mod(ii,6)+1});
end

disp(leg);
legend(leg, "location", "best");
set(gca, "fontsize", fs);

% I think this causes problems...
%title('Mean and Standard Error', 'Interpreter', 'none');

% Save
print('-dpng', strcat(saveFileName, '.png'));
print('-depsc', strcat(saveFileName, '.eps'));
