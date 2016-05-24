init:
	pip install -r requirements.txt
clean:
	rm -f -v */*.pyc
	rm -rf **/__pycache__
test: pytest clean
pytest:
	py.test
run:
	python nflstats/nflinterface.py
