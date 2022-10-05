function [result] = distortion(array)
unify = [1 0 0 0;0 1 0 0;0 0 1 0];

% method is equidistant
r = sqrt(array(1,:).^2+array(2,:).^2);
theta = atan(r);
thetas = [theta.^2;theta.^4;theta.^6;theta.^8];
ks = [-0.03116674  0.50057031 -7.69105705 41.71286545];
theta_d = theta.*(ks*thetas+1);
coe = repmat(theta_d./r,3,1);

unify = unify*array;
result = coe.*unify;
end