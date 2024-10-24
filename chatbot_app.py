import streamlit as st
from mistralai import Mistral
import pandas as pd
import PyPDF2

# Fonction pour générer une réponse à partir de l'API Mistral
def generate_response(user_input, context=None):
    model = "mistral-large-latest"
    
    # Initialiser le client Mistral avec la clé API
    client = Mistral(api_key=st.secrets["mistral_key"])

    # Préparer le message en fonction du contexte (si un fichier est téléchargé)
    messages = [
        {
            "role": "assistant",
            "content": "A chaque que tu vas répondre à une question réponds avec des punchlines en français",
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    # Si un contexte (fichier téléchargé) est fourni, l'ajouter aux messages
    if context:
        messages.insert(1, {
            "role": "context",
            "content": context,
        })

    # Appel à l'API Mistral pour générer une réponse
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    
    # Retourner le contenu de la réponse
    return chat_response.choices[0].message.content

# Titre de l'application
st.title("Chatbot avec Streamlit")
st.write("Bienvenue sur l'interface de chatbot. Posez-moi des questions ou téléchargez un fichier !")

# Initialisation de l'historique des conversations dans l'état de la session
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # Liste pour stocker les messages
if 'file_content' not in st.session_state:
    st.session_state.file_content = None  # Variable pour stocker le contenu du fichier téléchargé

# Formulaire d'entrée utilisateur pour poser des questions
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Vous :", key="input", placeholder="Pose-moi une question et je réponds avec style !")
    submit_button = st.form_submit_button(label='Envoyer')

# Si le bouton 'Envoyer' est cliqué et que l'utilisateur a saisi une question
if submit_button and user_input:
    # Ajout d'un spinner pour indiquer que le bot réfléchit à la réponse
    with st.spinner('Le bot réfléchit...'):
        # Vérifier si un fichier a été téléchargé et utiliser son contenu comme contexte
        if st.session_state.file_content is not None:
            response = generate_response(user_input, context=st.session_state.file_content)
        else:
            # Générer une réponse sans contexte si aucun fichier n'a été téléchargé
            response = generate_response(user_input)

    # Ajouter l'entrée utilisateur et la réponse à l'historique
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Limitation de l'historique à 10 messages pour éviter une accumulation excessive
if len(st.session_state.chat_history) > 10:
    st.session_state.chat_history.pop(0)

# Afficher l'historique des échanges utilisateur-bot
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}:** {message}")

# Ajouter un bouton pour réinitialiser l'historique et le contenu du fichier
if st.button('Réinitialiser'):
    st.session_state.chat_history = []  # Réinitialiser l'historique des conversations
    st.session_state.file_content = None  # Réinitialiser le contenu du fichier

# Section pour télécharger un fichier
st.write("### Téléchargez un fichier")
uploaded_file = st.file_uploader("Choisissez un fichier", type=["txt", "csv", "xlsx", "pdf"])

# Si un fichier est téléchargé
if uploaded_file is not None:
    # Afficher le nom du fichier téléchargé
    st.write("Vous avez téléchargé : ", uploaded_file.name)

    # Lire et afficher le contenu du fichier selon son type
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")  # Lire le fichier texte
        st.session_state.file_content = content  # Stocker le contenu du fichier dans l'état de la session
        st.write("Contenu du fichier :")
        st.text_area("Contenu", content, height=300)  # Afficher le texte dans une zone de texte
    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)  # Lire le fichier CSV en DataFrame
        st.session_state.file_content = df.to_string()  # Convertir le DataFrame en chaîne de caractères
        st.write("Aperçu du fichier CSV :")
        st.dataframe(df.head())  # Afficher les 5 premières lignes du fichier CSV
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)  # Lire le fichier Excel en DataFrame
        st.session_state.file_content = df.to_string()  # Convertir le DataFrame en chaîne de caractères
        st.write("Aperçu du fichier Excel :")
        st.dataframe(df.head())  # Afficher les 5 premières lignes du fichier Excel
    elif uploaded_file.type == "application/pdf":
        # Utiliser PyPDF2 pour lire le fichier PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()  # Extraire le texte de chaque page

        st.session_state.file_content = text  # Stocker le texte extrait dans l'état de la session
        st.write("Contenu extrait du fichier PDF :")
        st.text_area("Contenu", text, height=300)  # Afficher le texte extrait du PDF





