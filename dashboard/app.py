# ============================================================
# DASHBOARD KLIEN / PRESENTASI — KETERKAITAN & RISIKO EKSTREM HARGA CABAI
# Kota vs Kabupaten Cirebon · PIHPS Bank Indonesia · 2020–2026
# Jalankan : streamlit run dashboard_cabai_cirebon.py
# Data     : ekstrak Arsip_Semua_Output_EDA_1-16.zip ke ./data  (sub-folder bebas, dicari lewat NAMA berkas)
# Catatan  : seluruh angka dibaca langsung dari keluaran Tahap 5–15. Keterkaitan statistik, BUKAN kausalitas.
# ============================================================
import os, re, json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Harga Cabai Cirebon", page_icon="🌶️", layout="wide")

INTI = ["Cabai Merah Besar", "Cabai Merah Keriting", "Cabai Rawit Merah"]
SEMUA = ["Beras Kualitas Medium I", "Bawang Merah Ukuran Sedang", "Bawang Putih Ukuran Sedang"] + INTI + ["Daging Ayam Ras Segar", "Telur Ayam Ras Segar"]
KOTA, KAB = "Kota Cirebon", "Kabupaten Cirebon"
BIRU, ORG, HJU, MRH, ABU, UNG, TEAL = "#2563EB", "#F59E0B", "#10B981", "#EF4444", "#64748B", "#7C3AED", "#0D9488"
RAYA = {"Idulfitri": ["2020-05-24", "2021-05-13", "2022-05-02", "2023-04-22", "2024-04-10", "2025-03-31", "2026-03-21"],
        "Iduladha": ["2020-07-31", "2021-07-20", "2022-07-10", "2023-06-29", "2024-06-17", "2025-06-06", "2026-05-27"]}
pend = lambda k: str(k).replace("Cabai ", "")

# ---------- sidebar & gaya ----------
st.sidebar.markdown("## 🌶️ Pengaturan")
ROOT = st.sidebar.text_input("📁 Folder data", os.environ.get("DATA_ROOT", "./data"))
PRES = st.sidebar.toggle("🖥️ Mode presentasi", False, help="Huruf dan grafik lebih besar untuk layar proyektor.")
if st.sidebar.button("🔄 Muat ulang data"):
    st.cache_data.clear()
zoom = "html{font-size:115%}" if PRES else ""
TINGGI = 1.25 if PRES else 1.0
st.markdown(f"""<style>{zoom}
.block-container{{padding-top:1.1rem;max-width:1450px}}
.hero{{background:linear-gradient(120deg,#1E3A8A,#2563EB 52%,#F59E0B 150%);color:#fff;padding:1.5rem 1.9rem;border-radius:20px;margin-bottom:1rem;box-shadow:0 10px 28px rgba(37,99,235,.25)}}
.hero h1{{color:#fff;font-size:1.8rem;margin:0 0 .3rem;line-height:1.25}}.hero p{{margin:0;color:rgba(255,255,255,.93)}}
.kartu{{border-radius:16px;padding:.95rem 1.15rem;background:rgba(148,163,184,.10);border:1px solid rgba(148,163,184,.28);border-left:6px solid var(--w,#2563EB);height:100%}}
.kartu .j{{font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;color:#64748B;font-weight:650}}
.kartu .n{{font-size:1.75rem;font-weight:780;line-height:1.25;margin:.1rem 0}}.kartu .c{{font-size:.83rem;color:#64748B}}
.pesan{{border-radius:16px;padding:1rem 1.2rem;background:rgba(148,163,184,.08);border:1px solid rgba(148,163,184,.25);margin-bottom:.7rem}}
.pesan b.h{{font-size:1.05rem}}.pesan .s{{color:#64748B;font-size:.9rem;margin-top:.25rem}}
.baca,.awas{{border-radius:14px;padding:.8rem 1rem;font-size:.93rem;margin:.6rem 0}}
.baca{{background:rgba(37,99,235,.08);border:1px solid rgba(37,99,235,.25)}}.awas{{background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.4)}}
.lencana{{display:inline-block;padding:.1rem .6rem;border-radius:999px;font-size:.74rem;font-weight:650;color:#fff;margin-right:.35rem}}
button[data-baseweb="tab"]{{font-weight:650}}
</style>""", unsafe_allow_html=True)


def fm(x, d=2):  # format angka gaya Indonesia: 1.234,56
    if x is None or (isinstance(x, float) and np.isnan(x)): return "—"
    return f"{x:,.{d}f}".replace(",", "§").replace(".", ",").replace("§", ".")


def rg(s, d=2, suf=""):
    s = pd.Series(s).astype(float).replace([np.inf, -np.inf], np.nan).dropna()
    if s.empty: return "—"
    a, b = fm(s.min(), d), fm(s.max(), d)
    return (a if a == b else f"{a}–{b}") + suf


def md(t): return re.sub(r"\*(.+?)\*", r"<i>\1</i>", re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t))


def kartu(j, n, c="", w=BIRU):
    st.markdown(f"<div class='kartu' style='--w:{w}'><div class='j'>{j}</div><div class='n'>{n}</div><div class='c'>{c}</div></div>", unsafe_allow_html=True)


def info(t, jenis="baca"):
    st.markdown(f"<div class='{jenis}'>{'💡' if jenis == 'baca' else '⚠️'} {md(t)}</div>", unsafe_allow_html=True)


def plot(fig, h=440, hover="x unified"):
    fig.update_layout(template="plotly_white", height=int(h * TINGGI), margin=dict(l=10, r=10, t=50, b=10), hovermode=hover,
                      font=dict(family="Inter, Segoe UI, sans-serif", size=14 if PRES else 13), legend=dict(orientation="h", y=1.04, x=0))
    try: st.plotly_chart(fig, width="stretch")
    except Exception: st.plotly_chart(fig, use_container_width=True)


def tabel(df, h=None):
    kw = {"hide_index": True, **({"height": h} if h else {})}
    try: st.dataframe(df, width="stretch", **kw)
    except Exception: st.dataframe(df, use_container_width=True, **kw)


def lencana(t):
    t = str(t); w = HJU if "Tingkat 1" in t else (BIRU if "Tingkat 2" in t else ABU)
    return f"<span class='lencana' style='background:{w}'>{t}</span>"


def kategori(t):
    t = str(t); return "Temuan (Tingkat 1)" if "Tingkat 1" in t else ("Indikasi (Tingkat 2)" if "Tingkat 2" in t else "Keterbatasan / tidak didukung")


# ---------- data ----------
@st.cache_data(show_spinner=False)
def indeks(root):
    d = {}
    for dp, dirs, files in os.walk(root, followlinks=True):
        dirs.sort()
        for f in sorted(files):
            if f.lower().endswith((".csv", ".json")): d.setdefault(f, os.path.join(dp, f))
    return d


@st.cache_data(show_spinner=False)
def baca(p): return pd.read_csv(p)


IDX = indeks(ROOT) if os.path.isdir(ROOT) else {}
muat = lambda n: baca(IDX[n]) if n in IDX else None


@st.cache_data(show_spinner="Menyiapkan data harga…")
def siapkan(ph, pb):
    h = pd.read_csv(ph, parse_dates=["tanggal"]); b = pd.read_csv(pb, parse_dates=["tanggal", "tanggal_sebelumnya"])
    v = h[h.status_harga.eq("harga_valid")]
    P = v.pivot_table(index="tanggal", columns=["komoditas", "wilayah"], values="harga_rp", aggfunc="first").reindex(pd.DatetimeIndex(sorted(h.tanggal.unique())))
    b = b.sort_values(["komoditas", "tanggal"]).reset_index(drop=True); b["multihari"] = b.jarak_hari >= 2
    return P, b


if not (IDX.get("data_harga_eda5.csv") and IDX.get("data_perubahan_bersama_eda5.csv")):
    st.error(f"Berkas **data_harga_eda5.csv** dan **data_perubahan_bersama_eda5.csv** tidak ditemukan di `{ROOT}`. "
             "Ekstrak arsip ZIP ke folder `data` di samping file ini, lalu klik *Muat ulang data*."); st.stop()
P, BER = siapkan(IDX["data_harga_eda5.csv"], IDX["data_perubahan_bersama_eda5.csv"])
T14B, T15A, T14A, T13G, T14C, T13A, T15F = (muat(n) for n in ["t14b_ecm_spesifikasi.csv", "t15a_keluarga_utama.csv", "t14a_evt_skala_interval.csv",
                                                               "t13g_chi_final.csv", "t14c_hari_raya_peristiwa.csv", "t13a_markup.csv", "t15f_daftar_klaim.csv"])


def butuh(df, nama):
    if df is None: st.info(f"Berkas **{nama}** belum ditemukan di folder data."); return False
    return True


def lonjak(g, a):
    f = lambda x, z: x.notna() & z.notna() & (x > 0) & (100 * (z - x).abs() >= a * x)
    fk, fa = f(g.harga_kota_rp_sebelumnya, g.harga_kota_rp), f(g.harga_kabupaten_rp_sebelumnya, g.harga_kabupaten_rp)
    return fk | fa, fk


def wilson(k, n, z=1.645):
    if n == 0: return np.nan, np.nan
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; r = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(c - r, 0), min(c + r, 1)


def kum_log(s, H, a, b):
    H = pd.Timestamp(H); lo, hi = H + pd.Timedelta(days=a), H + pd.Timedelta(days=b)
    sb, sd = s[s.index < lo], s[(s.index >= lo) & (s.index <= hi)]
    return np.nan if len(sb) == 0 or len(sd) == 0 else float((np.log(sd.iloc[-1]) - np.log(sb.iloc[-1])) * 100)


# ---------- hero ----------
st.markdown("<div class='hero'><h1>Dinamika Harga dan Risiko Lonjakan Komoditas Pangan Strategis Kota Cirebon vs Kabupaten Cirebon</h1>"
            "<p>Seberapa cepat harga kedua wilayah saling menyesuaikan, dan seberapa besar serta sering lonjakan ekstrem terjadi. "
            f"Data harian PIHPS Bank Indonesia, {P.index.min():%b %Y} – {P.index.max():%b %Y}.</p></div>", unsafe_allow_html=True)
TAB = st.tabs(["🏠 Ringkasan", "📈 Harga", "🔁 Penyesuaian", "⚡ Risiko", "🎉 Hari raya", "💰 Premi Kota", "✅ Bukti & batasan", "🧪 Data & unduhan"])

# ============ 1. RINGKASAN ============
with TAB[0]:
    n_obs = int(BER.groupby("komoditas").size().iloc[0]) + 1
    hl = T14B[T14B.komoditas.isin(INTI)].half_life if T14B is not None else []
    aB = T15A[(T15A.uji == "U1")].estimasi if T15A is not None else []
    lj = T14A.laju_ge20_per250_1hari if T14A is not None else []
    chi = T13G[(T13G.hubungan == "serentak") & np.isclose(T13G.q, .95)].chi if T13G is not None else []
    c = st.columns(5)
    with c[0]: kartu("Waktu penyesuaian", f"{rg(hl, 1)} hari", "separuh selisih harga Kota–Kab hilang (hari kerja)", HJU)
    with c[1]: kartu("Koreksi Kabupaten (α_B)", rg(aB, 2), "porsi selisih yang dikoreksi per hari kerja", ORG)
    with c[2]: kartu("Lonjakan ≥20%", f"{rg(lj, 1)}×", "kejadian per 250 hari kerja (interval 1 hari)", MRH)
    with c[3]: kartu("Keserentakan ekstrem", rg(chi, 2), "peluang wilayah kedua ikut melonjak (acuan bebas 0,05)", UNG)
    with c[4]: kartu("Observasi", fm(n_obs, 0), "tanggal bersama per komoditas", BIRU)
    st.markdown("### Pesan utama")
    iduladha = T14C[(T14C.hari_raya == "Iduladha") & (T14C.jendela == "PRA")]["rata2_kumulatif_%"] if T14C is not None else []
    mk = T13A.selisih_rata2_Rp if T13A is not None else []
    pesan = [("⏱️ Harga kedua wilayah cepat kembali sejalan", f"Selisih harga Kota–Kabupaten menutup separuhnya dalam sekitar **{rg(hl, 1)} hari kerja**.", "Temuan (Tingkat 1)", "Pada ketiga cabai."),
             ("🔁 Kabupaten yang paling aktif menyesuaikan", f"Bila Kota lebih mahal dari biasanya, Kabupaten menaikkan harga sekitar **{rg(aB, 2)}** dari selisih itu per hari kerja. Kota ikut menyesuaikan lebih kecil dan tidak kokoh setelah koreksi uji ganda.", "Temuan (Tingkat 1)", "α_B (Kabupaten). α_K (Kota) hanya indikasi."),
             ("⚡ Lonjakan ekstrem hampir selalu serentak", f"Saat Kota melonjak ekstrem, Kabupaten ikut melonjak pada hari yang sama dengan peluang **{rg(chi, 2)}**; dengan jeda satu hari peluangnya turun mendekati acuan.", "Temuan (Tingkat 1)", "Bukan penjalaran bertahap."),
             ("📉 Risiko harian terukur", f"Lonjakan ≥20% sekitar **{rg(lj, 1)} kali per 250 hari kerja**. Interval multi-hari (Senin, sesudah libur) lebih berisiko.", "Indikasi (Tingkat 2)", "Bentuk ekor (berat/terbatas) tidak teridentifikasi."),
             ("🎉 Pola hari raya", f"Menjelang Iduladha harga cabai merah naik rata-rata **{rg(iduladha[:4] if len(iduladha) else [], 0, '%')}**, lalu turun tajam sepekan sesudah hari raya.", "Indikasi (Tingkat 2)", "Pola deskriptif, 7 peristiwa, tidak lolos koreksi Holm."),
             ("💰 Premi Kota berupa markup nominal", f"Kota rata-rata lebih mahal sekitar **Rp {rg(mk, 0)}**, relatif tetap berapa pun tingkat harganya.", "Indikasi (Tingkat 2)", "Bukan proporsional terhadap harga.")]
    a, b = st.columns(2)
    for i, (h, s, tk, ct) in enumerate(pesan):
        with (a if i % 2 == 0 else b):
            st.markdown(f"<div class='pesan'><b class='h'>{h}</b><div class='s'>{md(s)}</div><div style='margin-top:.4rem'>{lencana(tk)}<span style='color:#64748B;font-size:.82rem'>{ct}</span></div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 3])
    with c1:
        if T15F is not None:
            cn = T15F.tingkat.map(kategori).value_counts()
            fig = go.Figure(go.Pie(labels=cn.index, values=cn.values, hole=.55, marker_colors=[{"Temuan (Tingkat 1)": HJU, "Indikasi (Tingkat 2)": BIRU}.get(k, ABU) for k in cn.index], textinfo="value"))
            fig.update_layout(title="Klaim menurut tingkat bukti", showlegend=True, legend=dict(orientation="h")); plot(fig, 330, "closest")
    with c2:
        info("**Yang boleh disimpulkan:** harga kedua wilayah bergerak sangat searah, selisihnya cepat menutup, dan lonjakan ekstrem terjadi serentak. "
             "**Yang tidak boleh:** satu wilayah *menyebabkan* wilayah lain, atau *penyebab* lonjakan (pasokan, cuaca, hari raya). Uji asimetri berdaya rendah sehingga hasil 'tidak signifikan' bukan bukti simetri.", "awas")

# ============ 2. HARGA ============
with TAB[1]:
    c1, c2, c3 = st.columns([2, 3, 1.4])
    kom = c1.selectbox("Komoditas", SEMUA, index=SEMUA.index("Cabai Merah Besar"), key="hk")
    t0, t1 = P.index.min().date(), P.index.max().date()
    rng = c2.slider("Rentang tanggal", t0, t1, (t0, t1), format="DD MMM YYYY", key="hr")
    amb = c3.slider("Ambang lonjakan (%)", 10, 40, 20, 5, key="ha")
    o = st.columns(4)
    s_k, s_r, s_s = o[0].toggle("Tandai lonjakan", True), o[1].toggle("Tandai hari raya", True), o[2].toggle("Panel selisih", True)
    ma = o[3].slider("Rata-rata bergerak", 1, 60, 7)
    A, B = pd.Timestamp(rng[0]), pd.Timestamp(rng[1])
    D = P[[(kom, KOTA), (kom, KAB)]].dropna().loc[A:B]; D.columns = ["K", "A"]
    G = BER[(BER.komoditas == kom) & (BER.tanggal >= A) & (BER.tanggal <= B)].copy(); G["f"], G["fk"] = lonjak(G, amb)
    if len(D) < 5: st.warning("Rentang tanggal terlalu pendek."); st.stop()
    sel = (np.log(D.K) - np.log(D.A)) * 100
    m = st.columns(4)
    with m[0]: kartu("Harga Kota terakhir", f"Rp {fm(D.K.iloc[-1], 0)}", f"{D.index[-1]:%d %b %Y}", BIRU)
    with m[1]: kartu("Harga Kab terakhir", f"Rp {fm(D.A.iloc[-1], 0)}", f"selisih Rp {fm(D.K.iloc[-1] - D.A.iloc[-1], 0)}", ORG)
    with m[2]: kartu("Kota lebih mahal", f"{fm((sel > 0).mean() * 100, 0)}% hari", f"rata-rata selisih {fm(sel.mean())}%", UNG)
    with m[3]: kartu(f"Lonjakan ≥{amb}%", f"{int(G.f.sum())}", f"dari {len(G)} interval", MRH)
    fig = make_subplots(rows=2 if s_s else 1, cols=1, shared_xaxes=True, row_heights=[.68, .32] if s_s else [1], vertical_spacing=.06)
    for ser, nm, w in [(D.K, "Kota", BIRU), (D.A, "Kabupaten", ORG)]:
        fig.add_trace(go.Scatter(x=ser.index, y=ser.rolling(ma, min_periods=1).mean(), name=nm, line=dict(color=w, width=2)), row=1, col=1)
    if s_k:
        arah = np.sign(np.where(G.fk, G.perubahan_kota_persen, G.perubahan_kabupaten_persen))
        for ar, sim, w in [(1, "triangle-up", MRH), (-1, "triangle-down", "#0F172A")]:
            x = G[G.f & (arah == ar)]
            if len(x): fig.add_trace(go.Scatter(x=x.tanggal, y=x.harga_kota_rp, mode="markers", name=f"{'Naik' if ar > 0 else 'Turun'} ≥{amb}% (n={len(x)})", marker=dict(symbol=sim, size=11, color=w, line=dict(width=1, color="white")),
                                                customdata=np.c_[x.perubahan_kota_persen, x.perubahan_kabupaten_persen, x.jarak_hari],
                                                hovertemplate="%{x|%d %b %Y}<br>Δ Kota %{customdata[0]:.1f}% · Δ Kab %{customdata[1]:.1f}%<br>interval %{customdata[2]} hari<extra></extra>"), row=1, col=1)
    if s_s:
        fig.add_trace(go.Scatter(x=sel.index, y=sel, name="Selisih (%)", line=dict(color=UNG, width=1), opacity=.4), row=2, col=1)
        fig.add_trace(go.Scatter(x=sel.index, y=sel.rolling(21, min_periods=5).median(), name="Median 21 obs.", line=dict(color="#111827", width=2.2)), row=2, col=1)
        fig.add_hline(y=0, line_color="#94A3B8", row=2, col=1)
    if s_r:
        for t in sum(RAYA.values(), []):
            if A <= pd.Timestamp(t) <= B: fig.add_vline(x=t, line_dash="dot", line_color="rgba(100,116,139,.5)")
    fig.update_xaxes(rangeslider_visible=True, rangeslider_thickness=.06, row=2 if s_s else 1, col=1)
    fig.update_yaxes(tickformat=",.0f", title_text="Harga (Rp)", row=1, col=1); plot(fig, 650)
    info("Tarik slider di bawah grafik atau zoom untuk memperbesar periode. Garis biru dan oranye berdampingan; selisih (ungu) kecil dan cepat kembali ke rata-ratanya. Garis putus-putus = Idulfitri/Iduladha.")

# ============ 3. PENYESUAIAN ============
with TAB[2]:
    if butuh(T14B, "t14b_ecm_spesifikasi.csv"):
        st.markdown("#### Seberapa cepat selisih harga menutup? (half-life, hari kerja)")
        ks = list(dict.fromkeys(T14B.komoditas)); sp = list(dict.fromkeys(T14B.spesifikasi)); fig = go.Figure(); fig.add_vrect(x0=1, x1=2, fillcolor=HJU, opacity=.10, line_width=0)
        for i, s_ in enumerate(sp):
            d = T14B[T14B.spesifikasi == s_]
            fig.add_trace(go.Scatter(x=d.half_life, y=[ks.index(k) + (i - (len(sp) - 1) / 2) * .17 for k in d.komoditas], mode="markers", name=s_, marker=dict(size=12, line=dict(width=1, color="white")),
                                     error_x=dict(type="data", symmetric=False, array=(d.hl_atas - d.half_life).clip(lower=0), arrayminus=(d.half_life - d.hl_bawah).clip(lower=0)),
                                     customdata=d.komoditas, hovertemplate="%{customdata}<br>%{x:.2f} hari<extra>" + s_ + "</extra>"))
        fig.update_yaxes(tickmode="array", tickvals=list(range(len(ks))), ticktext=[pend(k) for k in ks], autorange="reversed"); fig.update_layout(xaxis_title="Half-life (bar = CI90)"); plot(fig, 380, "closest")
        info("Sekitar **1–2 hari kerja** pada semua cara hitung. Karena angkanya sedikit bergantung pada spesifikasi, yang dilaporkan adalah rentangnya.")
    if butuh(T15A, "t15a_keluarga_utama.csv"):
        st.markdown("#### Siapa yang menyesuaikan?")
        a = T15A[T15A.uji.isin(["U1", "U2"])]; fig = go.Figure()
        for u, nm, w in [("U1", "α_B · Kabupaten menyesuaikan ke Kota", ORG), ("U2", "α_K · Kota ikut menyesuaikan", BIRU)]:
            s = a[a.uji == u]
            fig.add_trace(go.Bar(x=[pend(k) for k in s.komoditas], y=s.estimasi, name=nm, marker_color=w, text=[f"p Holm {'<0,001' if p < .001 else fm(p, 3)}" for p in s.p_Holm_18], textposition="outside"))
        fig.add_hline(y=0, line_color=ABU); fig.update_layout(barmode="group", yaxis_title="Koefisien koreksi (per hari kerja)"); plot(fig, 380, "closest")
        info("α_B positif dan signifikan pada ketiga cabai. α_K negatif pada cabai merah tetapi tidak bertahan setelah koreksi 18 uji, dan tidak ada pada rawit. Kedua arah punya daya prediksi; selisih antar-arah tidak signifikan, jadi **jangan dibaca sebagai 'Kota memimpin Kabupaten'**.")
    st.markdown("#### 🎮 Simulasi interaktif (ilustrasi model, bukan hasil data)")
    c = st.columns(4); aK = c[0].slider("α_K (Kota)", -.6, 0.0, -.10, .01); aB_ = c[1].slider("α_B (Kabupaten)", 0.0, .8, .25, .01)
    d0 = c[2].slider("Selisih awal (%)", 1, 20, 10); H = c[3].slider("Horizon (hari kerja)", 5, 25, 12)
    rho = 1 + aK - aB_; t = np.arange(H + 1); dev = d0 * rho ** t
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Selisih harga (%)", "Perubahan kumulatif akibat koreksi (%)"))
    fig.add_trace(go.Scatter(x=t, y=dev, mode="lines+markers", name="Selisih", line=dict(color=UNG, width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=np.r_[0, np.cumsum((aK * dev)[:-1])], name="Kota", line=dict(color=BIRU)), row=1, col=2)
    fig.add_trace(go.Scatter(x=t, y=np.r_[0, np.cumsum((aB_ * dev)[:-1])], name="Kabupaten", line=dict(color=ORG)), row=1, col=2)
    fig.update_xaxes(title_text="Hari kerja"); plot(fig, 360)
    hlx = np.log(.5) / np.log(rho) if 0 < rho < 1 else (0.0 if rho <= 0 else np.inf); m = st.columns(3)
    with m[0]: kartu("Sisa selisih setelah 1 hari", f"ρ = {fm(rho)}", "", UNG)
    with m[1]: kartu("Half-life", "tidak menutup" if np.isinf(hlx) else f"{fm(hlx)} hari", "", HJU)
    with m[2]: kartu("Porsi koreksi oleh Kabupaten", f"{fm(aB_ / (aB_ - aK) * 100, 0)}%" if aB_ - aK > 0 else "—", "α_B / (α_B − α_K)", ORG)

# ============ 4. RISIKO ============
with TAB[3]:
    if butuh(T14A, "t14a_evt_skala_interval.csv"):
        d = T14A.copy(); d["seri"] = d.komoditas.map(pend) + " · " + d.wilayah.str.replace(" Cirebon", "", regex=False)
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=d.seri, y=d["RL250_1hari_%"], mode="markers", name="Interval 1 hari", marker=dict(size=13, color=BIRU),
                                     error_y=dict(type="data", symmetric=False, array=d["RL250_1hari_%_p95"] - d["RL250_1hari_%"], arrayminus=d["RL250_1hari_%"] - d["RL250_1hari_%_p5"])))
            fig.add_trace(go.Scatter(x=d.seri, y=d["RL250_multihari_%"], mode="markers", name="Interval multi-hari", marker=dict(size=13, color=MRH, symbol="diamond")))
            fig.update_layout(title="Kenaikan terbesar yang diharapkan sekali per 250 interval (%)", yaxis_title="%"); plot(fig, 400, "closest")
        with c2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=d.seri, y=d.laju_ge20_per250_1hari, mode="markers", name="Model (CI90)", marker=dict(size=13, color=ORG),
                                     error_y=dict(type="data", symmetric=False, array=d.laju_ge20_per250_1hari_p95 - d.laju_ge20_per250_1hari, arrayminus=d.laju_ge20_per250_1hari - d.laju_ge20_per250_1hari_p5)))
            fig.add_trace(go.Scatter(x=d.seri, y=d.laju_empiris_per250_1hari, mode="markers", name="Data nyata", marker=dict(size=12, color="#111827", symbol="diamond")))
            fig.update_layout(title="Klaster lonjakan ≥20% per 250 interval 1 hari", yaxis_title="kejadian"); plot(fig, 400, "closest")
        n0 = int(((d.xi_p5 <= 0) & (d.xi_p95 >= 0)).sum())
        info(f"Titik hitam (data nyata) berada dalam rentang model. Interval multi-hari jauh lebih berisiko. CI90 indeks ekor ξ memuat nol pada **{n0} dari {len(d)}** seri, jadi bentuk ekor tidak disimpulkan; yang dilaporkan hanya besar dan frekuensi lonjakan.", "awas")
    if butuh(T13G, "t13g_chi_final.csv"):
        st.markdown("#### Keserentakan lonjakan ekstrem (χ)")
        qs = sorted(T13G.q.unique()); q = st.radio("Kuantil ambang", qs, index=len(qs) - 1, horizontal=True, format_func=lambda v: f"q = {fm(v)}")
        s = T13G[np.isclose(T13G.q, q)]; fig = go.Figure()
        for h, w in zip(s.hubungan.unique(), [HJU, BIRU, ORG]):
            z = s[s.hubungan == h]; fig.add_trace(go.Bar(x=[pend(k) for k in z.komoditas], y=z.chi, name=h, marker_color=w, error_y=dict(type="data", symmetric=False, array=z.p95 - z.chi, arrayminus=z.chi - z.p5)))
        fig.add_hline(y=1 - q, line_dash="dash", line_color=MRH, annotation_text="acuan jika saling bebas"); fig.update_layout(barmode="group", yaxis_title="Peluang wilayah kedua ikut melonjak"); plot(fig, 380, "closest")
    st.markdown("#### 🧮 Kalkulator frekuensi (langsung dari data)")
    c = st.columns([3, 1.4, 1.4, 1.6]); ks = c[0].multiselect("Komoditas", SEMUA, default=INTI, key="fk"); wl = c[1].selectbox("Wilayah", ["Kota", "Kabupaten", "Salah satu"])
    ar = c[2].selectbox("Arah", ["Naik", "Turun", "Keduanya"]); x = c[3].slider("Ambang (%)", 5, 60, 20, key="fx"); rows = []
    for k in ks:
        g = BER[BER.komoditas == k]; f = lambda s: s >= x if ar == "Naik" else (s <= -x if ar == "Turun" else s.abs() >= x)
        fk, fa = f(g.perubahan_kota_persen), f(g.perubahan_kabupaten_persen); fl = fk if wl == "Kota" else (fa if wl == "Kabupaten" else fk | fa)
        for nm, mm in [("Interval 1 hari", ~g.multihari), ("Interval multi-hari", g.multihari)]:
            kk, nn = int(fl[mm].sum()), int(mm.sum()); lo, hi = wilson(kk, nn)
            rows.append({"Komoditas": k, "Jenis": nm, "Kejadian": kk, "Interval": nn, "Per 250": 250 * kk / nn, "CI90 bawah": 250 * lo, "CI90 atas": 250 * hi, "Kira-kira sekali tiap": f"{nn / kk:.0f} interval" if kk else "—"})
    if rows:
        R = pd.DataFrame(rows); fig = go.Figure()
        for nm, w in [("Interval 1 hari", BIRU), ("Interval multi-hari", MRH)]:
            s = R[R.Jenis == nm]; fig.add_trace(go.Bar(x=[pend(k) for k in s.Komoditas], y=s["Per 250"], name=nm, marker_color=w, error_y=dict(type="data", symmetric=False, array=s["CI90 atas"] - s["Per 250"], arrayminus=s["Per 250"] - s["CI90 bawah"])))
        fig.update_layout(barmode="group", yaxis_title=f"Kejadian per 250 interval ({ar.lower()} ≥{x}%)"); plot(fig, 340, "closest"); tabel(R.round(2))

# ============ 5. HARI RAYA ============
with TAB[4]:
    c = st.columns(3); hr = c[0].selectbox("Hari raya", list(RAYA), index=1); wl = c[1].selectbox("Wilayah ", [KOTA, KAB]); pra = c[2].slider("Jendela sebelum (hari)", 7, 45, 30)
    if butuh(T14C, "t14c_hari_raya_peristiwa.csv"):
        s = T14C[(T14C.hari_raya == hr) & (T14C.wilayah == wl)]; fig = go.Figure()
        for jd, nm, w in [("PRA", "Sebelum hari raya", MRH), ("HARI", "Sesudah hari raya (±1 pekan)", BIRU)]:
            z = s[s.jendela == jd]; fig.add_trace(go.Bar(x=[pend(k) for k in z.komoditas], y=z["rata2_kumulatif_%"], name=nm, marker_color=w, text=[f"naik {p} thn" for p in z.peristiwa_naik], textposition="outside"))
        fig.add_hline(y=0, line_color=ABU); fig.update_layout(barmode="group", yaxis_title="Rata-rata kumulatif perubahan harga (%)"); plot(fig, 360, "closest")
    kom = st.selectbox("Lihat lintasan per tahun untuk", INTI, key="rk"); s = P[(kom, wl)].dropna(); tg = RAYA[hr]; pas = 7
    fig = go.Figure(); dias = np.arange(-pra, pas + 8); jej = []
    for H, y in zip(tg, [pd.Timestamp(t).year for t in tg]):
        Ht = pd.Timestamp(H); tgl = [Ht + pd.Timedelta(days=int(q)) for q in dias]; dasar = s[s.index < Ht - pd.Timedelta(days=pra)]
        if len(dasar):
            v = s.reindex(s.index.union(tgl)).ffill().reindex(tgl).values / dasar.iloc[-1] * 100; jej.append(v); fig.add_trace(go.Scatter(x=dias, y=v, name=str(y), opacity=.8))
    if jej: fig.add_trace(go.Scatter(x=dias, y=np.nanmean(jej, axis=0), name="Rata-rata", line=dict(color="#111827", width=4)))
    fig.add_vline(x=0, line_dash="dash", line_color=ABU); fig.update_layout(xaxis_title=f"Hari relatif terhadap {hr}", yaxis_title="Indeks (100 = sebelum jendela)"); plot(fig, 400)
    info("Pola konsisten: naik menjelang Iduladha, turun sepekan sesudah kedua hari raya. Hanya **7 peristiwa** per hari raya, tiga cabai bergerak bersama (bukan tiga bukti terpisah), dan **tidak ada yang lolos koreksi Holm**. Baca sebagai pola deskriptif.", "awas")

# ============ 6. PREMI ============
with TAB[5]:
    c = st.columns(3); kom = c[0].selectbox("Komoditas  ", INTI, key="pk"); sat = c[1].radio("Satuan", ["Rupiah", "Persen"], horizontal=True); acu = c[2].toggle("Garis acuan", True)
    dd = P[[(kom, KOTA), (kom, KAB)]].dropna(); dd.columns = ["K", "A"]; rata, S = (dd.K + dd.A) / 2, dd.K - dd.A; y = S / 1000 if sat == "Rupiah" else S / dd.A * 100
    fig = go.Figure(go.Scatter(x=rata / 1000, y=y, mode="markers", marker=dict(size=5, opacity=.6, color=dd.index.year, colorscale="Viridis", showscale=True, colorbar=dict(title="Tahun")),
                               customdata=np.c_[dd.index.strftime("%d %b %Y")], hovertemplate="%{customdata[0]}<br>harga %{x:.1f} rb · selisih %{y:.2f}<extra></extra>", name="Hari"))
    if acu:
        xs = np.linspace(max(rata.min() / 1000, 1), rata.max() / 1000, 100); mr = S.mean() / 1000; k = (S / rata).mean()
        fig.add_trace(go.Scatter(x=xs, y=[mr] * 100 if sat == "Rupiah" else mr / xs * 100, name="Markup nominal tetap", line=dict(color=MRH, dash="dash", width=3)))
        fig.add_trace(go.Scatter(x=xs, y=k * xs if sat == "Rupiah" else [k * 100] * 100, name="Premi proporsional", line=dict(color="#111827", dash="dot", width=3)))
    fig.update_layout(xaxis_title="Harga rata-rata Kota & Kab (ribu Rp)", yaxis_title="Selisih Kota − Kab (" + ("ribu Rp)" if sat == "Rupiah" else "% dari harga Kab)")); plot(fig, 440, "closest")
    info("Selisih rupiah kira-kira tetap, sehingga dalam persen ia menyusut saat harga naik. Karena itu premi Kota tampak lebih besar ketika harga murah. Ini asosiasi statistik, bukan penjelasan sebab.")
    c1, c2 = st.columns(2); rz, db = muat("t12a_rezim.csv"), muat("t13b_dols.csv")
    with c1:
        st.markdown("**Rezim rata-rata selisih (ln Kota − ln Kab)**")
        if rz is not None: tabel(rz.rename(columns={"komoditas": "Komoditas", "rezim": "Rezim", "mulai": "Mulai", "akhir": "Akhir", "rata2_%": "Rata-rata (%)", "sd_%": "SD (%)"}).round(2))
        st.caption("Tanggal patahan adalah estimasi statistik; tidak dikaitkan dengan peristiwa tertentu.")
    with c2:
        st.markdown("**Elastisitas jangka panjang (DOLS)**")
        if db is not None: tabel(db[["komoditas", "spesifikasi", "beta", "ci90_bawah", "ci90_atas"]].round(3))
        st.caption("β sedikit di bawah 1 (≈0,96–0,98) sesuai markup nominal tetap, bukan kegagalan hukum satu harga.")

# ============ 7. BUKTI & BATASAN ============
with TAB[6]:
    t1, t2, t3 = st.tabs(["Register klaim", "Keterbatasan", "Definisi baku"])
    with t1:
        if butuh(T15F, "t15f_daftar_klaim.csv"):
            R = T15F.assign(Kategori=T15F.tingkat.map(kategori)); cn = R.Kategori.value_counts(); m = st.columns(3)
            for col, (nm, w) in zip(m, [("Temuan (Tingkat 1)", HJU), ("Indikasi (Tingkat 2)", BIRU), ("Keterbatasan / tidak didukung", ABU)]):
                with col: kartu(nm, f"{int(cn.get(nm, 0))} klaim", "", w)
            c = st.columns(3); kt = c[0].multiselect("Kategori", list(cn.index), default=list(cn.index)); kk = c[1].multiselect("Komoditas", sorted(R.komoditas.unique()), default=sorted(R.komoditas.unique())); q = c[2].text_input("🔎 Cari")
            F = R[R.Kategori.isin(kt) & R.komoditas.isin(kk)]
            if q: F = F[F.klaim.str.contains(q, case=False, na=False) | F.bukti.astype(str).str.contains(q, case=False, na=False)]
            for _, r in F.iterrows():
                with st.expander(f"{pend(r.komoditas)} — {r.klaim}"): st.markdown(lencana(r.tingkat) + f"<br>**Bukti:** {r.bukti}", unsafe_allow_html=True)
            info("Tingkat bukti = konsistensi pada variasi keputusan pemodelan dan koreksi uji ganda, **bukan** probabilitas kebenaran dan bukan bukti kausal.")
    with t2:
        d = muat("t16e_keterbatasan.csv")
        if butuh(d, "t16e_keterbatasan.csv"):
            for _, r in d.iterrows():
                with st.expander(f"{r.kode} · {r.keterbatasan}"): st.write(r.uraian); st.markdown(f"**Cara melaporkan:** {r.mitigasi_pelaporan}")
    with t3:
        d = muat("t16e_definisi.csv")
        if butuh(d, "t16e_definisi.csv"):
            for _, r in d.iterrows():
                with st.expander(f"{r.kode} · {r.istilah}"): st.write(r.definisi); st.caption(f"Tahap rujukan: {r.tahap_rujukan}")

# ============ 8. DATA & UNDUHAN ============
with TAB[7]:
    st.markdown("#### Pemeriksaan integritas langsung (dihitung dashboard)")
    cek = []
    cek.append(("Data inti Tahap 5 tersedia", "PASS", "ada"))
    n = BER.groupby("komoditas").size(); cek.append(("Jumlah observasi bersama sama untuk 8 komoditas", "PASS" if n.nunique() == 1 and len(n) == 8 else "FAIL", f"{n.min()}–{n.max()}"))
    t10i = muat("t10i_ringkasan_hasil_utama.csv")
    if t10i is not None and T14B is not None:
        a = t10i.set_index("komoditas").half_life_hari_kerja; b = T14B[T14B.spesifikasi == "log, rata-rata global"].set_index("komoditas").half_life
        cek.append(("Half-life Tahap 10 = Tahap 14 (log, global)", "PASS" if np.allclose(a.reindex(b.index), b, atol=1e-6) else "FAIL", f"selisih maks {np.nanmax(np.abs(a.reindex(b.index) - b)):.2e}"))
    for nm, df in [("t14b", T14B), ("t14a", T14A), ("t15a", T15A), ("t13g", T13G), ("t14c", T14C), ("t15f", T15F)]:
        cek.append((f"Berkas {nm} terbaca", "PASS" if df is not None else "FAIL", "ada" if df is not None else "tidak ada"))
    C = pd.DataFrame(cek, columns=["Pemeriksaan", "Status", "Nilai"]); C["Status"] = C.Status.map({"PASS": "✅ lolos", "FAIL": "❌ gagal"}); tabel(C)
    stj = IDX.get("t16_status.json")
    if stj:
        js = json.load(open(stj, encoding="utf-8"))
        if not js.get("status_kritis_lolos", False):
            info("Paket **Tahap 16** di arsip ini belum valid (angka resmi bernilai n/a, register klaim tidak terbentuk, cek integritas tahap 16 gagal karena berkas inti tidak ditemukan saat dijalankan). "
                 "Dashboard ini tidak memakainya: angka diambil langsung dari Tahap 13–15 dan register klaim dari t15f. Jalankan ulang Tahap 16 setelah semua berkas berada di satu folder yang terbaca.", "awas")
    st.markdown("#### Kelengkapan data harga")
    kel = P.notna().sum().rename("Tanggal valid").reset_index(); kel.columns = ["Komoditas", "Wilayah", "Tanggal valid"]; kel["Kosong"] = len(P) - kel["Tanggal valid"]; tabel(kel, 320)
    st.markdown("#### ⬇️ Unduh tabel hasil")
    pil = st.selectbox("Pilih berkas", sorted(k for k in IDX if k.startswith(("t1", "t7", "t8", "t9")) and k.endswith(".csv")))
    if pil: st.download_button(f"Unduh {pil}", open(IDX[pil], "rb").read(), pil, "text/csv")

st.markdown("---")
st.caption("Dashboard ini menyajikan keterkaitan statistik dari data harian PIHPS (Bank Indonesia). Bukan bukti kausalitas dan bukan penjelasan penyebab lonjakan harga.")