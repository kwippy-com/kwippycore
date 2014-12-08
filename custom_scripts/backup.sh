#!/bin/bash
DATE_VAL=`date +'%s'`
mysqldump -u kwippy_user -phelloworld69 kwippy_staging > /root/custom_scripts/sql_dump/"$DATE_VAL"-dump.sql
