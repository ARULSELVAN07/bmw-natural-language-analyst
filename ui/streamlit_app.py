import streamlit as st
import requests
import time

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="BMW Natural Language Analyst",
    page_icon="🚘",
    layout="wide",
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 16px;
            color: #666;
            margin-bottom: 25px;
        }

        .result-box {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
            background-color: #fafafa;
        }

        .time-box {
            padding: 10px 15px;
            border-radius: 8px;
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🚘 BMW Natural Language Data Analyst</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Ask questions about BMW vehicle sales, warranty costs, faults, and battery status."
    "</div>",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    api_url = st.text_input(
        "API URL",
        value="http://127.0.0.1:8000",
    )

    st.divider()

    st.subheader("Available MCP Tools")

    st.markdown(
        """
        - 🚗 `get_vehicle_sales()`
        - 💰 `get_warranty_cost()`
        - ⚠️ `get_fault_summary()`
        - 🔋 `get_battery_status()`
        """
    )

    st.divider()

    st.caption("Read-only BMW analytics")

# --------------------------------------------------
# Example Questions
# --------------------------------------------------

st.subheader("Example Questions")

examples = [
    "Which BMW model had the highest warranty cost in Chennai?",
    "Which model has the highest vehicle sales?",
    "What are the most common faults?",
    "Which vehicles have low battery status?",
]

cols = st.columns(2)

for index, example in enumerate(examples):

    with cols[index % 2]:

        if st.button(
            example,
            use_container_width=True,
        ):
            st.session_state.question = example

# --------------------------------------------------
# Question Input
# --------------------------------------------------

st.divider()

question = st.text_area(
    "Ask your BMW data question",
    value=st.session_state.get("question", ""),
    placeholder="Example: Which BMW model had the highest warranty cost in Chennai?",
    height=100,
)

# --------------------------------------------------
# Ask Button
# --------------------------------------------------

if st.button(
    "🔍 Analyze",
    type="primary",
    use_container_width=True,
):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    payload = {
        "question": question.strip()
    }

    # Start timer
    start_time = time.perf_counter()

    with st.spinner("Analyzing BMW data..."):

        try:

            response = requests.post(
                f"{api_url.rstrip('/')}/ask",
                json=payload,
                timeout=120,
            )

            # End timer
            execution_time = time.perf_counter() - start_time

            # --------------------------------------------------
            # Successful Response
            # --------------------------------------------------

            if response.status_code == 200:

                result = response.json()

                st.success("Analysis completed")

                # --------------------------------------------------
                # Execution Time
                # --------------------------------------------------

                st.markdown(
                    f"""
                    <div class="time-box">
                        ⏱️ <strong>Execution Time:</strong>
                        {execution_time:.2f} seconds
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # --------------------------------------------------
                # Narrative Answer
                # --------------------------------------------------

                st.subheader("📊 Analysis")

                answer = result.get(
                    "answer",
                    result.get(
                        "narrative",
                        result.get(
                            "response",
                            "No answer returned.",
                        ),
                    ),
                )

                st.markdown(
                    f'<div class="result-box">{answer}</div>',
                    unsafe_allow_html=True,
                )

                # --------------------------------------------------
                # SQL
                # --------------------------------------------------

                sql = result.get("sql")

                if sql:

                    with st.expander("🔎 Generated SQL"):
                        st.code(
                            sql,
                            language="sql",
                        )

                # --------------------------------------------------
                # Raw Data
                # --------------------------------------------------

                data = result.get("data")

                if data:

                    with st.expander("📋 Query Result"):

                        st.dataframe(
                            data,
                            use_container_width=True,
                        )

            # --------------------------------------------------
            # API Error
            # --------------------------------------------------

            else:

                st.error(
                    f"API request failed: {response.status_code}"
                )

                try:
                    st.json(response.json())
                except Exception:
                    st.code(response.text)

        # --------------------------------------------------
        # Connection Error
        # --------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the BMW Analyst API."
            )

            st.info(
                f"Make sure the API is running at: {api_url}"
            )

        # --------------------------------------------------
        # Timeout
        # --------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. Please try again."
            )

        # --------------------------------------------------
        # Other Error
        # --------------------------------------------------

        except Exception as exc:

            st.error(
                f"Unexpected error: {exc}"
            )