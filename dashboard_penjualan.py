# dashboard_penjualan.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

st.title("📊 Dashboard Penjualan Barang")

# Gunakan file dari Google Drive (public link)
file_id = '1_Q0Sf_Tz_PEPkA20Wwe3O1pQ1hXvDB_v'
drive_url = f'https://drive.google.com/uc?id={file_id}'

@st.cache_data
def load_excel_from_drive(url):
    r = requests.get(url)
    with open("temp.xlsx", "wb") as f:
        f.write(r.content)
    return pd.read_excel("temp.xlsx")

try:
    df = load_excel_from_drive(drive_url)

    # Info ringkas
    total_terjual = int(df['Jumlah Terjual'].sum())
    total_pendapatan = int(df['Total Pendapatan'].sum())
    total_laba = int(df['Laba'].sum())

    st.markdown("## 📌 Ringkasan Penjualan")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Unit Terjual", f"{total_terjual:,}")
    col2.metric("Total Pendapatan", f"Rp {total_pendapatan:,}")
    col3.metric("Total Laba", f"Rp {total_laba:,}")

    st.markdown("---")

    # Visualisasi penjualan per barang & laba per barang
    st.markdown("## 📦 Penjualan & Laba per Barang")
    col4, col5 = st.columns(2)
    with col4:
        st.markdown("**Jumlah Terjual per Barang**")
        penjualan_barang = df.groupby("Barang")['Jumlah Terjual'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.barplot(x=penjualan_barang.values, y=penjualan_barang.index, ax=ax, palette="Blues_d")
        ax.set_xlabel("Jumlah Terjual")
        st.pyplot(fig)

    with col5:
        st.markdown("**Laba per Barang**")
        laba_barang = df.groupby("Barang")['Laba'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.barplot(x=laba_barang.values, y=laba_barang.index, ax=ax, palette="Greens_d")
        ax.set_xlabel("Laba")
        st.pyplot(fig)

    st.markdown("---")

    # Penjualan berdasarkan wilayah & kategori
    st.markdown("## 🗺️ Penjualan per Wilayah & Kategori")
    col6, col7 = st.columns(2)
    with col6:
        st.markdown("**Distribusi Penjualan per Wilayah**")
        wilayah = df.groupby("Wilayah")['Jumlah Terjual'].sum()
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(wilayah, labels=wilayah.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    with col7:
        st.markdown("**Jumlah Terjual per Kategori**")
        kategori = df.groupby("Kategori")['Jumlah Terjual'].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sns.barplot(data=kategori, x="Jumlah Terjual", y="Kategori", ax=ax2, palette="viridis")
        st.pyplot(fig2)

    st.markdown("---")

    # Trend penjualan harian
    st.markdown("## 📈 Trend Penjualan Harian")
    df_by_date = df.groupby("Tanggal")["Jumlah Terjual"].sum().reset_index()
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df_by_date, x="Tanggal", y="Jumlah Terjual", ax=ax3, marker="o")
    ax3.set_ylabel("Jumlah Terjual")
    ax3.set_xlabel("Tanggal")
    ax3.set_title("Trend Penjualan per Hari")
    st.pyplot(fig3)

except Exception as e:
    st.error(f"Gagal memuat data dari Google Drive: {e}")
