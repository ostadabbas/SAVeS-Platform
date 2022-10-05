function timestamps = extract_time_from_topic(topic_messages,file_loc,file_name)
%extract time from a certain bag topic and write to txt file
% nu_bag = rosbag(bag_file_loc);
% bSel = select(nu_bag,'Topic',topic);
% msgStructs = readMessages(bSel,'DataFormat','struct');
msgStructs = topic_messages;
nu_len = length(msgStructs);
timestamps = strings(nu_len,1);

for i=1:nu_len
    timestamps(i) = strcat(int2str(msgStructs{i}.Header.Stamp.Sec),sprintf("%09d",msgStructs{i}.Header.Stamp.Nsec));
end

fileID = fopen(strcat(file_loc,file_name),'w');
formatSpec = '%s\n';
for i=1:nu_len
    fprintf(fileID,formatSpec,timestamps(i));
end
fclose(fileID);
end