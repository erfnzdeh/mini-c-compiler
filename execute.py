import os

from Tests.phase3_tester.test.vm import run


def exec(exe_path='output.txt' , result_path='expected.txt', error_path='error.txt'):
    if not os.path.exists(exe_path):
        print(f"{exe_path} not found.")
        return
    with open(exe_path, 'r') as f:
        code = f.read()
    if code[0]!= '0':
        print("EXEC : Invalid code format.")
        return
    code = code.strip().splitlines()
    result_file = open(result_path, "w")
    error_file = open(error_path, "w")
    output = run(code , output_file=result_file , error_file=error_file)
    result_file.close()
    error_file.close()


if __name__ == "__main__":
    exec()
