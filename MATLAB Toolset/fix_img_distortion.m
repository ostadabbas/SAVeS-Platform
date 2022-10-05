function J = fix_img_distortion(I)
radialDistortion = [-0.03116674  0.50057031];
projection0 = [1888.44515582,0,0;0,1888.40009491,0;613.18976514,482.11894092,1];
cameraParams = cameraParameters('IntrinsicMatrix',projection0,'RadialDistortion',radialDistortion);
J = undistortImage(I,cameraParams);
end