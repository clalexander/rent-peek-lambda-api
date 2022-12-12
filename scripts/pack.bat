@echo off

SET dist_dir=%cd%\dist
SET archive=lambda.zip
SET archive_path=%dist_dir%\%archive%
SET temp_path=%dist_dir%\temp.gz

IF not exist %dist_dir% (
  mkdir %dist_dir%
)

IF exist %archive_path% (
  DEL %archive_path%
)

IF exist %temp_path% (
  DEL %temp_path%
)

echo Building lambda zip...
tar -cf %temp_path% index.py^
  constants.py^
  aws.py^
  utils.py^
  rent_peek_generation.py
tar -r -f %temp_path% fonts
tar -r -f %temp_path% imgs
tar -a -f %archive_path% -c @%temp_path%

DEL %temp_path%

echo Lambda pack complete