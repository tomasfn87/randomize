#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Wrong input: please specify file name as argument. i.e: ./save_result_as_JSON.sh 'file_name'"
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
    echo -n "Wrong input: file name can use only letters, numbers,"
    echo -n " _ and -; empty spaces and dots will be converted to -."
    echo " i.e: ./save_result_as_JSON.sh 'file_name'"
    exit 2
fi

date_time=`date '+%Y-%m-%d_%Hh%Mmin%Ss'`
script_name=`basename "$0" | cut -d'.' -f1`
output_file="${date_time}__${output_file}.json"

file_content="["
file_content+="{\"file\": \"listToRandomize.json\", \"content\": `cat listToRandomize.json`},"
file_content+="{\"file\": \"lastResult.json\", \"content\": `cat lastResult.json`},"
file_content+="{\"file\": \"alreadyRandomized.json\", \"content\": `cat alreadyRandomized.json`}"
file_content+="]"

echo -e "Saving file as: $output_file"
echo "$file_content" > "$output_file"

if command -v jq &> /dev/null; then
    echo ''
    jq '' "./$output_file"

    tmp_content=`cat "$output_file" | jq '' -M`
    echo "$tmp_content" > "$output_file"
fi
