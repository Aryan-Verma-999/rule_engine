# API Endpoints for Rule Engine Application

1. **Create Rule**
   - **Method**: POST
   - **URL**: `/api/create_rule`
   - **Description**: Creates a new rule based on the provided rule string.
   - **Request Body** (JSON):
     ```json
     {
       "name": "rule_name",
       "rule": "age > 30 AND salary > 50000"
     }
     ```

2. **Combine Rules**
   - **Method**: POST
   - **URL**: `/api/combine_rules`
   - **Description**: Combines two or more existing rules into a new rule using an operator (AND/OR).
   - **Request Body** (JSON):
     ```json
     {
       "name": "combined_rule_name",
       "rules": ["rule1", "rule2"],
       "operator": "AND"
     }
     ```

3. **Evaluate Rule**
   - **Method**: POST
   - **URL**: `/api/evaluate_rule`
   - **Description**: Evaluates a specified rule against the predefined dataset.
   - **Request Body** (JSON):
     ```json
     {
       "name": "rule_name_to_evaluate"
     }
     ```
   - **Response** (JSON):
     ```json
     {
       "result": true
     }
     ```
## Add Headers
- **Content-Type**: `application/json`

# Example Data for Evaluation:
The rules can be evaluated against the following predefined dataset:
```json
{
  "age": 35,
  "department": "Sales",
  "salary": 60000,
  "experience": 3
}
