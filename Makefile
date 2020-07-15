.PHONY: doc test

doc:
	 docker run -v `pwd`/docs/:/data --rm -ti pandoc/latex:2.9 pandoc system-design.md --table-of-contents -o system-design.pdf

test:
	python -m unittest discover
	python -m unittest discover --start-dir lambdas/sqs_to_s3
	python -m unittest discover --start-dir lambdas/dynamo_inserter
