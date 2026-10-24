
import streamlit as st

from rag import answer_question


st.set_page_config(
    page_title="FinlandDoc AI",
    page_icon="📚",
    layout="centered",
)

st.title("📚 FinlandDoc AI")
st.write(
    "Suomenkielisten dokumenttien älykäs haku. "
    "Saat vastauksen dokumentin sisällön perusteella."
)

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
            st.success("Dokumentti ladattu onnistuneesti.")
        except UnicodeDecodeError:
            st.error("Tiedoston pitää olla UTF-8-koodattua tekstiä.")

document = st.text_area(
    "Dokumentin teksti",
    value=document,
    height=200,
    placeholder="Liitä dokumentin teksti tähän...",
)

question = st.text_input(
    "Mitä haluat tietää dokumentista?",
    placeholder="Esim. Miten vuosilomaa haetaan?",
)

if st.button("Etsi vastaus", type="primary"):
    if not document.strip() or not question.strip():
        st.warning("Anna sekä dokumentti että kysymys.")
    else:
        try:
            with st.spinner("Etsitään vastausta dokumentista..."):
                result = answer_question(document, question)

            st.subheader("Vastaus")

            if not result["sources"]:
                st.info(
                    "Dokumentista ei löytynyt kysymykseen sopivaa kohtaa."
                )
            else:
                st.write(result["answer"])

                st.subheader("Vastausta tukevat lähteet")

                for index, source in enumerate(
                    result["sources"], start=1
                ):
                    with st.expander(f"Lähde {index}", expanded=True):
                        st.write(source)

        except RuntimeError as error:
            st.error(str(error))
        except Exception as error:
            st.error(
                f"Odottamaton virhe: {type(error).__name__}: {error}"
            )
