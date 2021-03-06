#!/usr/bin/env python3

import fileinput

# sudo pip3 install termcolor
from termcolor import colored

# Represents a single error message
class CppError():
  # input_stream is a stream that can be iterated over as lines
  def __init__(self, input_stream):
    self.err_file = None
    self.err_line = None
    self.err_message = None
    self.err_src_snippet = None
    
    for line in input_stream:
      if " In function " in line or "file included from" in line or ("from " in line and (line[-1] == "," or line[-2] == "," )):
        continue # this data currently ignored
      
      if "^" in line and "~" in line:
        continue # ignore underline lines (we could parse out index data for the specific char where error occurs)
      
      if self.err_file == None and self.err_line == None:
        split_file_and_number = line.split(":")
        self.err_file = split_file_and_number[0]
        self.err_line = split_file_and_number[1]
        split_error_token = line.split("error:")
        self.err_message = split_error_token[1] if len(split_error_token) > 1 else ""
        # #error never has code after it, so we break on the first input line
        if "#error" in self.err_message:
          break
        
        continue
      
      if self.err_src_snippet == None:
        self.err_src_snippet = line.strip()
        continue
      
      break
      
      
    
    if self.err_file == None:
      raise Exception("No file in error message")

  def get_err_src_snippet(self):
    if self.err_src_snippet == None:
      return ""
    return self.err_src_snippet

  def translated_message(self):
    if " must return " in self.err_message:
      func_name = self.err_message.split(" ")[1][1:-1]
      ret_type = self.err_message.split(" ")[-1][1:-2]
      if func_name == "::main" or func_name == "main":
        return "hey ding-dong, your main function returns something of type {}, when any sane program will return an integer.".format(colored(ret_type, 'red'))
      else:
        return "The function {} must return something of type {}".format(colored(func_name, 'red'), colored(ret_type, 'red'))
    
    if "operand types are ‘std::ostream’" in self.err_message and "no match for ‘operator>>’" in self.err_message and "cout" in self.get_err_src_snippet():
      return "You appear to have written something like 'cout >> my_var', when you should have done 'cout << my_var'."
    
    if "cannot bind non-const lvalue reference of type" in self.err_message and "to an rvalue of type" in self.err_message:
      lval_type = self.err_message.split("lvalue reference of type ")[1].split(" to an rvalue")[0][1:-1]
      rval_type = self.err_message.split("rvalue of type ")[1].strip()[1:-1]
      
      return "You have passed a value of type {} to a function expecting a reference type {}".format(colored(rval_type, 'red'), colored(lval_type, 'red'))+"\n"+ \
             "Perform percussive ampersand maintenance by adding '&' before the value passed in until error goes away."
    
    if "expected ‘;’":
      return "You forgot a semicolon ding-dong"
    
    if len(self.get_err_src_snippet()) > 1:
      return self.err_message + "\n" + self.get_err_src_snippet()
    else:
      return self.err_message


if __name__ == '__main__':
  all_errors = []
  try:
    input_stream = fileinput.input()
    while True:
      try:
        # CppError throws exception at end of input
        err = CppError(input_stream)
        if "note: " in err.err_message or "note: " in err.get_err_src_snippet():
          continue
        if len(err.err_message) < 2:
          continue
        all_errors.append(err)
      except Exception as e:
        if "list index out of range" in str(e):
          continue
        else:
          raise e
      
  except Exception as e:
    #print(e)
    print("Done reading in errors")
  
  print("{} errors".format(len(all_errors)))
  print("")
  
#   if len(all_errors) > 99:
#     print("""
# # TODO 99 problems ASCII art
# """)
  
  for error in all_errors:
    print("in file {} line {}:".format(error.err_file, error.err_line))
    print(error.translated_message())
    print("")
  