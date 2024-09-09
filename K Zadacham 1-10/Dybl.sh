#!/bin/bash


directory="$1"

# Проверяем, передан ли путь к каталогу
if [ -z "$directory" ]; then
  echo "Необходимо указать путь к каталогу."
  exit 1
fi
if [ ! -d "$directory" ]; then
  echo "Указанный каталог не существует."
  exit 1
fi


cd "$directory" || exit


temp_file=$(mktemp)

find . -type f -exec sh -c 'sha256sum "$1" | cut -d" " -f1' _ {} \; > "$temp_file"

sort "$temp_file" | uniq -d | while read -r hash; do
  grep "^$hash" "$temp_file" | cut -d" " -f2-
  echo
done

rm "$temp_file"
