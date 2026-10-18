import streamlit as st
from common import init_page, entete

init_page("Accueil")
entete()

st.header("L'institut d'Emma")
st.write(
    "Emma, esthéticienne diplômée, ouvre son propre institut. "
    "À chaque chapitre, une situation concrète, une question de gestion, "
    "et les calculs qui permettent d'y répondre."
)

st.subheader("Comment ça marche")
st.write(
    "Chaque chapitre est indépendant : tu choisis celui que tu veux. "
    "Dans chaque chapitre, trois niveaux :"
)
st.markdown(
    "- **Facile** : la formule et le calcul sont donnés.\n"
    "- **Moyen** : seule la formule est donnée.\n"
    "- **Difficile** : aucune aide."
)

st.subheader("Les chapitres")
st.page_link("pages/1_Chapitre_1_Le_premier_mois.py", label="Chapitre 1 : Le premier mois", icon="💶")
