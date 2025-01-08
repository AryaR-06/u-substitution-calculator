# AI-Powered Integration Solver with Flask and T5 Transformers

An AI-driven web application for solving mathematical integration problems using **U-substitution**. This app utilizes a **T5 Transformer model** to analyze mathematical expressions and suggest optimal substitutions, making symbolic integration faster and more intuitive. Designed for students, researchers, and enthusiasts in mathematics and AI.

---

## **Features**
- **AI-Powered Substitution**: Uses a fine-tuned T5 Transformer model for substitution recommendations during integration.
- **Mathematical Symbolism**: Supports symbolic integration via SymPy, a Python library for mathematics.
- **Step-by-Step Output**: Provides detailed steps for solving integrals, including substitutions and transformations.
- **User-Friendly Interface**: A clean, responsive UI built with Flask and HTML templates.

---

## **AI at Work**
The core of the app lies in the **T5 Transformer model** fine-tuned for generating substitutions in integration problems. This model analyzes mathematical expressions and provides meaningful substitutions, which are then used to simplify the integration process. The AI component is powered by the **Hugging Face Transformers** library.

---

## **Live Demo**
[Check out the live app!](https://huggingface.co/spaces/AryaR-06/U-Substitution-Calculator)

---

## Using the Application
Enter a mathematical expression (e.g., sin(5*x) or (2*x + 3)*(x^2 + 3*x + 2)^(-1).
Click "Solve" to submit the expression.
View the generated substitution and step-by-step solution.
### Example Input and Output
Input: 
```
sin(5*x)
```
AI-Generated Output:
```
(1) ∫(sin(5*x))*dx
------------------------------------
(2) Let: u = 5*x
(3) du = (5)*dx
(4) dx = du/(5)
------------------------------------
(5) ∫(sin(u)*(1/5))*du
```
---

## AI and Technology Stack

### T5 Transformer Model:
Fine-tuned to understand mathematical expressions and generate optimal substitutions for integration.
Powered by the Hugging Face Transformers library.

### SymPy:
Handles symbolic mathematics and simplifies integrals based on the AI's suggestions.

### Flask:
Lightweight Python framework for creating the web application.

---

## Future Improvements
Address expression format restrictions by improving training data.
Add support for additional mathematical functions and operations.
Add support for various other integration methods
Enhance the UI for better accessibility and user experience.

---


## Work in Progress
This project is an active work in progress. While the core functionality is stable, improvements and enhancements are being actively developed to further expand its capabilities.


---


## Contributions

Contributions to this project are highly appreciated! If you’d like to improve the model or train your own version, follow the steps outlined in the accompanying Jupyter Notebook file:

1. **Extend the Training Data**:  
   - Explore the `data_generation` section of the notebook to create custom training data.
   - Consider adding more data generation functions to diversify and improve the dataset.

2. **Generate Training Data**:  
   - Once satisfied with your data generation functions, execute the `data_generation` section to create the training dataset.

3. **Install the Required Dependencies**:  
   - Ensure you have the correct version of the **Transformers** library as specified in the notebook to maintain compatibility.

4. **Train the Model**:  
   - Use the `train_model` section to fine-tune the T5 Transformer model with your training data.
   - Adjust the training settings (e.g., epochs, batch size, learning rate) as needed for optimal performance.
   - Upload the model to HuggingFace for ease of integration with the website

5. **Validate the Model**:  
   - Use the validation files and the `validate_model` section to evaluate your model’s performance.

6. **Test the Model Interactively**:  
   - Utilize the `user_input` section of the notebook to manually test the AI with real-world mathematical expressions and verify its output.

7. **Upload the Model to Hugging Face**:  
   - Once the model is trained, upload it to **Hugging Face Hub** for ease of integration with the website and broader accessibility.

Feel free to submit a pull request with your enhancements or reach out if you’d like to collaborate further. Your contributions can help improve the application and make it even more powerful!

