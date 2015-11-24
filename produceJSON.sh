#!/usr/bin/env bash

# $1 is assignment name
# $2 is filename
# $3 is the file containing the test cases

basedir=Student_work-collect
assigndir=$basedir/$1

if [[ -z "$2"]]; then
    echo "Assuming default structure"
    solutionsfile=$1_solutions.sage
    testcasefile=~/SMCHomeworkGeneration/$1/$1_grading_testcases
else
    solutionsfile=$2
    testcasefile=$3
fi

if [[ -d $assigndir ]]; then
    for student in $(ls $assigndir); do
        filename=$assigndir/$student/$solutionsfile    # this is the file that we're working with

        users=`sed -n 's/.*id:\s*\(.*\)/\1/p' $filename`
        if [[ -n "$users" ]]; then
            sage JSON.sage $filename $testcasefile $users
        fi
    done
fi
