plot_run('log_uniform_a.txt');
plot_run('log_uniform_b.txt');
plot_run('log_uniform_c.txt');
plot_run('log_gaussian_a.txt');
plot_run('log_gaussian_b.txt');
plot_run('log_gaussian_c.txt');
plot_gradient_run('log_gradient_a.txt');
plot_gradient_run('log_gradient_b.txt');
plot_gradient_run('log_gradient_c.txt');
plot_run('log_random_a.txt');
plot_run('log_random_b.txt');
plot_run('log_random_c.txt');
plot_run('log_explore_a.txt');
plot_run('log_explore_b.txt');
plot_run('log_linear_regression_a.txt');
plot_run('log_linear_regression_b.txt');
plot_run('log_linear_regression_c.txt');
plot_run('log_simplex_a.txt');
plot_run('log_simplex_b.txt');
plot_run('log_simplex_c.txt');

plot_several_runs({'log_uniform_a.txt', 'log_uniform_b.txt', 'log_uniform_c.txt'})
plot_several_runs({'log_gaussian_a.txt', 'log_gaussian_b.txt', 'log_gaussian_c.txt'})

plot_several_runs({'log_uniform_a.txt', 'log_gaussian_a.txt'});
plot_several_runs({'log_uniform_b.txt', 'log_gaussian_b.txt'});
plot_several_runs({'log_uniform_c.txt', 'log_gaussian_c.txt'});


plot_several_runs({'log_gaussian_a.txt', 'log_uniform_a.txt', 'log_gradient_a.txt', ...
                   'log_gaussian_b.txt', 'log_uniform_b.txt', 'log_gradient_b.txt', ...
                   'log_gaussian_c.txt', 'log_uniform_c.txt', 'log_gradient_c.txt'})
