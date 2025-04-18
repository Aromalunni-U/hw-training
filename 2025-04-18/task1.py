
name = "Aromalunni"
age = 21
marks = [30,40,50]

student = {
	"name":name,
	"age":age,
	"marks":marks
}


for key,value in student.items():
	print(f"{key} : {type(value)}")


total_marks = sum(marks)
average_mark = total_marks/ len(marks)


print("Total Marks :",total_marks)
print("Average Marks :",average_mark)


if average_mark >= 40:
	print("Passed")
else:
	print("Failed")


for mark in marks:
	print(mark)


marks = set(marks)
print(marks)

subjects = ("Emglish","Malayalam","Hindi")
print(subjects)

remarks = None
print(type(remarks))

is_passed = True
print(type(is_passed))

report = f"""
________Report_________

Student Name : {name}
Age 	     : {age}
Subjects     : {subjects}
marks 	     : {student["marks"]}
Total Mark   : {total_marks}
Average Mark : {average_mark}
Result       : {"Passed" if is_passed else "Failed"}
remark       : {remarks}
"""

print(report)