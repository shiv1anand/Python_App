import streamlit as st
import random
import string

def generate_password(length):
    """
    generate password:
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 special character
    """
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = '!#$%^&*()_+-=;:,.<>?'
    
    # ensuring every charector of required type is present
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(special)
    ]
    
    # adding rest ramdom charector
    all_chars = uppercase + lowercase + digits + special
    for i in range(length - 3):
        password.append(random.choice(all_chars))
    
    # Shufflingcharectors
    random.shuffle(password)
    
    return ''.join(password)

# Streamlit App
st.set_page_config(page_title="Password Generator", page_icon="🔐")

st.title("🔐 Password Generator")
st.write("Make secure and strong password")

# Password length input
length = st.slider(
    "Select password lenght:",
    min_value=6,
    max_value=32,
    value=12,
    step=1
)

st.write(f"Selected length: **{length} characters**")

# Generate button
if st.button("🔄 Generate Password", type="primary"):
    password = generate_password(length)
    st.session_state.password = password

# Display generated password
if 'password' in st.session_state:
    st.success("Password successfully generated!")
    
    # Password display with copy button
    st.code(st.session_state.password, language=None)
    
    # Info box
    st.info("""
    **Password contains:**
    - ✓ Uppercase letters (A-Z)
    - ✓ Lowercase letters (a-z)
    - ✓ Numbers (0-9)
    - ✓ Special characters (!#$%...)
    """)
    
