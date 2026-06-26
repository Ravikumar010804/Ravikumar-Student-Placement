import mysql.connector
from mysql.connector import Error

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ravi@@181229',
    'database': 'Placement_Management_System'
}

def get_connection():
    """Establish and return a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

# ==================== CREATE ====================

def create_student():
    print("\n--- Add New Student ---")

    name = input("Enter Name: ")
    roll_no = input("Enter Roll Number: ")
    branch = input("Enter Branch: ")

    try:
        cgpa = float(input("Enter CGPA: "))
    except ValueError:
        print("❌ Invalid CGPA.")
        return

    status = input("Enter Status (Eligible/Placed/Debarred): ") or "Eligible"

    conn = get_connection()

    if conn:
        try:
            cursor = conn.cursor()

            query = """
            INSERT INTO students
            (name, roll_no, branch, cgpa, status)
            VALUES (%s,%s,%s,%s,%s)
            """

            cursor.execute(query, (name, roll_no, branch, cgpa, status))
            conn.commit()

            print("✅ Student record added successfully.")

        except Error as e:
            print("❌ Error:", e)

        finally:
            cursor.close()
            conn.close()


# ==================== READ ====================

def read_students():

    print("\n========== STUDENT RECORDS ==========")

    conn = get_connection()

    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students")

            records = cursor.fetchall()

            if len(records) == 0:
                print("No Records Found.")
                return

            print("-"*80)
            print(f"{'ID':<5}{'NAME':<20}{'ROLL NO':<15}{'BRANCH':<10}{'CGPA':<10}{'STATUS':<15}")
            print("-"*80)

            for row in records:
                print(f"{row[0]:<5}{row[1]:<20}{row[2]:<15}{row[3]:<10}{row[4]:<10}{row[5]:<15}")

        except Error as e:
            print("❌ Error:", e)

        finally:
            cursor.close()
            conn.close()


# ==================== UPDATE ====================

def update_student():

    print("\n--- Update Student ---")

    roll_no = input("Enter Roll Number: ")

    conn = get_connection()

    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll_no,))
            student = cursor.fetchone()

            if student is None:
                print("❌ Student Not Found.")
                return

            print("\nCurrent Student Details")
            print("--------------------------")
            print("Name   :", student[1])
            print("RollNo :", student[2])
            print("Branch :", student[3])
            print("CGPA   :", student[4])
            print("Status :", student[5])

            new_cgpa = input("\nEnter New CGPA (Press Enter to Skip): ")
            new_status = input("Enter New Status (Press Enter to Skip): ")

            updates = []
            values = []

            if new_cgpa:
                try:
                    updates.append("cgpa=%s")
                    values.append(float(new_cgpa))
                except ValueError:
                    print("❌ Invalid CGPA.")
                    return

            if new_status:
                updates.append("status=%s")
                values.append(new_status)

            if not updates:
                print("No Changes Made.")
                return

            values.append(roll_no)

            query = f"UPDATE students SET {', '.join(updates)} WHERE roll_no=%s"

            cursor.execute(query, tuple(values))
            conn.commit()

            print("✅ Student Updated Successfully.")

        except Error as e:
            print("❌ Error:", e)

        finally:
            cursor.close()
            conn.close()


# ==================== DELETE ====================

def delete_student():

    print("\n--- Delete Student ---")

    roll_no = input("Enter Roll Number: ")

    conn = get_connection()

    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll_no,))
            student = cursor.fetchone()

            if student is None:
                print("❌ Student Not Found.")
                return

            confirm = input("Are you sure? (y/n): ")

            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll_no,))
                conn.commit()
                print("✅ Student Deleted Successfully.")
            else:
                print("Deletion Cancelled.")

        except Error as e:
            print("❌ Error:", e)

        finally:
            cursor.close()
            conn.close()


# ==================== MAIN MENU ====================

def main():

    while True:

        print("\n====================================")
        print(" PLACEMENT MANAGEMENT SYSTEM ")
        print("====================================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter Choice (1-5): ")

        if choice == '1':
            create_student()

        elif choice == '2':
            read_students()

        elif choice == '3':
            update_student()

        elif choice == '4':
            delete_student()

        elif choice == '5':
            print("Thank You!")
            break

        else:
            print("❌ Invalid Choice.")


if __name__ == "__main__":
    main()
