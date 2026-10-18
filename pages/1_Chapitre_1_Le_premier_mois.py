from common import init_page, afficher_chapitre

init_page("Chapitre 1")

afficher_chapitre(
    numero=1,
    titre="Le premier mois",
    question_emma="« Combien ai-je vraiment gagné ? »",
    histoire=(
        "Emma ouvre son institut un mardi matin de septembre. Après un premier mois intense, "
        "elle s'assoit devant sa caisse et regarde les reçus : 120 clientes, des soins, des produits "
        "vendus, des paiements encaissés. Quand elle essaie de répondre à la question simple "
        "« est-ce que ça marche ? », elle ne sait pas par où commencer."
    ),
    gid_donnees="1078135817",
    gid_kpi="2073564451",
)
