ready/report.pdf: report/report.pdf
	mkdir -p ./ready
	cp report/report.pdf ready/report.pdf

ready/stud-unit-test-report-prev.json: tests/res.json
	mkdir -p ./ready
	cp tests/res.json ready/stud-unit-test-report-prev.json

ready/main-cli-debug.py:


.PHONY: clean
clean:
	echo OK

ready/app-cli-debug:

ready/main-cli-debug:

ready/stud-unit-test-report.json: tests/res.json
	mkdir -p ./ready
	cp tests/res.json ready/stud-unit-test-report.json
