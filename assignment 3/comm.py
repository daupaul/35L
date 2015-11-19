#!/usr/bin/python

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys
from optparse import OptionParser

class comm:
    def __init__(self, filename, filename2):
        if filename != "-":
            f = open(filename, 'r')
        else:
            f = sys.stdin
        self.lines1 = f.readlines()
        f.close()
        if filename2 != "-":
            g = open(filename2,'r')
        else:
            g = sys.stdin
        self.lines2 = g.readlines()
        g.close()
        
    def colOne(self):
        return self.lines1
    
    def colTwo(self):
        return self.lines2

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE1 FILE2

Compare sorted files FILE1 and FILE2.
When there are no options, produce output with three columns.
Column one: lines unique to FILE1
Column two: lines unique to FILE2
Column three: lines in both files """

    parser = OptionParser(version=version_msg,
                          usage=usage_msg)     #create OptionParser instance

    parser.add_option("-1", "--suppress1",
                      action="store_true", default=False,
                      help="suppress output column 1")
    parser.add_option("-2", "--suppress2",
                      action="store_true", default=False,
                      help="suppress output column 2")
    parser.add_option("-3", "--suppress3", default=False,
                      help="suppress output column 3")
    parser.add_option("-u", "--notsorted",
                      action="store_true", default=False,
                      help="comparing files that are not sorted")

    #options: object containing all option args
    #args: list of positional args leftover after parsing options
    options, args = parser.parse_args(sys.argv[1:])

    if len(args) != 2:
        if len(args) == 0:
            parser.error("need operand")
        if len(args) == 1:
            parser.error("need operand after {0}".
                         format(args[0]))
        if len(args) > 2:
            parser.error("extra operand after {0}".
                         format(args[1]))
    input_filename = args[0]
    input_filename2 = args[1]

    #instantiate comm object w/ parameter input_filename
    #and input_filename2
    try:
        generator = comm(input_filename, input_filename2)
        a = generator.colOne()
        b = generator.colTwo()

    #error msg in the format of "I/O error(errno): strerror"
    except IOError as (errno, strerror):
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))
        
    supOne = options.suppress1
    supTwo = options.suppress2
    supThree = options.suppress3
    result = ""

    #some files don't end with \n
    if "\n" not in a[len(a)-1]:
        a[len(a)-1] += '\n'
    if "\n" not in b[len(b)-1]:
        b[len(b)-1] += '\n'
    
    #w/o -u
    if not options.notsorted:
        i = 0
        j = 0
        p1 = False
        p2 = False

        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                #check sort
                if i > 0 and a[i-1]>a[i] and not p1:
                    p1 = True
                    result += "File 1 is not sorted. \n"
                if not supOne:
                    result += a[i]
                i = i + 1
            elif a[i] > b[j]:
                if j > 0 and b[j-1]>b[j] and not p2:
                    p2 = True
                    result += "File 2 is not sorted. \n"
                if not supTwo:
                    if supOne:
                        result += b[j]
                    else:
                        result += "\t" + b[j]  #add tab char
                j = j + 1
            else:
                if not supThree:
                    if supThree and supTwo:
                        result += a[i]
                    elif supOne and not supTwo:
                        result += "\t" + a[i]
                    elif supTwo and not supOne:
                        result += "\t" + a[i]
                    else:
                        result += "\t\t" + a[i]
                    i = i + 1
                    j = j + 1

        if len(a) > i and not supOne:
            for p in range(i, len(a)):
                result += a[p]
        if len(b) > j and not supTwo:
            for p in range(j, len(b)):
                if supOne:
                    result += b[p]
                else:
                    result += "\t" + b[p]
    else:  #w/ -u
        for i in range(len(a)):
            exist=False
            for j in range(len(b)):
                if a[i] == b[j]:
                    if not supThree:
                        if supOne and supTwo:
                            result += a[i]
                        elif supOne and not supTwo:
                            result += "\t" + a[i]
                        elif supTwo and not supOne:
                            result += "\t" + a[i]
                        else:
                            result += "\t\t" + a[i]
                    b.pop(j) #delete that line in b
                    exist=True
                    break
            #doesn't exist in b
            if not exist and not supOne:
                result+= a[i]
        #add remaining lines in file2
        if not supTwo:
            for i in range(len(b)):
                if supOne:
                    result  += b[i]
                else:
                    result += "\t" + b[i]

    sys.stdout.write(result)
                            
# in order to make the Python file a standalone program
if __name__ == "__main__":
    main()
