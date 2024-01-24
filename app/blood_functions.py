# function to get the color correspondent to the blood indicator level
def get_blood_level_color(indicator_name, level, reference_ranges):
    if indicator_name in reference_ranges:
        reference = reference_ranges[indicator_name]
        min_range = reference.get("min")
        max_range = reference.get("max")

        if min_range is not None and max_range is not None:
            if level < min_range or level > max_range:
                return "red"
            elif abs(level - min_range) <= 0.2 * (max_range - min_range) or abs(level - max_range) <= 0.2 * (
                    max_range - min_range):
                return "yellow"
            else:
                return "green"
        else:
            return "Unknown reference range"
    else:
        return "Indicator not found in the reference"

# fucntion to update the dict adding the correspondent color as a key value next to the blood level
def color_mapping(blood_test, reference_ranges):
    colored_indicators = {}

    for indicator_name, level in blood_test.items():
        colored_indicators[indicator_name] = [level, get_blood_level_color(indicator_name, level, reference_ranges)]
    return colored_indicators



def determine_unit_and_code(test_name):
    # Add logic to determine the unit and unit code based on the test name
    # You might need more sophisticated logic or external reference data
    if "mg/dL" in test_name:
        return "mg/dL", "mg/dL"
    elif "g/dL" in test_name:
        return "g/dL", "g/dL"
    elif "U/L" in test_name:
        return "U/L", "U/L"
    elif "mmol/L" in test_name:
        return "mmol/L", "mmol/L"
    elif "ug/dL" in test_name:
        return "ug/dL", "ug/dL"
    elif "umol/L" in test_name:
        return "umol/L", "umol/L"
    else:
        return "unknown", "unknown"

def determine_interpretation_code(color):
    # Map color to interpretation code based on the provided mapping
    if color.lower() == "green":
        return "N"  # Normal range
    elif color.lower() == "yellow":
        return "R"  # Medium range
    elif color.lower() == "red":
        return "H"  # Extreme range
    else:
        return "unknown"
    
    
    
def color_percentages(blood_tests):
    blood_test = blood_tests[0]
    green = 0.0
    yellow = 0.0
    red = 0.0
    for key, value in blood_test.items():
        color = blood_test[key][1]
        if color == "green":
            green +=1
        if color == "yellow":
            yellow +=1
        if color == "red":
            red +=1
    return [green/37,yellow/37,red/37,] # there are 37 blood indicators