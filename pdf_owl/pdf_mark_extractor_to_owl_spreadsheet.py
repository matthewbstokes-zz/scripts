#!/bin/python

import pyPdf

input_pdf = '/home/user/Downloads/mt.pdf'
input_owl_spreadsheet = '/home/user/Downloads/owl_marks.csv'
output_updated_owl = '/home/user/Downloads/owl_with_midterm.csv'
midterm_weight = 10
student_num_col = 3

def main():
  # extract student number -> marks dictionary from pdf
  pdf = pyPdf.PdfFileReader(open(input_pdf, "rb"))
  pdf_text = pdf.getPage(0).extractText()
  id_marks = pdf_text.split('\n')
  id_marks[0] = id_marks[0][id_marks[0].index('Only')+4:] # fix first entry
  id_marks_dict = {}
  for entry in id_marks:
    id, _, mark = entry.split(' ')
    id_marks_dict[id] = mark

  # read in all gradebook items
  gradebook_lines = [line.strip() for line in open(input_owl_spreadsheet)]

  # get header
  header = gradebook_lines[0]

  # set mark to midterm mark in end column of owl_marks csv / gradebook
  ofile = open(output_updated_owl, 'w')
  ofile.write(header)
  ofile.write('\n')
  for grade in gradebook_lines[1:]:
    ofile.write(grade)
    try:
      percent = float(id_marks_dict[grade.split(',')[student_number_col]])
      mark = (percent / 100.0) * midterm_weight
      ofile.write(str(mark))
    except KeyError:
      print grade.split(',')[:student_num_col]
    ofile.write('\n')
  ofile.close()

if __name__ == "__main__":
  main()
