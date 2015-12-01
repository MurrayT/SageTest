#!/usr/bin/env bash

# $1 is assignment name
# $2 is filename
# $3 is the file containing the test cases

basedir=E-402-STFO-collect
assigndir=$basedir/assignments/$1

if [[ -z "$2"]]; then
    echo "Assuming default structure" >&2
    solutionsfile=$1_solutions.sage
    testcasefile=~/SMCHomeworkGeneration/$1/$1_grading_testcases
else
    solutionsfile=$2
    testcasefile=$3
fi

if [[ -d $assigndir ]]; then
    for student in $(ls $assigndir); do
        filename=$assigndir/$student/$solutionsfile    # this is the file that we're working with
        sage JSON.sage $filename $testcasefile
    done
fi
