TARGETS=main.pdf

all: ${TARGETS}

%.pdf : %.tex
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<

clean:
	rm -f *.aux *.log *~ *.dvi *.out *.bbl *.blg *.lot *.lof *.toc ${TARGETS}
