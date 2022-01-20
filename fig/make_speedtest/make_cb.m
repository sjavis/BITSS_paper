% min1 = importdata('outputs/minimum_1');
% min2 = importdata('outputs/minimum_2');
% ts = importdata('outputs/bits_f');
% ts2 = importdata('outputs/transition_state');

fid = fopen('states.json'); 
str = char(fread(fid,inf)');
fclose(fid); 
jsondata = jsondecode(str);
data = [jsondata.cb_m1; jsondata.cb_ts; jsondata.cb_m2];

facelist = importdata('cb_dlist');
faces = [facelist(:,3) facelist(:,4) facelist(:,5)];

R0 = 50; %Radius of the cylinder

%% Colourmap to visualise the radial displacement from R0
mymap=zeros(1000,3);
for i=1:1000

    if i<=250
        mymap(i,:) = [0.0 0.0 0.5] + [((i-1)/249)*0 ((i-1)/249)*0.4 ((i-1)/249)*0.5];
    elseif i>250 && i<=500
        mymap(i,:) = [0.0 0.4 1] + [((i-251)/249)*(0.9) ((i-251)/249)^1*(0.9-0.4) -((i-251)/249)*(0.1)];
    elseif i>500 && i<=750
        mymap(i,:) = [0.9 0.9 0.9] - [-((i-501)/249)*0.1 ((i-501)/249)^2*0.9 ((i-501)/249)*0.9];
    else
        mymap(i,:) = [1 0 0] - [ ((i-751)/249)*0.6 0 0];
    end

end


%% For each system, input the data, calculate the radial displacement field and visualise

N = size(jsondata.cb_m1,1)/3; %Number of coordinates
Ntot = size(data,1)/(3*N); %Number of differnt systems in the coords_in file


%Input data into arrays
X = reshape(data(1:3:end),[],Ntot);
Y = reshape(data(2:3:end),[],Ntot);
Z = reshape(data(3:3:end),[],Ntot);

% Rotate by phi for a better view
phi = 20 * pi/180;
Xt = X*cos(phi) + Z*sin(phi);
Z = -X*sin(phi) + Z*cos(phi);
X = Xt;

%Compute the radial dispalcement from R0 of each node
displacement_map = sqrt(X.^2+Z.^2) - R0;
dtotmax = max(abs(displacement_map), [], 'all');%*0.9;

for i = 1:Ntot

    % Plot 3D with radial dispalcement colormap
    new_fig()
    options = {'FaceVertexCData', displacement_map(:,i), 'Edgecolor', 'none', 'FaceColor', 'interp'};
    p = patch('Vertices', [X(:,i),Y(:,i),Z(:,i)], 'Faces', faces, options{:});
    material([0.35,0.5,0.2]);
    colormap(mymap)
    caxis([-dtotmax dtotmax])

    fig = gcf;
    fig.PaperPositionMode = 'auto';
    fig_pos = fig.PaperPosition;
    fig.PaperSize = [fig_pos(3) fig_pos(4)];
    saveas(fig, sprintf('b%d.png',i-1));

end


function new_fig()
    figure();
    set(gcf, 'Position',  [500, 300, 400, 400])
    set(gca, 'Box', 'off', 'Visible', 'off', 'Clipping', 'off', 'Units', 'normalized', 'Position', [0 0 1 1]);
    set(gca,'XTick',[], 'YTick', [], 'Ztick', []);
    axis image;
    view([1 1 4]);
    light('Position',[1 0.1 0.6],'Color','w');
end
