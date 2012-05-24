function runRobot(filepath)
  % TODO: define this function. It should just call the python executable.

  settings = getSettings();

  disp(settings.robotDir);
  disp(settings.robotExecutable);

  completeInputFilename = [filepath 'input.txt'];
  completeOutputFilename = [filepath 'output.txt'];

  if isunix
    command = [settings.robotDir settings.robotExecutable ' ' completeInputFilename ' ' completeOutputFilename];
    disp(sprintf('Running command: %s', command));
    
    % Takes ~12 seconds, at least
 
    [status, out] = system(command);
    while status ~= 0
      warning(sprintf('Exit code was %d, press Enter to redo the run', status));
      pause();
      [status, out] = system(command);
    end
    disp('Done running robot!');
  else
    error('No windows implementation for this yet');

end
