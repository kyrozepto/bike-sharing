import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide", page_title="Bike Rental Dashboard")
day_df = pd.read_csv("dashboard/main_data.csv")
hour_df = pd.read_csv("data/hour.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

with st.sidebar:
    # st.image("path_to_image.png", use_column_width=True)
    st.title("Filter by Date🗓️")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & (hour_df["dteday"] <= str(end_date))]
filtered_day_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

sns.set_theme(style="darkgrid", palette="muted")
plt.style.use("dark_background")
st.markdown("<h1 style='text-align: center; color: white;'>Bike Rental Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FF4B4B;'>Dasbor Analisa Bike Sharing Dataset dengan filter tanggal untuk menyesuaikan rentang waktu data yang ditampilkan.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rentals by Time of Day🕒")
    all_hours = pd.Index(range(24), name='hr')
    hourly_2011 = filtered_hour_df[filtered_hour_df['yr'] == 0].groupby('hr')['cnt'].mean().reindex(all_hours, fill_value=0)
    hourly_2012 = filtered_hour_df[filtered_hour_df['yr'] == 1].groupby('hr')['cnt'].mean().reindex(all_hours, fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(hourly_2011.index - 0.175, hourly_2011.values, width=0.35, label='2011')
    ax.bar(hourly_2012.index + 0.175, hourly_2012.values, width=0.35, label='2012')
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Rentals")
    ax.set_xticks(range(24))
    ax.legend()
    st.pyplot(fig)

    with st.expander("Insights: Rentals by Time of Day"):
        st.write("""
        Berdasarkan visualisasi hour_df menggunakan diagram bar, puncak penyewaan sepeda terjadi pada jam `8 pagi` 
        dan `5-6 sore`, baik pada tahun 2011 maupun 2012. Hal ini menunjukkan bahwa sepeda banyak digunakan untuk 
        perjalanan komuter, yaitu perjalanan ke dan dari kantor pada hari kerja.
        """)
        
with col2:
    st.subheader("Weekday vs Weekend Rentals💼")
    filtered_day_df['weekend'] = filtered_day_df['workingday'].apply(lambda x: 0 if x == 1 else 1)
    weekday_avg = filtered_day_df[filtered_day_df['workingday'] == 1]['cnt'].mean()
    weekend_avg = filtered_day_df[filtered_day_df['workingday'] == 0]['cnt'].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(['Workday', 'Weekend'], [weekday_avg, weekend_avg], color=['#FF4B4B', '#4B9FFF'])
    ax.set_ylabel("Average Rentals")
    st.pyplot(fig)
    
    with st.expander("Insights: Weekday vs Weekend Rentals"):
        st.write(f"Weekend rentals are {((weekend_avg - weekday_avg) / weekday_avg) * 100:.2f}% lower than workday rentals.")
        st.write("""
        Analisis day_df menunjukkan bahwa rata-rata penyewaan sepeda pada hari kerja lebih tinggi dibandingkan dengan akhir pekan. 
        Terdapat penurunan sebesar `5.55%` pada jumlah penyewaan sepeda di akhir pekan. Hal ini memperkuat kesimpulan bahwa sepeda lebih 
        banyak digunakan untuk keperluan komuter. Selain itu, visualisasi data menunjukkan bahwa penyewaan sepeda pada hari libur lebih 
        rendah daripada hari biasa, baik di tahun 2011 maupun 2012.
        """)

col1, col2= st.columns(2)

with col1:
    st.subheader("Rentals by Weather Conditions❄️")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(x='temp', y='cnt', hue='weathersit', palette='coolwarm', data=filtered_hour_df, ax=ax)
    ax.set_title("Rentals by Temperature with Weather Condition")
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Bike Rentals")
    st.pyplot(fig)

    with st.expander("Insights: Rentals by Weather Conditions"):
        st.write("""
        Hasil analisis juga menunjukkan korelasi positif antara suhu `(temp)` dengan jumlah penyewaan sepeda `(cnt)`. 
        Hal ini berlaku baik untuk pengguna terdaftar `(registered)` maupun pengguna tidak terdaftar `(casual)`. Namun, 
        pengaruh suhu lebih kuat pada pengguna yang tidak terdaftar, mengindikasikan bahwa mereka lebih spontan dalam 
        menyewa sepeda saat cuaca baik.
        """)
        
with col2:
    st.subheader("Seasonal and Weather Condition Analysis☀️")
    season_cnt = filtered_hour_df.groupby(by=['season', 'weathersit'])['cnt'].mean().unstack()
    fig, ax = plt.subplots(figsize=(7, 5))
    season_cnt.plot(kind='bar', ax=ax)
    ax.set_title("Average Rentals by Season and Weather Condition")
    ax.set_ylabel("Average Rentals")
    ticks = ax.get_xticks()
    season_labels = ['Spring', 'Summer', 'Fall', 'Winter']
    valid_labels = [season_labels[int(tick)] for tick in ticks if 0 <= int(tick) < len(season_labels)]
    ax.set_xticklabels(valid_labels, rotation=0)
    weathersit_labels = {
        1: "Clear/Partly Cloudy",
        2: "Mist + Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow"
    }
    handles, labels = ax.get_legend_handles_labels()
    new_labels = [weathersit_labels.get(int(l), l) for l in labels]
    ax.legend(handles, new_labels, title='Weather Condition')
    st.pyplot(fig)
    
    with st.expander("Insights: Seasonal and Weather Condition Analysis"):
        st.write("""
        Berdasarkan analisis hour_df, kondisi cuaca `Clear/Partly Cloudydy` memiliki rata-rata penyewaan sepeda tertinggi di semua musim. 
        Sebaliknya, kondisi cuaca `Light Snow/Rain` memiliki rata-rata penyewaan sepeda terendah di semua musim. Hal ini menunjukkan bahwa 
        cuaca baik mendorong penyewaan sepeda, sedangkan cuaca buruk, terutama hujan dan salju, dapat mengurangi jumlah penyewaan.
        """)
