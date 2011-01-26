TARGETS=main.pdf

all: ${TARGETS}


# pdflatex method

%.pdf : %.tex
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<


# latex method

#%.pdf : %.ps
#	ps2pdf $< $@
#
#%.ps : %.dvi
#	dvips -t letter -o $@ $<
#
#%.dvi : %.tex
#	latex $*
#	bibtex $*
#	latex $*
#	latex $*


clean:
	rm -f *.aux *.log *~ *.dvi *.out *.bbl *.blg *.lot *.lof *.toc ${TARGETS}
