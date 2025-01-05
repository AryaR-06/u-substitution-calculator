from flask import Flask, request, jsonify, render_template
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import re
import sympy as sp

app = Flask(__name__)

def generate_u_sub (expression):
    checkpoint = "AryaR-06/t5-u-sub"
    tokenizer = T5Tokenizer.from_pretrained(checkpoint)
    model = T5ForConditionalGeneration.from_pretrained(checkpoint)     
    model.eval()

    input = tokenizer(expression, truncation=True, padding="max_length", max_length=512, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(input_ids=input["input_ids"],
                                 attention_mask=input["attention_mask"],
                                  max_length=512,
                                  num_beams=4)

        prediction = tokenizer.decode(output[0], skip_special_tokens=True)
        return prediction      

def expr_tree_len(expr, max_depth=0, cur_depth=0):
    cur_depth += 1
    max_depth = max(max_depth, cur_depth)

    for arg in expr.args:
        max_depth = expr_tree_len(arg, max_depth=max_depth, cur_depth=cur_depth)

    return max_depth

def format_input (expression,early_return=False):
    if (expression.isalpha() and len(expression) != 1) or (expression.isnumeric()) or (not expression.strip()):
        raise ValueError

    expression = expression.replace("^", "**")
    expression = expression.replace("arcsin", "asin")
    expression = expression.replace("arccos", "acos")
    expression = expression.replace("arctan", "atan")
    expression = expression.replace("arccosec", "acsc")
    expression = expression.replace("arcsec", "asec")
    expression = expression.replace("arccot", "acot")

    expression = sp.sympify(expression)
    for subexpr in sp.preorder_traversal(expression):
        if subexpr.func != sp.Mul:
            expression = sp.collect(expression, subexpr)

    if early_return:
        return expression
    custom_arg_order = tuple(sorted(expression.args, key=expr_tree_len))

    if expression.func == sp.core.mul.Mul:
        expression = f"({sp.Mul(*custom_arg_order[:len(custom_arg_order)-1])})*{custom_arg_order[-1]}"

    expression = str(expression)
    expression = expression.replace("**", "^")
    expression = expression.replace("asin", "arcsin")
    expression = expression.replace("acos", "arccos")
    expression = expression.replace("atan", "arctan")
    expression = expression.replace("acsc", "arccosec")
    expression = expression.replace("asec", "arcsec")
    expression = expression.replace("acot", "arccot")
    expression = re.sub(r'sqrt\(([^()]+)\)', r'(\1)^(1/2)', expression)
    expression = re.sub(r'([a-zA-Z]+\([^()]*\)\^[0-9]+)', r'(\1)', expression)
    expression = re.sub(r'([\d]+\^[0-9]+)', r'(\1)', expression)
    expression = re.sub(r'([a-zA-Z]+\^[0-9]+)', r'(\1)', expression)
    expression = expression.replace("^", "**")

    return expression

def find_answer(formatted_expression):
    statements_to_print = []
    statements_to_print.append(f"(1)  {chr(0x222B)}({formatted_expression.replace('**', '^')})*dx")

    prediction = generate_u_sub (formatted_expression)

    if prediction == "0":
        statements_to_print.append("No Substitution Found")
        return statements_to_print
    else:
        statements_to_print.append(f"(2)  Let: u = {prediction.replace('**', '^')}")

        try:
            derivative = sp.diff(sp.sympify(prediction))
        except ValueError:
            statements_to_print.append("No Substitution Found")
            return statements_to_print
        if derivative == 0:
            statements_to_print.append("No Substitution Found")
            return statements_to_print

        statements_to_print.append(f"(3)  du = ({str(derivative).replace('**', '^')})*dx")
        statements_to_print.append(f"(4)  dx = du/({str(derivative).replace('**', '^')})")

        if formatted_expression.replace(prediction, 'u') == formatted_expression:
            statements_to_print.append("No Substitution Found")
            return statements_to_print

        substituted_integrand = format_input(f"{formatted_expression.replace(prediction, 'u')}/({str(derivative).replace('**', '^')})", True)
        substituted_integrand = sp.ratsimp(sp.trigsimp(substituted_integrand))

        if "x" in str(substituted_integrand).replace("exp","temp"):
            statements_to_print.append("No Substitution Found")
            return statements_to_print

        statements_to_print.append(f"(5)  {chr(0x222B)}({str(substituted_integrand).replace('**', '^')})*du")
        statements_to_print.insert(1, "-"*len(max(statements_to_print, key=lambda x: len(x))))
        statements_to_print.insert(5, "-"*len(max(statements_to_print, key=lambda x: len(x))))
        return statements_to_print

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    expression = data.get("expression")
    
    try:
        formatted_expression = format_input(expression)
        solution = find_answer(formatted_expression)

        if "No Substitution Found" in solution:
            solution = ["No Substitution Found"]

        return jsonify({"result": solution})
    except ValueError:
        return jsonify({"error": f"Input Error: Please check your formatting."}), 400
    except Exception:
        return jsonify({"error": f"Server Error: Please try again later."}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
