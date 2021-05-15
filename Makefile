.DEFAULT_GOAL 	:= help

run: ## run the visual application
	@streamlit run main.py visual

install: ## install dependencies
	@pip install -r requirements.txt

view: ## display the Makefile
	@cat Makefile

edit: ## open the Makefile with `code`
	@code Makefile

test:
	python -m unittest discover -s ./tests/ -v

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

