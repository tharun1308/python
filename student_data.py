import pandas as pd
import random
import string
from faker import Faker
import os



# Initialize Faker for generating fake data
fake = Faker()

# Function to generate random alphanumeric strings
def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to randomly introduce corruptions in data
def corrupt_data(value, corruption_type):
    if corruption_type == 'missing':
        return None
    elif corruption_type == 'wrong_type':
        return random_string(5)
    elif corruption_type == 'random_value':
        return random.choice([random_string(5), fake.name(), fake.date(), random.uniform(1.0, 4.0)])
    return value

# Generate data for 100 students
students = []
for i in range(100):
    student_id = random.randint(1000, 9999)
    name = fake.name()
    dob = fake.date_of_birth(minimum_age=17, maximum_age=22).strftime('%Y-%m-%d')
    address = fake.address().replace('\n', ', ')
    gpa = round(random.uniform(2.0, 4.0), 2)
    extracurriculars = ', '.join(fake.words(nb=3, ext_word_list=['Basketball', 'Debate Club', 'Drama Club', 'Science Olympiad', 'Student Government', 'Math Team', 'Track & Field', 'Volunteer Work']))
    admission_status = random.choice(['Accepted', 'Waitlisted', 'Rejected'])
    
    # Introduce corruption
    if random.random() < 0.1:  # 10% chance to corrupt data
        corruption_type = random.choice(['missing', 'wrong_type', 'random_value'])
        if corruption_type == 'missing':
            dob = corrupt_data(dob, 'missing')
        elif corruption_type == 'wrong_type':
            gpa = corrupt_data(gpa, 'wrong_type')
        elif corruption_type == 'random_value':
            address = corrupt_data(address, 'random_value')
    
    students.append([student_id, name, dob, address, gpa, extracurriculars, admission_status])

# Convert to DataFrame
columns = ['StudentID', 'Name', 'DOB', 'Address', 'GPA', 'Extracurriculars', 'Admission Status']
df = pd.DataFrame(students, columns=columns)

# Create the downloads folder if it doesn't exist
download_folder = 'downloads'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Save to CSV
csv_file_path = os.path.join(download_folder, 'student_data_corrupt.csv')
df.to_csv(csv_file_path, index=False)
print(f'CSV file with corrupted data created: {csv_file_path}')

# Save to Excel
excel_file_path = os.path.join(download_folder, 'student_data_corrupt.xlsx')
df.to_excel(excel_file_path, index=False)
print(f'Excel file with corrupted data created: {excel_file_path}')
