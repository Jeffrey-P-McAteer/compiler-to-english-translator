
# Compiler-to-English Translator

## What?

CS students often have difficulty reading compiler error messages.

`translator.py` takes in compiler output and translates common problems so
they are easy to understand.

## How?

```
g++ input_output_flips.cpp |& ./translator.py
```

Bash uses the `|&` token to combine stdout and stderr. `g++` prints errors to stderr,
so make sure the error stream is directed to `./translator.py`.

Also `./translator.py` uses python3.

## Prereqs

The `termcolor` module is used to provide terminal colors.

```
sudo pip3 install termcolor
```


