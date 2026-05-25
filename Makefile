VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: install develop uninstall clean
install: $(VENV)
	$(PIP) install .

$(VENV):
	python3 -m venv $(VENV)
	@echo ""
	@echo "  Run: source $(VENV)/bin/activate"

develop: $(VENV)
	$(PIP) install -e .

uninstall:
	$(PIP) uninstall global-weapons-tracker -y

clean:
	rm -rf $(VENV)