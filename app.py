import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Configure Gemini
GEMINI_API_KEY = "AIzaSyDoDT6-pFN_Bq3WLoDczx1zeKcMZrhlmvA"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def scrape_kynohealth():
    urls = [
        "https://www.kynohealth.com/",
        "https://www.kynohealth.com/provide-services",
        "https://www.kynohealth.com/about-us",
        "https://www.kynohealth.com/blog",
        "https://www.kynohealth.com/contact-us",
        "https://www.kynohealth.com/book-doctor/step-1",
        "https://www.kynohealth.com/terms-conditions",
        "https://www.kynohealth.com/return-policy",
    ]

    all_text = ""

    for url in urls:
        try:
            st.info(f"Scraping: {url}")
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')

            # Extract visible text from the page
            page_text = soup.get_text(separator='\n', strip=True)

            all_text += f"\n\n--- Page: {url} ---\n\n" + page_text
        except Exception as e:
            st.error(f"Error scraping {url}: {e}")

    return all_text

def ask_gemini(question, context):
    prompt = f"""
Context from KynoHealth website:
{context}

Question: {question}

Answer based on the context above. If the answer isn't in the context, say You've stumped me this time 😅 — can we explore it together?.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    st.title("KynoHealth Chatbot")

    if 'kyno_data' not in st.session_state:
        with st.spinner("Scraping KynoHealth website and specified pages..."):
            st.session_state.kyno_data = scrape_kynohealth()

    st.write("Ask questions about KynoHealth:")
    question = st.text_input("Your question:", key="question")

    if question:
        if st.session_state.kyno_data:
            answer = ask_gemini(question, st.session_state.kyno_data)
            st.write("Answer:", answer)
        else:
            st.error("Failed to load website data")

if __name__ == "__main__":
    main()
