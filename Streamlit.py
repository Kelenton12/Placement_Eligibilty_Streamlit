import streamlit as st
import pandas as pd
import mysql.connector
from io import BytesIO

# --- MySQL Configuration ---
config = {
    'host': 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
    'port': 4000,
    'user': 'ZyFH9eafC8zpw21.root',
    'password': 'nlNXl13dHcuL7tgs',
    'database': 'Student_Info1',
    'ssl_disabled': False,
    'ssl_ca': 'C:/Users/jamuna/Downloads/isrgrootx1(1).pem'
}

# --- Connect to MySQL ---
db = mysql.connector.connect(**config)
cursor = db.cursor()

# --- Streamlit UI ---
st.title("Placement Eligibility App")

# Fetch student list
cursor.execute("SELECT student_id, name FROM Student_table")
students = cursor.fetchall()
options = {f"{sid}. {name}": sid for sid, name in students}

sel = st.selectbox("Select student:", ["-- select --"] + list(options.keys()))
export_data = {}

if sel != "-- select --":
    sid = options[sel]

    # --- Student Info ---
    cursor.execute("SELECT * FROM Student_table WHERE student_id=%s", (sid,))
    student_row = cursor.fetchone()
    student_cols = [d[0] for d in cursor.description]
    student_df = pd.DataFrame([student_row], columns=student_cols)
    st.subheader("Student Details")
    st.dataframe(student_df)
    export_data["Student Info"] = student_df

    # --- Programming Skills ---
    cursor.execute("SELECT * FROM Programming_table WHERE student_id=%s", (sid,))
    prog_row = cursor.fetchone()
    prog_cols = [d[0] for d in cursor.description]
    prog_df = pd.DataFrame([prog_row], columns=prog_cols)
    st.subheader("Programming Skills")
    st.dataframe(prog_df)
    export_data["Programming Skills"] = prog_df

    # --- Soft Skills ---
    cursor.execute("SELECT * FROM Soft_skills WHERE student_id=%s", (sid,))
    soft_row = cursor.fetchone()
    soft_cols = [d[0] for d in cursor.description]
    soft_df = pd.DataFrame([soft_row], columns=soft_cols)
    st.subheader("Soft Skills")
    st.dataframe(soft_df)
    export_data["Soft Skills"] = soft_df

    # --- Placement Info ---
    cursor.execute("SELECT * FROM Placement_table WHERE student_id=%s", (sid,))
    place_row = cursor.fetchone()
    place_cols = [d[0] for d in cursor.description]
    place_df = pd.DataFrame([place_row], columns=place_cols)
    st.subheader("Placement Info")
    st.dataframe(place_df)
    export_data["Placement Info"] = place_df

    # --- Eligibility Check ---
    placement_status = place_df["placement_status"].iloc[0]
    if placement_status == "Placed":
        st.success(
            f"Eligible\n\n"
            f"Company: {place_df['company_name'].iloc[0]}\n"
            f"Package: ₹{place_df['placement_package'].iloc[0]} LPA\n"
            f"Date: {place_df['placement_date'].iloc[0]}"
        )
    elif placement_status == "Not Placed":
        st.error(" Not Eligible")
    else:
        st.warning("Placement status not specified")

    # --- Excel Export ---
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in export_data.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    output.seek(0)

    st.download_button(
        label="Download Student Details as Excel",
        data=output,
        file_name=f"{student_df['name'].iloc[0].replace(' ', '_')}_Placement_Info.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Close connection ---
cursor.close()
db.close()