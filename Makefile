.PHONY: check test validate eval eval-quick

# Free, fast checks: run before every commit.
check: test validate

# Unit tests for the build script.
test:
	python3 -m unittest discover -s tests

# Schema checks for the marketplace manifest and the skill.
validate:
	claude plugin validate --strict .
	claude plugin validate --strict skills

# Behaviour evals: real model calls on your account, so run them on purpose.
# Full run: 3 runs per case, with and without the skill for comparison.
eval:
	claude plugin eval . --scaffold --allow-tools Bash Write Edit --threshold 0.8 --max-cost-usd 15 --no-publish

# One run per case, skill loaded only: a cheap smoke test.
eval-quick:
	claude plugin eval . --scaffold --allow-tools Bash Write Edit --runs 1 --ablation none --max-cost-usd 5 --no-publish
