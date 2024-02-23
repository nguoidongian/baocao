import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
st.set_page_config(page_title='KHO VPIC1',layout="wide")
column1, column2 = st.columns(2)
# Function to save data to CSV file
def save_to_csv(data, filename):
    data.to_csv(filename, index=False)

# Function to plot bar chart from CSV data
def plot_bar_chart(data, y_column, selected_category, chart_title):
    filtered_data = data[data["Mã kho ERP"] == selected_category]
    fig = px.bar(filtered_data, x="Ngày gửi báo cáo", y=y_column, title=chart_title)
    st.plotly_chart(fig)

# Main function of the application
with column1:
    def main():
        st.title("Nhập Dữ liệu và Vẽ Biểu Đồ")

    # Sidebar options
        st.sidebar.header("Tùy chọn Người dùng")
        user_action = st.sidebar.radio("Chọn Hành động", ["Nhập Dữ liệu", "Xem Biểu Đồ"])

        if user_action == "Nhập Dữ liệu":
            input_data()
        elif user_action == "Xem Biểu Đồ":
            view_charts()

# Function to input data and save to CSV
    def input_data():
        st.header("Nhập Dữ liệu và Lưu vào File CSV")

    # Display input fields for Category, Value1, Value2, and Date
        category_input = st.text_input("Nhập Mã kho ERP:")
        value1_input = st.number_input("Nhập số mã fifo sai:", key="value1")
        value2_input = st.number_input("Nhập số phiếu chưa xác nhận:", key="value2")
        date_input = st.date_input("Chọn Ngày gửi báo cáo:", key="date")

    # Button to save data to CSV
        if st.button("Xác nhận"):
            if not category_input:
                st.warning("Vui lòng nhập Mã kho ERP.")
            else:
            # Read existing CSV file or create an empty DataFrame
                try:
                    data = pd.read_csv("data.csv")
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    data = pd.DataFrame(columns=["Mã kho ERP", "Số mã fifo sai", "Phiếu chưa xác nhận", "Ngày gửi báo cáo"])

            # Append new data to DataFrame
                new_data = pd.DataFrame({
                    "Mã kho ERP": [category_input],
                    "Số mã fifo sai": [value1_input],
                    "Phiếu chưa xác nhận": [value2_input],
                    "Ngày gửi báo cáo": [date_input.strftime("%Y-%m-%d")],  # Format date as string
                })
                data = pd.concat([data, new_data], ignore_index=True)

            # Save to CSV file
                save_to_csv(data, "data.csv")
                st.success("Dữ liệu đã được thêm và lưu vào file CSV.")

# Function to view bar charts from CSV data
def view_charts():
    st.header("Xem Biểu Đồ theo Ngày từ Dữ liệu CSV")

    # Read data from CSV file or display a message if the file is empty or not found
    try:
        data = pd.read_csv("data.csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.info("Không có dữ liệu nào để hiển thị. Vui lòng nhập dữ liệu trước.")

    # Display data
    st.subheader("Dữ liệu từ File CSV:")
    st.write(data)

    # Filter by "Mã kho ERP"
    selected_category = st.selectbox("Chọn Mã kho ERP:", data["Mã kho ERP"].unique())

    # Plot bar chart for "Số mã fifo sai"
    if not data.empty:
        plot_bar_chart(data, y_column="Số mã fifo sai", selected_category=selected_category,
                       chart_title=f"Biểu đồ Số mã fifo sai theo Ngày - Mã kho {selected_category}")

        # Plot bar chart for "Phiếu chưa xác nhận"
        plot_bar_chart(data, y_column="Phiếu chưa xác nhận", selected_category=selected_category,
                       chart_title=f"Biểu đồ Phiếu chưa xác nhận theo Ngày - Mã kho {selected_category}")

# Run the main function
if __name__ == "__main__":
    main()
