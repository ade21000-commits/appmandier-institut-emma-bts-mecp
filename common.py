import pandas as pd
import streamlit as st

# ---------------------------------------------------------------
# Réglages communs à tous les chapitres
# ---------------------------------------------------------------
LIEN_PUBLICATION = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vS2BqusEeKXdUnHzR1VEUVuYQGlS0jZY_f1KUeDg0soLilm7xzrUxMAFJvUMJxVY4sjqXQCsyuJ10IT/pub"
)
GID_CHAPITRES = "465085677"
GID_DONNEES = "733959936"
GID_KPI = "1289976720"

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


def charger_chapitres():
    df = charger(GID_CHAPITRES)
    return df.dropna(subset=["chapitre"])


def en_nombre(texte):
    """'1,5' -> 1.5 ; '3 383,33' -> 3383.33"""
    propre = str(texte).replace(" ", "").replace("\xa0", "").replace(" ", "")
    return float(propre.replace(",", "."))


def texte_ou_vide(valeur):
    return "" if pd.isna(valeur) else str(valeur)


def verifier_reponse(reponse_eleve, reponse_attendue, tolerance):
    return abs(reponse_eleve - reponse_attendue) <= tolerance


def lignes_du_chapitre(df, numero):
    return df[df["chapitre"].astype(str).str.strip() == str(numero)]


# ---------------------------------------------------------------
# Affichage d'un chapitre complet
# ---------------------------------------------------------------
def afficher_chapitre(numero):
    entete()

    try:
        df_chapitres = charger_chapitres()
        df_donnees = lignes_du_chapitre(charger(GID_DONNEES).dropna(subset=["donnee"]), numero)
        df_kpi = lignes_du_chapitre(charger(GID_KPI).dropna(subset=["kpi"]), numero)
        infos = lignes_du_chapitre(df_chapitres, numero)
    except Exception:
        st.error("Impossible de lire les données du Google Sheet. Réessaie dans un instant.")
        return

    if infos.empty or df_kpi.empty:
        st.warning("Ce chapitre n'est pas encore rempli dans le Google Sheet.")
        return

    infos = infos.iloc[0]
    st.header(f"Chapitre {numero} : {infos['titre']}")
    st.subheader(infos["question_emma"])
    st.info(infos["histoire"])

    niveau = st.radio(
        "Choisis ton niveau",
        list(NIVEAUX.keys()),
        horizontal=True,
        key=f"niveau_ch{numero}",
    )
    regles = NIVEAUX[niveau]
    st.caption(regles["aide"])

    with st.expander("Les données d'Emma", expanded=True):
        libelles = df_donnees["libelle"].where(
            df_donnees["libelle"].notna(),
            df_donnees["donnee"].str.replace("_", " ").str.capitalize(),
        )
        tableau = pd.DataFrame({"Donnée": libelles.values, "Valeur": df_donnees["valeur"].values})
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

        facteur = en_nombre(ligne["facteur_tolerance"]) if pd.notna(ligne["facteur_tolerance"]) else 1.0
        tolerance = regles["tolerance"] * facteur

        reponse = st.number_input(
            f"Ta réponse ({ligne['unite']})",
            value=None,
            step=0.01,
            format="%.2f",
            help=f"Marge d'erreur acceptée : ± {tolerance:g}",
            key=f"rep_ch{numero}_{niveau}_{ligne['kpi']}",
        )

        if verifie:
            attendu = en_nombre(ligne["reponse"])
            if reponse is None:
                st.warning("Pas de réponse.")
            elif verifier_reponse(reponse, attendu, tolerance):
                bonnes += 1
                st.success("Correct.")
            else:
                st.error("Ce n'est pas ça.")
            with st.expander("Voir la correction"):
                st.write(f"Formule : {ligne['formule_texte']}")
                st.write(f"Calcul : {ligne['calcul_texte']}")
                commentaire = texte_ou_vide(ligne["interpretation"])
                if commentaire:
                    st.write(commentaire)
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
