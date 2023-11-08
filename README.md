#Table Sorting Source Code
This repository accompanies to show given data on a table and sorting the values by clicking on headings.

##Installation
For command line usage:
```
pip3 install argparse
```
Analysis tool for data:
```
pip3 install pandas
```


##Usage
The first array contains the headings values:
```
python3 sortTable.py --rows ["A","B","C","D"] [5,6,7,8] [3,5,3,9]
```
or
```
python3 sortTable.py -r ["A","B","C","D"] [5,6,7,8] [3,5,3,9]
```
You can also give csv file to read data:
```
python3 sortTable.py --open data.csv
```
or
```
python3 sortTable.py -o data.csv
```
