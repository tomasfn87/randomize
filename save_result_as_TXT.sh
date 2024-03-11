#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Wrong input: please specify file name as argument. i.e: ./save_result.sh 'file_name'"
    exit 1
fi

output_file="$1"
output_file=`echo "$output_file" | tr -cd '[:alnum:] _\-.'`
output_file=`echo "$output_file" | sed 's/ \{1,\}/-/g'`
output_file=`echo "$output_file" | sed 's/\.\{1,\}/-/g'`
output_file=`echo "$output_file" | sed 's/\-\{2,\}/-/g'`
output_file=`echo "$output_file" | sed 's/^ *//g' | sed 's/ *$//g'`
output_file=`echo "$output_file" | sed 's/ /-/g'`
output_file=`echo "$output_file" | sed 's/\./-/g'`


if [ -z "$output_file" ]; then
    echo "Wrong input: please specify file name as argument. i.e: ./save_result.sh 'file_name'"
    exit 1
fi

date_time=`date '+%Y-%m-%d_%H-%M-%S'`
script_name=`basename "$0" | cut -d'.' -f1`
output_file="${date_time}__${output_file}.txt"

file_content="listToRandomize.json\n"
file_content+="--------------------\n"
file_content+=`cat listToRandomize.json`
file_content+="\n\n"

file_content+="lastResult.json\n"
file_content+="---------------\n"
file_content+=`cat lastResult.json`
file_content+="\n\n"

file_content+="alreadyRandomized.json\n"
file_content+="----------------------\n"
file_content+=`cat alreadyRandomized.json`
file_content+=""

echo -e "Saving file as: $output_file\n"
echo -e "$file_content" > "$output_file"
cat "$output_file"
