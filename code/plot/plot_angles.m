function plot_angles()
dat = load('../../hyperneat_runs/hyperneatTo20gens_101/neat_110115_211410_00000_002_filt');
tt = linspace(0, 12, size(dat,1));

figure(1);
plot(tt, dat, 'linewidth', 2, 'linewidth', 4);
xlabel('Time (s)',       'fontsize', 22);
ylabel('Motor Position', 'fontsize', 22);
print('-depsc2', '-F:18', 'neat_110115_211410_00000_002_filt.eps');

figure(2);
plot(tt(1:85), dat(1:85,:), 'linewidth', 4);
xlabel('Time (s)',       'fontsize', 22);
ylabel('Motor Position', 'fontsize', 22);
print('-depsc2', '-F:18', 'neat_110115_211410_00000_002_filt_zoom.eps');




figure(3);
tt = linspace(0, 12, size(dat,1) * .6);
synth = (ones(9, 1) * 150*sin(tt*1))';
synth(:,[1,3,5,7]) = synth(:,[1,3,5,7]) * 1.6;
synth(:,[1,2,3,4]) = synth(:,[1,2,3,4]) * -.78;
synth(:,[1,2,5,6]) = synth(:,[1,2,5,6]) * 1.9;
synth(:,[1,3,5,7]) = synth(:,[1,3,5,7]) + 800;   % inner
synth(:,[2,4,6,8]) = synth(:,[2,4,6,8]) + 40;    % outer
synth(:,[9]) = synth(:,[9]) * 0 + 512;           % center

%synth(:,[1,3,5,7]) = min(synth(:,[1,3,5,7]), (60+120)*1024/240);   % inner
%synth(:,[1,3,5,7]) = max(synth(:,[1,3,5,7]), (-85+120)*1024/240);  % inner
%synth(:,[2,4,6,8]) = min(synth(:,[2,4,6,8]), (39+120)*1024/240);   % outer
%synth(:,[2,4,6,8]) = max(synth(:,[2,4,6,8]), (-113+120)*1024/240); % outer
%synth(:,[9]) = min(synth(:,[9]), (39+120)*1024/240);               % center
%synth(:,[9]) = max(synth(:,[9]), (-113+120)*1024/240);             % center

synth(:,[1,3,5,7]) = min(synth(:,[1,3,5,7]), 770);   % inner
synth(:,[1,3,5,7]) = max(synth(:,[1,3,5,7]), 150);  % inner
synth(:,[2,4,6,8]) = min(synth(:,[2,4,6,8]), 680);   % outer
synth(:,[2,4,6,8]) = max(synth(:,[2,4,6,8]), 30); % outer
synth(:,[9]) = min(synth(:,[9]), 623);               % center
synth(:,[9]) = max(synth(:,[9]), 392);             % center


plot(tt, synth, 'linewidth', 4);
xlabel('Time (s)',       'fontsize', 22);
ylabel('Motor Position', 'fontsize', 22);
print('-depsc2', '-F:18', 'sinemodel_gait.eps');



figure(4);
rand('state', 0);
synth = (ones(9, 1) * zeros(size(tt)));
for ii = 1:9
  for jj = 1:length(tt)
    if jj == 1
      synth(ii,jj) = (rand-.5)*10;
    else
      synth(ii,jj) = synth(ii,jj-1) + rand-.5;
    end
  end
  len = 20;
  temp = conv(synth(ii,:), ones(len,1)/len);
  synth(ii,:) = temp(1:length(synth(ii,:)));
end
chop = synth(:,len:end);
chop -= min(min(chop));
chop *= 1023 / max(max(chop));
plot(tt(1:length(chop)), chop, 'linewidth', 4);
xlabel('Time (s)',       'fontsize', 22);
ylabel('Motor Position', 'fontsize', 22);
axis('tight');
print('-depsc2', '-F:18', 'example_gait.eps');



