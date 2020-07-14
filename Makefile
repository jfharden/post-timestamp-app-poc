.PHONY: doc

doc:
	 docker run -v `pwd`/docs/:/data --rm -ti pandoc/latex:2.9 pandoc system-design.md --table-of-contents -o system-design.pdf
