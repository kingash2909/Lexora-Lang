"""
===============================================================================
LEXORA PROGRAMMING LANGUAGE INTERPRETER
Version: 1.0.0
Author: Ashish Mishra

Description:
    A revolutionary English-like programming language interpreter that makes
    coding accessible through natural language syntax. Lexora allows users to
    write code using plain English commands, eliminating traditional programming
    syntax barriers.

Key Features:
    - Natural language syntax (Display, Set, If, Repeat, etc.)
    - Object-Oriented Programming support (Classes, Inheritance, Interfaces)
    - Functions with parameters and return values
    - Control structures (If/Elif/Else, Repeat loops, For/While)
    - Data structures (Lists, Dictionaries)
    - File I/O operations
    - Error handling with Try/Catch
    - Built-in mathematical functions
    - Async/await support
    - Web scraping capabilities

Usage:
    Command Line:
        python lexora.py script.lx          # Run .lx file
        python lexora.py "Display 'Hello'"   # Run inline code
    
    As Module:
        from lexora import SimpleEnglishInterpreter
        interpreter = SimpleEnglishInterpreter()
        interpreter.execute_script("Display 'Hello World'")

License:
    MIT License - See LICENSE file for details

Repository:
    https://github.com/yourusername/lexora-lang

Documentation:
    https://lexora.dev/docs
===============================================================================
"""

# =============================================================================
# IMPORTS - Standard Library Modules
# =============================================================================
import sys      # System-specific parameters and functions
import math     # Mathematical functions and constants
import time     # Time-related functions and sleep
import random   # Random number generation
import threading  # Thread-based parallelism
import json     # JSON encoding/decoding
import asyncio  # Asynchronous I/O and coroutines
import os       # Operating system interface

# =============================================================================
# CLASS: SimpleEnglishInterpreter - Main Interpreter Engine
# =============================================================================
class SimpleEnglishInterpreter:
    """
    Core interpreter class for the Lexora programming language.
    
    This class handles parsing and execution of Lexora code, maintaining
    program state including variables, functions, classes, and control flow.
    
    Attributes:
        variables (dict): Storage for all program variables and constants
        functions (dict): Registered function definitions
        classes (dict): Registered class definitions
        line_number (int): Current line being executed
        returning (bool): Flag for return statement execution
        breaking (bool): Flag for break statement execution
        continuing (bool): Flag for continue statement execution
        last_error (Exception): Most recent error encountered
        global_scope (dict): Reference to global variable scope
    
    Example:
        >>> interpreter = SimpleEnglishInterpreter()
        >>> interpreter.execute_script('''
        ... Set x to 10
        ... Display x
        ... ''')
    """
    def __init__(self):
        self.variables = {"_constants_": {}}  # Store variables and constants
        self.functions = {}  # Store function definitions
        self.classes = {}    # Store class definitions
        self.line_number = 0
        self.returning = False
        self.breaking = False
        self.continuing = False
        self.last_error = None
        self.global_scope = self.variables

    def _call_method_if_exists(self, obj_name, method_name, *args):
        if obj_name in self.variables:
            obj = self.variables[obj_name]
            if isinstance(obj, dict) and "_class_" in obj:
                class_name = obj["_class_"]
                method_data = self._get_class_method(class_name, method_name)
                if method_data:
                    self.parse_and_execute_call(f"Call {obj_name}.{method_name}")

    def _get_class_method(self, class_name, method_name):
        if class_name not in self.classes:
            return None
        
        # Check own methods
        if method_name in self.classes[class_name]["methods"]:
            return self.classes[class_name]["methods"][method_name]
        
        # Check parent methods
        parent = self.classes[class_name].get("parent")
        if parent:
            return self._get_class_method(parent, method_name)
        
        return None

    def execute_script(self, lines, line_offset=0):
        """Execute a list of commands, supporting multi-line blocks."""
        i = 0
        self.returning = False
        self.breaking = False
        self.continuing = False
        
        # First pass: Remove multi-line comments
        in_multiline_comment = False
        cleaned_lines = []
        for line in lines:
            line_content = line.strip()
            
            # Check for multi-line comment delimiters
            if '/*' in line_content and '*/' in line_content:
                # Single line with both open and close
                import re
                line_content = re.sub(r'/\*.*?\*/', '', line_content)
            elif '/*' in line_content:
                # Start of multi-line comment
                in_multiline_comment = True
                line_content = line_content.split('/*')[0]
            elif '*/' in line_content:
                # End of multi-line comment
                in_multiline_comment = False
                line_content = line_content.split('*/')[1]
            elif in_multiline_comment:
                # Inside multi-line comment, skip line
                line_content = ''
            
            cleaned_lines.append(line_content)
        
        lines = cleaned_lines
        
        while i < len(lines):
            if self.returning or self.breaking or self.continuing:
                break
                
            self.line_number = i + 1 + line_offset
            line_content = lines[i].split("#")[0].strip()  # Remove single-line comments
            if not line_content:
                i += 1
                continue

            command = line_content
            # Check for block starts
            if command.startswith("If") and command.endswith(":"):
                branches, next_i = self._get_conditional_structure(lines, i)
                i = next_i
                
                executed = False
                for cond_str, block, offset in branches:
                    try:
                        if cond_str is None or eval(self._convert_condition(cond_str), self.variables, self.variables):
                            self.execute_script(block, offset)
                            executed = True
                            break
                    except Exception as e:
                        print(f"Error on line {self.line_number}: In If condition: {e}")
                        break
                continue
            elif command.startswith("While") and command.endswith(":"):
                condition = command[6:-1].strip()
                block, next_i = self._get_block(lines, i)
                try:
                    while eval(self._convert_condition(condition), self.variables, self.variables):
                        self.execute_script(block, line_offset + i + 1)
                        if self.returning: break
                        if self.breaking:
                            self.breaking = False
                            break
                        if self.continuing:
                            self.continuing = False
                            continue
                except Exception as e:
                    print(f"Error on line {self.line_number}: In While loop: {e}")
                i = next_i
                continue
            elif command.startswith("Do:") : # Do-While implementation
                block, next_i = self._get_block(lines, i, break_on_while=True)
                i = next_i
                # Expecting 'While [condition]:' line next
                if i < len(lines):
                    while_line = lines[i].split("#")[0].strip()
                    if while_line.startswith("While") and while_line.endswith(":"):
                        condition = while_line[6:-1].strip()
                        try:
                            while True:
                                self.execute_script(block, line_offset + i)
                                if self.returning: break
                                if self.breaking: self.breaking = False; break
                                if self.continuing: self.continuing = False; continue
                                if not eval(self._convert_condition(condition), self.variables, self.variables): break
                        except Exception as e: print(f"Error on line {self.line_number}: In Do-While: {e}")
                        i += 1
                    else:
                        print(f"Error on line {self.line_number}: Expected 'While [condition]:' after 'Do' block, but found '{while_line}'.")
                else:
                    print(f"Error on line {self.line_number}: Missing 'While' condition for 'Do' block.")
                continue
            elif command.startswith("Repeat") and " times:" in command:
                try:
                    count_str = command[7:].split(" times:")[0].strip()
                    count = int(eval(count_str, self.variables, self.variables))
                    block, next_i = self._get_block(lines, i)
                    for _ in range(count):
                        self.execute_script(block, line_offset + i + 1)
                        if self.returning: break
                        if self.breaking:
                            self.breaking = False
                            break
                        if self.continuing:
                            self.continuing = False
                            continue
                    i = next_i
                except Exception as e:
                    print(f"Error on line {self.line_number}: In Repeat loop: {e}")
                    i += 1
                continue
            elif command.startswith("For") and command.endswith(":"):
                try:
                    loop_def = command[4:-1].strip()
                    if " in " in loop_def: # For item in list:
                        parts = loop_def.split(" in ")
                        var_name = parts[0].strip()
                        iterable = eval(parts[1].strip(), self.variables, self.variables)
                        block, next_i = self._get_block(lines, i)
                        for val in iterable:
                            self.variables[var_name] = val
                            self.execute_script(block, line_offset + i + 1)
                            if self.returning: break
                            if self.breaking:
                                self.breaking = False
                                break
                            if self.continuing:
                                self.continuing = False
                                continue
                        i = next_i
                    else: # For i from start to end [step S]:
                        parts = loop_def.split(" from ")
                        var_name = parts[0].strip()
                        range_part = parts[1]
                        step = 1
                        if " step " in range_part:
                            range_part, step_str = range_part.split(" step ")
                            step = int(eval(step_str, self.variables, self.variables))
                        
                        start_str, end_str = range_part.split(" to ")
                        start = int(eval(start_str, self.variables, self.variables))
                        end = int(eval(end_str, self.variables, self.variables))
                        
                        block, next_i = self._get_block(lines, i)
                        for val in range(start, end + 1, step):
                            self.variables[var_name] = val
                            self.execute_script(block, line_offset + i + 1)
                            if self.returning: break
                            if self.breaking:
                                self.breaking = False
                                break
                            if self.continuing:
                                self.continuing = False
                                continue
                        i = next_i
                except Exception as e:
                    print(f"Error on line {self.line_number}: In For loop definition: {e}")
                    i += 1
                continue
            elif command.startswith("Try:"):
                try_block, catch_block, finally_block, next_i = self._get_try_structure(lines, i)
                i = next_i
                try:
                    self.execute_script(try_block, line_offset + i)
                except Exception as e:
                    if catch_block:
                        self.variables["last_error"] = str(e)
                        self.execute_script(catch_block, line_offset + i)
                    else:
                        print(f"Unhandled Exception on line {self.line_number}: {e}")
                finally:
                    if finally_block:
                        self.execute_script(finally_block, line_offset + i)
                continue
            elif (command.startswith("Class ") or command.startswith("Abstract Class ") or command.startswith("Interface ")) and command.endswith(":"):
                is_abstract = command.startswith("Abstract Class ")
                is_interface = command.startswith("Interface ")
                
                if is_abstract:
                    class_def = command[15:-1].strip()
                elif is_interface:
                    class_def = command[10:-1].strip()
                else:
                    class_def = command[6:-1].strip()
                
                parent = None
                if " inherits " in class_def:
                    parts = class_def.split(" inherits ")
                    class_name = parts[0].strip()
                    parent = parts[1].strip()
                else:
                    class_name = class_def
                
                # Extract class body by finding matching End
                block_lines = []
                i += 1
                nesting = 1
                define_nesting = 0  # Track nested Defines inside class
                while i < len(lines) and nesting > 0:
                    line = lines[i].split("#")[0].strip()
                    if not line:
                        i += 1
                        continue
                    
                    # Track Define blocks separately
                    if line.startswith("Define") and " as:" in line and line.endswith(":"):
                        define_nesting += 1
                    elif line == "End":
                        if define_nesting > 0:
                            # This End closes a Define, not the class
                            define_nesting -= 1
                        else:
                            # This End closes the class
                            nesting -= 1
                            if nesting == 0:
                                break
                    
                    # Always add the line
                    block_lines.append(lines[i])
                    i += 1
                
                self.classes[class_name] = {
                    "parent": parent, 
                    "methods": self._parse_class_methods(block_lines),
                    "is_abstract": is_abstract,
                    "is_interface": is_interface
                }
                
                # Verify parent exists
                if parent and parent not in self.classes:
                    print(f"Warning: Parent class '{parent}' not found for '{class_name}'")

                i += 1  # Move past the "End"
                continue
            elif command.startswith("Switch ") and command.endswith(":"):
                switch_val_expr = command[7:-1].strip()
                switch_val = eval(self._convert_condition(switch_val_expr), self.variables, self.variables)
                i += 1
                matched = False
                while i < len(lines):
                    line = lines[i].split("#")[0].strip()
                    if not line: i += 1; continue
                    if line.startswith("Case ") and line.endswith(":"):
                        case_val_expr = line[5:-1].strip()
                        case_val = eval(self._convert_condition(case_val_expr), self.variables, self.variables)
                        block, next_i = self._get_block(lines, i, break_on_else=True)
                        if case_val == switch_val and not matched:
                            self.execute_script(block, line_offset + i + 1)
                            matched = True
                        i = next_i
                    elif line == "Default:":
                        block, next_i = self._get_block(lines, i, break_on_else=True)
                        if not matched:
                            self.execute_script(block, line_offset + i + 1)
                            matched = True
                        i = next_i
                    elif line == "End":
                        i += 1
                        break
                    else:
                        # Skip case/default blocks that didn't match
                        if line.startswith("Case ") or line == "Default:":
                            _, next_i = self._get_block(lines, i, break_on_else=True)
                            i = next_i
                        else:
                            i += 1
                continue
            elif command.startswith("Match ") and command.endswith(":"):
                match_val_expr = command[6:-1].strip()
                match_val = eval(match_val_expr, self.variables, self.variables)
                i += 1
                matched = False
                while i < len(lines):
                    line = lines[i].split("#")[0].strip()
                    if not line:
                        i += 1
                        continue
                    if line.startswith("Case ") and line.endswith(":"):
                        case_val_expr = line[5:-1].strip()
                        case_val = eval(case_val_expr, self.variables, self.variables)
                        block, next_i = self._get_block(lines, i, break_on_else=True)
                        if case_val == match_val and not matched:
                            self.execute_script(block, line_offset + i + 1)
                            matched = True
                        i = next_i
                    elif line == "End":
                        i += 1
                        break
                    else:
                        i += 1
                continue
            elif command.startswith("Define") and " as:" in command:
                try:
                    if command.endswith(":"):
                        if " with " in command:
                            parts = command[7:].split(" with ", 1)
                            func_name = parts[0].strip()
                            param_part = parts[1].split(" as:", 1)[0].strip()
                            params = []
                            defaults = {}
                            for p in param_part.split(","):
                                p = p.strip()
                                if "=" in p:
                                    name, val = p.split("=", 1)
                                    name = name.strip()
                                    params.append(name)
                                    defaults[name] = eval(val.strip(), self.variables, self.variables)
                                else:
                                    params.append(p)
                        else:
                            func_name = command[7:].split(" as:", 1)[0].strip()
                            params = []
                            defaults = {}
                        
                        block, next_i = self._get_block(lines, i)
                        self.functions[func_name] = (block, line_offset + i + 1, params, defaults)
                        i = next_i
                    else:
                        func_name, func_body = command[7:].split(" as:", 1)
                        self.functions[func_name] = ([func_body.strip()], self.line_number, [], {})
                        i += 1
                except Exception as e:
                    print(f"Error on line {self.line_number}: In Define: {e}")
                    i += 1
                continue
            elif command.startswith("Return "):
                try:
                    val_str = command[7:].strip()
                    self.variables["_return_value_"] = eval(val_str, self.variables, self.variables)
                    self.returning = True
                    break
                except Exception as e:
                    print(f"Error on line {self.line_number}: In Return: {e}")
                    i += 1
                continue
            else:
                self.parse_and_execute(command)
                i += 1

    def _get_block(self, lines, start_index, break_on_else=False, break_on_while=False):
        """Extract a block of lines until 'End' (or Else/Else If/While) is encountered."""
        block = []
        i = start_index + 1
        nesting = 1
        while i < len(lines):
            line = lines[i].split("#")[0].strip()
            if not line:
                i += 1
                continue
            
            # Check for block-starting keywords that increase nesting
            # Only count them if they're at the current nesting level or higher
            if (line.startswith("If") or line.startswith("While") or line.startswith("For") or line.startswith("Repeat") or line.startswith("Try") or line.startswith("Class") or line.startswith("Match") or line.startswith("Do:")) and line.endswith(":"):
                if nesting == 1 and break_on_while and line.startswith("While"):
                    return block, i
                nesting += 1
            elif line == "End":
                nesting -= 1
                if nesting == 0:
                    return block, i + 1
            elif nesting == 1:
                if break_on_else and (line.startswith("Else If") or line.startswith("Else:") or line.startswith("Catch") or line.startswith("Finally") or line.startswith("Case ")):
                    return block, i
                if break_on_while and line.startswith("While"):
                    return block, i
                # Add line to block (including Define statements)
                block.append(lines[i])
            else:
                # We're inside a nested block, still add the line
                block.append(lines[i])
            i += 1
        return block, i

    def _get_try_structure(self, lines, start_index):
        try_block = []
        catch_block = []
        finally_block = []
        
        i = start_index
        # Get try block
        try_block, next_i = self._get_block(lines, i, break_on_else=True)
        i = next_i
        
        line = lines[i].split("#")[0].strip()
        if line.startswith("Catch"):
            catch_block, next_i = self._get_block(lines, i, break_on_else=True)
            i = next_i
            line = lines[i].split("#")[0].strip()
            
        if line.startswith("Finally:"):
            finally_block, next_i = self._get_block(lines, i, break_on_else=True)
            i = next_i
            line = lines[i].split("#")[0].strip()
            
        if line == "End":
            return try_block, catch_block, finally_block, i + 1
        return try_block, catch_block, finally_block, i

    def _parse_class_methods(self, block):
        methods = {}
        i = 0
        while i < len(block):
            line = block[i].split("#")[0].strip()
            if line.startswith("Define") and " as:" in line:
                if line.endswith(":"):
                    if " with " in line:
                        parts = line[7:].split(" with ", 1)
                        func_name = parts[0].strip()
                        param_part = parts[1].split(" as:", 1)[0].strip()
                        params = []
                        defaults = {}
                        for p in param_part.split(","):
                            p = p.strip()
                            if "=" in p:
                                name, val = p.split("=", 1)
                                name = name.strip()
                                params.append(name)
                                defaults[name] = eval(val.strip(), self.variables, self.variables)
                            else:
                                params.append(p)
                    else:
                        func_name = line[7:].split(" as:", 1)[0].strip()
                        params = []
                        defaults = {}
                    
                    inner_block, next_i = self._get_block(block, i)
                    methods[func_name] = (inner_block, params, defaults)
                    i = next_i
                else:
                    func_name, func_body = line[7:].split(" as:", 1)
                    methods[func_name] = ([func_body.strip()], [], {})
                    i += 1
            else:
                i += 1
        return methods

    def _get_conditional_structure(self, lines, start_index):
        branches = []
        i = start_index
        first_if = True
        
        while i < len(lines):
            line = lines[i].split("#")[0].strip()
            if not line:
                if first_if: # Should not happen as start_index points to an 'If'
                    i += 1
                    continue
                else: # Stop if we hit an empty line between branches? No, allow it.
                    i += 1
                    continue
                
            if line.startswith("If"):
                if not first_if: # Another 'If' starts, so the previous structure is done
                    return branches, i
                cond = line[3:].rstrip(":").strip()
                block, next_i = self._get_block(lines, i, break_on_else=True)
                branches.append((cond, block, i + 1))
                i = next_i
                first_if = False
            elif line.startswith("Else If"):
                cond = line[8:].rstrip(":").strip()
                block, next_i = self._get_block(lines, i, break_on_else=True)
                branches.append((cond, block, i + 1))
                i = next_i
            elif line.startswith("Else:"):
                block, next_i = self._get_block(lines, i, break_on_else=True)
                branches.append((None, block, i + 1))
                i = next_i
            elif line == "End":
                return branches, i + 1
            else:
                # Not part of the structure, stop here
                return branches, i
                
        return branches, i

    def parse_and_execute(self, command):
        if not command.strip() or command.startswith("#"): return

        if command.startswith("Display"):
            content = command[8:].strip()
            try:
                if (content.startswith('"') and content.endswith('"') and content.count('"') == 2) or \
                   (content.startswith("'") and content.endswith("'") and content.count("'") == 2):
                    print(content[1:-1])
                else:
                    # Convert object.field syntax before evaluation
                    converted_content = self._convert_condition(content)
                    result = eval(converted_content, self.variables, self.variables)
                    if isinstance(result, tuple): print(" ".join(map(str, result)))
                    else: print(result)
            except Exception as e:
                print(f"Error on line {self.line_number}: In Display: {content} ({e})")

        elif command == "New Line":
            # Print a blank line (like Python's print())
            print()  # This outputs '\n'

        elif command == "Next Line":
            # Move to next line without printing anything (carriage return + line feed)
            print()  # Same as New Line - outputs '\n'

        elif command.startswith("Set"):
            if " to Call " in command:
                self.parse_and_execute_call(command)
                return
            
            if " to New " in command:
                parts = command.split(" to New ")
                var_name = parts[0][4:].strip()
                class_name = parts[1].strip()
                if class_name in self.classes:
                    class_data = self.classes[class_name]
                    if class_data.get("is_abstract") or class_data.get("is_interface"):
                        print(f"Error on line {self.line_number}: Cannot instantiate abstract class or interface '{class_name}'.")
                        return
                    
                    self.variables[var_name] = {"_class_": class_name, "fields": {}}
                    # Call Initialize if defined
                    self._call_method_if_exists(var_name, "Initialize")
                else:
                    print(f"Error on line {self.line_number}: Class '{class_name}' undefined.")
                return

            parts = command.split(" to ")
            if len(parts) >= 2:
                var_name = parts[0][4:].strip()
                value_expr = " to ".join(parts[1:]).strip()
                
                # Constant check
                if var_name in self.variables.get("_constants_", {}):
                    print(f"Error on line {self.line_number}: Cannot reassign constant '{var_name}'.")
                    return

                # Handle field access like Set user.name to "Ashish"
                if "." in var_name:
                    obj_name, field_name = var_name.split(".", 1)
                    if obj_name in self.variables and isinstance(self.variables[obj_name], dict) and "_class_" in self.variables[obj_name]:
                        try:
                            self.variables[obj_name]["fields"][field_name] = eval(self._convert_condition(value_expr), self.variables, self.variables)
                        except Exception as e:
                            self.variables[obj_name]["fields"][field_name] = value_expr.strip('"').strip("'")
                        return

                # Special cases for Set
                if value_expr.startswith("Random between "):
                    try:
                        range_parts = value_expr[15:].split(" and ")
                        start = int(eval(range_parts[0].strip(), self.variables, self.variables))
                        end = int(eval(range_parts[1].strip(), self.variables, self.variables))
                        self.variables[var_name] = random.randint(start, end)
                    except Exception as e: print(f"Error on line {self.line_number}: In Random: {e}")
                elif value_expr.startswith("Absolute of "):
                    try:
                        val = float(eval(self._convert_condition(value_expr[12:].strip()), self.variables, self.variables))
                        self.variables[var_name] = abs(val)
                    except Exception as e: print(f"Error on line {self.line_number}: In Absolute: {e}")
                elif value_expr.startswith("Round "):
                    try:
                        val = float(eval(self._convert_condition(value_expr[6:].strip()), self.variables, self.variables))
                        self.variables[var_name] = round(val)
                    except Exception as e: print(f"Error on line {self.line_number}: In Round: {e}")
                elif value_expr.startswith("Number from "):
                    try:
                        val = eval(self._convert_condition(value_expr[12:].strip()), self.variables, self.variables)
                        self.variables[var_name] = float(val) if '.' in str(val) else int(val)
                    except Exception as e: print(f"Error on line {self.line_number}: In Number from: {e}")
                elif value_expr.startswith("String from "):
                    try:
                        val = eval(self._convert_condition(value_expr[12:].strip()), self.variables, self.variables)
                        self.variables[var_name] = str(val)
                    except Exception as e: print(f"Error on line {self.line_number}: In String from: {e}")
                elif value_expr.startswith("Boolean from "):
                    try:
                        val = eval(self._convert_condition(value_expr[13:].strip()), self.variables, self.variables)
                        self.variables[var_name] = bool(val)
                    except Exception as e: print(f"Error on line {self.line_number}: In Boolean from: {e}")
                elif value_expr.startswith("Byte from "):
                    try:
                        val = int(eval(self._convert_condition(value_expr[10:].strip()), self.variables, self.variables))
                        self.variables[var_name] = bytes([val % 256])
                    except Exception as e: print(f"Error on line {self.line_number}: In Byte from: {e}")
                elif value_expr.startswith("Character from "):
                    try:
                        val = int(eval(self._convert_condition(value_expr[15:].strip()), self.variables, self.variables))
                        self.variables[var_name] = chr(val)
                    except Exception as e: print(f"Error on line {self.line_number}: In Character from: {e}")
                elif value_expr.startswith("Set from "):
                    try:
                        val = eval(self._convert_condition(value_expr[9:].strip()), self.variables, self.variables)
                        self.variables[var_name] = set(val)
                    except Exception as e: print(f"Error on line {self.line_number}: In Set from: {e}")
                elif value_expr.startswith("Lambda("):
                    # Lambda(x): x * 2
                    try:
                        params_part = value_expr[7:].split("):")[0]
                        body_part = value_expr.split("):")[1].strip()
                        params = [p.strip() for p in params_part.split(",")]
                        self.variables[var_name] = {"_type_": "lambda", "params": params, "body": body_part}
                    except Exception as e: print(f"Error on line {self.line_number}: In Lambda: {e}")
                elif value_expr == "Null":
                    self.variables[var_name] = None
                elif value_expr.startswith("Sin of "):
                    try: self.variables[var_name] = math.sin(math.radians(float(eval(self._convert_condition(value_expr[7:]), self.variables, self.variables))))
                    except Exception as e: print(f"Error on line {self.line_number}: In Sin: {e}")
                elif value_expr.startswith("Cos of "):
                    try: self.variables[var_name] = math.cos(math.radians(float(eval(self._convert_condition(value_expr[7:]), self.variables, self.variables))))
                    except Exception as e: print(f"Error on line {self.line_number}: In Cos: {e}")
                elif value_expr.startswith("Tan of "):
                    try: self.variables[var_name] = math.tan(math.radians(float(eval(self._convert_condition(value_expr[7:]), self.variables, self.variables))))
                    except Exception as e: print(f"Error on line {self.line_number}: In Tan: {e}")
                elif value_expr.startswith("Type of "):
                    try:
                        val = eval(self._convert_condition(value_expr[8:].strip()), self.variables, self.variables)
                        self.variables[var_name] = str(type(val).__name__)
                    except Exception as e: print(f"Error on line {self.line_number}: In Type of: {e}")
                else:
                    try:
                        # Convert condition-like syntax (bitwise, etc.) in value expressions
                        converted_expr = self._convert_condition(value_expr)
                        self.variables[var_name] = eval(converted_expr, self.variables, self.variables)
                    except Exception as e:
                        if value_expr.startswith('"') and value_expr.endswith('"'): self.variables[var_name] = value_expr[1:-1]
                        elif value_expr.isalnum(): self.variables[var_name] = value_expr
                        else: print(f"Error on line {self.line_number}: Invalid expression for Set: {value_expr}")
            else:
                print(f"Error on line {self.line_number}: Invalid syntax for Set: {command}")

        elif command.startswith("Constant "):
            parts = command[9:].split(" as ")
            if len(parts) == 2:
                name = parts[0].strip()
                val_expr = parts[1].strip()
                try:
                    val = eval(self._convert_condition(val_expr), self.variables, self.variables)
                    self.variables[name] = val
                    self.variables["_constants_"][name] = True
                except Exception as e: print(f"Error on line {self.line_number}: Defining constant: {e}")

        elif command.startswith("Increment "):
            var_name = command[10:].strip()
            if var_name in self.variables: self.variables[var_name] += 1
            else: print(f"Error on line {self.line_number}: '{var_name}' undefined.")

        elif command.startswith("Decrement "):
            var_name = command[10:].strip()
            if var_name in self.variables: self.variables[var_name] -= 1
            else: print(f"Error on line {self.line_number}: '{var_name}' undefined.")

        elif command.startswith("Search "):
            # Search [val] in [list] into [var]
            try:
                parts = command[7:].split(" in ")
                val = eval(self._convert_condition(parts[0].strip()), self.variables, self.variables)
                rest = parts[1].split(" into ")
                list_name = rest[0].strip()
                var_name = rest[1].strip()
                if list_name in self.variables and isinstance(self.variables[list_name], (list, str)):
                    try:
                        self.variables[var_name] = self.variables[list_name].index(val)
                    except ValueError:
                        self.variables[var_name] = -1
                else: print(f"Error on line {self.line_number}: '{list_name}' is not a list or string.")
            except Exception as e: print(f"Error on line {self.line_number}: In Search: {e}")

        elif command.startswith("Spawn Thread Call "):
            func_part = command[18:].strip()
            thread = threading.Thread(target=self.parse_and_execute_call, args=("Call " + func_part,))
            thread.start()
            print(f"Thread spawned for '{func_part}'")

        elif command.startswith("Filter "):
            # Filter list_name where "condition" into result_list
            parts = command[7:].split(" where ")
            list_name = parts[0].strip()
            rest = parts[1].split(" into ")
            condition = rest[0].strip().strip('"').strip("'")
            result_name = rest[1].strip()
            if list_name in self.variables and isinstance(self.variables[list_name], list):
                self.variables[result_name] = [item for item in self.variables[list_name] if eval(self._convert_condition(condition.replace("item", str(item))), self.variables, self.variables)]
            else: print(f"Error on line {self.line_number}: '{list_name}' is not a list.")

        elif command.startswith("Map "):
            # Map list_name using "expression" into result_list
            parts = command[4:].split(" using ")
            list_name = parts[0].strip()
            rest = parts[1].split(" into ")
            expr = rest[0].strip().strip('"').strip("'")
            result_name = rest[1].strip()
            if list_name in self.variables and isinstance(self.variables[list_name], list):
                self.variables[result_name] = [eval(expr.replace("item", str(item)), self.variables, self.variables) for item in self.variables[list_name]]
            else: print(f"Error on line {self.line_number}: '{list_name}' is not a list.")

        elif command.startswith("Reduce "):
            # Reduce list_name using "expression" into result_var starting with initial_val
            try:
                parts = command[7:].split(" using ")
                list_name = parts[0].strip()
                rest = parts[1].split(" into ")
                expr = rest[0].strip().strip('"').strip("'")
                final_parts = rest[1].split(" starting with ")
                result_name = final_parts[0].strip()
                initial_val = eval(self._convert_condition(final_parts[1].strip()), self.variables, self.variables)
                
                if list_name in self.variables and isinstance(self.variables[list_name], list):
                    acc = initial_val
                    for item in self.variables[list_name]:
                        acc = eval(expr.replace("acc", str(acc)).replace("item", str(item)), self.variables, self.variables)
                    self.variables[result_name] = acc
                else: print(f"Error on line {self.line_number}: '{list_name}' is not a list.")
            except Exception as e: print(f"Error on line {self.line_number}: In Reduce: {e}")

        elif command.startswith("Async Call "):
            # Simulated async call
            func_part = command[11:].strip()
            print(f"Async call initiated for '{func_part}'...")
            # We'll use a thread but label it as async for Lexora
            thread = threading.Thread(target=self.parse_and_execute_call, args=("Call " + func_part,))
            thread.start()
            self.variables["_last_async_task_"] = thread

        elif command == "Await":
            if "_last_async_task_" in self.variables:
                self.variables["_last_async_task_"].join()
                print("Task completed.")
            else: print(f"Error on line {self.line_number}: No async task to await.")

        elif command.startswith("Get current time into "):
            var_name = command[22:].strip()
            self.variables[var_name] = time.strftime("%H:%M:%S")

        elif command.startswith("Get current date into "):
            var_name = command[22:].strip()
            self.variables[var_name] = time.strftime("%Y-%m-%d")

        elif command.startswith("Network Request "):
            # Network Request "url" into result_var
            try:
                import requests
                parts = command[16:].split(" into ")
                url = eval(self._convert_condition(parts[0].strip()), self.variables, self.variables)
                var_name = parts[1].strip()
                response = requests.get(url)
                self.variables[var_name] = response.text
                print(f"Request to {url} successful.")
            except ImportError: print(f"Error: 'requests' library not found. Install with 'pip install requests'.")
            except Exception as e: print(f"Error on line {self.line_number}: Network request failed: {e}")

        elif command == "Break":
            self.breaking = True

        elif command == "Continue":
            self.continuing = True

        elif command.startswith("Create Lock "):
            lock_name = command[12:].strip()
            self.variables[lock_name] = threading.Lock()
            print(f"Lock '{lock_name}' created.")

        elif command.startswith("Acquire "):
            lock_name = command[8:].strip()
            if lock_name in self.variables and isinstance(self.variables[lock_name], threading.Lock):
                self.variables[lock_name].acquire()
            else: print(f"Error on line {self.line_number}: '{lock_name}' is not a Lock.")

        elif command.startswith("Release "):
            lock_name = command[8:].strip()
            if lock_name in self.variables and isinstance(self.variables[lock_name], threading.Lock):
                try: self.variables[lock_name].release()
                except RuntimeError: print(f"Error on line {self.line_number}: Lock '{lock_name}' was not acquired.")
            else: print(f"Error on line {self.line_number}: '{lock_name}' is not a Lock.")

        elif command.startswith("Delete "):
            var_name = command[7:].strip()
            if var_name in self.variables:
                # Call Destroy if defined
                self._call_method_if_exists(var_name, "Destroy")
                del self.variables[var_name]
            else:
                print(f"Error on line {self.line_number}: Variable '{var_name}' not found.")

        elif command.startswith("Import "):
            lib_name = command[7:].strip().strip('"').strip("'")
            # In a real language, we'd load a file.
            filename = lib_name + ".lx"
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as file:
                        lines = file.readlines()
                        # Execute in a temporary interpreter to avoid polluting main state except for funcs/classes
                        temp_interpreter = SimpleEnglishInterpreter()
                        temp_interpreter.execute_script(lines)
                        # Merge functions and classes
                        self.functions.update(temp_interpreter.functions)
                        self.classes.update(temp_interpreter.classes)
                        # Merge variables
                        for k, v in temp_interpreter.variables.items():
                            if k != "_constants_":
                                self.variables[k] = v
                        if "_constants_" in temp_interpreter.variables:
                            self.variables["_constants_"].update(temp_interpreter.variables["_constants_"])
                        print(f"Imported library '{lib_name}' from {filename}")
                except Exception as e:
                    print(f"Error on line {self.line_number}: Failed to import '{lib_name}': {e}")
            else:
                print(f"Error on line {self.line_number}: Library '{lib_name}' (file '{filename}') not found.")

        elif command.startswith("Raise "):
            error_msg = command[6:].strip().strip('"').strip("'")
            raise Exception(error_msg)

        elif command.startswith("Append to file "):
            # Append to file "filename", "content"
            parts = command[15:].split(",", 1)
            if len(parts) == 2:
                filename = parts[0].strip().strip('"').strip("'")
                content = parts[1].strip()
                try:
                    data = str(eval(self._convert_condition(content), self.variables, self.variables)) if not (content.startswith('"') or content.startswith("'")) else content[1:-1]
                    with open(filename, 'a') as file:
                        file.write(data + "\n")
                        print(f"Content appended to {filename}")
                except Exception as e: print(f"Error on line {self.line_number}: Appending to file: {e}")

        elif command.startswith("Lint "):
            filename = command[5:].strip().strip('"').strip("'")
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as file:
                        lines = file.readlines()
                        nesting = 0
                        errors = []
                        for idx, line in enumerate(lines):
                            l = line.split("#")[0].strip()
                            if not l: continue
                            if (l.startswith("If") or l.startswith("While") or l.startswith("For") or l.startswith("Define") or l.startswith("Repeat") or l.startswith("Try") or l.startswith("Class") or l.startswith("Match") or l.startswith("Do:") or l.startswith("Switch")) and l.endswith(":"):
                                nesting += 1
                            elif l == "End":
                                nesting -= 1
                                if nesting < 0: errors.append(f"Line {idx+1}: Unexpected 'End'")
                        if nesting > 0: errors.append(f"Missing {nesting} 'End' statement(s)")
                        
                        if errors:
                            print(f"Lint found {len(errors)} error(s) in '{filename}':")
                            for err in errors: print(f" - {err}")
                        else: print(f"Lint passed for '{filename}'.")
                except Exception as e: print(f"Linting failed: {e}")
            else: print(f"File '{filename}' not found for Lint.")

        elif command.startswith("Format "):
            filename = command[7:].strip().strip('"').strip("'")
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as file:
                        lines = file.readlines()
                        formatted_lines = []
                        indent = 0
                        for line in lines:
                            l = line.split("#")[0].strip()
                            if not l:
                                formatted_lines.append("\n")
                                continue
                            
                            # Decrease indent BEFORE line if it's End or Case/Default
                            if l == "End" or l.startswith("Case ") or l == "Default:" or l.startswith("Catch") or l.startswith("Finally"):
                                indent = max(0, indent - 1)
                            
                            formatted_lines.append("    " * indent + l + "\n")
                            
                            # Increase indent AFTER line if it starts a block
                            if (l.startswith("If") or l.startswith("While") or l.startswith("For") or l.startswith("Define") or l.startswith("Repeat") or l.startswith("Try") or l.startswith("Class") or l.startswith("Match") or l.startswith("Do:") or l.startswith("Switch")) and l.endswith(":") or l.startswith("Case ") or l == "Default:" or l.startswith("Catch") or l.startswith("Finally"):
                                indent += 1
                        
                        with open(filename, 'w') as file:
                            file.writelines(formatted_lines)
                        print(f"File '{filename}' formatted successfully.")
                except Exception as e: print(f"Formatting failed: {e}")
            else: print(f"File '{filename}' not found for Format.")

        elif command.startswith("Multiply "):
            try:
                parts = command[9:].split(" by ")
                val = eval(self._convert_condition(parts[1].strip()), self.variables, self.variables)
                var_name = parts[0].strip()
                self.variables[var_name] = self.variables.get(var_name, 1) * val
            except Exception as e: print(f"Error on line {self.line_number}: Invalid Multiply: {command}")

        elif command.startswith("Divide "):
            try:
                parts = command[7:].split(" by ")
                val = eval(self._convert_condition(parts[1].strip()), self.variables, self.variables)
                var_name = parts[0].strip()
                if val == 0: print(f"Error on line {self.line_number}: Division by zero.")
                else: self.variables[var_name] = self.variables.get(var_name, 1) / val
            except Exception as e: print(f"Error on line {self.line_number}: Invalid Divide: {command}")

        elif command.startswith("Add"):
            try:
                parts = command[4:].split(" to ")
                val = eval(self._convert_condition(parts[0].strip()), self.variables, self.variables)
                var_name = parts[1].strip()
                self.variables[var_name] = self.variables.get(var_name, 0) + val
            except Exception as e: print(f"Error on line {self.line_number}: Invalid Add: {command}")

        elif command.startswith("Subtract"):
            try:
                parts = command[9:].split(" from ")
                val = eval(self._convert_condition(parts[0].strip()), self.variables, self.variables)
                var_name = parts[1].strip()
                self.variables[var_name] = self.variables.get(var_name, 0) - val
            except Exception as e: print(f"Error on line {self.line_number}: Invalid Subtract: {command}")

        elif command.startswith("Append"):
            try:
                parts = command[7:].split(" to ")
                val = eval(self._convert_condition(parts[0].strip()), self.variables, self.variables)
                list_name = parts[1].strip()
                if list_name not in self.variables: self.variables[list_name] = []
                if isinstance(self.variables[list_name], list): self.variables[list_name].append(val)
                else: print(f"Error on line {self.line_number}: '{list_name}' is not a list.")
            except Exception as e: print(f"Error on line {self.line_number}: Invalid Append: {command}")

        elif command.startswith("Remove from"):
            try:
                parts = command[12:].split(" at index ")
                list_name = parts[0].strip()
                index = int(eval(self._convert_condition(parts[1].strip()), self.variables, self.variables))
                if list_name in self.variables and isinstance(self.variables[list_name], list):
                    if 0 <= index < len(self.variables[list_name]): self.variables[list_name].pop(index)
                    else: print(f"Error on line {self.line_number}: Index {index} out of range for '{list_name}'.")
                else: print(f"Error on line {self.line_number}: '{list_name}' is not a list.")
            except Exception as e: print(f"Error on line {self.line_number}: Invalid Remove: {command}")

        elif command.startswith("Clear "):
            try:
                name = command[6:].strip()
                if name in self.variables:
                    val = self.variables[name]
                    if isinstance(val, list): self.variables[name] = []
                    elif isinstance(val, dict): self.variables[name] = {}
                    elif isinstance(val, str): self.variables[name] = ""
                    else: self.variables[name] = None
                else: print(f"Error on line {self.line_number}: '{name}' undefined.")
            except Exception as e: print(f"Error on line {self.line_number}: In Clear: {e}")

        elif command.startswith("Join "):
            # Join list with delimiter into string
            try:
                parts = command[5:].split(" with ")
                list_name = parts[0].strip()
                delimiter = eval(self._convert_condition(parts[1].strip()), self.variables, self.variables)
                if list_name in self.variables and isinstance(self.variables[list_name], list):
                    result = delimiter.join(str(item) for item in self.variables[list_name])
                    print(result)
                else: print(f"Error on line {self.line_number}: '{list_name}' is not a list.")
            except Exception as e: print(f"Error on line {self.line_number}: In Join: {e}")

        elif command.startswith("Split "):
            try:
                # Split "text" by "delimiter" into result_list
                parts = command[6:].split(" by ")
                text_expr = parts[0].strip()
                rest = parts[1].split(" into ")
                delimiter = eval(self._convert_condition(rest[0].strip()), self.variables, self.variables)
                var_name = rest[1].strip()
                text = str(eval(self._convert_condition(text_expr), self.variables, self.variables))
                self.variables[var_name] = text.split(delimiter)
            except Exception as e: print(f"Error on line {self.line_number}: In Split: {e}")

        elif command.startswith("Replace "):
            try:
                # Replace "old" with "new" in text_var
                parts = command[8:].split(" with ")
                old = eval(self._convert_condition(parts[0].strip()), self.variables, self.variables)
                rest = parts[1].split(" in ")
                new = eval(self._convert_condition(rest[0].strip()), self.variables, self.variables)
                var_name = rest[1].strip()
                if var_name in self.variables:
                    self.variables[var_name] = str(self.variables[var_name]).replace(str(old), str(new))
                else: print(f"Error on line {self.line_number}: '{var_name}' undefined.")
            except Exception as e: print(f"Error on line {self.line_number}: In Replace: {e}")

        elif command.startswith("Wait for "):
            try:
                seconds = float(eval(self._convert_condition(command[9:].replace(" seconds", "").replace(" second", "").strip()), self.variables, self.variables))
                time.sleep(seconds)
            except Exception as e: print(f"Error on line {self.line_number}: In Wait: {e}")

        elif command.startswith("Length of "):
            try:
                name = command[10:].strip()
                # Check if it's a direct variable or needs evaluation
                if name in self.variables:
                    val = self.variables[name]
                    result = len(val)
                    print(result)
                else:
                    # Try to evaluate as expression
                    converted = self._convert_condition(name)
                    val = eval(converted, self.variables, self.variables)
                    result = len(val)
                    print(result)
            except Exception as e: 
                print(f"Error on line {self.line_number}: In Length of: {e}")

        elif command.startswith("Uppercase "):
            try:
                name = command[10:].strip()
                val = str(self.variables.get(name, ""))
                print(val.upper())
            except Exception as e: print(f"Error on line {self.line_number}: In Uppercase: {e}")

        elif command.startswith("Lowercase "):
            try:
                name = command[10:].strip()
                val = str(self.variables.get(name, ""))
                print(val.lower())
            except Exception as e: print(f"Error on line {self.line_number}: In Lowercase: {e}")

        elif command.startswith("Keys of "):
            try:
                name = command[8:].strip()
                val = self.variables.get(name)
                if isinstance(val, dict): print(list(val.keys()))
                else: print(f"Error on line {self.line_number}: '{name}' is not a dictionary.")
            except Exception as e: print(f"Error on line {self.line_number}: In Keys of: {e}")

        elif command.startswith("Get "):
            var_name = command[4:].strip()
            self.variables[var_name] = input(f"Enter value for {var_name}: ")

        elif command.startswith("Call "):
            self.parse_and_execute_call(command)

        elif command.startswith("Read "):
            filename = command[5:].strip().strip('"').strip("'")
            try:
                with open(filename, 'r') as file: print(file.read())
            except FileNotFoundError: print(f"Error on line {self.line_number}: File '{filename}' not found.")

        elif command.startswith("Write "):
            parts = command[6:].split(",", 1)
            if len(parts) == 2:
                filename = parts[0].strip().strip('"').strip("'")
                content = parts[1].strip()
                try:
                    if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
                        data = content[1:-1]
                    else: data = str(eval(self._convert_condition(content), self.variables, self.variables))
                    with open(filename, 'w') as file:
                        file.write(data)
                        print(f"Content written to {filename}")
                except Exception as e: print(f"Error on line {self.line_number}: Writing to file: {e}")
            else: print(f"Error on line {self.line_number}: Invalid Write syntax: {command}")

        elif command.startswith("Power "):
            parts = command[6:].split(" to the power of")
            if len(parts) == 2:
                try:
                    base = float(eval(self._convert_condition(parts[0].strip()), self.variables, self.variables))
                    exponent = float(eval(self._convert_condition(parts[1].strip()), self.variables, self.variables))
                    print(math.pow(base, exponent))
                except Exception as e: print(f"Error on line {self.line_number}: Invalid Power: {e}")

        elif command.startswith("SquareRoot "):
            value_str = command[11:].strip()
            if value_str:
                try:
                    value = float(eval(self._convert_condition(value_str), self.variables, self.variables))
                    if value < 0: print(f"Error on line {self.line_number}: Cannot calculate sqrt of negative.")
                    else: print(f"{math.sqrt(value):.2f}")
                except Exception as e: print(f"Error on line {self.line_number}: Invalid SquareRoot: {e}")
            else: print(f"Error on line {self.line_number}: No value for SquareRoot")
        else:
            # Check if it's a direct function call without 'Call' keyword
            if command.split("(")[0].strip() in self.functions:
                self.parse_and_execute_call("Call " + command)
            else:
                print(f"Error on line {self.line_number}: Unknown command: {command.strip()}")

    def parse_and_execute_call(self, command):
        is_assignment = False
        var_to_assign = None
        if "Set " in command and " to Call " in command:
            is_assignment = True
            parts = command.split(" to Call ")
            var_to_assign = parts[0][4:].strip()
            func_call_part = parts[1].strip()
        else:
            func_call_part = command[5:].strip()

        if " with " in func_call_part:
            parts = func_call_part.split(" with ", 1)
            func_name = parts[0].strip()
            arg_part = parts[1].strip()
            args = [eval(self._convert_condition(arg.strip()), self.variables, self.variables) for arg in arg_part.split(",")]
        else:
            func_name = func_call_part
            args = []

        # Handle class methods like Call user.greet
        if "." in func_name:
            obj_name, method_name = func_name.split(".", 1)
            if obj_name in self.variables and isinstance(self.variables[obj_name], dict) and "_class_" in self.variables[obj_name]:
                class_name = self.variables[obj_name]["_class_"]
                method_data = self._get_class_method(class_name, method_name)
                if method_data:
                    block, params, defaults = method_data
                    
                    # Handle default arguments for methods
                    call_vars = defaults.copy()
                    for p, a in zip(params, args):
                        call_vars[p] = a
                    
                    old_variables = self.variables.copy()
                    # Add 'self' to local variables
                    self.variables.update(call_vars)
                    self.variables["self"] = old_variables[obj_name]
                    
                    self.returning = False
                    self.execute_script(block, self.line_number)
                    ret_val = self.variables.get("_return_value_")
                    # Update fields back to object
                    if "self" in self.variables:
                        old_variables[obj_name]["fields"] = self.variables["self"]["fields"]
                    self.variables = old_variables
                    self.returning = False
                    if is_assignment and var_to_assign: self.variables[var_to_assign] = ret_val
                    return
                else:
                    print(f"Error on line {self.line_number}: Method '{method_name}' not found for '{obj_name}' of class '{class_name}'")
                    return
            print(f"Error on line {self.line_number}: Method '{method_name}' not found for '{obj_name}'")
            return

        if func_name in self.functions:
            block, offset, params, defaults = self.functions[func_name]
            # Handle default arguments
            call_vars = defaults.copy()
            for p, a in zip(params, args):
                call_vars[p] = a
            
            # Check if we have all required params
            if len(args) < (len(params) - len(defaults)) or len(args) > len(params):
                 print(f"Error on line {self.line_number}: '{func_name}' argument mismatch.")
            else:
                old_variables = self.variables.copy()
                self.variables.update(call_vars)
                self.returning = False
                self.execute_script(block, offset)
                ret_val = self.variables.get("_return_value_")
                self.variables = old_variables
                self.returning = False
                if is_assignment and var_to_assign: self.variables[var_to_assign] = ret_val
        elif func_name in self.variables and isinstance(self.variables[func_name], dict) and self.variables[func_name].get("_type_") == "lambda":
            # Handle Lambda calls
            lambda_obj = self.variables[func_name]
            params = lambda_obj["params"]
            body = lambda_obj["body"]
            
            call_vars = {}
            for p, a in zip(params, args):
                call_vars[p] = a
            
            try:
                # Lambdas are single expression
                result = eval(self._convert_condition(body), self.variables, self.variables)
                if is_assignment and var_to_assign: self.variables[var_to_assign] = result
                else: print(result)
            except Exception as e:
                print(f"Error on line {self.line_number}: In Lambda call: {e}")
        else:
            print(f"Error on line {self.line_number}: Undefined function '{func_name}'")

    def _convert_condition(self, condition):
        # Membership first (to avoid 'is' conflict)
        condition = condition.replace(" is not in ", " not in ")
        condition = condition.replace(" is in ", " in ")
        
        # Bitwise
        condition = condition.replace(" bit and ", " & ")
        condition = condition.replace(" bit or ", " | ")
        condition = condition.replace(" bit xor ", " ^ ")
        condition = condition.replace(" bit not ", " ~ ")
        condition = condition.replace(" shift left ", " << ")
        condition = condition.replace(" shift right ", " >> ")

        # Handle object field access: obj.name -> obj['fields']['name']
        import re
        # Find all occurrences of word.word where the first word is a known object
        potential_objs = [k for k, v in self.variables.items() if isinstance(v, dict) and "_class_" in v]
        for obj in potential_objs:
            condition = re.sub(rf'\b{obj}\.([a-zA-Z_][a-zA-Z0-9_]*)', rf"{obj}['fields']['\1']", condition)
        
        # Always handle 'self' specifically if it exists in scope
        if "self" in self.variables:
             condition = re.sub(r'\bself\.([a-zA-Z_][a-zA-Z0-9_]*)', r"self['fields']['\1']", condition)

        # File exists check in condition
        if "file exists " in condition:
            parts = condition.split("file exists ")
            filename = parts[1].strip()
            # Wrap in os.path.exists
            return f"__import__('os').path.exists({filename})"

        # Reflection - MUST be before 'is' replacement
        if " is instance of " in condition:
            parts = condition.split(" is instance of ")
            obj = parts[0].strip()
            cls = parts[1].strip()
            # In Lexora, objects are dicts with '_class_' key
            return f"(isinstance({obj}, dict) and {obj}.get('_class_') == '{cls}')"

        # Comparison
        condition = condition.replace("is less than or equal to", "<=")
        condition = condition.replace("is greater than or equal to", ">=")
        condition = condition.replace("is less than", "<")
        condition = condition.replace("is greater than", ">")
        
        # Basic keyword mapping
        condition = condition.replace(" and ", " and ")
        condition = condition.replace(" or ", " or ")
        condition = condition.replace(" not ", " not ")
        condition = condition.replace(" equals ", " == ")
        condition = condition.replace(" is ", " == ")
        
        return condition

def main():
    interpreter = SimpleEnglishInterpreter()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                interpreter.execute_script(lines)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
    else:
        # REPL mode
        print("Lexora 7.0 Ultimate Edition - Interactive Shell")
        print("Type 'exit' to quit.")
        while True:
            try:
                line = input("lx> ")
                if line.lower() == 'exit': break
                if not line.strip(): continue
                # Basic block handling for REPL
                if line.endswith(":"):
                    block = [line]
                    while True:
                        inner = input(".. ")
                        block.append(inner)
                        if inner.strip() == "End": break
                    interpreter.execute_script(block)
                else:
                    interpreter.execute_script([line])
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
