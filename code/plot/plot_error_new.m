function plot_error_new(files, saveFileName)

mark = {};
  mark{end+1} = 'v';
  mark{end+1} = 's';
  mark{end+1} = 'd';%<
  mark{end+1} = 'o';
  mark{end+1} = '.';%>
  mark{end+1} = '^';

mark2 = {};
  mark2{end+1} = '-v';
  mark2{end+1} = '-s';
  mark2{end+1} = '-d';
  mark2{end+1} = '-o';
  mark2{end+1} = '-.';
  mark2{end+1} = '-^';

clr = {};
  clr{end+1} = 'r';
  clr{end+1} = 'k';
  clr{end+1} = 'b';
  clr{end+1} = [0.5, 0.75, 0.15];%green
  clr{end+1} = [.3, 0, .5]; %purple
  clr{end+1} = [1 128/255, 0];%pumpkin
  
figure(2); clf; hold on;
ax = zeros(4, 1);
ax(1) = 0; ax(2) = 80; ax(3) = 0; ax(4) = 20;
axis(ax);
fs = 30; %font size
xlabel("Iteration", "fontsize", fs);
ylabel("Body lengths per minute", "fontsize", fs);
set(gcf, 'DefaultLineLineWidth', 2.5);

%leg = cell(1, (((length(files))/3)-1));
leg = cell(1, 6);

frac = 15;
markSize = 11;

for ii = 0:(((length(files))/3)-1)
  a = files{(ii * 3) + 1};
  b = files{(ii * 3) + 2};
  c = files{(ii * 3) + 3};
  [aN,aiteration,aparameters,afitness,abest] = load_run_data(a);
  [bN,biteration,bparameters,bfitness,bbest] = load_run_data(b);
  [cN,citeration,cparameters,cfitness,cbest] = load_run_data(c);
  
  legName = strrep (a, "_", "\\_");
  legName = substr(legName, 6, (length(legName) - 12));
  leg{1, ii+1} = legName;
  
  plot([-10, -9], [-10, -9], mark2{mod(ii,6)+1}, 'color', clr{mod(ii,6)+1}, 'MarkerFaceColor', clr{mod(ii,6)+1});
end

for ii = 0:(((length(files))/3)-1)
  a = files{(ii * 3) + 1};
  b = files{(ii * 3) + 2};
  c = files{(ii * 3) + 3};
  [aN,aiteration,aparameters,afitness,abest] = load_run_data(a);
  [bN,biteration,bparameters,bfitness,bbest] = load_run_data(b);
  [cN,citeration,cparameters,cfitness,cbest] = load_run_data(c);
  
  
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
  fracLen = 2;
  someMeans = zeros(fracLen, 1);
  someX = zeros(fracLen, 1);
  someSD = zeros(fracLen, 1);
  for i = 1:fracLen
    ind = round(i * N/2);
    if (ii == 2 && i == 1)
      ind = ind - 2;
    elseif (ii==2)
      ind = ind -1;
    end
    someMeans(i) = means(ind);
    someX(i) = x(ind);
    %someX(i) = x(ind);
    someSD(i) = stdev(ind);
  end
  
  e = errorbar(someX, someMeans, someSD);
  %set(e, 'linestyle', 'none');
  %set(e, 'color', clr{mod(ii,6)+1}, 'markerSize', markSize);
  set(e, 'color', clr{mod(ii,6)+1}, 'marker', '.');
  plot(means, 'color', clr{mod(ii,6)+1});
  plot(someX, someMeans, mark{mod(ii,6)+1}, 'color', clr{mod(ii,6)+1}, 'MarkerFaceColor', 'k', 'markerSize', markSize);
end

disp(leg);
legend(leg);
set(gca, "fontsize", fs);

% I think this causes problems...
%title('Mean and Standard Error', 'Interpreter', 'none');

% Save
print('-dpng', strcat(saveFileName, '.png'));
print('-depsc', strcat(saveFileName, '.eps'));
