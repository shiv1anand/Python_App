import streamlit as st
import json
import os
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Contact Book",
    page_icon="📞",
    layout="wide"
)

# File to store contacts
CONTACTS_FILE = 'contacts.json'

# Load contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

# Initialize session state
if 'contacts' not in st.session_state:
    st.session_state.contacts = load_contacts()

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# Title
st.title("📞 Contact Book")
st.markdown("---")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📋 View Contacts", "➕ Add/Edit Contact", "🔍 Search Contact"])

# TAB 1: View All Contacts
with tab1:
    st.header("All Contacts")
    
    if len(st.session_state.contacts) == 0:
        st.info("No contacts found. Add your first contact!")
    else:
        # Display contacts in a table
        contact_data = []
        for i, contact in enumerate(st.session_state.contacts):
            contact_data.append({
                "S.No": i + 1,
                "Name": contact['name'],
                "Phone": contact['phone'],
                "Email": contact['email'],
                "Address": contact['address']
            })
        
        df = pd.DataFrame(contact_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("Manage Contacts")
        
        # Select contact to edit or delete
        contact_names = [f"{i+1}. {c['name']} - {c['phone']}" for i, c in enumerate(st.session_state.contacts)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_contact = st.selectbox("Select a contact:", [""] + contact_names, key="manage_contact")
        
        with col2:
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                if st.button("✏️ Edit", use_container_width=True, disabled=not selected_contact, key="edit_btn"):
                    if selected_contact:
                        index = contact_names.index(selected_contact)
                        st.session_state.edit_mode = True
                        st.session_state.edit_index = index
                        st.success(f"✏️ Now editing contact. Go to 'Add/Edit Contact' tab to make changes.")
                        st.rerun()
            
            with action_col2:
                if st.button("🗑️ Delete", use_container_width=True, type="primary", disabled=not selected_contact):
                    if selected_contact:
                        index = contact_names.index(selected_contact)
                        deleted_contact = st.session_state.contacts.pop(index)
                        save_contacts(st.session_state.contacts)
                        st.success(f"✅ Contact '{deleted_contact['name']}' deleted successfully!")
                        st.rerun()

# TAB 2: Add/Edit Contact
with tab2:
    if st.session_state.edit_mode:
        st.header("✏️ Edit Contact")
        contact_to_edit = st.session_state.contacts[st.session_state.edit_index]
        default_name = contact_to_edit['name']
        default_phone = contact_to_edit['phone']
        default_email = contact_to_edit['email']
        default_address = contact_to_edit['address']
    else:
        st.header("➕ Add New Contact")
        default_name = ""
        default_phone = ""
        default_email = ""
        default_address = ""
    
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Name *", value=default_name, placeholder="Enter full name")
        phone = st.text_input("Phone Number *", value=default_phone, placeholder="Enter phone number")
        email = st.text_input("Email", value=default_email, placeholder="Enter email address")
        address = st.text_area("Address", value=default_address, placeholder="Enter full address")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit = st.form_submit_button("💾 Save Contact", use_container_width=True, type="primary")
        
        with col2:
            if st.session_state.edit_mode:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                if cancel:
                    st.session_state.edit_mode = False
                    st.session_state.edit_index = None
                    st.rerun()
        
        if submit:
            if not name or not phone:
                st.error("⚠️ Name and Phone Number are required fields!")
            else:
                contact = {
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "address": address.strip()
                }
                
                if st.session_state.edit_mode:
                    st.session_state.contacts[st.session_state.edit_index] = contact
                    save_contacts(st.session_state.contacts)
                    st.success(f"✅ Contact '{name}' updated successfully!")
                    st.session_state.edit_mode = False
                    st.session_state.edit_index = None
                else:
                    st.session_state.contacts.append(contact)
                    save_contacts(st.session_state.contacts)
                    st.success(f"✅ Contact '{name}' added successfully!")
                
                st.rerun()

# TAB 3: Search Contact
with tab3:
    st.header("🔍 Search Contacts")
    
    search_term = st.text_input("Search by Name or Phone Number", placeholder="Type to search...")
    
    if search_term:
        search_results = []
        for contact in st.session_state.contacts:
            if (search_term.lower() in contact['name'].lower() or 
                search_term in contact['phone']):
                search_results.append(contact)
        
        if search_results:
            st.success(f"Found {len(search_results)} contact(s)")
            
            for i, contact in enumerate(search_results):
                with st.container():
                    st.markdown(f"### {i+1}. {contact['name']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**📱 Phone:** {contact['phone']}")
                        st.write(f"**✉️ Email:** {contact['email'] or 'N/A'}")
                    with col2:
                        st.write(f"**🏠 Address:** {contact['address'] or 'N/A'}")
                    st.markdown("---")
        else:
            st.warning("No contacts found matching your search.")
    else:
        st.info("Enter a name or phone number to search.")

# Sidebar - Statistics
with st.sidebar:
    st.header("📊 Statistics")
    st.metric("Total Contacts", len(st.session_state.contacts))
    
    if st.session_state.contacts:
        contacts_with_email = sum(1 for c in st.session_state.contacts if c['email'])
        contacts_with_address = sum(1 for c in st.session_state.contacts if c['address'])
        
        st.metric("With Email", contacts_with_email)
        st.metric("With Address", contacts_with_address)
    
    st.markdown("---")
    st.info("💡 **Tip:** Use the tabs above to view, add, or search contacts!")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.contacts = load_contacts()
        st.rerun()
