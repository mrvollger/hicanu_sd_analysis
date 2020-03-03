#!/usr/bin/env python
import argparse
import sys

parser = argparse.ArgumentParser(description="")
parser.add_argument("infile", help="paf file")
parser.add_argument("-s", "--string", help="string option")
parser.add_argument("-n", "--number", help="numeric option", type=int, default=5)
parser.add_argument("-l", "--list", nargs="*", help="list with zero or more entries")
parser.add_argument('-d', help="store args.d as true if -d",  action="store_true", default=False)
args = parser.parse_args()

import pandas as pd


col = [ "q_name", "q_len", "q_st", "q_en", "strand", "r_name", "r_len", "r_st", "r_en", "match", "aln_len", "qual", "tp"]
df = pd.read_csv(args.infile, sep="\t", comment=":", names=col)

# restuns end postions in ref and dist from contig start
def get_end(row, start=True):
	if(row["strand"] == "+"):
		if(start):
			return( row["r_st"], row["r_st"]+1, row["q_st"])
		else:
			return(row["r_en"]-1, row["r_en"], row["q_len"] - row["q_en"])
	else:
		if(start):
			return(row["r_en"]-1, row["r_en"], row["q_st"])
		else:
			return(row["r_st"], row["r_st"]+1, row["q_len"]-row["q_en"])



#
out = []
for contig, group in df.groupby(by="q_name"):
	
	start = group.loc[ group["q_st"].idxmin() ]
	end = group.loc[ group["q_en"].idxmax() ]

	start["break_st"], start["break_en"], start["diff"] = get_end(start)
	start["end"] = "Start"
	end["break_st"], end["break_en"], end["diff"] = get_end(end, start=False)
	end["end"] = "End"
	out += [start, end]
	

out = pd.DataFrame(out)

out[["r_name", "break_st", "break_en", "q_name", "q_len", "end", "diff"]].to_csv(sys.stdout, sep="\t", header=False, index=False)


