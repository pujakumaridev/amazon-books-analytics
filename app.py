
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Amazon Books Analytics",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded"
)

ORANGE = "#FF9900"
BACKGROUND = "#111820"
CARD = "#202C38"
BORDER = "#344251"
TEXT = "#E8EDF2"
MUTED = "#AAB5C0"

# =====================================================
# 2. PROFESSIONAL DESIGN AND ICONS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

.stApp {
    background: #111820;
    color: #E8EDF2;
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: #111820;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #19232D;
    border-right: 1px solid #344251;
}

h1, h2, h3 {
    color: #F5F7FA !important;
    font-family: 'Inter', sans-serif;
    font-weight: 600 !important;
}

p, label {
    color: #AAB5C0;
}

.material-symbols-outlined {
    font-family: 'Material Symbols Outlined';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    line-height: 1;
    display: inline-flex;
    vertical-align: middle;
    color: #FF9900;
    margin-right: 9px;
}

.brand-title {
    color: #FF9900;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 1px;
}

.brand-subtitle {
    color: #AAB5C0;
    font-size: 11px;
    letter-spacing: 2px;
}

.section-title {
    color: #F5F7FA;
    font-size: 21px;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 16px;
}

.metric-card {
    background: #202C38;
    border: 1px solid #344251;
    border-left: 4px solid #FF9900;
    padding: 18px 14px;
    border-radius: 10px;
    height: 125px;
    box-sizing: border-box;
    overflow: hidden;
}

.metric-label {
    color: #AAB5C0;
    font-size: 12px;
    margin-bottom: 14px;
    white-space: nowrap;
}

.metric-value {
    color: #FF9900;
    font-size: 23px;
    font-weight: 700;
    white-space: nowrap;
}

.metric-icon {
    color: #FF9900;
    font-size: 23px;
}

.info-card {
    background: #202C38;
    border: 1px solid #344251;
    border-radius: 10px;
    padding: 17px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #344251;
    border-radius: 10px;
}

.stButton button,
.stDownloadButton button {
    background: #FF9900;
    color: #111820;
    border: none;
    border-radius: 7px;
    font-weight: 600;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: #E68A00;
    color: #111820;
}

hr {
    border-color: #344251;
}

[data-testid="stMetric"] {
    background: #202C38;
    border: 1px solid #344251;
    border-radius: 10px;
    padding: 16px;
}

[data-testid="stMetricLabel"] {
    color: #AAB5C0 !important;
}

[data-testid="stMetricValue"] {
    color: #FF9900 !important;
}

.stTextInput input {
    background: #202C38;
    color: white;
    border: 1px solid #344251;
}

.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background: #202C38;
    border-color: #344251;
}

.stCaption {
    color: #AAB5C0;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. HELPER FUNCTIONS
# =====================================================

def icon_heading(icon_name, heading):
    st.markdown(
        f'<div class="section-title">'
        f'<span class="material-symbols-outlined">'
        f'{icon_name}</span>{heading}</div>',
        unsafe_allow_html=True
    )


def metric_card(icon_name, label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                <span class="material-symbols-outlined metric-icon">
                    {icon_name}
                </span>
                {label}
            </div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 4. LOAD CSV DATA
# =====================================================

@st.cache_data
def load_data():

    file_path = Path(__file__).parent / "books.csv"

    if not file_path.exists():
        return None

    data = pd.read_csv(file_path)

    # Standardize column names
    data.columns = (
        data.columns.str.strip()
        .str.replace(" ", "_")
    )

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Convert numeric columns
    numeric_columns = [
        "User_Rating", "Reviews", "Price", "Year"
    ]

    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(
                data[col].astype(str).str.replace(",", "", regex=False),
                errors="coerce"
            )

    return data


df = load_data()

if df is None:
    st.error("books.csv was not found. Keep it in the same folder as app.py.")
    st.stop()


# =====================================================
# 5. CHECK DATASET COLUMNS
# =====================================================

required_columns = [
    "Name",
    "Author",
    "User_Rating",
    "Reviews",
    "Price",
    "Year",
    "Genre"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "Your CSV is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.info(
        "Expected columns: Name, Author, User_Rating, "
        "Reviews, Price, Year, Genre"
    )
    st.stop()

# Clean text fields
for col in ["Name", "Author", "Genre"]:
    df[col] = df[col].astype("string").str.strip()

df = df.dropna(subset=required_columns)

df = df[
    (df["Name"] != "") &
    (df["Author"] != "") &
    (df["Genre"] != "")
]

if df.empty:
    st.error("No valid book records are available.")
    st.stop()


# =====================================================
# 6. DASHBOARD HEADER
# =====================================================

header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown(
        """
        <div class="brand-title">
            AMAZON BOOKS ANALYTICS
        </div>
        <div class="brand-subtitle">
            BUSINESS INTELLIGENCE & DATA VISUALIZATION
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col2:
    st.markdown(
        "<div style='text-align:right;color:#AAB5C0;"
        "font-size:12px;padding-top:12px;'>"
        "PYTHON | PANDAS | STREAMLIT</div>",
        unsafe_allow_html=True
    )

st.markdown("---")


# =====================================================
# 7. SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown(
    """
    <div class="brand-title" style="font-size:20px;">
        <span class="material-symbols-outlined">
            tune
        </span>
        FILTER PANEL
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

search_text = st.sidebar.text_input(
    "Search Books or Authors",
    placeholder="Enter a book title or author..."
)

all_genres = sorted(df["Genre"].dropna().unique().tolist())

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    options=all_genres,
    default=all_genres
)

all_years = sorted(
    df["Year"].dropna().unique().tolist()
)

selected_years = st.sidebar.multiselect(
    "Select Publication Year",
    options=all_years,
    default=all_years
)

rating_range = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Amazon Books Analytics | Data Exploration"
)


# =====================================================
# 8. FILTER DATA
# =====================================================

filtered_df = df[
    (df["Genre"].isin(selected_genres)) &
    (df["Year"].isin(selected_years)) &
    (df["User_Rating"] >= rating_range)
].copy()

if search_text.strip():
    search = search_text.strip()

    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(
            search, case=False, na=False
        ) |
        filtered_df["Author"].str.contains(
            search, case=False, na=False
        )
    ]

if filtered_df.empty:
    st.warning(
        "No books match your current search and filters. "
        "Try changing your selections."
    )
    st.stop()


# =====================================================
# 9. KEY PERFORMANCE INDICATORS
# =====================================================

icon_heading("dashboard", "Overview & Key Statistics")

total_books = len(filtered_df)

average_rating = filtered_df["User_Rating"].mean()

average_price = filtered_df["Price"].mean()

total_reviews = filtered_df["Reviews"].sum()

k1, k2, k3, k4 = st.columns(4)

with k1:
    metric_card(
        "menu_book",
        "TOTAL BOOKS",
        f"{total_books:,}"
    )

with k2:
    metric_card(
        "star",
        "AVERAGE RATING",
        f"{average_rating:.2f} / 5"
    )

with k3:
    metric_card(
        "payments",
        "AVERAGE PRICE",
        f"${average_price:,.2f}"
    )

with k4:
    metric_card(
        "rate_review",
        "TOTAL REVIEWS",
        (
    f"{total_reviews / 1_000_000:.2f}M"
    if total_reviews >= 1_000_000
    else f"{total_reviews / 1_000:.1f}K"
    if total_reviews >= 1_000
    else f"{total_reviews:,.0f}"
)
    )

st.markdown("---")


# =====================================================
# 10. GENRE ANALYSIS
# =====================================================

icon_heading("category", "Category Analysis")

left, right = st.columns(2)

with left:

    st.markdown("**Book Distribution by Genre**")

    genre_data = (
        filtered_df.groupby("Genre")
        .size()
        .reset_index(name="Total Books")
    )

    fig = px.pie(
        genre_data,
        names="Genre",
        values="Total Books",
        hole=0.60,
        color_discrete_sequence=[
            "#FF9900",
            "#526A80",
            "#8C9DAE"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=TEXT,
        margin=dict(t=25, b=25, l=20, r=20),
        legend_title_text="Genre"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.markdown("**Top 10 Authors by Book Count**")

    author_data = (
        filtered_df["Author"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    author_data.columns = ["Author", "Total Books"]

    author_data = author_data.sort_values(
        "Total Books", ascending=True
    )

    fig = px.bar(
        author_data,
        x="Total Books",
        y="Author",
        orientation="h",
        color="Total Books",
        color_continuous_scale=[
            "#526A80",
            "#FF9900"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=TEXT,
        coloraxis_showscale=False,
        margin=dict(t=25, b=25, l=10, r=20),
        xaxis_title="Number of Books",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# 11. RATING AND PRICE ANALYSIS
# =====================================================

st.markdown("---")

icon_heading("insights", "Rating & Pricing Insights")

left, right = st.columns(2)

with left:

    st.markdown("**Customer Rating Distribution**")

    fig = px.histogram(
        filtered_df,
        x="User_Rating",
        nbins=10,
        color_discrete_sequence=[ORANGE]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=TEXT,
        xaxis_title="Customer Rating",
        yaxis_title="Number of Books",
        margin=dict(t=25, b=25, l=20, r=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.markdown("**Book Price vs Customer Rating**")

    fig = px.scatter(
        filtered_df,
        x="Price",
        y="User_Rating",
        color="Genre",
        hover_name="Name",
        hover_data=["Author", "Reviews"],
        color_discrete_sequence=[
            ORANGE,
            "#7896B0",
            "#B0BEC9"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=TEXT,
        xaxis_title="Book Price",
        yaxis_title="Customer Rating",
        margin=dict(t=25, b=25, l=20, r=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# 12. BOOK CATALOGUE
# =====================================================

st.markdown("---")

icon_heading("library_books", "Book Catalogue")

st.caption(
    "Explore books available in the selected dataset."
)

catalogue = filtered_df[
    [
        "Name",
        "Author",
        "Genre",
        "Year",
        "User_Rating",
        "Reviews",
        "Price"
    ]
].sort_values(
    "Reviews",
    ascending=False
)

st.dataframe(
    catalogue,
    use_container_width=True,
    hide_index=True,
    height=350,
    column_config={
        "Name": st.column_config.TextColumn(
            "Book Title",
            width="large"
        ),
        "Author": st.column_config.TextColumn(
            "Author",
            width="medium"
        ),
        "User_Rating": st.column_config.NumberColumn(
            "Rating",
            format="%.1f / 5"
        ),
        "Reviews": st.column_config.NumberColumn(
            "Reviews",
            format="%d"
        ),
        "Price": st.column_config.NumberColumn(
            "Price",
            format="$%.2f"
        )
    }
)


# =====================================================
# 13. TOP 10 BOOKS
# =====================================================

st.markdown("---")

icon_heading("trending_up", "Top 10 Books by Reviews")

top_books = filtered_df.nlargest(
    min(10, len(filtered_df)),
    "Reviews"
)

for rank, (_, book) in enumerate(
    top_books.iterrows(),
    start=1
):
    with st.container(border=True):

        c1, c2, c3 = st.columns([0.6, 4, 1.3])

        with c1:
            st.markdown(
                f"<h3 style='color:#FF9900;'>{rank:02d}</h3>",
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"**{book['Name']}**"
            )
            st.caption(
                f"Author: {book['Author']} | "
                f"Genre: {book['Genre']} | "
                f"Year: {book['Year']:.0f}"
            )

        with c3:
            st.markdown(
                f"**{book['User_Rating']:.1f} / 5**"
            )
            st.caption(
                f"{book['Reviews']:,.0f} reviews"
            )


# =====================================================
# 14. BOOK DETAILS AND SEARCH
# =====================================================

st.markdown("---")

icon_heading("search", "Book Details Explorer")

book_options = sorted(
    filtered_df["Name"].unique().tolist()
)

selected_book = st.selectbox(
    "Choose a book to view its details",
    options=book_options
)

book_info = filtered_df[
    filtered_df["Name"] == selected_book
].iloc[0]

d1, d2 = st.columns(2)

with d1:
    st.markdown(
        f"""
        <div class="info-card">
            <div style="color:#AAB5C0;font-size:12px;">
                BOOK TITLE
            </div>
            <h3 style="color:#FF9900;">
                {book_info['Name']}
            </h3>
            <p><b>Author:</b> {book_info['Author']}</p>
            <p><b>Genre:</b> {book_info['Genre']}</p>
            <p><b>Year:</b> {book_info['Year']:.0f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with d2:
    st.markdown(
        f"""
        <div class="info-card">
            <div style="color:#AAB5C0;font-size:12px;">
                BOOK PERFORMANCE
            </div>
            <h3 style="color:#FF9900;">
                {book_info['User_Rating']:.1f} / 5
            </h3>
            <p><b>Customer Reviews:</b> {book_info['Reviews']:,.0f}</p>
            <p><b>Price:</b> ${book_info['Price']:,.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 15. DOWNLOAD FILTERED DATA
# =====================================================

st.markdown("---")

icon_heading("download", "Export Dataset")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Books CSV",
    data=csv_data,
    file_name="amazon_books_analysis.csv",
    mime="text/csv"
)


# =====================================================
# 16. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;padding:15px;">
        <div style="color:#FF9900;font-weight:600;">
            AMAZON BOOKS ANALYTICS
        </div>
        <div style="color:#8996A3;font-size:12px;margin-top:8px;">
            Developed using Python | Pandas | Streamlit | Plotly
        </div>
        <div style="color:#8996A3;font-size:11px;margin-top:5px;">
            Data Analysis and Visualization Project
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
