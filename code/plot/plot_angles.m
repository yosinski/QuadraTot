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

