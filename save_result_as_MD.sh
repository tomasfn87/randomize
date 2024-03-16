#!/bin/bash

source './colorize.sh'

for file in alreadyRandomized.json lastResult.json listToRandomize.json; do
  if [ ! -f "$file" ]; then
    echo "`toRed ERROR`: the file `toYellow $file` does not exist. Aborting the script."
    exit 1
  fi
done

if [ $# -eq 0 ]; then
    echo "`toRed ERROR`: wrong input. Please specify file name as argument. i.e: `toYellow ./save_result_as_MD.sh\ 'file_name'`."
    exit 2
fi

output_file="$1"
output_file=`echo "$output_file" | tr -cd '[:alnum:] _\-.'`
output_file=`echo "$output_file" | sed 's/ \{1,\}/-/g'`
output_file=`echo "$output_file" | sed 's/\.\{1,\}/-/g'`
output_file=`echo "$output_file" | sed 's/\-\{2,\}/-/g'`
output_file=`echo "$output_file" | sed 's/_\{2,\}/_/g'`
output_file=`echo "$output_file" | sed 's/^ *//g' | sed 's/ *$//g'`
output_file=`echo "$output_file" | sed 's/ /-/g'`
output_file=`echo "$output_file" | sed 's/\./-/g'`

if [ -z "$output_file" ]; then
    echo -n "Wrong input: file name can use only letters, numbers,"
    echo -n " _ and -; empty spaces and dots will be converted to -."
    echo " i.e: ./save_result_as_MD.sh 'file_name'"
    exit 3
fi

date_time=`date '+%Y-%m-%d_%Hh%Mmin%Ss'`
output_file="${date_time}__${output_file}.md"

file_content='# [`randomize`](https://github.com/tomasfn87/randomize)\n\n'
file_content+='## Log report\n\n'

file_content+='### *__File__:* `listToRandomize.json`\n\n'
file_content+='```json\n'
file_content+="`cat listToRandomize.json`\n"
file_content+='```\n\n'
file_content+='---\n\n'

file_content+='### *__File__:* `lastResult.json`\n\n'
file_content+='```json\n'
file_content+="`cat lastResult.json`\n"
file_content+='```\n\n'
file_content+='---\n\n'

file_content+='### *__File__:* `alreadyRandomized.json`\n\n'
file_content+='```json\n'
file_content+="`cat alreadyRandomized.json`\n"
file_content+='```'

echo -e "Saving file as: $output_file\n"
echo -e "$file_content" > "$output_file"
cat "$output_file"
