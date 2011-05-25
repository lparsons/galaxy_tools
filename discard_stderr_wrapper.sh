#!/bin/sh

# STDERR wrapper - discards STDERR if command execution was OK.

#
# This script executes a given command line,
# while saving the STDERR in a temporary file.
#
# When the command is completed, it checks to see if the exit code was zero.
# if so - the command is assumed to have succeeded - the STDERR file is discarded.
# if not - the command is assumed to have failed, and the STDERR file is dumped to the real STDERR
#
#
# Use this wrapper for tools which insist on writting stuff to STDERR
# even if they succeeded - which throws galaxy off balance.
#
#
# Copyright 2009 (C) by Assaf Gordon
# This file is distributed under the BSD license.
#
# Modified by Lance Parsons (2011)
# Echo STDERR to STDOUT if return code was 0

TMPFILE=$(mktemp -t tmp.XXXXXXXXXX) || exit 1
#CWD=`pwd`
#DIRECTORY=$(cd `dirname $0` && pwd)
#cd $DIRECTORY
"$@" 2> $TMPFILE

EXITCODE=$?
# Exitcode != 0 ?
if [ "$EXITCODE" -ne "0" ]; then
	cat $TMPFILE >&2
else
#	echo "Testing STDOUT"
	cat $TMPFILE >&1
fi
rm $TMPFILE
cd $CWD
exit $EXITCODE
