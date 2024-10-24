import streamlit as st
from mistralai import Mistral
import pandas as pd
import fitz  # PyMuPDF

# Fonction pour générer une réponse à partir de l'API Mistral
def generate_response(user_input, context=None):
    model = "mistral-large-latest"
    
    # Initialiser le client Mistral avec la clé API
    client = Mistral(api_key=st.secrets["mistral_key"])

    # Préparer le message en fonction du contexte (fichier téléchargé)
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

    # Si un contexte est fourni, l'ajouter aux messages
    if context:
        messages.insert(1, {
            "role": "context",
            "content": context,
        })

    # Appel à l'API pour générer une réponse
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content

# Titre de l'application
st.title("Chatbot avec Streamlit")
st.write("Bienvenue sur l'interface de chatbot. Posez-moi des questions ou téléchargez un fichier !")

# Initialisation de l'historique des conversations
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'file_content' not in st.session_state:
    st.session_state.file_content = None

# Formulaire d'entrée utilisateur
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Vous :", key="input", placeholder="Pose-moi une question et je réponds avec style !")
    submit_button = st.form_submit_button(label='Envoyer')

if submit_button and user_input:
    # Ajout d'un spinner pour indiquer que le bot réfléchit
    with st.spinner('Le bot réfléchit...'):
        # Vérifier si un fichier a été téléchargé
        if st.session_state.file_content is not None:
            # Générer une réponse en incluant le contenu du fichier
            response = generate_response(user_input, context=st.session_state.file_content)
        else:
            # Générer une réponse sans contexte
            response = generate_response(user_input)

    # Ajout de l'entrée utilisateur et de la réponse à l'historique
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Limitation de l'historique à 10 messages pour éviter une accumulation infinie
if len(st.session_state.chat_history) > 10:
    st.session_state.chat_history.pop(0)

# Affichage de l'historique des échanges
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}:** {message}")

# Ajout d'un bouton pour réinitialiser l'historique
if st.button('Réinitialiser'):
    st.session_state.chat_history = []
    st.session_state.file_content = None  # Réinitialiser le contenu du fichier

# Ajout d'une épingle pour télécharger des fichiers
st.write("### Téléchargez un fichier")
uploaded_file = st.file_uploader("Choisissez un fichier", type=["txt", "csv", "xlsx", "pdf"])

if uploaded_file is not None:
    # Affiche le nom du fichier téléchargé
    st.write("Vous avez téléchargé : ", uploaded_file.name)

    # Lire le contenu du fichier en fonction de son type
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
        st.session_state.file_content = content  # Stocker le contenu dans l'état de la session
        st.write("Contenu du fichier :")
        st.text_area("Contenu", content, height=300)
    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.session_state.file_content = df.to_string()  # Convertir le DataFrame en string
        st.write("Aperçu du fichier CSV :")
        st.dataframe(df.head())  # Afficher les 5 premières lignes
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
        st.session_state.file_content = df.to_string()  # Convertir le DataFrame en string
        st.write("Aperçu du fichier Excel :")
        st.dataframe(df.head())  # Afficher les 5 premières lignes
    elif uploaded_file.type == "application/pdf":
        # Lire le contenu du fichier PDF
        pdf_document = fitz.open(uploaded_file)
        text = ""
        for page in pdf_document:
            text += page.get_text()  # Extraire le texte de chaque page
        pdf_document.close()
        
        st.session_state.file_content = text  # Stocker le texte dans l'état de la session
        st.write("Contenu du fichier PDF :")
        st.text_area("Contenu", text, height=300)


