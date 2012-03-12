TARGETS=main.pdf

all: ${TARGETS}

%.pdf : %.tex
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<

skim: ${TARGETS}
	skimreload ${TARGETS}

clean:
	rm -f *.aux *.log *~ *.dvi *.out *.bbl *.blg *.lot *.lof *.toc ${TARGETS}
