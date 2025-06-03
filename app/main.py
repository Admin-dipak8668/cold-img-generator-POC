import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# 🛠 Set layout early
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/lead-software-engineer-itc/job/R-51405")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for i, job in enumerate(jobs):
                skills = job.get('skills') or []
                if isinstance(skills, str):
                    skills = [s.strip() for s in skills.split(",")]
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)

                with st.expander(f"Email - {job.get('role', 'Unknown')}"):
                    st.markdown(email)

        except Exception as e:
            import traceback
            st.error(f"An Error Occurred: {e}")
            st.text(traceback.format_exc())

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
