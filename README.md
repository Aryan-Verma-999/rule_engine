# Simple Rule Engine Application

This project is a **Simple Rule Engine** application built using Python. It allows you to create, combine, and evaluate rules based on a predefined dataset. The application includes a **Flask REST API** and a **Tkinter-based GUI**, offering both a programmatic and graphical way to manage the rules.
A **Flask API** for managing and evaluating rules.
2. A **Tkinter GUI** for user interaction to create, combine, and evaluate rules in a visually friendly interface.

## Technologies Used

- **Python**: The core programming language used.
- **Flask**: For serving the API endpoints.
- **Tkinter**: For building the desktop GUI interface.
- **Threading**: To run Flask and Tkinter concurrently.
- **SimpleDialog**: For creating input prompts in the Tkinter GUI.
  
## Features

### 1. Create Rules
- You can define custom rules as simple conditional expressions using comparison operators (`>`, `<`, `>=`, `<=`, `==`).
- Rules can be created using both the GUI and via the REST API.
- Example of a rule: `age > 30 AND salary > 50000`

### 2. Combine Rules
- Multiple rules can be combined using logical operators (`AND`, `OR`).
- Combined rules can also be created through both the GUI and API.
- Example: Combining rules like `age > 30` and `salary > 50000` using `AND`.

### 3. Evaluate Rules
- Rules can be evaluated against a predefined dataset, returning whether the rule conditions hold true for the dataset.
- Both individual and combined rules can be evaluated.

### 4. API Integration
- The application provides a REST API via Flask, making it accessible for programmatic interactions.

### 5. GUI for Ease of Use
- A Tkinter-based graphical interface allows users to create, combine, and evaluate rules without needing to interact with the API directly.

## GUI Features
The Tkinter-based GUI allows you to perform the following actions:

- Create Rule: Enter a rule name and a condition to define a new rule.
- Combine Rules: Combine existing rules using logical operators.
- Evaluate Rule: Select a rule from the list and evaluate it against the predefined dataset.
- View Available Rules: The list of created rules is displayed in the GUI for easy access.
## GUI Overview
- The GUI has an intuitive layout with buttons for creating, combining, and evaluating rules.
- The Listbox in the GUI displays all available rules, which are updated dynamically as new rules are created.
- You can interact with the GUI without needing to interact with the API directly.

## Predefined Dataset

The rules created in the application are evaluated against the following sample dataset:

```json
{
  "age": 35,
  "department": "Sales",
  "salary": 60000,
  "experience": 3
}
```
## How to Run
### 1. Install Dependencies
Ensure you have Python installed. Install the required packages using the following command:

```bash
pip install -r requirements.txt
```
### 2. Run the Application
Start the application using the following command:

```bash
python app.py
```
This will start both the Flask API (running on port 5000) and the Tkinter GUI.

### 3. Using the API
The API will be available at http://localhost:5000. You can use tools like Postman or cURL to interact with it.

### 4. Using the GUI
A Tkinter window will pop up, where you can create, combine, and evaluate rules.

## How it Works
- Creating Rules: You can create rules using operands (like age > 30) and logical operators (AND, OR).
- Combining Rules: Multiple rules can be combined to form complex logic.
- Evaluating Rules: The rules are evaluated against a predefined dataset using the conditions provided.
