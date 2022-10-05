function target_arr = time_match(source_time_file,source_arr,target_time_file)
%This function is used to match the source array to target timestamp
%accroding to the timeframe provided
source_time = load(source_time_file);
target_time = load(target_time_file);
[row_ct,~] = size(source_arr);

target_len = length(target_time);
target_arr = zeros(row_ct,target_len);
for i=1:target_len
    temp_time = source_time-target_time(i);
    [~,min_idx] = min(abs(temp_time));
    target_arr(:,i) = source_arr(:,min_idx);
end
end