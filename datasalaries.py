import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px # interactive charts 
from wordcloud import WordCloud

# Navbar
from streamlit_option_menu import option_menu

# ISO 3166
import pycountry
import country_converter as coco

st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_title="Visualisasi Data ",
    page_icon=":📊:",)

# Membaca datasets
df = pd.read_csv('ds_salaries.csv')
df['work_year'] = df['work_year'].astype(str)

# convert country code iso 3166 to country name
# company location
def convert_country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except LookupError:
        return "Unknown"

# Menerapkan fungsi konversi pada kolom "company_location"
df["country_company"] = df["company_location"].apply(convert_country_code_to_name)
# Menampilkan df yang telah dikonversi
print(df)


# employee residence
def convert_country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except LookupError:
        return "Unknown"

# Menerapkan fungsi konversi pada kolom "employee_residence"
df["country_employee"] = df["employee_residence"].apply(convert_country_code_to_name)

# Menampilkan df yang telah dikonversi
print(df)

# side bar
st.sidebar.image('UINSA.png', caption="Final Project Data Visualization")

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
year = st.sidebar.multiselect(
    "Select the Year:",
    options=df["work_year"].unique(),
    default=df["work_year"].unique()
)

df_selection = df.query(
    "work_year == @year"
)
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the Location:",
    options=df["country_company"].unique(),
    default=df["country_company"].unique()
)

# MEDIA QUERY UNTUK SELEKSI FILTER
df_location = df.query(
    "country_company == @country & work_year == @year"
)

st.markdown("# Data Science Salaries")
# Sub Judul
st.markdown("Explore the dataset to know more about Data Science Salaries")

selected = option_menu(
    menu_title=None,  # required
    options=["EDA", "Visualizations", "Comparatives", "Proportions", "Maps"],  # required
    icons=["clipboard-data", "bar-chart", "speedometer2", "pie-chart", "globe-asia-australia"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)

if selected == "EDA": 
    st.markdown("## Exploratory Data Analysis")
    # Dataframe
    st.markdown("### Detailed Data View")
    st.dataframe(df_selection)
    # time.sleep(1)
    # # STATISTIC DESCRIPTIVE
    st.subheader('Statistic Descriptive')
    st.write(df_selection.describe())
    # CHECK NULL VALUE
    st.subheader('Checkin Null Value')
    st.write(df.isnull().sum())

if selected == "Visualizations":
    st.markdown("## Data Processing and Visualization")
    st.subheader("Metric")

    jobs = len(df_selection['job_title'].unique())
    employeeres = len(df_selection['employee_residence'].unique())
    companyloc = len(df_selection['company_location'].unique())

    col1, col2, col3 = st.columns(3)
    col1.metric("Job Totals", f"{str(jobs)} Jobs", "Totals")
    col2.metric("Employee Residence", f"{str(employeeres)} Country", "Totals")
    col3.metric("Company Location", f"{str(companyloc)} Country", "-Totals")
   

    st.markdown("### Trend Job ")

    default_job="Data Analyst", "Data Engineer", "Data Scientist", "Machine Learning Engineer", "Analytics Engineer"
  
    job = st.multiselect(
        "Select the Job:",
        options=df["job_title"].unique(),
        default=default_job
    )

    # MEDIA QUERY UNTUK SELEKSI FILTER
    df_trend = df.query(
        "job_title == @job & country_company == @country"
    )
    
    job_count = df_trend.groupby(['work_year', 'job_title']).size().reset_index(name='count')

    # Menampilkan line chart pekerjaan per tahun kerja
    fig = px.line(job_count, x='work_year', 
                  y='count', 
                  color='job_title',
                  title='Pekerjaan per Tahun Kerja', 
                  labels={'work_year': 'Year', 'count': 'Frequency'})
    
    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top 7 Jobs with Most Employees ")
    top_5 = df_location['job_title'].value_counts().nlargest(15).reset_index()
    fig2 = px.bar(data_frame=top_5, y='index', x='job_title', orientation='h', title='Chart of Top 7 Job Titles', color = top_5['job_title'], color_continuous_scale='Sunset')

    fig2.update_layout(
        yaxis={'title': 'Job Titles'},
        yaxis_autorange='reversed',
        xaxis={'title': 'Employees'},
        height=600
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Top 7 Jobs with Average Salaries ")

    top_salary = df_location.groupby('job_title').agg({'salary_in_usd':'mean'}).sort_values(by='salary_in_usd', ascending=False).head(15)
    st.write(top_salary.head(7))


    fig = px.bar(data_frame=top_salary, x='salary_in_usd', y=top_salary.index, orientation='h',title='Top 7 Jobs with Average Salaries', color = 'salary_in_usd', color_continuous_scale='Sunsetdark')
    fig.update_layout(
        xaxis={'title': 'Job Titles'},
        yaxis={'title': 'Average Salaries'},
        yaxis_autorange='reversed',
        height=600
        )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Average Salary Based On Experience Level ")

    df_location['experience_level'].replace(['SE','MI','EN','EX'],["Senior-level / Expert","Mid-level / Intermediate","Entry-level / Junior","Executive-level / Director"],inplace=True)

    avg_salary = df_location.groupby('experience_level').agg({'salary_in_usd':'mean'}).sort_values(by='salary_in_usd', ascending=False).head(5)
    st.write(avg_salary.head(5))

    fig = px.bar(data_frame=avg_salary, x=avg_salary.index, y='salary_in_usd',title='Chart of Average Salary Based on Experience Level', color = 'salary_in_usd', color_continuous_scale='Magenta')
    fig.update_layout(
        # xaxis_tickangle=-45
        xaxis={'title': 'Experience Level'},
        yaxis={'title': 'Average Salaries'}, 
        height=600
        )
    st.plotly_chart(fig, use_container_width=True)

    # Word cloud
    st.markdown("# Word Cloud")
    # Preprocessing teks
    text = df_location['job_title'].values
    text = ' '.join(text)

    # Sidebar untuk mengatur parameter WordCloud
    st.sidebar.title("WordCloud Options")
    max_words = st.sidebar.slider("Max Words", min_value=100, max_value=2000, value=1000)
    background_color = st.sidebar.selectbox("Background Color", ["black", "white"])
    collocations = st.sidebar.checkbox("Include Collocations", value=False)

    # Membuat WordCloud
    wc = WordCloud(background_color=background_color, width=1200, height=600,
                contour_width=0, contour_color="#410F01", max_words=max_words,
                scale=1, collocations=collocations, repeat=True, min_font_size=1)

    
    # Mengenerate dan menampilkan WordCloud saat ada perubahan pada parameter
    def generate_wordcloud():
        wc.generate(text)
        plt.figure(figsize=[12, 6])
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        return plt

    # Menampilkan WordCloud dalam aplikasi Streamlit
    st.markdown("### Top Words in the Text")
    st.pyplot(generate_wordcloud())

if selected == "Comparatives":
    
    # Perbandingan rata rata gaji berdasar lokasi perusahaan
    st.markdown("### Comparison of Average Salaries Between Jobs at Each Company Location")

    # Mengatur tata letak halaman Streamlit
    col1, col2 = st.columns(2)

    with col1:
        filter1 = st.selectbox("Select Location 1", pd.unique(df['country_company']))

        filtered1 = df[df['country_company'] == filter1]
        avg_salary = filtered1.groupby('job_title').agg({'salary_in_usd': 'mean'}).sort_values(by='salary_in_usd', ascending=False)
        st.write(avg_salary)

    with col2:
        filter2 = st.selectbox("Select Location 2", pd.unique(df['country_company']))

        filtered2 = df[df['country_company'] == filter2]
        avg_salary = filtered2.groupby('job_title').agg({'salary_in_usd': 'mean'}).sort_values(by='salary_in_usd', ascending=False)
        st.write(avg_salary)

    avg_salary = filtered1.groupby('job_title').agg({'salary_in_usd': 'mean'}).sort_values(by='salary_in_usd', ascending=False)
    fig1 = px.bar(data_frame=avg_salary, x='salary_in_usd', y=avg_salary.index,
            title='Location 1', color='salary_in_usd',
            color_continuous_scale='Bluyl')
    fig1.update_layout(xaxis={'title': 'Job Titles'}, yaxis={'title': 'Average Salaries'}, height=600, width=750, yaxis_autorange='reversed')
    st.plotly_chart(fig1, use_container_width=True)

    avg_salary = filtered2.groupby('job_title').agg({'salary_in_usd': 'mean'}).sort_values(by='salary_in_usd', ascending=False)
    fig2 = px.bar(data_frame=avg_salary, x='salary_in_usd', y=avg_salary.index,
            title='Location 2', color='salary_in_usd',
            color_continuous_scale='Sunsetdark')
    fig2.update_layout(xaxis={'title': 'Job Titles'}, yaxis={'title': 'Average Salaries'}, height=600, width=750, yaxis_autorange='reversed')
    st.plotly_chart(fig2, use_container_width=True)


# Proporsi
if selected == "Proportions":

    # Membuat diagram pie dengan Streamlit
    # Proporsi experience level
    st.title('Proportion')

    st.markdown("## Proportion of Experience Level")

    col1, col2 = st.columns(2)
    with col1:
        df_location['experience_level'].replace(['SE','MI','EN','EX'],["Senior-level / Expert","Mid-level / Intermediate","Entry-level / Junior","Executive-level / Director"],inplace=True)
        experience_counts = df_location['experience_level'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_location['experience_level'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='experience_level', title='Frequency of Experience Level', text=experience_counts.values,
                        color='experience_level', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'Experience Level'}, yaxis={'title': 'Frequency'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=experience_counts.index, values=experience_counts.values,
                        title='Proportion of Experience Level')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Proporsi employment type 
    st.markdown("## Proportion of Employment Type") 
    col1, col2 = st.columns(2)
    with col1:

        df_location['employment_type'].replace(['FT','PT','CT','FL'],["Full Time","Part Time","Contract","Freelance"],inplace=True)

        employment_counts = df_location['employment_type'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_location['employment_type'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='employment_type', title='Frequency of Employment Type', text=employment_counts.values,
                        color='employment_type', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'employment_type'}, yaxis={'title': 'Frequency'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=employment_counts.index, values=employment_counts.values,
                        title='Proportion of Employment Type')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Proporsi Remote ratio  
    st.markdown("## Proportion of Remote Ratio")
    col1, col2 = st.columns(2)
    with col1:

        df_location['remote_ratio'].replace([100, 50, 0],["WFH","Hybrid","WFO"],inplace=True)

        ratio = df_location['remote_ratio'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_location['remote_ratio'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='remote_ratio', title='Frequency of Remote Ratio', text=ratio.values,
                        color='remote_ratio', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'remote_ratio'}, yaxis={'title': 'Frequency'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=ratio.index, values=ratio.values,
                        title='Proportion of Remote Ratio')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Proporsi Company Size  
    st.markdown("## Proportion of Company Size")
    col1, col2 = st.columns(2)
    with col1:

        df_location['company_size'].replace(["S", "M", "L"],["Small","Medium","Large"],inplace=True)

        ratio = df_location['company_size'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_location['company_size'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='company_size', title='Frequency of Company Size', text=ratio.values,
                        color='company_size', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'company_size'}, yaxis={'title': 'Frequency'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=ratio.index, values=ratio.values,
                        title='Proportion of Company Size')
        
        st.plotly_chart(fig_pie, use_container_width=True)

    # Proporsi YEAR 
    st.markdown("## Proportion of Year")
    df_loc = df.query(
    "country_company == @country")
    col1, col2 = st.columns(2)
    with col1:

        ratio = df_loc['work_year'].value_counts()
        
        # st.markdown("Frequency of Experience Level")
        top_5 = df_loc['work_year'].value_counts().reset_index().head(5)
        fig_bar = px.bar(data_frame=top_5, x='index', y='work_year', title='Frequency of Year', text=ratio.values,
                        color='work_year', color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_bar.update_layout(xaxis={'title': 'work_year'}, yaxis={'title': 'Frequency'})

        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # st.markdown("Proportion of Experience Level")
        fig_pie = px.pie(names=ratio.index, values=ratio.values,
                        title='Proportion of Year')
        
        st.plotly_chart(fig_pie, use_container_width=True)



if selected == "Maps":
    st.markdown("## Distribution Map")
    st.markdown("### Employee Location Distribution Map")
    if st.checkbox('Show Map Employee'):

        # Convert kode negara ke ISO3166
        converted_country = coco.convert(names=df_selection['employee_residence'], to="ISO3")

        df_selection['employee_residence'] = converted_country
        employee = df_selection['employee_residence'].value_counts()
        
        fig = px.choropleth(locations=employee.index,
                            color=employee.values,
                            color_continuous_scale=px.colors.sequential.solar,
                            template='plotly_dark')

        fig.update_layout(font = dict(size= 14, family="Franklin Gothic"), height=600, width=900)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Company Location Distribution Map")
    if st.checkbox('Show Map Company'): 

        # Convert kode negara ke ISO3166
        converted_country = coco.convert(names=df_selection['company_location'], to="ISO3")

        df_selection['company_location'] = converted_country
        company = df_selection['company_location'].value_counts()
        
        fig = px.choropleth(locations=company.index,
                            color=company.values,
                            color_continuous_scale=px.colors.sequential.PuRd,
                            template='plotly_dark')
        

        fig.update_layout(font = dict(size= 14, family="Franklin Gothic"), height=600, width=900)
        st.plotly_chart(fig, use_container_width=True)


        st.markdown("#### Company Size Location Distribution Map")

        # Convert kode negara
        converted_country = coco.convert(names=df_selection['company_location'], to="ISO3")

        df_selection['company_location'] = converted_country

        # replace kolom
        df_selection['company_size'].replace(["S", "M", "L"],["Small","Medium","Large"],inplace=True)
        
        # grup 
        exlevel_location = df_selection.groupby(['company_size','company_location']).size()

        small_location = exlevel_location['Small']
        medium_location = exlevel_location['Medium']
        large_location = exlevel_location['Large']

        if st.checkbox('Show Map Small Company Size'):

            fig1 = px.choropleth(locations=small_location.index,
                                color=small_location.values,
                                color_continuous_scale=px.colors.sequential.Peach,
                                template='plotly_dark',
                                title = 'Small Company Size Location')
            
            fig1.update_layout(font = dict(size = 17, family="Franklin Gothic"))

            st.plotly_chart(fig1, use_container_width=True)

        if st.checkbox('Show Map Medium Company Size'):

            fig2 = px.choropleth(locations=medium_location.index,
                                color=medium_location.values,
                                color_continuous_scale=px.colors.sequential.dense,
                                template='plotly_dark',
                                title = 'Medium Company Size Location')
            
            fig2.update_layout(font = dict(size = 17, family="Franklin Gothic"))
            st.plotly_chart(fig2, use_container_width=True)

        if st.checkbox('Show Map Large Company Size'):
    
            fig3 = px.choropleth(locations=large_location.index,
                                color=large_location.values,
                                color_continuous_scale=px.colors.sequential.GnBu,
                                template='plotly_dark',
                                title = 'Large Company Size Location')
            
            fig3.update_layout(font = dict(size = 17, family="Franklin Gothic"))
            st.plotly_chart(fig3, use_container_width=True)

# Menambah info pada side bar
st.sidebar.markdown("[Data Source](https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023)")
st.sidebar.info("Code by [Izzi](https://www.linkedin.com/in/ahmadkemalalizzi/) &  [Izza](https://www.linkedin.com/in/el-nikmatul-izza-505ab827b)")
st.sidebar.info("Self Exploratory Visualization on Data Science Salaries 2023 - Brought To you By [Izzi](https://www.instagram.com/_kemalizzi/) & [Izza](https://www.instagram.com/izzaryu/)  ")
st.sidebar.text("Built with Streamlit by Izzi & Izza")