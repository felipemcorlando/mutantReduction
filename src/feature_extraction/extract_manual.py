import os

def count_operators(file_path):
    operator_counts = {
        '+': 0,
        '-': 0,
        '*': 0,
        '/': 0
    }

    try:
        with open(file_path, 'r') as file:
            content = file.read()

            operator_counts['+'] = content.count('+')
            operator_counts['-'] = content.count('-')
            operator_counts['*'] = content.count('*')
            operator_counts['/'] = content.count('/')

    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None

    return operator_counts



directory = './data/output/' 


for i in range(0, 30):
    file_path = os.path.join(directory, f"mutant_{i}.py")

    result = count_operators(file_path)
    #print(result)

    if result:
        print(f"Operator counts in {file_path}:")
        for operator, count in result.items():
            print(f"{operator}: {count}")
