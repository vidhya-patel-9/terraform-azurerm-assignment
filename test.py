# Before (duplicate code)
result1 = some_function(param1, param2)
result2 = some_function(param3, param4)

# After (refactored)
def process_data(param1, param2):
    # Your code to process data
    return result

result1 = process_data(param1, param2)
result2 = process_data(param3, param4)
