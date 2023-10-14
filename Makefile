##########################################
# openscad Makefile
# Tom Draper 2017
##########################################
# Targets
# $@ = file to be made
# $? = changed dependents
# $< = file that caused action
# $* = prefix shared by target and dependent files

# Identify SCAD files
PY	= $(wildcard *.py) # List all python files in directory
	
# Secondary files automatically created
SCAD	= $(PY:.py=.scad)
STL	= $(SCAD:.scad=.stl)
DXF	= $(SCAD:.scad=.dxf)

AUTO = $(SCAD) $(STL) $(DXF)

all:	$(SCAD)

stl:	$(STL)

dxf:	$(DXF)

%.scad: %.py
	python3 $< > $@

%.stl:	%.scad
	openscad -m make -o $@ $<

%.dxf:	%.scad
	openscad -o $@ $<

clean:
	/bin/rm -f $(AUTO)

.SECONDARY:	$(SCAD) $(STL) $(DXF)
.PHONY:		all clean stl dxf
