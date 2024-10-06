import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens

def generate_arduino_sketch(tokens):
    setup_code = ""  # To store pinMode statements
    loop_code = ""   # To store the rest of the code
    index = 0
    while index < len(tokens):
        token = tokens[index]

        # Handle pin initialization in setup
        if token == "set" and tokens[index + 3] == "as":
            pin_number = tokens[index + 2]
            mode = tokens[index + 4]
            setup_code += "pinMode(" + pin_number + ", " + mode.upper() + ");\n"
            index += 5

        # Handle digitalWrite and analogWrite in loop
        elif token == "to":
            pin_number = tokens[index - 2]
            value = tokens[index + 1]
            if value.isdigit():  # Analog Write
                loop_code += "analogWrite(" + pin_number + ", " + value + ");\n"
            else:  # Digital Write
                loop_code += "digitalWrite(" + pin_number + ", " + value.upper() + ");\n"
            index += 2

        # Handle delays in loop
        elif token == "delay":
            time = tokens[index + 2]
            loop_code += "delay(" + time + ");\n"
            index += 4

        # Handle variable initialization in loop
        elif token == "initialize":
            var_name = tokens[index + 1]
            var_value = tokens[index + 3]
            loop_code += "int " + var_name + " = " + var_value + ";\n"
            index += 4

        # Handle reading sensor values (both analog and digital)
        elif token == "read" and tokens[index + 1] == "pin":
            pin_number = tokens[index + 2]
            var_name = tokens[index + 4]
            if "analog" in text:  # Check for analog read
                loop_code += "int " + var_name + " = analogRead(" + pin_number + ");\n"
            else:  # Default to digital read
                loop_code += "int " + var_name + " = digitalRead(" + pin_number + ");\n"
            index += 5

        # Handle if statements in loop
        elif token == "if":
            condition = " ".join(tokens[index + 1:tokens.index("then", index)])
            loop_code += "if (" + condition + ") {\n"
            index = tokens.index("then", index) + 1

        # Handle else statements in loop
        elif token == "else":
            loop_code += "} else {\n"
            index += 1

        # Handle end if statement in loop
        elif token == "end" and tokens[index + 1] == "if":
            loop_code += "}\n"
            index += 2

        # Handle for loop in loop
        elif token == "repeat":
            times = tokens[index + 2]
            loop_code += "for (int i = 0; i < " + times + "; i++) {\n"
            index += 3

        # Handle end of loop
        elif token == "end" and tokens[index + 1] == "loop":
            loop_code += "}\n"
            index += 2

        else:
            index += 1

    # Final generated sketch with setup and loop functions
    sketch = "void setup() {\n" + setup_code + "}\n\n"
    sketch += "void loop() {\n" + loop_code + "}\n"
    
    return sketch

if _name_ == "_main_":
    text = """
    set pin 13 as output
    set pin 9 as output
    set pin 13 to high

    delay for 1 second
    set pin 13 to low
    delay for 500 milliseconds
    set pin 9 to 128

    initialize sensor_value as 300
    if sensor_value > 500 then
    set pin 13 to high
    else
    set pin 13 to low
    end if

    repeat for 5 times
    set pin 13 to high
    delay for 1 millisecond
    set pin 13 to low
    end loop

    read pin A0 as sensor_value
    """
    
    tokens = tokenize_text(text)
    sketch = generate_arduino_sketch(tokens)

    print(sketch)