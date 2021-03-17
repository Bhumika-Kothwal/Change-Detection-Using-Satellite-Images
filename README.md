# Change-Detection-Using-Satellite-Images 

## 1. Program file name : DetectChange.py 

### Description of program 

### Outputs

### Conclusion    

### Doubts
* Correct result for some images not obtained -     
  This issue is currently being worked on.
  More explaination in [#1](https://github.com/Bhumika-Kothwal/Change-Detection-Using-Satellite-Images/issues/1) in Issues section.
  

## 2. Program file name : DetectChange_h4.py , DetectChange_h5.py

### Description of program    
The program file DetectChange_h4.py contains the code with hxh non-overlapping box value as 4x4 (even value of h) and program file DetectChange_h5.py contains the code with hxh non-overlapping box value as 5x5 (even value of h) to create eigen vector space for finding PCA components.

### Outputs
Both the programs with value of hxh non-overlapping box as 4x4 and 5x5 give expected change detection output.

### Conclusion
* hxh non-overlapping box set to create eigen vector space takes both odd and even values of h (concluded by practically experimenting)
