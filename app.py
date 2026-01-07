import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Data Dashboard",layout = "wide")

st.title("📊 Interactive Data Dashboard!😉")
# st.write("Upload a CSV file to begin")
uploaded_file = st.file_uploader("Upload a CSV file",type = ["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="latin1")
    df = df.copy()
    df.columns = df.columns.str.strip()

    for col in df.columns:
        df[col] =pd.to_numeric(df[col],errors="ignore")

    filtered_df = df.copy()
    filtered_df = filtered_df.reset_index(drop=True)
    numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()
    categorical_cols = filtered_df.select_dtypes(include="object").columns.tolist()

    tab1,tab2,tab3,tab4 = st.tabs(["📄Overview", "📈Charts","🎛️Filters","🎭Story"])


    with tab1:
        st.subheader("Data Overview")
        st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
        st.dataframe(df.head())
    

    with tab2:
        st.subheader("Charts")
        st.success(f"Filtered rows: {filtered_df.shape[0]}")
        numeric_cols = filtered_df.select_dtypes(include = ["number"]).columns.tolist()
        if len(numeric_cols)>=2:
            x_axis = st.selectbox("Select X-axis",numeric_cols)
            y_axis = st.selectbox("Select Y-axis",numeric_cols)

            fig = px.line(
                filtered_df,
                x = x_axis,
                y = y_axis,
                title = f"{y_axis} VS {x_axis}"
            )

            st.plotly_chart(fig,use_container_width=True)
        else:
            st.warning("⚠️Not enough numeric data to plot⚠️")
    with tab3:
        st.subheader("Filters")
        for col in df.select_dtypes(include=["object"]).columns:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals)<20:
                selected_vals = st.multiselect(
                    f"Filter {col}",
                    options= unique_vals,
                    default=unique_vals
                )
                filtered_df[filtered_df[col].isin(selected_vals)]
        st.success(f"Filtered rows: {filtered_df.shape[0]}")

    with tab4:
        st.subheader("🎭Data Story Mode")

        scene = st.radio(
            "Story Progress",
            ["Scene 1: Setup","Scene 2: Change","Scene 3: Conflict","Scene 4: Insight"],
            horizontal=True
        )

        if scene == "Scene 1: Setup":
            st.markdown('The Big Picture')

            st.metric("Rows",filtered_df.shape[0])
            st.metric("Columns",filtered_df.shape[1])

            if numeric_cols:
                st.info("This dataset contains measurable numeric data.")
            else:
                st.warning("This dataset is mostly descriptive (text-based).")
        elif scene == "Scene 2: Change":
            st.markdown("Something Changed")

            if categorical_cols and numeric_cols:
                group_col = st.selectbox("Group by",categorical_cols)
                value_col = st.selectbox("Measure",numeric_cols)

                summary = filtered_df.groupby(group_col)[value_col].sum().sort_values()

                st.bar_chart(summary)

                st.info(
                    f"{summary.idxmax()} leads in {value_col}, while {summary.idxmin()} trails"
                )
            else:
                st.warning("Not enough structure to analyse Changes.")

        elif scene == "Scene 3: Conflict":
            st.markdown("Tension in the Data")

            if numeric_cols:
                col = st.selectbox("Analyse Column",numeric_cols)
                negatives = filtered_df[filtered_df[col]<0]

                if not negatives.empty:
                    st.error(f"{len(negatives)} records have negative {col} values.")
                    st.dataframe(negatives.head())
                else:
                    st.success("No obvious conflicts detected.")
            else:
                st.info("No numeric columns to inspect for connflicts.")

        elif scene == "Scene 4: Insight":
            st.markdown("Insight")

            if numeric_cols:
                col = st.selectbox("Reflect on",numeric_cols)
                st.metric("Average",filtered_df[col].mean())
                st.metric("Max",filtered_df[col].max())
                st.metric("Min",filtered_df[col].min())

                st.markdown(
                    f"> **Insight:** The distribution of `{col}` tells the real story - not just totals."
                )
            else:
                st.markdown(
                    "> **Insight:** The dataset is descriptive. Stories here are about categories, not quantitites."
                )
else:
    st.info("⚠️!!!Please Upload a CSV file to continue.!!!⚠️")
