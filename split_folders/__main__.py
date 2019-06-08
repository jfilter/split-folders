from .split import *
import argparse
import sys

if __name__=="__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-r", "--ratio",nargs='*',type=float,
	    help="The ratio to split. e.g. for train/val/test `.8 .1 .1` or for train/val `.8 .2`. Default is `.8 .1 .1`, just pass `-r` for default.")
	ap.add_argument("-f", "--fixed",nargs='*',type=int,
	    help="Set the absolute number of items per validation/test set. The remaining items constitute the training set. e.g. for train/val/test `100 100` or for train/val `100`. Default is `100 100`, just pass `-f` for default.")
	ap.add_argument("-s", "--seed", type=int, default=1337,
	    help="Set seed value for shuffling the items. defaults to 1337.")
	ap.add_argument("-os", "--oversample",action='store_true',
	    help="Enable oversampling of imbalanced datasets, works only with --fixed.")
	ap.add_argument("-i", "--input", required=True,
		help="The input folder path.")
	ap.add_argument("-o", "--output", default='output',
		help="Path to the output folder. defaults to `output`. Get created if non-existent.")
	args = vars(ap.parse_args())
	
	#Check if ratio and fixed, both are not set
	if '-r' not in sys.argv and '-f' not in sys.argv:
		print("You need to chose either `ratio` or `fixed`")
		quit()
	#Check if ratio and fixed are both set
	elif '-f' in sys.argv and '-r' in sys.argv:
		print("You can not choose both, chose either `ratio` or `fixed`")
		quit()	

	if '-r' in sys.argv:
		if args["oversample"]:
			print("Oversampling will be ignored as it only works with `fixed`")
		ratiovar = tuple(args["ratio"])
		if len(ratiovar)<1:
			ratiovar = [.8,.1,.1]
		if len(ratiovar)==1:
			print("You have to give more than one ratio value")
			quit()
		ratio(args["input"], output=args["output"], seed=args["seed"], ratio=ratiovar)
	elif '-f' in sys.argv:
		splitvar = tuple(args["fixed"])
		if len(splitvar)<1:
			splitvar = [100,100]
		fixed(args["input"], output=args["output"], seed=args["seed"], fixed=splitvar, oversample=args["oversample"])