% Week 7, Question 2

T = [   5.828507487520803   3.448242928452581
   5.252321131447595  3.7689018302828736 
   4.981790349417643   3.5170698835274594  
   5.515306156405986  3.6013011647254585 
   5.0593128119800355   3.7050216306156365  ];

% Compute the following differenes
% System 1 - System 2
dt12 = T(:,1) - T(:,2);

% multiplier for confidence interval
mf = tinv(0.975,4)/sqrt(5);

% confidence interval for dt12
mean(dt12) + [-1 1]*std(dt12)*mf



