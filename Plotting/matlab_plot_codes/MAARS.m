% Read the CSV file
data = readtable('MAARS_combined_tasks_sets_IR_data.csv');

% Extract unique task counts
task_counts = unique(data.TaskCount);

% Create a new figure
figure;

% Hold the plot for multiple scatter plots
hold on;

% Determine gray shades for each task count
num_shades = length(task_counts);
gray_shades = linspace(0, 0.7, num_shades);  % Create shades from black (0) to light gray (0.8)

% Loop through each task count and plot
for i = 1:length(task_counts)
    % Filter data for the current task count
    current_data = data(data.TaskCount == task_counts(i), :);

    % Scatter plot for the current task count with different shades of gray
    scatter(current_data.Utilization, current_data.InferabilityRate, ...
        36,'MarkerEdgeColor', [gray_shades(i), gray_shades(i), gray_shades(i)], 'MarkerFaceColor', [gray_shades(i), gray_shades(i), gray_shades(i)],'DisplayName', sprintf('%d Tasks', task_counts(i)));
end

% for i = 1:length(task_counts)
%     % Filter data for the current task count
%     current_data = data(data.TaskCount == task_counts(i), :);
% 
%     % Scatter plot for the current task count with different shades of gray
%     scatter(current_data.Utilization, current_data.InferabilityRate, ...
%         36, 'MarkerEdgeColor', [gray_shades(i), gray_shades(i), gray_shades(i)],'DisplayName', sprintf('%d Tasks', task_counts(i)));
% end


 
% Label the axes
xlabel('Utilization');
ylabel('IR');

% Set the title
% title('Inferability Rate vs Utilization');

% Add legend
legend show;

% Set axis limits
xlim([0 1]); % This can be adjusted based on your data range
ylim([0 1]); % Assuming Inferability Rate (ScheduleEntropy) is between 0 and 1

% Hold off the plot
hold off;

% Save the plot as an image (optional)
saveas(gcf, 'inferability_rate_MAARS_plot_gray.png');
