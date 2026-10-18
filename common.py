import pandas as pd
import streamlit as st

# ---------------------------------------------------------------
# Réglages communs à tous les chapitres
# ---------------------------------------------------------------
LIEN_PUBLICATION = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vS2BqusEeKXdUnHzR1VEUVuYQGlS0jZY_f1KUeDg0soLilm7xzrUxMAFJvUMJxVY4sjqXQCsyuJ10IT/pub"
)

NIVEAUX = {
    "Facile": {
        "tolerance": 1.0,
        "formule": True,
        "calcul": True,
        "aide": "Tu as la formule et le calcul à faire.",
    },
    "Moyen": {
        "tolerance": 0.5,
        "formule": True,
        "calcul": False,
        "aide": "Tu as la formule, à toi de faire le calcul.",
    },
    "Difficile": {
        "tolerance": 0.1,
        "formule": False,
        "calcul": False,
        "aide": "Aucune aide : retrouve la formule seule.",
    },
}


def init_page(titre_onglet):
    st.set_page_config(page_title=f"L'appMandier - {titre_onglet}", page_icon="💄", layout="centered")
    st.markdown(
        "<style>.stApp {background-color: #f5f5f0;}</style>",
        unsafe_allow_html=True,
    )


def entete():
    st.title("💄🌺 L'appMandier - BTS 2 MECP")
    st.caption("by la team love")


# ---------------------------------------------------------------
# Lecture du Google Sheet
# ---------------------------------------------------------------
def url_onglet(gid):
    return f"{LIEN_PUBLICATION}?gid={gid}&single=true&output=csv"


@st.cache_data(ttl=60)
def charger(gid):
    return pd.read_csv(url_onglet(gid), dtype=str)


def en_nombre(texte):
    """'1,5' -> 1.5 ; '3 383,33' -> 3383.33"""
    propre = str(texte).replace(" ", "").replace("\xa0", "").replace(" ", "")
    return float(propre.replace(",", "."))


def verifier_reponse(reponse_eleve, reponse_attendue, tolerance):
    return abs(reponse_eleve - reponse_attendue) <= tolerance


# ---------------------------------------------------------------
# Affichage d'un chapitre complet
# ---------------------------------------------------------------
def afficher_chapitre(numero, titre, question_emma, histoire, gid_donnees, gid_kpi):
    entete()
    st.header(f"Chapitre {numero} : {titre}")
    st.subheader(question_emma)
    st.info(histoire)

    niveau = st.radio(
        "Choisis ton niveau",
        list(NIVEAUX.keys()),
        horizontal=True,
        key=f"niveau_ch{numero}",
    )
    regles = NIVEAUX[niveau]
    st.caption(regles["aide"] + f" Tolérance : ± {regles['tolerance']}")

    try:
        df_donnees = charger(gid_donnees)
        df_kpi = charger(gid_kpi)
    except Exception:
        st.error("Impossible de lire les données du Google Sheet. Réessaie dans un instant.")
        return

    df_donnees = df_donnees.dropna(subset=["donnee"])
    df_kpi = df_kpi.dropna(subset=["kpi"])

    with st.expander("Les données d'Emma", expanded=True):
        tableau = pd.DataFrame(
            {
                "Donnée": df_donnees["donnee"].str.replace("_", " ").str.capitalize(),
                "Valeur": df_donnees["valeur"],
            }
        )
        st.dataframe(tableau, hide_index=True)

    cle_verifie = f"verifie_ch{numero}_{niveau}"
    verifie = st.session_state.get(cle_verifie, False)

    st.divider()
    bonnes = 0
    total = len(df_kpi)

    for _, ligne in df_kpi.iterrows():
        st.markdown(f"**{ligne['kpi']}** · {ligne['question']}")

        if regles["formule"]:
            st.caption(f"Formule : {ligne['formule_texte']}")
        if regles["calcul"]:
            calcul_sans_resultat = str(ligne["calcul_texte"]).rsplit(" = ", 1)[0]
            st.caption(f"Calcul : {calcul_sans_resultat}")

        reponse = st.number_input(
            f"Ta réponse ({ligne['unite']})",
            value=None,
            step=0.01,
            format="%.2f",
            key=f"rep_ch{numero}_{niveau}_{ligne['kpi']}",
        )

        if verifie:
            attendu = en_nombre(ligne["reponse"])
            if reponse is None:
                st.warning("Pas de réponse.")
            elif verifier_reponse(reponse, attendu, regles["tolerance"]):
                bonnes += 1
                st.success("Correct.")
            else:
                st.error("Ce n'est pas ça.")
            with st.expander("Voir la correction"):
                st.write(f"Formule : {ligne['formule_texte']}")
                st.write(f"Calcul : {ligne['calcul_texte']}")
        st.write("")

    def valider():
        st.session_state[cle_verifie] = True

    def recommencer():
        st.session_state[cle_verifie] = False
        for cle in list(st.session_state.keys()):
            if cle.startswith(f"rep_ch{numero}_{niveau}_"):
                del st.session_state[cle]

    if verifie:
        st.subheader(f"Score : {bonnes} / {total}")
        st.button("Recommencer ce niveau", on_click=recommencer)
    else:
        st.button("Vérifier mes réponses", on_click=valider, type="primary")
