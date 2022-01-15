dist:
	@python -m build
publish:
	@python -m twine upload dist/*
test:
	python -m unittest
.PHONY: clean dist publish test
clean:
	@rm -rf dist
	@rm -rf src/codeforces_client.egg-info
