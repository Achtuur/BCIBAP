eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = 1;

% epochs = 0.5 : 0.25 : 4;
epochs = 3.25;
i = 1;
for k = epochs
    [X,features,Y,featurelabels, mu_train, sigma_train] = getFeatures(dataset, path2dataset, FileIndices, k);
    
    %% Create model
    disp('Creating model...');
    tic;

    [lab, predicted, savepath] = CreateModel(X, Y, featurelabels);

    t = toc;
    fprintf("Done creating model, took %.3f seconds\n", t);
    %% Save model
    disp('Saving Model');
    tic;

%     save(savepath, 'Fs', 'EpochLengthSec', '-append');

    t = toc;
    fprintf("Done saving model, took %.3f seconds\n", t);
%     figure(i)
%     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);
%     plt.Title = sprintf("epochlengthsec = %s", k);
%     title(fig.axes, sprintf("epochlengthsec = %s", k));
end


