@echo off

SET dist_dir=%cd%\dist
SET archive=lambda_deps.zip
SET archive_path=%dist_dir%\%archive%
SET requirements=%cd%\requirements.txt
SET target=python\lib\python3.8\site-packages

IF not exist %dist_dir% (
  mkdir %dist_dir%
)

IF exist %archive_path% (
  DEL %archive_path%
)

echo Installing dependencies...
for /F "tokens=*" %%A in (%requirements%) do (
  if not %%A == boto3 (
    echo %%A
    pip install --target=%target% --python 3.8 --only-binary=:all: --upgrade --no-user %%A
  )
)

echo Building dependency zip
tar -a -c -f %archive_path% %target%
echo Lambda pack complete