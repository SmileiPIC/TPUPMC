#!/bin/bash

MPIEXEC=mpirun

H=$PWD # current dir
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ) # dir of this script
smilei=$DIR/../Smilei/smilei # path to the smilei executable
script=$0 # name of this script

# Function to explain usage
usage () {
    echo "usage: $script namelist1 [namelist2 ...] [-o outdir]"
}

# Check that at least one argument provided
if [ "$#" -lt 1 ]; then
    usage
    exit 1
fi
proc=1


# Loop additional namelists
namelists=()
namelist_files=()
firstnamelist=""

while [[ $# -ge 1 ]]; do
    arg=$1
    # If -o option, leave
    if [[ $arg == -o* ]]; then
        break
    fi
    # Try to convert to absolute path
    absnml="$(cd "$(dirname "$arg")" && pwd)/$(basename "$arg")"
    # If file, then add it as namelist
    if [ -f $absnml ]; then
        echo "Namelist found: "$absnml
        namelists+=("`basename $absnml`")
        namelist_files+=("$absnml")
        # Save the first namelist
        if [ -z $firstnamelist ]; then
            firstnamelist=$absnml
        fi
    # Otherwise add it as python commands
    else
        namelists+=("\"$arg\"")
    fi
    shift
done

# Error if no namelist
if [ -z $firstnamelist ]; then
    echo "$script: At least one namelist must be provided."
    usage
    exit 1
fi

# Next argument, if exists, is the outdir 
base="`basename $firstnamelist .py`" # strip directory and extension of first namelist
echo $base
outdir=$base # by default, the outdir is same as first namelist
# otherwise, provided as argument
if [ "$#" -gt 0 ]; then
    if [[ $1 == -o ]]; then
        shift
        if [ "$#" -lt 1 ]; then
            usage
            exit 1
        fi
        outdir=$1
        shift
    fi
fi

# If outdir already exist, error
if [ -d $outdir ]; then
  echo "*   "
  echo "*   Directory $outdir already exists. Removing"
  echo "*   "
  rm -rf $outdir
fi

# Error if arguments leftover
if [ "$#" -gt 0 ]; then
    usage
    exit 1
fi

# Make new directory, go there, and run
mkdir -p $outdir
# copy namelists there
for namelist in "${namelist_files[@]}"; do
    cp $namelist $outdir
done
cd $outdir
$MPIEXEC -mca btl tcp,sm,self -np $proc $smilei "${namelists[@]}"
cd $H

echo "Launching smileiQt.pt $outdir"
smileiQt.py $outdir


