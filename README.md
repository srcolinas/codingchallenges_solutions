# Soluctions to Coding Challenges

Here I host personal solutions to coding challenges from https://codingchallenges.fyi

Each solution is in its own `{name}/{language-identifier}cc{name}` folder (e.g. the folder `./wc/pywc` host the solution for a `wc` tool written in python) and I host solutions in both Python and Rust. Keep in mind the following while going through the implemented solutions:

* **Python**: `poetry` will be used to manage dependencies and environments, so to execute any of the implementaions and tests, it is more convenient to do it through `poetry`; for example, you can run the script for *Write Your Own wc Tool* by `cd` into `wc/pyccwc` and then do `poetry run python pyccwc/main.py ../text.txt` (inspect `pyproject.toml` file to find command line tool). Likewise, you can run the tests for such project with `poetry run pytest tests/` inside the same folder. There will be a script named as the folder for you to use as well.
* **Rust**: Use `cargo` to build and test as usual.



## Summary of implementations
<br/>

The table below helps to navigate through the solutions that have been implemented.

Challenge  | Python version notes | Rust version notes |
---------- | ----------- | -----------
[Write Your Own wc Tool](https://codingchallenges.fyi/challenges/challenge-wc) | [link](wc/pyccwc)  | [link](wc/rccwc/)
... | ... | ...