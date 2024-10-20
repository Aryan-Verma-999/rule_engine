import tkinter as tk 
from tkinter import simpledialog, messagebox
from flask import Flask, jsonify, request
import threading

# Initialize Flask app
app = Flask(__name__)

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value  # e.g., age > 30
        self.left = left  # Left child (for operators)
        self.right = right  # Right child (for operators)

    def __repr__(self):
        return f"Node({self.type}, {self.value})"

# Sample In-memory Storage for Rules
rule_store = {}

# Pre-defined data for evaluation
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

# Function to create a rule (Converts rule string to AST)
def create_rule(rule_string):
    if "AND" in rule_string:
        parts = rule_string.split("AND")
        left = parts[0].strip()
        right = parts[1].strip()
        root = Node("operator", "AND")
        root.left = Node("operand", left)
        root.right = Node("operand", right)
    elif "OR" in rule_string:
        parts = rule_string.split("OR")
        left = parts[0].strip()
        right = parts[1].strip()
        root = Node("operator", "OR")
        root.left = Node("operand", left)
        root.right = Node("operand", right)
    else:
        root = Node("operand", rule_string.strip())
    
    return root

# Function to combine multiple rules
def combine_rules(rules, operator="AND"):
    combined_root = Node("operator", operator)
    current = combined_root

    for i, rule in enumerate(rules):
        if i == 0:
            current.left = rule_store[rule]
        else:
            current.right = rule_store[rule]
            if i < len(rules) - 1:
                new_node = Node("operator", operator)
                current.right = new_node
                current = new_node
    
    return combined_root

# Enhanced function to evaluate a rule against the data set
def evaluate_rule(ast, data):
    if ast.type == "operand":
        condition = ast.value.strip()

        # Handling different comparison operators
        if ">=" in condition:
            attribute, value = condition.split(">=")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) >= value
        
        elif "<=" in condition:
            attribute, value = condition.split("<=")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) <= value
        
        elif ">" in condition:
            attribute, value = condition.split(">")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) > value
        
        elif "<" in condition:
            attribute, value = condition.split("<")
            attribute = attribute.strip()
            value = int(value.strip())
            return data.get(attribute) < value
        
        elif "==" in condition:
            attribute, value = condition.split("==")
            attribute = attribute.strip()
            value = value.strip().replace('"', '')  # For string comparisons
            return data.get(attribute) == value

    elif ast.type == "operator":
        left_eval = evaluate_rule(ast.left, data)
        right_eval = evaluate_rule(ast.right, data)
        
        if ast.value == "AND":
            return left_eval and right_eval
        elif ast.value == "OR":
            return left_eval or right_eval

    return False

# API endpoint to create a rule
@app.route('/api/create_rule', methods=['POST'])
def api_create_rule():
    rule_name = request.json.get('name')
    rule_string = request.json.get('rule')
    
    if rule_name and rule_string:
        rule_store[rule_name] = create_rule(rule_string)
        return jsonify({"message": f"Rule '{rule_name}' created!"}), 201
    return jsonify({"error": "Invalid input"}), 400

# API endpoint to combine rules
@app.route('/api/combine_rules', methods=['POST'])
def api_combine_rules():
    rule_name = request.json.get('name')
    rule_list = request.json.get('rules')
    operator = request.json.get('operator')

    if rule_name and rule_list and operator in ["AND", "OR"]:
        combined_ast = combine_rules(rule_list, operator)
        rule_store[rule_name] = combined_ast
        return jsonify({"message": f"Combined rule '{rule_name}' created!"}), 201
    return jsonify({"error": "Invalid input"}), 400

# API endpoint to evaluate a rule
@app.route('/api/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    rule_name = request.json.get('name')
    
    if rule_name in rule_store:
        result = evaluate_rule(rule_store[rule_name], data)
        return jsonify({"result": result}), 200
    return jsonify({"error": f"Rule '{rule_name}' does not exist."}), 404

# GUI Class for the Rule Engine App
class RuleEngineApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Rule Engine App")
        master.geometry("400x300")

        # Frame to display rule operations
        self.frame_top = tk.Frame(master)
        self.frame_top.pack(pady=10)

        self.label = tk.Label(self.frame_top, text="Simple Rule Engine", font=("Helvetica", 14, "bold"))
        self.label.grid(row=0, column=0, padx=10, pady=5)

        # Display available rules
        self.rule_listbox_label = tk.Label(master, text="Available Rules:", font=("Helvetica", 10))
        self.rule_listbox_label.pack()

        self.rule_listbox = tk.Listbox(master, height=5)
        self.rule_listbox.pack(fill=tk.BOTH, padx=20, pady=10)
        self.refresh_rule_list()

        # Frame for buttons
        self.frame_buttons = tk.Frame(master)
        self.frame_buttons.pack(pady=10)

        self.create_button = tk.Button(self.frame_buttons, text="Create Rule", command=self.create_rule)
        self.create_button.grid(row=0, column=0, padx=10)

        self.combine_button = tk.Button(self.frame_buttons, text="Combine Rules", command=self.combine_rules)
        self.combine_button.grid(row=0, column=1, padx=10)

        self.evaluate_button = tk.Button(self.frame_buttons, text="Evaluate Rule", command=self.evaluate_rule_gui)
        self.evaluate_button.grid(row=0, column=2, padx=10)

        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack(pady=10)

    def refresh_rule_list(self):
        """Refresh the listbox with the available rules."""
        self.rule_listbox.delete(0, tk.END)
        for rule in rule_store.keys():
            self.rule_listbox.insert(tk.END, rule)

    def create_rule(self):
        """Create a new rule and store it."""
        rule_name = simpledialog.askstring("Input", "Enter rule name:")
        rule_string = simpledialog.askstring("Input", "Enter rule (e.g., 'age > 30 AND salary > 50000'): ")

        if rule_name and rule_string:
            try:
                rule_store[rule_name] = create_rule(rule_string)
                messagebox.showinfo("Success", f"Rule '{rule_name}' created!")
                self.refresh_rule_list()
            except Exception as e:
                messagebox.showerror("Error", f"Error creating rule: {str(e)}")
        else:
            messagebox.showerror("Error", "Rule name and string cannot be empty!")

    def combine_rules(self):
        """Combine existing rules into a new one."""
        rule_name = simpledialog.askstring("Input", "Enter combined rule name:")
        rule_list = simpledialog.askstring("Input", "Enter rule names to combine (comma-separated):").split(",")
        operator = simpledialog.askstring("Input", "Enter combination operator (AND/OR):").strip().upper()

        if rule_name and rule_list and operator in ["AND", "OR"]:
            try:
                combined_ast = combine_rules(rule_list, operator)
                rule_store[rule_name] = combined_ast
                messagebox.showinfo("Success", f"Combined rule '{rule_name}' created!")
                self.refresh_rule_list()
            except Exception as e:
                messagebox.showerror("Error", f"Error combining rules: {str(e)}")
        else:
            messagebox.showerror("Error", "Invalid input! Ensure the operator is 'AND' or 'OR'.")

    def evaluate_rule_gui(self):
        """Evaluate a rule against the predefined dataset."""
        rule_name = simpledialog.askstring("Input", "Enter rule name to evaluate:")

        if rule_name in rule_store:
            try:
                result = evaluate_rule(rule_store[rule_name], data)
                messagebox.showinfo("Result", f"Evaluation Result: {result}")
            except Exception as e:
                messagebox.showerror("Error", f"Error evaluating rule: {str(e)}")
        else:
            messagebox.showerror("Error", f"Rule '{rule_name}' does not exist.")

# Function to run Flask app in a separate thread
def run_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start the Tkinter GUI app
    root = tk.Tk()
    app = RuleEngineApp(root)
    root.mainloop()