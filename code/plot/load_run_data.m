function [N,iteration,parameters,fitness,best] = load_run_data(filename)
  % Load raw data from file
  %data = dlmread(filename);
  data = load(filename);

  % Separate into variables
  N          = size(data,1);
  iteration  = 1:N;
  parameters = data(:,1:5);
  fitness    = data(:,6);  
  % Convert from px/10sec to body length/min
  for j=1:N
    fitness(j) = fitness(j) * .0838;
  end
  best = zeros(5,1);
  best(1) = fitness(1);
  for ii=2:N
    best(ii) = max(best(ii-1), fitness(ii));
  end
end
