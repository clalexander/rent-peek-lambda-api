#!/bin/bash

# To be used to create lambda layer archive

dist_dir="$PWD/dist"
archive="lambda_deps.zip"
archive_path="$dist_dir/$archive"
requirements="$PWD/requirements.txt"
target="./python/lib/python3.8/site-packages"

if [[ ! -d $dist_dir ]]; then
  mkdir $dist_dir
fi

# delete archive if it exists
if [[ -e $archive_path ]]; then
  rm $archive_path
fi

# install dependencies
echo "Installing dependencies..."
for dep in $(cat "$requirements"); do
  # igrnore boto3
  if [[ $dep != "boto3" ]]; then
    echo $dep
    pip install --target=$target --python 3.8 --only-binary=:all: --upgrade $dep
  fi
done

# pack dependencies
echo "Building dependency zip..."
zip -rq $archive_path $target

echo "Pack dependencies complete"
