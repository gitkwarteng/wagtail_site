clean: ## Remove files not in source control
	find . -type f -name "*.pyc" -delete

release: clean ## Creates release
	# pip install twine wheel
	rm -rf dist/*
	# rm -rf src/oscar/static/*
	./setup.py sdist bdist_wheel
	# twine upload -s dist/*

build:
	python setup.py sdist bdist_wheel
