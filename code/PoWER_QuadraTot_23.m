function PoWER_with_Evolving_Policy_Parameterization_QuadraTot_23
%
% Author: Petar Kormushev
% April 2012
%
close all;
clear all;
clc;

%% Parameters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
for i=1:1
    relearn = 0;
    [Return, s_Return, param, rl] = RL_PoWER(4, 4, relearn);
end

end

function path = getDataPath()
  path = '/DATA/QuadraTot/';
end

%% RL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Return, s_Return, param, rl] = RL_PoWER(fromKnots, toKnots, relearn, Return, s_Return, param, rl);
disp('Starting RL...');
%  rl_m = m; % make a copy of m

hFig = figure('Name', 'Rollouts', 'position', [50, 100, 800, 600]);
hFigResults = figure('Name', 'Results', 'position',[1000,600,800,400]); axis on; grid on; hold on;
hFigExported = figure('Name', 'Exported trajectory', 'position', [850, 100, 600, 400]); hold on; box on; grid on;

plotRollouts(hFig, 0, 0, 0, 0);

% START of PoWER algorithm
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% number of iterations
n_iter = 60;
% number of parameters of the policy = number of spline knots here
n_splines = 8;
n_rfs = n_splines*(fromKnots - 1);  % because the last knot of the spline y(n) = y(1)

importanceSamplingTopCount = 3;  % how many top rollouts to use for importance sampling

if relearn==0
  Return = zeros(1,n_iter+1);
  s_Return = zeros(n_iter+1,2);

  % initialize parameters
  param = zeros(n_rfs,n_iter+1);
end

% randn('state',20); % fixed random seed

% set fixed variance
variance(1:n_rfs) = 0.008.*ones(n_rfs,1);
disp('Variance for a single nbState is:');
% variance'
varianceDecay = 0.98;
varianceLog = []; % just to declare the variable

initialPos(0+1) = 600; % joint 0
initialPos(1+1) = 20;
initialPos(2+1) = 600;
initialPos(3+1) = 20;
initialPos(4+1) = 600;
initialPos(5+1) = 20;
initialPos(6+1) = 600;
initialPos(7+1) = 20; % joint 7
%initialPos(8+1) = 512; % body joint - 8
initialPos = initialPos ./ 1024; % normalize in (0,1)

% initial splines
for si=1:n_splines
  policy(1).n_splines = n_splines;
  policy(1).s(si).n = fromKnots; % number of spline knots
  policy(1).s(si).x = 0:1/(policy(1).s(si).n-1):1; % x positions of knots
  policy(1).s(si).y = initialPos(si)*ones(1,policy(1).s(si).n); % set initial policy y values to the middle 0.5
  % now turn it into a cyclic spline
  [policy(1).s(si).pp, policy(1).s(si).x, policy(1).s(si).y, policy(1).s(si).n] = getCyclicSplinePlus6e(policy(1).s(si).x, policy(1).s(si).y);
  plotSpline(policy(1).s(si).pp, policy(1).s(si).n, policy(1).s(si).x, policy(1).s(si).y, 'green', 3); % visualize the spline
end
%pause

% initialize the parameters to optimize with their current values
param(:,1) = policyToParam(policy(1));

disp('param - in the BEGINNING');
param(:,1)'

% pause

disp('Running PoWER algorithm...');

if relearn==1 % resume learning of a previous session
    % load iteration number
    iter_matrix = dlmread([getDataPath() 'iter.txt']);
    iter = iter_matrix(1,1);
    load([getDataPath() num2str(iter,'%03d') '/workspace.mat']); % loads ALL workspace variables!!
    % iter = iter + 1; ?? no, let it repeat it, if necessary I can just reuse the previous reward
    % here make changes to parameters, if necessary, e.g. variability, etc.
    % ...
else
    iter = 1;
end
% do the iterations
while (iter <= n_iter)

    %if (mod(iter,100)==0)
        disp(['Iteration: ', num2str(iter)]);
    %end

%     disp('param:');
%     param(:,iter)'

    if fromKnots < toKnots
        % regularly increase the number of knots
        increaseInterval = round(n_iter / (toKnots - fromKnots));
        if (mod(iter,increaseInterval)==0)
            n_rfs = n_rfs + 1;
            n2 = policy(iter).s(1).n + 1; % TODO: loop for all splines!!!!
            disp(['Increasing the # of knots to ', num2str(n2)]);
            param = zeros(n_rfs,n_iter+1);
            variance(1:n_rfs) = 1.0 * variance(1:1) * ones(n_rfs,1); % copy prev. variance
            for i=1:iter
                [policy(i).s(1).pp, policy(i).s(1).x, policy(i).s(1).y] = getNewSplineCyclic(policy(i).s(1).pp, policy(i).s(1).x, n2);
                policy(i).s(1).n = n2;
                param(:,i) = policy(i).s(1).y(1+3:end-1-3)';
            end
        end
    end

    % plot the rollout / all rollouts so far
    plotRollouts(hFig, iter, iter, policy, n_splines);
    filepath = [getDataPath() num2str(iter,'%03d') '/'];
    mkdir(filepath);
    exportTrajectoryWithoutRescaling(policy(iter), hFigExported, filepath);

    if iter == 1
      noGUI = 0 % 1 to hide the GUI for the first half of trials
    elseif iter < 0.8*n_iter
      noGUI = 0 % 1 to hide the GUI for the first half of trials
    else
      noGUI = 0 % 0 to show the GUI for the second half of trials
    end
    runSimulator(filepath, noGUI); % 1 for noGUI

    % for real robot experiment
    rl(iter).traj = Load_trajectory([getDataPath() num2str(iter,'%03d') '/output.txt']);

    % calculate the return of the current rollout
 	  Return(iter) = ReturnOfRollout(rl(iter).traj);
 	  disp(['Current rollout return: ', num2str(Return(iter))]);
     
    % plot the results / all results so far
    plotResults(hFigResults, iter, variance, varianceLog(:,1:iter-1), Return(:,1:iter));
    
    % save iteration number
    dlmwrite([getDataPath() 'iter.txt'], iter);
    %mkdir([getDataPath() num2str(iter,'%03d')]);
    save([getDataPath() num2str(iter,'%03d') '/workspace.mat']); % saves ALL workspace variables!! Nice!
    % disp('Saved workspace. ENTER to continue...');
    % pause
    
    % this lookup table will be used for the importance sampling
    s_Return(1,:) = [Return(iter) iter];
    s_Return = sortrows(s_Return);
    
    % update the policy parameters
    param_nom = zeros(n_rfs,1);
    param_dnom = 0;
    
    if relearn==0
      min_count = iter; % only the rollouts from current batch so far
    else
      min_count = n_iter; % all previous experiences
    end
    % calculate the expectations (the normalization is taken care of by the division)
    % as importance sampling we take the top best rollouts
    for i=1:min(min_count,importanceSamplingTopCount) % TODO: how many are optimal??
      % get the rollout number for the top best rollouts
      j = s_Return(end+1-i,2);

      % calculate the exploration with respect to the current parameters
      temp_explore = (param(:,j)-param(:,iter));

      % always have the same exploration variance, and assume that always only one basis functions is active we get these simple sums
      param_nom = param_nom + temp_explore*(Return(j).^6); % TODO: ^6 to put more weight on the higher rewards
      param_dnom = param_dnom + (Return(j).^6);
    end
    
    % update the parameters
    param(:,iter+1) = param(:,iter) + param_nom./(param_dnom+1.e-10);
    
    % decay the variance
    variance(:) = variance(:) .* varianceDecay;
    varianceLog(1,iter) = variance(1); % TODO: fix size and uncomment line

    % add noise
    param(:,iter+1) = param(:,iter+1) + variance(:).^.5.*randn(n_rfs,1);
       
    % apply the new parameters from RL
    policy(iter+1) = policy(iter); % copy all fields from old policy
    policy(iter+1) = paramToPolicy(param(:, iter+1), policy(iter+1));

iter = iter + 1;    
end % iter loop

iter = iter - 1;

[best_reward best_iter] = max(Return)

disp('param - before the start:');
param(:,1)'

disp('param - best after the RL optimization:');
param(:,best_iter)'

disp('Initial return, before optimization with RL');
Return(1)

disp('Best return:');
Return(best_iter)

% plot the rollout / all rollouts so far
plotResults(hFigResults, iter, variance, varianceLog(:,1:iter-1), Return(:,1:iter));
% plot best traj in red
plotRollouts(hFig, iter, best_iter, policy, n_splines);

% run the best trial again using the simulator  
disp('Press ENTER to see the best trial...');
pause
filepath = [getDataPath() num2str(best_iter,'%03d') '/'];
runSimulator(filepath, 0);

% END of PoWER algorithm
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end


%% Plot
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function plotResults(hFig, n_rfs, variance, varianceLog, Return)
  figure(hFig);

  subplot(1,2,1);
  %figure('Name', 'Variance over rollouts'); hold on;
  for i=1:size(varianceLog,1)
      plot(varianceLog(i,:), 'color', [0 0 0]);
  end
  ylabel('variance');
  xlabel('rollouts');

  subplot(1,2,2);
  %figure('Name', 'Return over rollouts'); hold on;
  plot(Return);
  %axis([0 max(size(Return)) 0 1]);
  xlim([0 max(size(Return))]);
  ylabel('return');
  xlabel('rollouts');
end


%% get a new cyclic spline pp2, for a new number of spline knots n2,
% replacing the old (also cyclic!) spline pp
function [pp2, x2, y2] = getNewSplineCyclic(pp, x, n2)
  x2 = x(1+3) : (x(end-3)-x(1+3))/(n2-6-1):x(end-3); % x positions of knots
  y2 = ppval(pp, x2); % get the value of the old spline pp for the new knots x2
%  pp2 = spline(x2, y2);
  [pp2, x2, y2] = getCyclicSplinePlus6(x2, y2);
end

%% plots a spline pp
function plotSpline(pp, n, x, y, clr, wdt, stl)
  if nargin < 7
    stl = '-';
  end
  % show the knots  
  plot(x,y, 'o', 'color', clr, 'linewidth', wdt);
  % visualize the spline
  sx = x(1):0.01:x(end); % controls the smoothness of visualization of the spline
  sy = ppval(pp, sx);
  plot(sx, sy, 'color', clr, 'linewidth', wdt, 'linestyle', stl); % Problem!! The spline might go
% outside [0,1] interval!!! maybe better to use DMP/attractors?? Or Gaussians?
end

%% get a new spline pp2, which is cyclic, i.e. replaces y(n) with y(1) as last
% knot and also adds 3 knots on each side to "wrap" cyclicly the spline
% which makes sure the pos and pos dot at both ends match
function [pp2, x2, y2, n2] = getCyclicSplinePlus6e(x, y) % NEW version 6e, can work even if there are only 3 knots!
  n = max(size(x));
  dx = x(2)-x(1);
  n2 = n+2*3; % new number of spline knots
  x2 = [ x(1)-3*dx  x(1)-2*dx  x(1)-dx  x(1:n-1)  x(n)  x(n)+dx  x(n)+2*dx  x(n)+3*dx ];
  if n == 3
  y2 = [ y(n-1)     y(n-2)     y(n-1)   y(1:n-1)  y(1)  y(2)     y(1)       y(2) ]; % replaces y(n) with y(1)
  elseif n > 3
  y2 = [ y(n-3)     y(n-2)     y(n-1)   y(1:n-1)  y(1)  y(2)     y(3)       y(4) ]; % replaces y(n) with y(1)
  else
    error('Unsupported number of knots n!')
  end;
  pp2 = spline(x2, y2); % calculate the spline  
end

%% plot all rollouts so far
function plotRollouts(hFig, n_iter, highlight_iter, policy, n_splines)
  figure(hFig);
  clf; % clears the figure
  hold on;
  %    axis([-1 2 0 1]);
  xlim([-1 2]);

  clrmap = colormap(jet(n_splines));
  for iter=1:n_iter
    for si=1:n_splines
  %        clr = 'green';
          clr = clrmap(si,:);
          clr = (0.5 + 0.5*iter/n_iter) * clr; % gradient
          wdt = 2;
  %         if iter==highlight_iter % only for one
  %           wdt = 4;
  %           % clr = [1 0 0]; % red
  %         end
          plotSpline(policy(iter).s(si).pp, policy(iter).s(si).n, policy(iter).s(si).x, policy(iter).s(si).y, clr, wdt); % visualize the spline
    end
  end
  % plot the highlighted iteration last, to be on top of all others
  for si=1:n_splines
    wdt = 4;
    % clr = [1 0 0]; % red
    clr = clrmap(si,:);
    plotSpline(policy(highlight_iter).s(si).pp, policy(highlight_iter).s(si).n, policy(highlight_iter).s(si).x, policy(highlight_iter).s(si).y, clr, wdt); % visualize the spline
  end

  % draw vertical lines to mark a single time interval
  line([0 ; 0], [-0.1 ; 1.1], 'color', 'black', 'linewidth', 2);
  line([1 ; 1], [-0.1 ; 1.1], 'color', 'black', 'linewidth', 2);
end


%% Export the produced trajectory to execute it on the robot
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function exportTrajectoryWithoutRescaling(policy, hFig, filepath);
  % the policy contains: policy.pp, policy.x, policy.y, policy.n

  % timing
  total_duration = 12; % 12 sec total duration of walking
  cycle_duration = 1.8; % 1.3 sec period
  nbCycles = total_duration / cycle_duration;
  dt = 0.1; % 100 ms discretization step / control loop
  nbCycleSamples = cycle_duration / dt + 1;
  nbTotalSamples = total_duration / dt + 1;

  cycleTime = (0: dt: cycle_duration)';
  totalTime = (0: dt: total_duration)';

  % stretch the spline over the duration of one cycle
  for si=1:policy.n_splines
    s(si).XX = policy.s(si).x(1+3) : (policy.s(si).x(end-3)-policy.s(si).x(1+3))/(nbCycleSamples-1) : policy.s(si).x(end-3);
    s(si).YY = ppval(policy.s(si).pp, s(si).XX);
  end
  
  % rescale the trajectory y from [0,1] to stretch inside [zmin,zmax]
  posMin = 256;
  posMax = posMin + 512;
  posRange = posMax - posMin;
  for si=1:policy.n_splines
    % rescale
    s(si).cyclePos = s(si).YY .* posRange + posMin;
    s(si).cyclePos = s(si).cyclePos(:);
    % repeat cycle
    s(si).totalPos = [repmat(s(si).cyclePos(1:end-1), ceil(nbCycles), 1) ; s(si).cyclePos(end)]; % the last pos in a cycle is the same as the first pos in the next cycle
    s(si).totalPos = s(si).totalPos(1:nbTotalSamples); % the last cycle will probably be interrupted before its end
  end
  
  % plot the 'Exported trajectory' velocity and acceleration
  figure(hFig); clf; hold on; box on; grid on;
  clrmap = colormap(jet(policy.n_splines));
  for si=1:policy.n_splines
    plot(totalTime, s(si).totalPos, 'color', clrmap(si,:), 'linewidth', 2); % all cycles
    plot(cycleTime, s(si).cyclePos, 'color', clrmap(si,:), 'linewidth', 4); % just the first cycle is thicker, to highlight it
  end
  
  % Generate file input.txt for the simulator
  inputData = [];
  inputData = [inputData ; 0 512.0*ones(1, 9)]; % straight pose, fixed
  fixedPos = 512.0 * ones(nbTotalSamples, 1); % one column fixed value
  % individual joint's trajectories
  j(:,0+1) = s(1).totalPos; % fixedPos;
  j(:,1+1) = s(2).totalPos;
  j(:,2+1) = s(3).totalPos;
  j(:,3+1) = s(4).totalPos;
  j(:,4+1) = s(5).totalPos;
  j(:,5+1) = s(6).totalPos;
  j(:,6+1) = s(7).totalPos;
  j(:,7+1) = s(8).totalPos;
  j(:,8+1) = fixedPos;
  inputData = [inputData ; 2+totalTime, j(:,:)];

  % Export to a text file, for loading by the QuadraTot simulator
  dlmwrite([filepath '/input.txt'], '# Automatically generated file by Petar''s RL algorithm, containing joint trajectories for QuadraTot', 'delimiter', '');
  dlmwrite([filepath '/input.txt'], inputData , 'delimiter', ' ', '-append');

  % ---------------------------
  % #straight out pose
  % 2 512.0 512.0 512.0 512.0 512.0 512.0 512.0 512.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % #pose 1
  % 6 770.0 40.0 770.0 40.0 770.0 40.0 770.0 40.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % 12 770.0 40.0 770.0 40.0 770.0 40.0 770.0 40.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % #pose 2
  % 16 700.0 100.0 700.0 100.0 700.0 100.0 700.0 100.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % 20 700.0 100.0 700.0 100.0 700.0 100.0 700.0 100.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % #pose 3
  % 24 512.0 150.0 512.0 150.0 512.0 150.0 512.0 150.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % 28 512.0 150.0 512.0 150.0 512.0 150.0 512.0 150.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % #straight out
  % 32 512.0 512.0 512.0 512.0 512.0 512.0 512.0 512.0 512.0 0 0 0 0 0 0 0 0 0 0 0
  % ---------------------------
end

%% Calculate the return (reward function) of a rollout
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function r = ReturnOfRollout(traj)

  % r = 0.456;
  % return;

  % maxHeight = max(traj(:,4))
  % r = maxHeight;
  % return

  % avgHeight = mean(traj(:,4))
  % r = exp(avgHeight);
  % return

  avgHeight = mean(traj(:,4))
  distTraveled = norm(traj(end,2:4) - traj(1,2:4)) % in [cm]
  duration = traj(end,1) - traj(1,1) % in [s]
  avgSpeed = distTraveled / duration % in [cm/s]

  r = avgSpeed;
%  r = (10*avgSpeed + avgHeight)^10; % combining speed and height
  return
end

function param = policyToParam(policy)
  param = [];
  for si=1:policy.n_splines
    param = [param ; policy.s(si).y(1+3:end-1-3)']; % excluding y(n) cause it's equal to y(1)
  end
end

function policy = paramToPolicy(param, policy)
  nbKnots = policy.s(1).n-3-3; % exclude the additional knots added for cyclicity of the spline
  nbPar = nbKnots - 1;
  for si=1:policy.n_splines
    % apply the new parameters from RL
    policy.s(si).y = [ param((si-1)*nbPar+1:si*nbPar)' param((si-1)*nbPar+1) ]; % y(n) = y(1)
    %    policy.pp = spline(policy.x, policy.y); % re-calculate the spline 
    % now turn it into a cyclic spline
    [policy.s(si).pp, policy.s(si).x, policy.s(si).y, policy.s(si).n] = getCyclicSplinePlus6e(policy.s(si).x(1+3:end-3), policy.s(si).y);
  end
end

%% Load traj that the robot moved (returns matrix with 4 columns: t, x, y, z)
function traj = Load_trajectory(filename) % E.g. 'data/001/output_001.txt'
  hFig = figure('Name', '3D trajectory'); hold on; box on; grid on;

  % load electric current usage data
  data = dlmread(filename, '', 14, 0); % skip the first 13 lines
  traj = [data(:,1) data(:,20) data(:,22) data(:,21)]; % t, x, y, z

  plot3(traj(:,2), traj(:,3), traj(:,4), 'linewidth', 2);
  % plot traj starting pos
  plot3(traj(1,2), traj(1,3), traj(1,4),'.','markersize',20,'color',[0 1 0]);
  % plot traj end pos
  plot3(traj(end,2), traj(end,3), traj(end,4),'X','markersize',20,'color',[1 0 0]);

  view(3); axis equal;
  mn = min(min(traj(:,2:4)));
  mx = max(max(traj(:,2:4)));
  range = mx - mn;
  mn = mn - 0.1*range;
  mx = mx + 0.1*range;
  axis([mn mx mn mx mn mx]);
  xlabel('x'); ylabel('y'); zlabel('z');

  hFig = figure('Name', 'Individual axis trajectories', 'position', [1260, 200, 600, 900]); hold on; box on; grid on;
  subplot(3,1,1);
  plot(traj(:,1), traj(:,2), 'linewidth', 2);
  xlabel('time'); ylabel('x');
  ylim([mn mx]);
  subplot(3,1,2);
  plot(traj(:,1), traj(:,3), 'linewidth', 2);
  xlabel('time'); ylabel('y');
  ylim([mn mx]);
  subplot(3,1,3);
  plot(traj(:,1), traj(:,4), 'linewidth', 2);
  xlabel('time'); ylabel('z');
  ylim([mn mx]);
end

%% Execute the external binary file of the simulator
function runSimulator(filepath, noGUI)
  disp('Trajectory exported to input.txt file. Next, the simulator will be executed.');

  simulator_dir = '"/RESEARCH/SOFTWARE/Jason Yosinski''s Quadruped robot simulator/Simulator/2012_04_20 standalone_win32/"';
  simulator_filename = 'test.exe';
  exe_file = [simulator_dir simulator_filename];
  filepathDOS = strrep(filepath, '/', '\');
  disp('Going to execute command:');
  command1 = ['cd ' simulator_dir]
  command2 = [exe_file ' -i ' filepathDOS 'input.txt' ' -o ' filepathDOS 'output.txt']
  if noGUI == 1
    command2 = [command2 ' -n '];
  end
  if noGUI == 0
    disp('Press ENTER to execute simulator...');
    % pause
  end
  [s,w] = dos([command1 ' & ' command2]);  % TODO: why it's so slow to copy from my VM ubuntu, and so fast from WAM??
%     disp('Press ENTER to continue...');
%     pause
end

