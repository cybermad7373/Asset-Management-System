import streamlit as st
from datetime import datetime
from assets.main.main_module import MainModule
from assets.entity.asset import Asset
from assets.entity.employee import Employee

# Initialize the main application
main_app = MainModule()

# Custom CSS for better styling
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .stButton button {
        width: 100%;
    }
    .stDataFrame {
        width: 100%;
    }
    .success-message {
        color: green;
        font-weight: bold;
    }
    .error-message {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def login_page():
    st.title(" Digital Asset Management System")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("assets/images/logo.png", width=300)

    with col2:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="user@company.com")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Login"):
                try:
                    user = main_app.service.login(email, password)
                    if user:
                        st.session_state.current_user = user
                        st.session_state.is_admin = user.get_is_admin()
                        st.session_state.employee_id = user.get_employee_id()
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")

def admin_dashboard():
    st.title(f" Admin Dashboard")
    st.sidebar.header(f"Welcome {st.session_state.current_user.get_name()}")

    menu = st.sidebar.radio("Menu", ["Assets", "Employees", "Reports"])

    if menu == "Assets":
        st.header(" Asset Management")
        action = st.selectbox("Action", ["View All", "Add Asset", "Update Asset", "Delete Asset", "Allocate Asset", "Deallocate Asset", "Perform Maintenance"])

        if action == "View All":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM assets")
            st.dataframe(cursor.fetchall())

        elif action == "Add Asset":
            with st.form("add_asset_form"):
                st.write("### Add New Asset")
                name = st.text_input("Asset Name")
                asset_type = st.selectbox("Type", ["Laptop", "Camera", "Vehicle", "Equipment"])
                serial_number = st.text_input("Serial Number")
                purchase_date = st.date_input("Purchase Date")
                location = st.text_input("Location")
                status = st.selectbox("Status", ["in_use", "decommissioned", "under_maintenance"])
                owner_id = st.number_input("Owner ID (optional)", min_value=0, step=1, format="%d")

                if st.form_submit_button("Add Asset"):
                    asset = Asset(
                        name=name,
                        type=asset_type,
                        serial_number=serial_number,
                        purchase_date=purchase_date.strftime("%Y-%m-%d"),
                        location=location,
                        status=status,
                        owner_id=owner_id if owner_id > 0 else None
                    )
                    if main_app.service.add_asset(asset):
                        st.success("Asset added successfully!")
                    else:
                        st.error("Failed to add asset")

        elif action == "Update Asset":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("SELECT asset_id, name FROM assets")
            assets = cursor.fetchall()
            asset_options = {f"{a['asset_id']} - {a['name']}": a['asset_id'] for a in assets}
            selected_asset = st.selectbox("Select Asset to Update", options=list(asset_options.keys()))

            if selected_asset:
                asset_id = asset_options[selected_asset]
                asset = main_app.service.get_asset(asset_id)

                if asset:
                    with st.form("update_asset_form"):
                        st.write("### Update Asset")
                        name = st.text_input("Name", value=asset.get_name())
                        asset_type = st.text_input("Type", value=asset.get_type())
                        serial_number = st.text_input("Serial Number", value=asset.get_serial_number())
                        purchase_date = st.text_input("Purchase Date", value=asset.get_purchase_date())
                        location = st.text_input("Location", value=asset.get_location())
                        status = st.text_input("Status", value=asset.get_status())
                        owner_id = st.text_input("Owner ID", value=str(asset.get_owner_id()) if asset.get_owner_id() else "")

                        if st.form_submit_button("Update Asset"):
                            updated_asset = Asset(
                                asset_id=asset_id,
                                name=name,
                                type=asset_type,
                                serial_number=serial_number,
                                purchase_date=purchase_date,
                                location=location,
                                status=status,
                                owner_id=int(owner_id) if owner_id else None
                            )
                            if main_app.service.update_asset(updated_asset):
                                st.success("Asset updated successfully!")
                            else:
                                st.error("Failed to update asset")

        elif action == "Delete Asset":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("SELECT asset_id, name FROM assets")
            assets = cursor.fetchall()
            asset_options = {f"{a['asset_id']} - {a['name']}": a['asset_id'] for a in assets}
            selected_asset = st.selectbox("Select Asset to Delete", options=list(asset_options.keys()))

            if selected_asset and st.button("Delete Asset"):
                asset_id = asset_options[selected_asset]
                if main_app.service.delete_asset(asset_id):
                    st.success("Asset deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete asset")

        elif action == "Allocate Asset":
            with st.form("allocate_asset_form"):
                st.write("### Allocate Asset")
                asset_id = st.number_input("Asset ID", min_value=1, step=1)
                employee_id = st.number_input("Employee ID", min_value=1, step=1)
                allocation_date = st.date_input("Allocation Date")

                if st.form_submit_button("Allocate"):
                    if main_app.service.allocate_asset(asset_id, employee_id, allocation_date.strftime("%Y-%m-%d")):
                        st.success("Asset allocated successfully!")
                    else:
                        st.error("Failed to allocate asset")

        elif action == "Deallocate Asset":
            with st.form("deallocate_asset_form"):
                st.write("### Deallocate Asset")
                asset_id = st.number_input("Asset ID", min_value=1, step=1)
                employee_id = st.number_input("Employee ID", min_value=1, step=1)
                return_date = st.date_input("Return Date")

                if st.form_submit_button("Deallocate"):
                    if main_app.service.deallocate_asset(asset_id, employee_id, return_date.strftime("%Y-%m-%d")):
                        st.success("Asset deallocated successfully!")
                    else:
                        st.error("Failed to deallocate asset")

        elif action == "Perform Maintenance":
            with st.form("maintenance_form"):
                st.write("### Perform Maintenance")
                asset_id = st.number_input("Asset ID", min_value=1, step=1)
                maintenance_date = st.date_input("Maintenance Date")
                description = st.text_area("Description")
                cost = st.number_input("Cost", min_value=0.0, format="%.2f")

                if st.form_submit_button("Record Maintenance"):
                    if main_app.service.perform_maintenance(
                            asset_id,
                            maintenance_date.strftime("%Y-%m-%d"),
                            description,
                            cost
                    ):
                        st.success("Maintenance recorded successfully!")
                    else:
                        st.error("Failed to record maintenance")

    elif menu == "Employees":
        st.header("👥 Employee Management")
        action = st.selectbox("Action", ["View All", "Add Employee", "Update Employee"])

        if action == "View All":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees")
            st.dataframe(cursor.fetchall())

        elif action == "Add Employee":
            with st.form("add_employee_form"):
                st.write("### Add New Employee")
                name = st.text_input("Name")
                department = st.text_input("Department")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                is_admin = st.checkbox("Is Admin")

                if st.form_submit_button("Add Employee"):
                    employee = Employee(
                        name=name,
                        department=department,
                        email=email,
                        password=password,
                        is_admin=is_admin
                    )
                    if main_app.service.add_employee(employee, st.session_state.current_user):
                        st.success("Employee added successfully!")
                    else:
                        st.error("Failed to add employee")

        elif action == "Update Employee":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("SELECT employee_id, name FROM employees")
            employees = cursor.fetchall()
            employee_options = {f"{e['employee_id']} - {e['name']}": e['employee_id'] for e in employees}
            selected_employee = st.selectbox("Select Employee to Update", options=list(employee_options.keys()))

            if selected_employee:
                employee_id = employee_options[selected_employee]
                employee = main_app.service.get_employee(employee_id)

                if employee:
                    with st.form("update_employee_form"):
                        st.write("### Update Employee")
                        name = st.text_input("Name", value=employee.get_name())
                        department = st.text_input("Department", value=employee.get_department())
                        email = st.text_input("Email", value=employee.get_email())
                        new_password = st.text_input("New Password (leave blank to keep current)", type="password")

                        if st.form_submit_button("Update Employee"):
                            updated_employee = Employee(
                                employee_id=employee_id,
                                name=name,
                                department=department,
                                email=email,
                                password=new_password if new_password else None,
                                is_admin=employee.get_is_admin()
                            )
                            if main_app.service.update_employee(updated_employee, st.session_state.current_user):
                                st.success("Employee updated successfully!")
                            else:
                                st.error("Failed to update employee")

    elif menu == "Reports":
        st.header("📊 Reports")
        report_type = st.selectbox("Report Type", ["Asset Status", "Maintenance History", "Allocation History"])

        if report_type == "Asset Status":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.asset_id, a.name, a.type, a.status, 
                       e.name AS owner_name, e.department AS owner_department
                FROM assets a
                LEFT JOIN employees e ON a.owner_id = e.employee_id
                ORDER BY a.status, a.type
            """)
            st.dataframe(cursor.fetchall())

        elif report_type == "Maintenance History":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.maintenance_id, a.name AS asset_name, 
                       m.maintenance_date, m.description, m.cost
                FROM maintenance_records m
                JOIN assets a ON m.asset_id = a.asset_id
                ORDER BY m.maintenance_date DESC
            """)
            st.dataframe(cursor.fetchall())

        elif report_type == "Allocation History":
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT aa.allocation_id, a.name AS asset_name, 
                       e.name AS employee_name, aa.allocation_date, aa.return_date
                FROM asset_allocations aa
                JOIN assets a ON aa.asset_id = a.asset_id
                JOIN employees e ON aa.employee_id = e.employee_id
                ORDER BY aa.allocation_date DESC
            """)
            st.dataframe(cursor.fetchall())

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

def employee_dashboard():
    st.title(f"👤 Employee Portal - {st.session_state.current_user.get_name()}")
    st.sidebar.header(f"Welcome {st.session_state.current_user.get_name()}")

    tab1, tab2, tab3, tab4 = st.tabs(["My Assets", "Request Asset", "Maintenance", "My Profile"])

    with tab1:
        st.header("📋 My Assigned Assets")
        try:
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.* FROM assets a
                JOIN asset_allocations aa ON a.asset_id = aa.asset_id
                WHERE aa.employee_id = %s AND aa.return_date IS NULL
            """, (st.session_state.employee_id,))

            assets = cursor.fetchall()
            if assets:
                st.dataframe(assets)

                # Return asset functionality
                asset_options = {f"{a['asset_id']} - {a['name']}": a['asset_id'] for a in assets}
                selected_asset = st.selectbox("Select Asset to Return", options=list(asset_options.keys()))

                if st.button("Return Asset"):
                    asset_id = asset_options[selected_asset]
                    if main_app.service.deallocate_asset(
                            asset_id,
                            st.session_state.employee_id,
                            datetime.now().strftime("%Y-%m-%d")
                    ):
                        st.success("Asset returned successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to return asset")
            else:
                st.info("No assets currently assigned to you")

        except Exception as e:
            st.error(f"Error: {str(e)}")

    with tab2:
        st.header("🔄 Request New Asset")
        with st.form("request_asset_form"):
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.asset_id, a.name 
                FROM assets a
                WHERE a.status = 'in_use' 
                AND a.asset_id NOT IN (
                    SELECT asset_id FROM asset_allocations 
                    WHERE return_date IS NULL
                )
            """)
            available_assets = cursor.fetchall()

            if available_assets:
                asset_options = {f"{a['asset_id']} - {a['name']}": a['asset_id'] for a in available_assets}
                selected_asset = st.selectbox("Available Assets", options=list(asset_options.keys()))
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")

                if st.form_submit_button("Submit Request"):
                    asset_id = asset_options[selected_asset]
                    if main_app.service.reserve_asset(
                            asset_id,
                            st.session_state.employee_id,
                            datetime.now().strftime("%Y-%m-%d"),
                            start_date.strftime("%Y-%m-%d"),
                            end_date.strftime("%Y-%m-%d")
                    ):
                        st.success("Asset request submitted successfully!")
                    else:
                        st.error("Failed to submit asset request")
            else:
                st.info("No assets currently available for request")

    with tab3:
        st.header("🛠️ Request Maintenance")
        with st.form("maintenance_request_form"):
            cursor = main_app.service.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.* FROM assets a
                JOIN asset_allocations aa ON a.asset_id = aa.asset_id
                WHERE aa.employee_id = %s AND aa.return_date IS NULL
            """, (st.session_state.employee_id,))
            my_assets = cursor.fetchall()

            if my_assets:
                asset_options = {f"{a['asset_id']} - {a['name']}": a['asset_id'] for a in my_assets}
                selected_asset = st.selectbox("Select Asset", options=list(asset_options.keys()))
                issue = st.text_area("Describe the issue")

                if st.form_submit_button("Submit Request"):
                    asset_id = asset_options[selected_asset]
                    if main_app.service.perform_maintenance(
                            asset_id,
                            datetime.now().strftime("%Y-%m-%d"),
                            issue,
                            0.0  # Cost will be set by admin
                    ):
                        st.success("Maintenance request submitted successfully!")
                    else:
                        st.error("Failed to submit maintenance request")
            else:
                st.info("You don't have any assets to request maintenance for")

    with tab4:
        st.header("👤 My Profile")
        employee = st.session_state.current_user

        with st.form("update_profile_form"):
            st.write("### Update Your Profile")
            name = st.text_input("Name", value=employee.get_name())
            department = st.text_input("Department", value=employee.get_department())
            email = st.text_input("Email", value=employee.get_email())
            new_password = st.text_input("New Password (leave blank to keep current)", type="password")

            if st.form_submit_button("Update Profile"):
                updated_employee = Employee(
                    employee_id=employee.get_employee_id(),
                    name=name,
                    department=department,
                    email=email,
                    password=new_password if new_password else None,
                    is_admin=employee.get_is_admin()
                )
                if main_app.service.update_employee(updated_employee, st.session_state.current_user):
                    st.success("Profile updated successfully!")
                    # Refresh the current user in session
                    st.session_state.current_user = main_app.service.get_employee(employee.get_employee_id())
                else:
                    st.error("Failed to update profile")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

def main():
    st.set_page_config(
        page_title="Asset Management System",
        page_icon="📋",
        layout="wide"
    )

    if "current_user" not in st.session_state:
        login_page()
    else:
        if st.session_state.get("is_admin", False):
            admin_dashboard()
        else:
            employee_dashboard()

if __name__ == "__main__":
    main()