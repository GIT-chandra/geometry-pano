%POLYGON = [-11.5064 -27.575021; -11.5064 -20.500054; -11.5064 -18.484006; -11.5064 -15.101428; -11.5064 -8.299923; -11.5064 -8.297466999999999; 15.931567 -8.297466999999999; 15.9383 -8.297466999999999; 15.9383 -8.299923; 15.9383 -15.101428; 15.9383 -18.484006; 15.9383 -20.500054; 15.9383 -27.575021; 15.9383 -27.57659; 15.9383 -27.578032; 15.9383 -27.579348; 15.9383 -27.580538; 15.9383 -27.581579; 15.9383 -27.582485; 15.9383 -27.583247; 15.9383 -27.583867; 15.9383 -27.6025; -11.326211 -27.6025; -11.5064 -27.6025; -11.5064 -27.583247; -11.5064 -27.582485; -11.5064 -27.581579; -11.5064 -27.580538; -11.5064 -27.579348; -11.5064 -27.578032; -11.5064 -27.57659; -11.5064 -27.575021];
%LINE =[0 0; 42.4709545984076 0];
%%intersectLinePolygon(LINE,POLYGON)
%
%plot(POLYGON(:,1),POLYGON(:,2))
%hold on
%plot(LINE(:,1),LINE(:,2))

% Compute intersection points between 2 simple polylines
clear all
close all

z_res = 180; 
cyl_res = 360;
r = 1;
R = 30;
angs = linspace(0,2*pi,cyl_res);  % angle in radians,expected
x_dirs = cos(angs);
y_dirs = sin(angs);

slopes = y_dirs./x_dirs;
dirs = [x_dirs',y_dirs'];
x_disp = 3.56; y_disp = 2.0015;
circ_smaller = r*dirs + [x_disp*ones(360,1),y_disp*ones(360,1)];
circ_larger = R*dirs + [x_disp*ones(360,1),y_disp*ones(360,1)];

circular = zeros(360*2,2);
for i = [1,linspace(4,358*2,179)+1]
  j = (i-1)/2 + 1;
  circular(i,:) = circ_smaller(j,:);
  circular(i+1,:) = circ_larger(j,:);
  circular(i+2,:) = circ_larger(j+1,:);
  circular(i+3,:) = circ_smaller(j+1,:);
end

%drawPolyline(circular, 'b');

%i=717; j = 360
%circular(i,:) = circ_smaller(j,:);
%circular(i+1,:) = circ_larger(j,:);
%circular(i+2,:) = circ_larger(1,:);
%circular(i+3,:) = circ_smaller(1,:);
%poly1 = [20 10 ; 20 50 ; 60 50 ; 60 10;20 10];
%poly2 = [10 40 ; 30 40 ; 30 60 ; 50 60 ; 50 40 ; 70 40];

for i = 1:1
  poly3 = [20 20 ; -20 20 ; -20 -20 ; 20 -20 ; 20 20];
  pts = intersectPolylines(circular, poly3);
  disp(i);
  for p = 1:rows(pts)
    pt = pts(p,:);  
    find(abs(slopes - (pt(2)-y_disp)/(pt(1) - x_disp)) < 0.005)
  end
end

%figure; hold on; 
%drawPolyline(circular, 'b');
%drawPolyline(poly3, 'm');
%drawPoint(pts);

%axis([0 80 0 80]);