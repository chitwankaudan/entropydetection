TXT_FILES = $(wildcard haystacks/*.txt)
DAT_FILES = $(patsubst haystacks/%.txt, haystacks/%.dat, $(TXT_FILES))

env : environment.yml
	conda env create -f environment.yml

scan : $(DAT_FILES) $(TXT_FILES)
	python scan.py

.PHONY : haystacks
haystacks :
	mkdir haystacks
	python rand_sig.py 10 --dSNR 5 5
	python rand_sig.py 10 --dSNR 5 5 --NeedleType 'noise'

.PHONY : clean
clean :
	rm -r haystacks/
	