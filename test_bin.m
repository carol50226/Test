clear all;
% fileID = fopen('nine.bin','wb');
% fwrite(fileID,[1:0.5:5],'double');
% fwrite(fileID,[5:0.5:10],'double');
% fclose(fileID);


fid=fopen('whuR2018_6_17_9_30','rb');
%fid=fopen('tttt','rb');
WN=fread(fid,1,'int');
TOW=fread(fid,1,'int');
sv_num = fread(fid,1,'uint8');
svtype = fread(fid,1,'char');
svid = fread(fid,1,'int8');
A = fread(fid,19,'double');

%B=reshape(A,19,[]);
%B=B';
fclose(fid);