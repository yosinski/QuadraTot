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

package:
	cp main.tex abstract.tex introduction.tex relatedWork.tex problemDefinition.tex experimentalSetup.tex platformDetails.tex fitnessEvaluation.tex learningMethods.tex hyperNeatMethod.tex results.tex conclusion.tex futureWork.tex acknowledgments.tex references.bib ownstyles.sty alifexi.sty ../figures/robot_whitebg.jpg ../figures/topdown2.jpg ../figures/wiiMote_crop.jpg ../figures/robot_led_crop.jpg ../figures/linearInterp.pdf ../figures/hyperneatExplanation.png ../figures/SpiderANN.jpg ../figures/std_error.pdf ../figures/hnResults.pdf ../figures/neat_110115_211410_00000_002_filt_zoom.pdf YOSINSKI/
	cd YOSINSKI && mv main.tex YOSINSKI.tex
	cd YOSINSKI && pdflatex YOSINSKI
	cd YOSINSKI && bibtex YOSINSKI
	cd YOSINSKI && pdflatex YOSINSKI
	cd YOSINSKI && pdflatex YOSINSKI
	cd YOSINSKI && rm *.aux *.log *.blg
	tar cvzf YOSINSKI.tgz YOSINSKI

clean:
	rm -f *.aux *.log *~ *.dvi *.out *.bbl *.blg *.lot *.lof *.toc ${TARGETS}
