function fea_box = feature_box(an_array)
%return all boxplot info for a frame
    demo_readable = an_array;
    demo_ifeature = zeros(6,1);
    demo_ifeature(1) = max(demo_readable);
    demo_ifeature(2) = prctile(demo_readable,75);
    demo_ifeature(3) = mean(demo_readable);
    demo_ifeature(4) = median(demo_readable);
    demo_ifeature(5) = prctile(demo_readable,25);
    demo_ifeature(6) = min(demo_readable);
    fea_box = demo_ifeature;
end