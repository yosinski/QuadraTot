function dists()
%


ptsx = [48 495; 340 481; 616 469; 889 453];

ptsy = [329 200; 340 481; 353 759];

dx = diff(ptsx);
dy = diff(ptsy);

mn = mean([dx(:,1); dy(:,2)]);

disp(sprintf('mean pixels per square = %g', mn));

ppcm = mn / ((19 + 9/16) * 2.54);
disp(sprintf('pixels per cm = %g', ppcm))
