import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

@st.cache_data 
def load_data():
    merged_data = pd.read_csv('merged_data.csv')
    # Tambahkan kolom season di sini agar konsisten
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    merged_data['season'] = merged_data['season_day'].map(season_mapping)
    return merged_data

merged_data = load_data()

st.sidebar.title("Filter Data")
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim:",
    options=merged_data['season'].unique(),
    default=merged_data['season'].unique()
)

# Filter data berdasarkan musim yang dipilih
merged_data_filtered = merged_data[merged_data['season'].isin(selected_seasons)]


st.title('Dashboard Analisis Penyewaan Sepeda')

def show_explanation(title, explanation):
    with st.expander(f"Penjelasan: {title}"):
        st.write(explanation)

# 1. Total Penyewaan Sepeda di Setiap Jam (PAKAI DATA FILTERED)
st.header('1. Total Penyewaan Sepeda di Setiap Jam')
data_total_jam = merged_data_filtered.groupby('hr').agg({'cnt_hour': 'sum'}).reset_index()
data_sorted = data_total_jam.sort_values(by="hr")

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(data_sorted["hr"], data_sorted["cnt_hour"], marker='o', linewidth=2, color='#3498db')
ax1.set_xlabel("Jam", fontsize=12)
ax1.set_ylabel("Total Penyewaan", fontsize=12)
ax1.set_title("Total Penyewaan Sepeda di Setiap Jam", fontsize=14)

min_val = data_total_jam["cnt_hour"].min()
max_val = data_total_jam["cnt_hour"].max()
yticks = np.linspace(min_val, max_val, 6).astype(int)
ax1.set_yticks(yticks)

ax1.set_xticks(range(24))

ax1.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig1)

# Menampilkan total penyewaan di jam tertentu
st.write("**Total Penyewaan Tertinggi:**")
st.write(f"- Jam 17: {data_total_jam.loc[data_total_jam['hr'] == 17, 'cnt_hour'].values[0]} penyewaan")
st.write(f"- Jam 4: {data_total_jam.loc[data_total_jam['hr'] == 4, 'cnt_hour'].values[0]} penyewaan (terendah)")

# Eksplaner untuk Total Penyewaan per Jam
explanation1 = """
**Penjelasan:**
- Grafik ini menunjukkan total penyewaan sepeda dalam 24 jam.
- Sumbu X menunjukkan jam (0-23), sedangkan sumbu Y menunjukkan total penyewaan.
- Titik tertinggi menunjukkan jam dengan penyewaan terbanyak.
"""
show_explanation("Total Penyewaan per Jam", explanation1)

# 2. Rata-Rata Penyewaan Sepeda per Jam (PAKAI DATA FILTERED)
st.header('2. Rata-Rata Penyewaan Sepeda per Jam')
data_rata_rata_jam = merged_data_filtered.groupby('hr').agg({'cnt_hour': 'mean'}).reset_index()
data_by_hour = data_rata_rata_jam.sort_values(by='hr')

fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(data_by_hour['hr'], data_by_hour['cnt_hour'], marker='o', linewidth=2, color='#3498db')
ax2.set_xlabel('Jam', fontsize=12)
ax2.set_ylabel('Rata-Rata Penyewaan', fontsize=12)
ax2.set_title('Rata-Rata Penyewaan Sepeda per Jam', fontsize=14)

max_val = data_by_hour['cnt_hour'].max() * 1.05
ax2.set_ylim(0, max_val)

ax2.set_xticks(range(24))

ax2.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig2)

# Menampilkan rata-rata penyewaan di jam tertentu
st.write("**Rata-Rata Penyewaan Tertinggi:**")
st.write(f"- Jam 17: {data_rata_rata_jam.loc[data_rata_rata_jam['hr'] == 17, 'cnt_hour'].values[0]:.2f} penyewaan")
st.write(f"- Jam 4: {data_rata_rata_jam.loc[data_rata_rata_jam['hr'] == 4, 'cnt_hour'].values[0]:.2f} penyewaan (terendah)")

# Eksplaner untuk Rata-Rata Penyewaan per Jam
explanation2 = """
**Penjelasan:**
- Grafik ini menunjukkan rata-rata penyewaan sepeda dalam 24 jam.
- Sumbu X menunjukkan jam (0-23), sedangkan sumbu Y menunjukkan rata-rata penyewaan.
- Titik tertinggi menunjukkan jam dengan rata-rata penyewaan terbanyak.
"""
show_explanation("Rata-Rata Penyewaan per Jam", explanation2)

# 3. Proporsi Total Penyewaan berdasarkan Tipe Hari (PAKAI DATA FILTERED)
st.header('3. Proporsi Total Penyewaan berdasarkan Tipe Hari')
merged_data_filtered['day_type'] = 'Unknown'
merged_data_filtered.loc[(merged_data_filtered['holiday_day'] == 0) & (merged_data_filtered['workingday_day'] == 1), 'day_type'] = 'Working Day'
merged_data_filtered.loc[(merged_data_filtered['holiday_day'] == 1), 'day_type'] = 'Holiday'
merged_data_filtered.loc[(merged_data_filtered['holiday_day'] == 0) & (merged_data_filtered['workingday_day'] == 0), 'day_type'] = 'Weekend/Non-Working'

total_day_type = merged_data_filtered.groupby('day_type')['cnt_day'].sum().reset_index()

fig3, ax3 = plt.subplots(figsize=(8, 8))
ax3.pie(total_day_type['cnt_day'], labels=total_day_type['day_type'], autopct='%1.1f%%')
ax3.set_title('Proporsi Total Penyewaan berdasarkan Tipe Hari')
ax3.axis('equal')  

st.pyplot(fig3)

# Menampilkan total penyewaan berdasarkan tipe hari
st.write("**Total Penyewaan berdasarkan Tipe Hari:**")
for _, row in total_day_type.iterrows():
    st.write(f"- {row['day_type']}: {row['cnt_day']} penyewaan")

# Eksplaner untuk Proporsi Total Penyewaan berdasarkan Tipe Hari
explanation3 = """
**Penjelasan:**
- Pie chart ini menunjukkan proporsi total penyewaan sepeda berdasarkan tipe hari.
- Tipe hari dibagi menjadi **Working Day**, **Holiday**, dan **Weekend/Non-Working**.
- Persentase menunjukkan seberapa besar kontribusi setiap tipe hari terhadap total penyewaan.
"""
show_explanation("Proporsi Total Penyewaan berdasarkan Tipe Hari", explanation3)

# 4. Perbandingan Rata-rata Penyewaan berdasarkan Tipe Hari (PAKAI DATA FILTERED)
st.header('4. Perbandingan Rata-rata Penyewaan berdasarkan Tipe Hari')
rata_rata_day_type = merged_data_filtered.groupby('day_type')['cnt_day'].mean().reset_index()

# Pastikan tidak ada nilai NaN
rata_rata_day_type = rata_rata_day_type.dropna()

rata_rata_day_type['cnt_day'] = rata_rata_day_type['cnt_day'].astype(float)

fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(rata_rata_day_type['cnt_day'], 
        labels=rata_rata_day_type['day_type'], 
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        explode=[0.05] * len(rata_rata_day_type),
        colors=['#ff9999','#66b3ff','#99ff99'])

ax4.set_title('Perbandingan Rata-rata Penyewaan Sepeda berdasarkan Tipe Hari', fontsize=14)
ax4.axis('equal') 

ax4.legend(rata_rata_day_type['day_type'], loc="best")

st.pyplot(fig4)

# Menampilkan rata-rata penyewaan berdasarkan tipe hari
st.write("**Rata-Rata Penyewaan berdasarkan Tipe Hari:**")
for _, row in rata_rata_day_type.iterrows():
    st.write(f"- {row['day_type']}: {row['cnt_day']:.2f} penyewaan")

# Eksplaner untuk Perbandingan Rata-rata Penyewaan berdasarkan Tipe Hari
explanation4 = """
**Penjelasan:**
- Pie chart ini membandingkan rata-rata penyewaan sepeda berdasarkan tipe hari.
- Tipe hari dibagi menjadi **Working Day**, **Holiday**, dan **Weekend/Non-Working**.
- Explode dan shadow digunakan untuk memberikan efek visual yang lebih menarik.
"""
show_explanation("Perbandingan Rata-rata Penyewaan berdasarkan Tipe Hari", explanation4)

# 5. Analisis Lanjutan: Rata-rata Penyewaan berdasarkan Musim dan Tipe Hari (PAKAI DATA FILTERED)
st.header('5. Analisis Lanjutan: Rata-rata Penyewaan berdasarkan Musim dan Tipe Hari')

seasonal_analysis = merged_data_filtered.groupby(['season', 'day_type'])['cnt_day'].mean().reset_index()

fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.barplot(x='season', y='cnt_day', hue='day_type', data=seasonal_analysis, ax=ax5, palette='Set2')
ax5.set_title('Rata-rata Penyewaan berdasarkan Musim dan Tipe Hari', fontsize=14)
ax5.set_xlabel('Musim', fontsize=12)
ax5.set_ylabel('Rata-rata Penyewaan', fontsize=12)
ax5.legend(title='Tipe Hari', loc='upper right')

st.pyplot(fig5)

# Menampilkan rata-rata penyewaan berdasarkan musim dan tipe hari
st.write("**Rata-Rata Penyewaan berdasarkan Musim dan Tipe Hari:**")
for _, row in seasonal_analysis.iterrows():
    st.write(f"- Musim {row['season']}, {row['day_type']}: {row['cnt_day']:.2f} penyewaan")

# Eksplaner untuk Analisis Lanjutan
explanation5 = """
**Penjelasan:**
- Grafik ini menunjukkan rata-rata penyewaan sepeda berdasarkan musim dan tipe hari.
- Musim dibagi menjadi **Spring**, **Summer**, **Fall**, dan **Winter**.
- Tipe hari dibagi menjadi **Working Day**, **Holiday**, dan **Weekend/Non-Working**.
- Grafik ini membantu memahami bagaimana musim dan tipe hari memengaruhi penyewaan sepeda.
"""
show_explanation("Rata-rata Penyewaan berdasarkan Musim dan Tipe Hari", explanation5)