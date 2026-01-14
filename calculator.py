import streamlit as st
st.set_page_config(page_title="Calculator", page_icon="🔢")
st.title("🔢 Simple Calculator")
st.write("Perform basic arithmetic operations")

# Create two columns for number inputs
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("Enter first number:", value=0.0, format="%.2f")

with col2:
    num2 = st.number_input("Enter second number:", value=0.0, format="%.2f")

# Operation selection
operation = st.selectbox(
    "Select operation:",
    ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]
)

# Calculate button
if st.button("Calculate", type="primary"):
    result = None
    error = None
    
    if operation == "Addition (+)":
        result = num1 + num2
        operation_symbol = "+"
    elif operation == "Subtraction (-)":
        result = num1 - num2
        operation_symbol = "-"
    elif operation == "Multiplication (×)":
        result = num1 * num2
        operation_symbol = "×"
    elif operation == "Division (÷)":
        if num2 == 0:
            error = "Error: Division by zero is not allowed!"
        else:
            result = num1 / num2
            operation_symbol = "÷"
    
    # Display result
    if error:
        st.error(error)
    else:
        st.success(f"**Result:** {num1} {operation_symbol} {num2} = **{result:.2f}**")
        

# Instructions
with st.expander("ℹ️ How to use"):
    st.write("""
    1. Enter the first number
    2. Enter the second number
    3. Select the operation you want to perform
    4. Click the 'Calculate' button to see the result
    
    **Supported Operations:**
    - Addition: Adds two numbers
    - Subtraction: Subtracts the second number from the first
    - Multiplication: Multiplies two numbers
    - Division: Divides the first number by the second (cannot divide by zero)
    """)