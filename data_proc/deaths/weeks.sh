# Filter from original downloaded DEUTNPstfmout.csv
# relevant years (2012 and later)
# and total number of deaths
# call this file by "source weeks.sh"
#
echo "Year,Week,Total" > ./DEUTNPstmfout_weeks.csv 

awk 'BEGIN{FS=",";OFS=","}{if ($4 =="b" && $2 < 2024 && $2>2012)  print $2,$3,$10}' ../../data_raw/deaths/DEUTNPstmfout.csv >> ./DEUTNPstmfout_weeks.csv 
