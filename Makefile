.PHONY: install
install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "Run: source .venv/bin/activate"
