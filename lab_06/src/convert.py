import csv

def csv_to_latex(csv_filename):
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        
        latex_code = "\\begin{longtable}{|" + "r|" * len(headers) + "}\n\\hline\n"
        
        latex_code += " & ".join(headers) + " \\\\ \\hline\n"
        
        for row in reader:
            latex_code += " & ".join(row) + " \\\\ \\hline\n"
        
        latex_code += "\\end{longtable}"
        
    return latex_code

csv_filename = 'res.csv'
latex_table = csv_to_latex(csv_filename)

print(latex_table)
