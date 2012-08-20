TARGETS=main.pdf

all: ${TARGETS}

#%.pdf : %.tex
#	pdflatex $<
#	bibtex $*
#	pdflatex $<
#	pdflatex $<

# HACK for no bib file
%.pdf : %.tex
	pdflatex $<
	pdflatex $<

quick :
	pdflatex main

skimreload :
	skimreload main.pdf

clean:
	rm -f *.aux *.log *~ *.dvi *.out *.bbl *.blg *.lot *.lof *.toc ${TARGETS}
