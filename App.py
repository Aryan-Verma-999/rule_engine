import tkinter as tk
from tkinter import simpledialog, messagebox
from flask import Flask, jsonify, request
import threading
import json
import os

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

# File to save and load rules
RULE_FILE = "rules.json"

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

# Function to save rules to a JSON file
def save_rules_to_file():
    with open(RULE_FILE, 'w') as f:
        json.dump(rule_store, f)

# Function to load rules from a JSON file
def load_rules_from_file():
    if os.path.exists(RULE_FILE):
        with open(RULE_FILE, 'r') as f:
            return json.load(f)
    return {}

# GUI Class for the Rule Engine App
class RuleEngineApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Rule Engine App")
        master.geometry("400x400")

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

        self.clear_button = tk.Button(self.frame_buttons, text="Clear All Rules", command=self.clear_rules)
        self.clear_button.grid(row=1, column=0, padx=10)

        self.delete_button = tk.Button(self.frame_buttons, text="Delete Rule", command=self.delete_rule)
        self.delete_button.grid(row=1, column=1, padx=10)

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_app)
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
        """Combine existing rules into a new rule."""
        rule_names = simpledialog.askstring("Input", "Enter the rule names to combine (comma separated):")
        operator = simpledialog.askstring("Input", "Enter operator (AND/OR):")

        if rule_names and operator:
            rule_list = [rule.strip() for rule in rule_names.split(",")]
            combined_rule_name = simpledialog.askstring("Input", "Enter the combined rule name:")

            if combined_rule_name and all(rule in rule_store for rule in rule_list):
                combined_ast = combine_rules(rule_list, operator)
                rule_store[combined_rule_name] = combined_ast
                messagebox.showinfo("Success", f"Combined rule '{combined_rule_name}' created!")
                self.refresh_rule_list()
            else:
                messagebox.showerror("Error", "Invalid rule names or operator.")

    def evaluate_rule_gui(self):
        """Evaluate the selected rule."""
        selected_rule = self.rule_listbox.curselection()
        if selected_rule:
            rule_name = self.rule_listbox.get(selected_rule[0])
            result = evaluate_rule(rule_store[rule_name], data)
            messagebox.showinfo("Evaluation Result", f"Result of rule '{rule_name}': {result}")
        else:
            messagebox.showerror("Error", "Please select a rule to evaluate.")

    def clear_rules(self):
        """Clear all stored rules."""
        rule_store.clear()
        self.refresh_rule_list()
        messagebox.showinfo("Success", "All rules cleared.")

    def delete_rule(self):
        """Delete a selected rule."""
        selected_rule = self.rule_listbox.curselection()
        if selected_rule:
            rule_name = self.rule_listbox.get(selected_rule[0])
            del rule_store[rule_name]
            self.refresh_rule_list()
            messagebox.showinfo("Success", f"Rule '{rule_name}' deleted.")
        else:
            messagebox.showerror("Error", "Please select a rule to delete.")

    def exit_app(self):
        """Exit the app and save rules to file."""
        save_rules_to_file()
        self.master.quit()


if __name__ == "__main__":
    # Load rules from file
    rule_store.update(load_rules_from_file())
    
    root = tk.Tk()
    app = RuleEngineApp(root)
    
    # Run the Flask app in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False))
    flask_thread.start()

    root.mainloop()
