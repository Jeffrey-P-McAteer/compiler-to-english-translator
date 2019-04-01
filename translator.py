#!/usr/bin/env python3

import fileinput

# Represents a single error message
class CppError():
  # input_stream is a stream that can be iterated over as lines
  def __init__(self, input_stream):
    self.err_file = None
    self.err_line = None
    self.err_message = None
    self.err_src_snippet = None
    
    for line in input_stream:
      if " In function " in line or "file included from" in line or ("from " in line and line[-1] == ","):
        continue # this data currently ignored
      
      if self.err_file == None and self.err_line == None:
        split_file_and_number = line.split(":")
        self.err_file = split_file_and_number[0]
        self.err_line = split_file_and_number[1]
        split_error_token = line.split("error:")
        self.err_message = split_error_token[1] if len(split_error_token) > 1 else ""
        continue
      
      if self.err_src_snippet == None:
        self.err_src_snippet = line.strip()
        continue
      
      break
      
      
    
    if self.err_file == None:
      raise Exception("No file in error message")

  def translate_message(self):
    if " must return " in self.err_message:
      func_name = self.err_message.split(" ")[1][1:-1]
      ret_type = self.err_message.split(" ")[-1][1:-2]
      return "The function {} must return something of type {}".format(func_name, ret_type)
    
    return self.err_message


if __name__ == '__main__':
  all_errors = []
  try:
    input_stream = fileinput.input()
    while True:
      # CppError throws exception at end of input
      err = CppError(input_stream)
      all_errors.append(err)
      
  except Exception as e:
    #print(e)
    print("Done reading in errors")
  
  print("{} errors".format(len(all_errors)))
  
  for error in all_errors:
    print(error.translate_message())
  