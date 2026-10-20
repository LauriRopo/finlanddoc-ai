
import streamlit as st

from search import search_document

st.set_page_config(page_title="FinlandDoc AI", page_icon="📚")

st.title("FinlandDoc AI")
st.write("Suomenkielisten dokumenttien älykäs haku")

uploaded_file = st.file_uploader(
    "Lataa tekstidokumentti (.txt)",
    type=["txt"],
)

document = ""

if uploaded_file is not None:
    if uploaded_file.size > 1_000_000:
        st.error("Tiedosto on liian suuri. Enimmäiskoko on 1 MB.")
    else:
        try:
            document = uploaded_file.getvalue().decode("utf-8")
            st.success("Dokumentti ladattu.")
        except UnicodeDecodeError:
            st.error("Tiedoston pitää olla UTF-8-koodattua tekstiä.")

document = st.text_area(
    "Dokumentin teksti",
    value=document,
    height=200,
)

question = st.text_input("Mitä haluat tietää?")

if st.button("Etsi"):
    if not document.strip() or not question.strip():
        st.warning("Anna dokumentti ja kysymys.")
    else:
        matches = search_document(document, question)

        if matches:
            st.subheader("Löydetyt kohdat")

            for index, match in enumerate(matches, start=1):
                st.markdown(f"**{index}.** {match}")
        else:
            st.info("Sopivaa kohtaa ei löytynyt.")