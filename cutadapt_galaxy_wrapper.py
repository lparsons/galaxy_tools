#!/usr/bin/env python
"""
SYNOPSIS

    cutadapt_galaxy_wrapper.py 
        -i input_file
        -o output_file
        [-f format (fastq/fastq/etc.)]
        [-a 3' adapter sequence]
        [-b 3' or 5' anywhere adapter sequence]
        [-e error_rate]
        [-n count]
        [-O overlap_length]
        [--discard discard trimmed reads]
        [-m minimum read length]
        [-M maximum read length]
        [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

   Wrapper for cutadapt running as a galaxy tool

AUTHOR

    Lance Parsons <lparsons@princeton.edu>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import sys, os, traceback, optparse, shutil, subprocess, tempfile
import re
#from pexpect import run, spawn

def stop_err( msg ):
    sys.stderr.write( '%s\n' % msg )
    sys.exit()

def main ():

    global options, args
    # Setup Parameters 
    params = []
    if options.adapters != None:
        params.append("-a %s" % " -a ".join(options.adapters))
    if options.anywhere_adapters != None:
        params.append("-b %s" % " -b ".join(options.anywhere_adapters))
    if options.output_file != None:
        params.append("-o %s" % options.output_file)
    if options.error_rate != None:
        params.append("-e %s" % options.error_rate)
    if options.count != None:
        params.append("-n %s" % options.count)
    if options.overlap_length != None:
        params.append("-O %s" % options.overlap_length)
    if options.discard_trimmed:
        params.append("--discard")
    if options.minimum_length != None:
        params.append("-m %s" % options.minimum_length)
    if options.maximum_length != None:
        params.append("-M %s" % options.maximum_length)

    # cutadapt relies on the extension to determine file format: .fasta or .fastq
    input_name = '.'.join((options.input,options.format))
    # make temp directory
    tmp_dir = tempfile.mkdtemp()

    try:
        # make a link to the input file in the tmp_dir
        input_file = os.path.join(tmp_dir,os.path.basename(input_name)) 
        os.symlink( options.input, input_file) 
        
        # generate commandline
        cmd = 'cutadapt %s %s' % (' '.join(params),input_file)
        proc = subprocess.Popen( args=cmd, shell=True, cwd=tmp_dir,
                                stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()
        returncode = proc.returncode
        if returncode != 0:
            raise Exception, 'Execution of cutadapt failed.\n%s' % stderrdata
        print stderrdata

    finally:
        # clean up temp dir
        if os.path.exists( input_name ):
            os.remove( input_name )
        if os.path.exists( tmp_dir ):
            shutil.rmtree( tmp_dir )

if __name__ == '__main__':
    try:
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option( '-i', '--input', dest='input', help='The sequence input file' )
        parser.add_option( '-f', '--format', dest='format', default='fastq',
                          help='The sequence input file format (default: fastq)' )
        parser.add_option ('-a', '--adapter', action='append', dest='adapters', help='3\' adapter sequence(s)')
        parser.add_option ('-b', '--anywhere', action='append', dest='anywhere_adapters', help='5\' or 3\' "anywhere" adapter sequence(s)')
        parser.add_option ('-e', '--error-rate', dest='error_rate', help='Maximum allowed error rate')
        parser.add_option ('-n', '--times', dest='count', help='Try to remove adapters COUNT times')
        parser.add_option ('-O', '--overlap', dest='overlap_length', help='Minimum overlap length')
        parser.add_option ('--discard', '--discard-trimmed', dest='discard_trimmed', action='store_true', default=False, help='Discard reads that contain the adapter')
        parser.add_option ('-m', '--minimum-length', dest='minimum_length', help='Discard reads that are shorter than LENGTH')
        parser.add_option ('-M', '--maximum-length', dest='maximum_length', help='Discard reads that are longer than LENGTH')
        parser.add_option ('-o', '--output', dest='output_file', help='The modified sequences are written to the file')
        (options, args) = parser.parse_args()
        if options.input == None:
             stop_err("Misssing option --input")
        if options.output_file == None:
             stop_err("Misssing option --output")
        if not os.path.exists(options.input):
            stop_err("Unable to read intput file: %s" % options.input)
   #if len(args) < 1:
        #    parser.error ('missing argument')
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

