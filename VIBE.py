# Fatima Ammour
# CIS261
# Wk10 VIBE Coding

"""Manage student records, test scores, averages, and letter grades."""

STUDENT_FILE = "students.txt"


class Student:
	"""Store one student's ID and three test scores."""

	def __init__(self, name, student_id, scores):
		self.name = name
		self.student_id = student_id
		self.scores = scores

	def update_score(self, test_number, score):
		"""Update one of the student's test scores."""
		if test_number not in {1, 2, 3}:
			raise ValueError("Test number must be 1, 2, or 3.")
		if not 0 <= score <= 100:
			raise ValueError("Score must be between 0 and 100.")
		self.scores[test_number - 1] = score

	def average(self):
		return sum(self.scores) / len(self.scores)

	def grade(self):
		average = self.average()
		if average >= 90:
			return "A"
		if average >= 80:
			return "B"
		if average >= 70:
			return "C"
		if average >= 60:
			return "D"
		return "F"

	def display(self):
		print(f"\nName: {self.name}")
		print(f"Student ID: {self.student_id}")
		for number, score in enumerate(self.scores, start=1):
			print(f"Test {number}: {score:.2f}")
		print(f"Average: {self.average():.2f}")
		print(f"Letter grade: {self.grade()}")

	def to_file_line(self):
		values = [
			self.name,
			self.student_id,
			*(f"{score:.2f}" for score in self.scores),
			f"{self.average():.2f}",
			self.grade(),
		]
		return "|".join(values)


def get_score(label):
	while True:
		try:
			score = float(input(f"{label} (0-100): "))
			if 0 <= score <= 100:
				return score
		except ValueError:
			pass
		print("Please enter a number from 0 through 100.")


def load_students():
	students = {}
	try:
		with open(STUDENT_FILE, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.strip().split("|")
				if len(fields) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				name, student_id, test1, test2, test3, _, _ = fields
				scores = [float(test1), float(test2), float(test3)]
				if any(not 0 <= score <= 100 for score in scores):
					raise ValueError
				students[student_id] = Student(name, student_id, scores)
	except FileNotFoundError:
		pass
	except (OSError, ValueError):
		print(f"Could not read {STUDENT_FILE}; invalid records were skipped.")
	return students


def save_students(students):
	try:
		with open(STUDENT_FILE, "w", encoding="utf-8") as file:
			for student_id in sorted(students):
				file.write(students[student_id].to_file_line() + "\n")
		print(f"Student records saved to {STUDENT_FILE}.")
	except OSError as error:
		print(f"Could not save {STUDENT_FILE}: {error}")


def add_student(students):
	name = input("Student name: ").strip()
	student_id = input("Student ID: ").strip()
	if not name or not student_id:
		print("Student name and ID cannot be blank.")
		return
	if "|" in name or "|" in student_id:
		print("Student name and ID cannot contain '|'.")
		return
	if student_id in students:
		print("That student ID already exists.")
		return
	scores = [get_score(f"Test {number}") for number in range(1, 4)]
	students[student_id] = Student(name, student_id, scores)
	print(f"Added {name}.")


def update_test_score(students):
	if not students:
		print("No students have been added yet.")
		return
	student_id = input("Student ID: ").strip()
	if student_id not in students:
		print("Student ID not found.")
		return
	while True:
		try:
			test_number = int(input("Test number to update (1, 2, or 3): "))
			if test_number in {1, 2, 3}:
				break
		except ValueError:
			pass
		print("Please enter 1, 2, or 3.")
	students[student_id].update_score(test_number, get_score(f"Test {test_number}"))
	print(f"Updated score for {students[student_id].name}.")


def view_students(students):
	if not students:
		print("No students have been added yet.")
		return
	for student_id in sorted(students):
		students[student_id].display()


def display_summary(students):
	if not students:
		print("No students have been added yet.")
		return
	averages = [student.average() for student in students.values()]
	print(f"\nClass average: {sum(averages) / len(averages):.2f}")
	print(f"Students: {len(students)}")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average: {min(averages):.2f}")


def main():
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s) from {STUDENT_FILE}.")
	actions = {
		"1": add_student,
		"2": update_test_score,
		"3": view_students,
		"4": display_summary,
	}
	while True:
		print("\nStudent Record Manager")
		print("1. Add student")
		print("2. Update test score")
		print("3. View student records")
		print("4. View class summary")
		print("5. Exit")
		choice = input("Choose an option: ").strip()
		if choice == "5":
			save_students(students)
			print("Goodbye!")
			break
		action = actions.get(choice)
		if action is None:
			print("Please choose an option from 1 to 5.")
		else:
			action(students)
			if choice in {"1", "2"}:
				save_students(students)


if __name__ == "__main__":
	main()

