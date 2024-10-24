import streamlit as st
from mistralai import Mistral
import pandas as pd
import pdfplumber  # Importer la bibliothèque pdfplumber pour traiter les fichiers PDF

# Fonction pour générer une réponse à partir de l'API Mistral
def generate_response(user_input, context=None):
    model = "mistral-large-latest"  # Définir le modèle Mistral à utiliser
    
    # Créer un client Mistral avec la clé API stockée dans les secrets Streamlit
    client = Mistral(api_key=st.secrets["mistral_key"])

    # Préparer les messages pour l'API
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

    # Si un contexte (comme le texte d'un fichier) est fourni, l'ajouter aux messages
    if context:
        messages.insert(1, {
            "role": "context",
            "content": context,
        })

    # Appeler l'API pour obtenir une réponse
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content  # Retourner le contenu de la réponse

# Titre de l'application
st.title("Chatbot avec Streamlit")
st.write("Bienvenue sur l'interface de chatbot. Posez-moi des questions ou téléchargez un fichier !")

# Initialisation de l'historique des conversations
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # Historique des messages
if 'file_content' not in st.session_state:
    st.session_state.file_content = None  # Contenu du fichier téléchargé

# Formulaire d'entrée utilisateur
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Vous :", key="input", placeholder="Pose-moi une question et je réponds avec style !")
    submit_button = st.form_submit_button(label='Envoyer')

# Lorsque l'utilisateur soumet une question
if submit_button and user_input:
    with st.spinner('Le bot réfléchit...'):  # Indicateur de chargement
        # Si un fichier a été téléchargé, inclure son contenu comme contexte
        if st.session_state.file_content is not None:
            response = generate_response(user_input, context=st.session_state.file_content)
        else:
            response = generate_response(user_input)  # Sinon, juste utiliser la question

    # Ajouter l'entrée utilisateur et la réponse à l'historique
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Limitation de l'historique à 10 messages pour éviter l'encombrement
if len(st.session_state.chat_history) > 10:
    st.session_state.chat_history.pop(0)

# Affichage de l'historique des échanges
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}:** {message}")

# Section pour télécharger des fichiers
st.write("### Téléchargez un fichier")
uploaded_file = st.file_uploader("Choisissez un fichier", type=["txt", "csv", "xlsx", "pdf"])

# Si un fichier est téléchargé
if uploaded_file is not None:
    st.write("Vous avez téléchargé : ", uploaded_file.name)

    # Lire le contenu du fichier en fonction de son type
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")  # Lire le fichier texte
        st.session_state.file_content = content  # Stocker le contenu pour une utilisation ultérieure
        st.write("Contenu du fichier :")
        st.text_area("Contenu", content, height=300)  # Afficher le contenu dans une zone de texte
    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)  # Lire le fichier CSV dans un DataFrame
        st.session_state.file_content = df.to_string()  # Convertir le DataFrame en chaîne de caractères
        st.write("Aperçu du fichier CSV :")
        st.dataframe(df.head())  # Afficher un aperçu du DataFrame
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)  # Lire le fichier Excel dans un DataFrame
        st.session_state.file_content = df.to_string()  # Convertir le DataFrame en chaîne de caractères
        st.write("Aperçu du fichier Excel :")
        st.dataframe(df.head())  # Afficher un aperçu du DataFrame
    elif uploaded_file.type == "application/pdf":
        # Lire le contenu du fichier PDF avec pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()  # Extraire le texte de chaque page
        st.session_state.file_content = text  # Stocker le contenu pour une utilisation ultérieure
        st.write("Contenu du fichier PDF :")
        st.text_area("Contenu", text, height=300)  # Afficher le texte extrait dans une zone de texte



