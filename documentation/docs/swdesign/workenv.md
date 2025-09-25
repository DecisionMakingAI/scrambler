## Introduction

Many times the command line statements to perform certain operations are forgotten and have to be looked  up.
This section is a collection of the ones that I have had to look up that I expect to use from time to time.

## Work Environment Adjustments for Development

I use 'vi' as the text editor of choice.
It defaults to using tabs with 8 spaces.
A '.exrc' file is created in the home directory with the following added:

```text
:se ts=4
:se expandtab
```

## Python Debugging Without the Use of Graphical Tools

The [documentation](https://docs.python.org/3/library/pdb.html) descirbes the details of the available operaions.
To get started, simply enter the following command.

```bash
python -m pdb *script.py*
```

## Using Pip to Upgrade Modules

When upgrading, pip requires a list of modules (there is no all).
This script is one way to accomplish this:

```bash
pip install -U `pip list --outdated | awk 'NR>2 {print $1}'`
```

