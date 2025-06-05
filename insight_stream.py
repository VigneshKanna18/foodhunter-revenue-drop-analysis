import streamlit as st
import MySQLdb
import pandas
def QnA():
    pass
def main():
    section = st.sidebar.selectbox(
        "select pages", ('Connection', 'Dashboard', 'QnA')
    )
    if section == 'Connection':
        st.markdown("""
        <style>
        .custom-title{
            font-size: 35px;
            color: gray;
            font-weight: bold;
        }
        </style>
       <div class = "custom-title"> Source Connection & Data Exploration </div>""", unsafe_allow_html=True)
        with st.sidebar.container(border=True):
            dbms = st.selectbox( "select dbms", ('MYSQL', 'PostgreSQL', 'MSSQLServer'))
            host = st.text_input('enter host : ')
            user = st.text_input('enter user : ')
            password = st.text_input('enter password : ', type = 'password')
        if dbms == 'MYSQL':
            try:
                conn =  MySQLdb.connect(host = host, user = user, password = password)
                st.sidebar.success("Connected successfully! Here are the databases:")
                cursor = conn.cursor()
                cursor.execute('SHOW DATABASES;')
                databases = [row[0] for row in cursor.fetchall()]
                database = st.sidebar.selectbox('select database', databases)
                cursor.execute(f'USE {database};')
                cursor.execute(f'SHOW TABLES;')
                tables = [row[0] for row in cursor.fetchall()]
                table = st.sidebar.selectbox('select table', tables)
                cursor.execute(f"SELECT * FROM `{database}`.`{table}`;")
                records = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                st.dataframe(pandas.DataFrame(records, columns= columns), height = 500, hide_index = True)
                cursor.close()
                conn.close()
            except MySQLdb.Error as err:
                st.sidebar.error(f"Failed to connect to MySQL: {err}")
                return
    if section == 'Dashboard':
       st.markdown("""
        <style>
        .custom-title{
            font-size: 35px;
            color: gray;
            font-weight: bold;
        }
        </style>
       <div class = "custom-title"> Foodhunter Dashboard </div>""", unsafe_allow_html=True)
    if section == "QnA":
        pass
if __name__ == '__main__':
    main()
