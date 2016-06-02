init: npm
	pip install -r requirements.txt
npm:
	pushd . && \
	cd nflstats/static && \
	npm install && \
	popd
clean:
	rm -f -v */*.pyc
	rm -rf **/__pycache__
test: pytest clean
pytest:
	py.test
run:
	python nflstats/nflinterface.py
