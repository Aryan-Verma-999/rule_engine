# Test Cases for Rule Engine API

This file contains the test cases for the Rule Engine API implemented in Flask. The test cases are designed to validate the functionality of the API endpoints for creating rules, combining rules, and evaluating rules.

---

## Test Case 1: Create Individual Rules and Verify AST Representation

### **Description:**
Test the creation of individual rules using the `/api/create_rule` endpoint and ensure that the Abstract Syntax Tree (AST) representation of each rule is correct.

### **Steps:**
1. **Create a Rule:**
   - **Endpoint:** `POST /api/create_rule`
   - **Request Body:**
     ```json
     {
       "name": "age_rule",
       "rule": "age > 30 AND salary > 50000"
     }
     ```
   - **Expected Response:**
     ```json
     {
       "message": "Rule 'age_rule' created successfully"
     }
     ```

2. **Verify AST Representation:**
   - Check the backend or response for the AST representation.
   - Example AST for the rule:
     ```json
     {
       "type": "BinaryOperation",
       "operator": "AND",
       "left": {
         "type": "BinaryOperation",
         "operator": ">",
         "left": {
           "type": "Variable",
           "value": "age"
         },
         "right": {
           "type": "Literal",
           "value": 30
         }
       },
       "right": {
         "type": "BinaryOperation",
         "operator": ">",
         "left": {
           "type": "Variable",
           "value": "salary"
         },
         "right": {
           "type": "Literal",
           "value": 50000
         }
       }
     }
     ```

### **Expected Outcome:**
The individual rule is successfully created and the AST representation matches the logical structure of the rule.

---

## Test Case 2: Combine Example Rules and Verify AST Representation

### **Description:**
Test the combination of multiple rules using the `/api/combine_rules` endpoint and ensure the resulting AST correctly reflects the combined logic.

### **Steps:**
1. **Create Two Rules:**
   - **Rule 1:** `age_rule` (as in Test Case 1)
   - **Rule 2:** `salary_rule`
     - **Endpoint:** `POST /api/create_rule`
     - **Request Body:**
       ```json
       {
         "name": "salary_rule",
         "rule": "salary > 40000"
       }
       ```
     - **Expected Response:**
       ```json
       {
         "message": "Rule 'salary_rule' created successfully"
       }
       ```

2. **Combine Rules:**
   - **Endpoint:** `POST /api/combine_rules`
   - **Request Body:**
     ```json
     {
       "name": "combined_rule",
       "rules": ["age_rule", "salary_rule"],
       "operator": "AND"
     }
     ```
   - **Expected Response:**
     ```json
     {
       "message": "Combined rule 'combined_rule' created successfully"
     }
     ```

3. **Verify Combined AST Representation:**
   - Check the backend or response for the AST representation of the combined rule.
   - Example AST for the combined rule:
     ```json
     {
       "type": "BinaryOperation",
       "operator": "AND",
       "left": {
         "type": "BinaryOperation",
         "operator": ">",
         "left": {
           "type": "Variable",
           "value": "age"
         },
         "right": {
           "type": "Literal",
           "value": 30
         }
       },
       "right": {
         "type": "BinaryOperation",
         "operator": ">",
         "left": {
           "type": "Variable",
           "value": "salary"
         },
         "right": {
           "type": "Literal",
           "value": 40000
         }
       }
     }
     ```

### **Expected Outcome:**
The combined rule is successfully created, and the AST reflects the combined logic of the two rules.

---

## Test Case 3: Evaluate Rule with Sample Data

### **Description:**
Test the evaluation of a rule using the `/api/evaluate_rule` endpoint with predefined sample data.

### **Steps:**
1. **Create a Combined Rule:**
   - Use the combined rule from Test Case 2 (`combined_rule`).

2. **Evaluate the Combined Rule:**
   - **Endpoint:** `POST /api/evaluate_rule`
   - **Request Body:**
     ```json
     {
       "name": "combined_rule"
     }
     ```
   - **Expected Response:**
     ```json
     {
       "result": true
     }
     ```

3. **Sample Data for Evaluation:**
   - The sample data used for rule evaluation is:
     ```json
     {
       "age": 35,
       "salary": 60000
     }
     ```

4. **Modify Sample Data:**
   - Test with different sample data to validate the rule.
   - Example for a failure scenario:
     ```json
     {
       "age": 25,
       "salary": 35000
     }
     ```
   - **Expected Response:**
     ```json
     {
       "result": false
     }
     ```

### **Expected Outcome:**
The evaluation returns the correct result (`true` or `false`) based on the sample data and rule.

---

## Test Case 4: Combine Additional Rules and Test Functionality

### **Description:**
Test the functionality of combining additional rules using the `/api/combine_rules` endpoint and evaluate the combined rule.

### **Steps:**
1. **Create Additional Rules:**
   - **Rule 1:** `age_rule` (already created in previous test cases)
   - **Rule 2:** `salary_rule` (already created in previous test cases)
   - **Rule 3:** New Rule `experience_rule`
     - **Endpoint:** `POST /api/create_rule`
     - **Request Body:**
       ```json
       {
         "name": "experience_rule",
         "rule": "experience > 2"
       }
       ```

2. **Combine Additional Rules:**
   - **Endpoint:** `POST /api/combine_rules`
   - **Request Body:**
     ```json
     {
       "name": "combined_experience_rule",
       "rules": ["age_rule", "salary_rule", "experience_rule"],
       "operator": "AND"
     }
     ```

3. **Evaluate the Combined Rule:**
   - **Endpoint:** `POST /api/evaluate_rule`
   - **Request Body:**
     ```json
     {
       "name": "combined_experience_rule"
     }
     ```

4. **Expected Response:**
   ```json
   {
     "result": true
   }
5. **Test Failure Scenario:**
- **Modify the sample data to trigger a rule failure:**
```json
{
  "age": 25,
  "salary": 35000,
  "experience": 1
}
```
- **Expected Response:**
```json
{
  "result": false
}
```
- **Expected Outcome:**
- The combined rule is successfully created and evaluated. The result should correctly reflect whether the rule conditions are met based on the provided sample data.

# Conclusion
- These test cases cover the fundamental functionalities of creating rules, combining rules, and evaluating them. They ensure that the API behaves as expected and processes logic in a structured and correct manner.