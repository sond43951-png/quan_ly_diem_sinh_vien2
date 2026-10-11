import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cau hinh trang
st.set_page_config(page_title="Quan ly diem sinh vien", layout="wide")
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. Tao du lieu 10 sinh vien
data = {
    "Ho_ten": [
        "Nguyen Van An", "Tran Thi Binh",
        "Le Minh Cuong", "Pham Thi Dung",
        "Hoang Van Em", "Vu Thi Ha",
        "Dang Quoc Huy", "Tran Van Kien",
        "Ly Thi Lan", "Bui Anh Tuan"
    ],
    "Chuyen_can": [9, 8, 7, 9, 8, 8, 7, 9, 8, 7],
    "Giua_ky":    [8, 7, 8, 9, 7, 8, 6, 8, 7, 8],
    "Cuoi_ky":    [9, 8, 8, 9, 8, 7, 7, 9, 8, 8]
}

df = pd.DataFrame(data)

# 3. Tinh diem tong ket
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# 4. Xep loai
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 5. Hien thi bang diem
st.subheader("1. Bảng điểm sinh viên")
bang_hien_thi = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})
st.dataframe(bang_hien_thi, use_container_width=True, hide_index=True)

# 6. Thong ke
st.subheader("2. Thống kê kết quả")
diem_tb = df["Tong_ket"].mean()
sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = int((df["Tong_ket"] >= 5).sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
c2.metric("Số sinh viên đạt", f"{so_sv_dat}/10")
c3.metric("Điểm cao nhất", f"{sv_cao_nhat['Tong_ket']:.2f}")
c4.metric("Điểm thấp nhất", f"{sv_thap_nhat['Tong_ket']:.2f}")

st.write("**Sinh viên có điểm cao nhất:**", sv_cao_nhat["Ho_ten"])
st.write("**Sinh viên có điểm thấp nhất:**", sv_thap_nhat["Ho_ten"])

# 7. Chon sinh vien
st.subheader("3. Tra cứu điểm từng sinh viên")
ten_chon = st.selectbox("Chọn một sinh viên:", df["Ho_ten"].tolist())
sv = df[df["Ho_ten"] == ten_chon].iloc[0]

a, b, c, d, e = st.columns(5)
a.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
b.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
c.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")
d.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
e.metric("Xếp loại", sv["Xep_loai"])

# 8. Bieu do cot
st.subheader("4. Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(df["Ho_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# 9. Thong tin nguoi tao - SUA LAI THONG TIN CUA BAN
st.divider()
st.caption("Người tạo ứng dụng: [Họ và tên của bạn] | MSSV: [Mã số sinh viên của bạn]")
