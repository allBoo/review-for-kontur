#!/bin/bash

if [ "$MIGRATE_DB" != "" ]; then
  ./manage.py migrate --noinput
fi

if [[ $@ == "bash" ]]
then
	echo "Command line argument is set [$@].";
	exec "bash";
elif [[ $@ == "debug" ]]
then
	echo "Command line argument is set [$@].";
	exec "fastapi" "dev" "--host" "0" "app/api.py";
elif [[ $@ != "" ]]
then
	echo "Command line argument is set [$@].";
	exec "bash" "-c" "$@";
else
	echo "Command line argument not set.";
	exec "fastapi" "run" "app/api.py"
fi
