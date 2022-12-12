#!/bin/bash

dist_dir="$PWD/dist"
archive="lambda.zip"
archive_path="$dist_dir/$archive"

if [[ ! -d $dist_dir ]]; then
  mkdir $dist_dir
fi

# delete archive if it exists
if [[ -e $archive_path ]]; then
  rm $archive_path
fi

echo "Building lambda zip..."
zip -rjq $archive_path "$PWD/index.py"
zip -rjq $archive_path "$PWD/constants.py"
zip -rjq $archive_path "$PWD/aws.py"
zip -rjq $archive_path "$PWD/utils.py"
zip -rjq $archive_path "$PWD/rent_peek_generation.py"
zip -rq $archive_path "./imgs/"

echo "Lambda pack complete"
