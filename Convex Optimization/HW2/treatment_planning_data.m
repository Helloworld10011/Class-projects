% radiation treatment planning data file
% this one is randomly generated; a real one would use the beam geometry
rand('state',0);
n = 300; % number of beams
mtumor = 100; % number of tumor voxels
mother = 400; % number of other voxels
Atumor = sprand(mtumor,n,0.2);
Atumor = Atumor + [5*sprand(mtumor,mtumor,0.2) zeros(mtumor,n-mtumor)];
Aother= sprand(mother,n,0.2);
Bmax = 10;
Dtarget = 1;
Dother = 0.25;