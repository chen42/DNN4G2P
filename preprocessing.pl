#!/usr/bin/perl

# I started this in R, but merging in R is too slow. So the rotated data frame is saved and the genotype data is merged with the phenotype (coat color) using the code below. 

$fn=$ARGV[0]; # e.g. hschr1t.txt. This is the rotated genotype data frame

if ($fn=~/hschr(\d+)t/){
	$chr=$1;
} else {
	print "wrong file name: $fn\n";
	exit;
}

open(GT, $fn) || die; # genotype data 
open (FH, "coatColor.txt") || die; ## phenotype data 
while (<FH>){
	if ($_=~/(^.+)\t(.+$)/){
			$cc{$1} = $2;
	}
}

open (OUT, ">chr$chr\_all.csv") || die;

## formatting for rQTL data format, line two is chr, line three is loc. 
while (<GT>) {
	$cnt++;
	if ($cnt==1) {
		$header=$_;
		$header=~s/\t/,/g;
		print OUT "pheno,$header";
	} elsif ($cnt==-2) { #disable this section, which is only used for generateing rQTL data format
		@l=split(/\t/, $_);
		foreach (@l){
			$out.="1,";
		}
		$out=~s/,1,$//; ## somehow there is one extra 1 as needed 
		print OUT ",$out\n";
		$out='';
		#add a third line
		@l=split(/,/, $header);
		foreach (@l){
			if ($_=~/Rn34_$chr(\d+)/) {; 
				$out.=$1.",";
			}
		}
		$out=~s/,$/\n/;
		print OUT ",$out";
		$out='';
	} elsif  ($_=~/^"(.+)"\t(.+$)/){ ## encode coat color
		$id=$1;
		$genotype=$2;
		$genotype=~s/\t/,/g;
		$id=~s/_DNA//;

		if ($cc{$id}) { 
			$cC=$cc{$id};
			$cC=~s/\t/,/g;
			$cC=~s/^DBsp/1/;
			$cC=~s/^DB/0/;
			$cC=~s/^LBsp/3/;
			$cC=~s/^LB/2/;
			$cC=~s/^W/4/;
			$cC=~s/NA/-1/g;
			print OUT "$cC,$genotype\n";
		}
	} 
}



