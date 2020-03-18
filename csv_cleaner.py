import csv

filename = 'AB_NYC_2019.csv'

orig = open(filename, 'rb')
data = orig.read()
orig.close()

cleaned_filename = 'cleaned_file.csv'
cleaned_file = open(cleaned_filename, 'wb')
cleaned_file.write(data.replace(b'\x00', b''))
cleaned_file.close()
cleaned_file = open(cleaned_filename, 'a')
cleaned_file.write('\r')
cleaned_file.close()
