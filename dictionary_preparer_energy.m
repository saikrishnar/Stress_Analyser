% This program is to calculate the energy to be used in the unit selection based  voice

% Clear the workspace
clc; clear all; close all;

addpath 'STRAIGHTV40';
% Set the paths to the folders
waves = dir('../wav');
energypath = '../energy';
% mfccpath = '../mfcc';
f0path = '../f0';
mkdir('../f0/');
mkdir('../energy');
% Loop through all the waves
for i = 4%:length(waves)
    
    i
    % Loops through each file in speaker
    reffilename = waves(i).name;
    [refstr,tok] = strtok(reffilename,'.');
    
    % Read the wave and apply the diff operation
    [y,fs] = wavread(strcat('../wav/', reffilename));
    y = diff(y);
    y(end+1) = y(end);
    
    %        % Obtain mfcc
    %         mfcc = melcepst(y,fs);
    %
    % Defining the system parameters
    frSize = 20*(fs/1000);
    frShift = 5*(fs/1000);
    frOvlap = frSize - frShift;
    
    
    % Apply the buffer on the frames
    yb = buffer(y,frSize,frOvlap,'nodelay');
    ybw = bsxfun(@times,yb,hamming(frSize));
    
    % Obtain energy
    energy = sum(yb.^2);
    
    %        % Obtain pitch
    %         [f0, ~,~,~] = fxpefac(y, fs, frShift)
    %
    UPPER_F0 = 480;
    LOWER_F0 = 70;
    prm.F0frameUpdateInterval = frShift;
    prm.spectralUpdateInterval = frShift;
    prm.F0searchUpperBound = UPPER_F0;
    prm.F0searchLowerBound = LOWER_F0;
    
    
    % STRAIGHT ANALYSIS
    [f0, ap] = exstraightsource(y,fs,prm);
    
    
    % Write in file
    destination = strcat(energypath, '/', refstr, '.energy');
    dlmwrite(destination, energy, 'delimiter', '\n');
    
%     destination = strcat(mfccpath, '/', refstr, '.mfcc');
%     dlmwrite(destination, mfcc, 'delimiter', ' ');
    
    
    destination = strcat(f0path, '/', refstr, '.f0');
    dlmwrite(destination, f0, 'delimiter', '\n');
    
    
    
end
