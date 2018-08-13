#! /usr/bin/env python3
import argparse
import pyparsing as pp
import pprint
import datetime
from time import strptime
   


parser = argparse.ArgumentParser()

parser.add_argument('filename', help='Name of file to be parsed. Required.')
parser.add_argument('--fileType', '-t', help='Type of file to be parsed. (E.g., syslog)')
parser.add_argument('--limit', '-l', type=int, help='Number of lines to parse in increments of 20.')
parser.add_argument('--output', '-o', help='Name of output file, if any.')

args = parser.parse_args()


currentYear = now = datetime.datetime.now().year
# Grammar
month = pp.Word(pp.alphas,exact=3) #string.uppercase, string.lowercase,
integer = pp.Word(pp.nums)
serverDateTime = pp.Combine(month + " " + integer + " " + integer + ":" + integer + ":" + integer)
hostname = pp.Word(pp.alphas + pp.nums + "_" + "-")# + pp.Optional(pp.Suppress("[") + integer + pp.Suppress("]")) + pp.Suppress(":")
message = pp.Regex(".*") +  pp.Optional(pp.Suppress(":"))
serverDateTime.setParseAction(lambda t:(str(currentYear) + ' ' + ' '.join(t)))

bnf = serverDateTime + hostname + message # + daemon 


fields = []
results = []
#open file in try block
try:
    f = open(args.filename)
except:
    print('Whoa, nelly!')

with f:
    # following constructed to get around a 40-line limit TODO: check buffer on read. also, consider replacing with filestream
    if args.limit:
        x = 0;z=0;
        if 0 < args.limit <= 20:
            z = 1
            x = args.limit
        else:
            if x % 40 == 0:
                z = int(args.limit/20)
                x = 20
            else:
                print('blah!')
        for y in range(0,z):
            for i in range(0,x):
                lines = f.readline()
            
                try:
                    fields.append(bnf.parseString(lines))
                
                
                except: 
                    print('Error:','\n','Line: ', lines[i])
    else:
        #lines = f.read()
        lines = f.readline()
        #print(lines)
        #count = 0
        try:
            #for line in lines:
            fields.append(bnf.parseString(lines))
               # count += 1        
        except: 
            print('Error:')
            
    #if args.fileType == 'syslog':
        #
            #results = (OneOrMore(Group(serverDateTime))).parseString(line).asDict()
            #text = line
        #print(lines)
        
#print('1: ' fields[0][0])
#d = pp.dictOf(pp.OneOrMore(pp.Group(columnKey + fields)))
                
           
pprint.pprint(fields)