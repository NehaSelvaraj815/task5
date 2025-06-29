import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    name TEXT PRIMARY KEY,
    phone TEXT,
    gmail TEXT
)
""")
conn.commit()

def display_contact():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    if not rows:
        print("📭 Contact book is empty.\n")
        return

    print("\n Contact List")
    print("-" * 70)
    print(f"{'Name':<20}{'Phone Number':<20}{'Gmail':<30}")
    print("-" * 70)
    for name, phone, gmail in rows:
        print(f"{name:<20}{phone:<20}{gmail:<30}")
    print("-" * 70 + "\n")

while True:
    print("""
===========================
📱 Personal Contact Book
===========================
1. Add new contact
2. Search contact
3. Display contacts
4. Edit contact
5. Delete contact
6. Exit
""")
    try:
        choice = int(input(" Enter your choice (1-6): "))
    except ValueError:
        print(" Please enter a valid number.\n")
        continue

    if choice == 1:
        name = input(" Enter contact name: ")
        phone = input(" Enter mobile number: ")
        gmail = input(" Enter Gmail address: ")
        try:
            cursor.execute("INSERT INTO contacts (name, phone, gmail) VALUES (?, ?, ?)", (name, phone, gmail))
            conn.commit()
            print(" Contact added successfully.\n")
        except sqlite3.IntegrityError:
            print(" Contact with this name already exists.\n")

    elif choice == 2:
        search_name = input("🔍 Enter the name to search: ")
        cursor.execute("SELECT * FROM contacts WHERE name = ?", (search_name,))
        result = cursor.fetchone()
        if result:
            name, phone, gmail = result
            print(f"\n Contact found:")
            print(f"   Name  : {name}")
            print(f"   Phone : {phone}")
            print(f"   Gmail : {gmail}\n")
        else:
            print(" Contact not found.\n")

    elif choice == 3:
        display_contact()

    elif choice == 4:
        edit_name = input("✏ Enter the name to edit: ")
        cursor.execute("SELECT * FROM contacts WHERE name = ?", (edit_name,))
        result = cursor.fetchone()
        if result:
            name, phone, gmail = result
            print(f"\nCurrent details for {name}:")
            print(f"   Phone : {phone}")
            print(f"   Gmail : {gmail}")
            new_phone = input(" Enter new phone number (or press Enter to keep unchanged): ")
            new_gmail = input("Enter new Gmail (or press Enter to keep unchanged): ")
            if not new_phone.strip():
                new_phone = phone
            if not new_gmail.strip():
                new_gmail = gmail
            cursor.execute("UPDATE contacts SET phone = ?, gmail = ? WHERE name = ?", (new_phone, new_gmail, edit_name))
            conn.commit()
            print(" Contact updated successfully.\n")
            display_contact()
        else:
            print(" Contact not found.\n")

    elif choice == 5:
        delete_name = input("🗑 Enter the name to delete: ")
        cursor.execute("SELECT * FROM contacts WHERE name = ?", (delete_name,))
        result = cursor.fetchone()
        if result:
            confirm = input(f"Are you sure you want to delete {delete_name}? (y/n): ")
            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM contacts WHERE name = ?", (delete_name,))
                conn.commit()
                print(" Contact deleted.\n")
                display_contact()
            else:
                print(" Delete cancelled.\n")
        else:
            print(" Contact not found.\n")

    elif choice == 6:
        print("👋 Exiting Contact Book. Goodbye!")
        break

    else:
        print(" Please choose a number between 1 and 6.\n")

# Close connection when the program exits
conn.close()