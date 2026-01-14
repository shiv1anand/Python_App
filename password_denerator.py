import streamlit as st
import random
import string

def generate_password(length):
    # Define character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    numbers = string.digits
    special = '!#$%^&*'
    
    # Make sure we have at least one of each required type
    password = []
    password.append(random.choice(uppercase))
    password.append(random.choice(lowercase))
    password.append(random.choice(special))
    
    # Fill the rest with random characters
    all_characters = uppercase + lowercase + numbers + special
    for i in range(length - 3):
        password.append(random.choice(all_characters))
    
    # Shuffle the password
    random.shuffle(password)
    
    # Convert list to string
    return ''.join(password)

# App title
st.title("Password Generator")

# Get password length from user
length = st.number_input("Enter password length:", min_value=6, max_value=20, value=12)

# Generate button
if st.button("Generate Password"):
    new_password = generate_password(length)
    st.text_area("Your Password:", new_password, height=100)
    st.write("Copy the password above!")