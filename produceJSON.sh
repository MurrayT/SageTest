#!/usr/bin/env bash

# $1 is assignment name
# $2 is filename
# $3 is the file containing the test cases

basedir=Student_work-collect
assigndir=$basedir/$1

if [[ -d $assigndir ]]; then
    for student in $(ls $assigndir); do
        filename=$assigndir/$student/$2    # this is the file that we're working with

        users=`sed -n 's/.*id:\s*\(.*\)/\1/p' $filename`
        if [[ -n "$users" ]]; then
            sage JSON.sage $filename $3 $users
        fi
    done
fi
