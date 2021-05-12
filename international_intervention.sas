data temp;
		input passengers @@;
		date = intnx( 'month', '1jan2010'd, _n_-1 );
		format date monyy7.;
		datalines;
6.81
6.01
7.53
6.94
7.40
8.10
9.05
8.64
6.84
7.07
6.51
7.27
7.15
6.20
7.73
7.49
7.67
8.25
9.38
8.67
6.89
6.88
6.43
7.33
7.16
6.52
8.06
7.61
7.73
8.51
9.30
8.89
7.10
6.95
6.71
7.50
7.33
6.56
8.33
7.56
8.02
8.88
9.71
9.40
7.26
7.27
6.88
7.97
7.67
6.77
8.50
8.09
8.48
9.20
9.99
9.63
7.34
7.29
7.05
8.17
7.94
6.89
8.52
8.12
8.57
9.35
10.40
9.98
7.66
7.74
7.33
8.41
8.22
7.28
8.85
8.24
8.66
9.65
10.65
9.85
7.77
7.75
7.26
8.74
8.45
7.24
8.93
9.10
9.18
10.21
11.19
10.38
7.73
8.03
7.68
8.91
8.56
7.60
9.60
9.04
9.42
10.57
11.39
10.62
8.21
8.40
8.05
9.21
8.96
7.87
9.95
9.46
9.95
11.02
11.64
11.04
8.59
8.68
8.24
9.57
9.14
7.94
4.64
0.13
0.19
0.40
1.12
1.38
1.40
1.97
2.45
3.25
2.98
;

run;


data alldata;
		set temp;


			if '01mar2020'd<=date<='01jul2020'd then ls = 1;
			else ls = 0;


			if date = '01aug2020'd then tc = 1;
			else tc=0;

run;


ods html style=statistical;
ods graphics on;

proc arima data=alldata	plots = all;
      identify var=passengers(1 12) crosscorr=(ls(1 12) tc(1 12));
      estimate q =(1) (12)  input = (ls/(1)tc) method=ml;
	  forecast id=date interval=month back = 7 lead = 7 printall out=b;
run;
quit;

ods graphics off;
ods html close;