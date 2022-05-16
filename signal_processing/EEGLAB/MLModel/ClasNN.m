eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = [1:6];

epochs = 0.5 : 0.25 : 4;
final_results = cell(size(epochs, 2), 2);
i = 1;
for k = epochs
    [features,labels,featurelabels] = CNN(dataset, path2dataset, FileIndices, k);
    
    % Train CNN here


     final_results(i, :) = {features featurelabels};
%     figure(i)
     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);
%     plt.Title = sprintf("epochlengthsec = %s", k);
%     title(fig.axes, sprintf("epochlengthsec = %s", k));
end