
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

## Example io

```
g++ input_output_flips.cpp |& ./translator.py
```

yields

```
Done reading in errors
2 errors

in file input_output_flips.cpp line 5:
Your main function returns something of type int, when any sane program will return an integer.

in file input_output_flips.cpp line 6:
You appear to have written something like 'cout >> my_var', when you should have done 'cout << my_var'.

```

## Prereqs

The `termcolor` module is used to provide terminal colors.

```
sudo pip3 install termcolor
```


