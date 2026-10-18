import streamlit as st
from common import init_page, entete, charger_chapitres

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

PAGES = {
    "1": "pages/1_Chapitre_1_Le_premier_mois.py",
    "2": "pages/2_Chapitre_2_Gagner_sa_vie.py",
    "3": "pages/3_Chapitre_3_Les_clientes.py",
    "4": "pages/4_Chapitre_4_Operationnel.py",
    "5": "pages/5_Chapitre_5_Nouvelles_clientes.py",
    "6": "pages/6_Chapitre_6_Recrutement.py",
    "7": "pages/7_Chapitre_7_Investissement.py",
}

st.subheader("Les chapitres")
try:
    chapitres = charger_chapitres()
    for _, ligne in chapitres.iterrows():
        numero = str(ligne["chapitre"]).strip()
        if numero in PAGES:
            st.page_link(PAGES[numero], label=f"Chapitre {numero} : {ligne['titre']}")
except Exception:
    st.error("Impossible de lire la liste des chapitres dans le Google Sheet. Réessaie dans un instant.")
