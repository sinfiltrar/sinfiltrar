#!/bin/bash

DBHOST=sinfiltrar2.c2yrjc7heqtk.us-west-2.rds.amazonaws.com
DATE=`date +"%Y%m%d"`
FILENAME=sinfiltrar-$DATE.sql
FILEPATH=/tmp/$FILENAME
export PGPASSWORD=$DBPASS

echo -e "Connecting to \033[37m$DBHOST\033[0m"
echo -e "Dumping remote database to \033[37m$FILEPATH\033[0m"
if ! pg_dump -h $DBHOST -U postgres -Fc sinfiltrar > $FILEPATH ; then 
	echo -e"\033[31mError\033[0m: Unable to dump remote database"
	exit 1
fi

echo "Dropping old database"
if ! dropdb sinfiltrar --if-exists ; then
        echo -e "\033[31mError\033[0m: Unable to dump remote database"
	exit 1
fi

echo "Importing into \033[37m$FILEPATH\033[0m local database"
if ! pg_restore -C -d sinfiltrar -h localhost $FILEPATH  ; then
	echo -e "\033[31mError\033[0m: Unable to import dump to local database"
	exit 1
fi
