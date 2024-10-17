ready/report.pdf: docs/report_lab_01_AA.pdf
	mkdir -p ./ready
	cp docs/report_lab_01_AA.pdf ready/report.pdf

ready/stud-unit-test-report-prev.json: tests/res.json
	mkdir -p ./ready
	cp tests/res.json ready/stud-unit-test-report-prev.json

ready/main-cli-debug.py: src/alg1.py src/alg2.py src/alg3.py src/tests.py
	mkdir -p ./ready
	cp src/* ready/

.PHONY: clean
clean:
	echo OK

ready/app-cli-debug:

ready/stud-unit-test-report.json: tests/res.json
	mkdir -p ./ready
	cp tests/res.json ready/stud-unit-test-report.json