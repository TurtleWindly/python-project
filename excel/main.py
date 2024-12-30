import os
import sys
import win32com.client

def get_macros(fName, path=os.getcwd()):
    print(f"Path: {path}")
    fName = os.path.join(path, fName)
    print(f"File name: {fName}")

    xlApp = win32com.client.Dispatch("Excel.Application")
    fTest = xlApp.Workbooks.Open(fName)

    for i in fTest.VBProject.VBComponents:
        print(f"Macro name: {i.Name}")

        num_lines = i.CodeModule.CountOfLines
        for j in range(1, num_lines + 1):
            if "Sub" in i.CodeModule.Lines(j, 1) and "End Sub" not in i.CodeModule.Lines(j, 1):
                print(i.CodeModule.Lines(j, 1))

    xlApp.Application.Quit()
    del xlApp

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cần duy nhất tên file")
        exit()
    file_name = sys.argv[1]
    get_macros(file_name)
