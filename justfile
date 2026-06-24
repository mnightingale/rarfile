set shell := ["bash", "-eu", "-c"]

PYTHONS := "3.9 3.10 3.11 3.12 3.13 3.14 pypy3.9 pypy3.10 pypy3.11"

test PYTHON="3.9" CRYPTO="cryptography":
    uv venv --python {{PYTHON}} --clear
    uv sync \
        --extra test \
        {{ if CRYPTO != "" { "--extra " + CRYPTO } else { "" } }} \
        --reinstall-package rarfile
    uv run test/run.py {{PYTHON}} {{CRYPTO}}

test-all:
    #!/usr/bin/env sh
    for py in {{PYTHONS}}; do
        for crypto in "" pycryptodome cryptography; do
            just test "$py" "$crypto"
        done
    done

lint:
    uv run --extra lint --extra test pylint rarfile dumprar.py test

docs:
    uv run --extra docs sphinx-build -b html doc doc/_build

all: lint docs test

clean:
	rm -rf __pycache__ build dist
	rm -f *.pyc MANIFEST *.orig *.rej *.html *.class test/*.pyc
	rm -rf doc/_build doc/_static doc/_templates doc/html
	rm -rf .coverage cover*
	rm -rf src/*.egg-info
	rm -f test/files/*.rar. test/files/*.rar.[pjt]* *.diffs
	rm -rf tmp
	rm -f src/rarfile/*.so
	rm -f .coverage.*
	rm -f uv.lock
