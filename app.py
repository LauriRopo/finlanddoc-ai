
import streamlit as st

from search import search_document

from rag import answer_question

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
        try:
            result = answer_question(document, question)

            st.subheader("Vastaus")
            st.write(result["answer"])

            if result["sources"]:
                st.subheader("Lähteet")

                for index, source in enumerate(
                    result["sources"], start=1
                ):
                    st.markdown(f"**Lähde {index}:** {source}")

        except RuntimeError as error:
            st.error(str(error))
        except Exception as error:
            st.error(
        f"Virhe: {type(error).__name__}: {error}"
            )   