import streamlit as st
from mistralai import Mistral

# Fonction pour générer une réponse à partir de l'API Mistral
def generate_response(user_input):
    model = "mistral-large-latest"
    
    # Initialiser le client Mistral avec la clé API
    client = Mistral(api_key=st.secrets["mistral_key"])

    # Appel à l'API pour générer une réponse
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "assistant",
                "content": "A chaque que tu vas répondre à une question réponds avec des punchlines en français",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )
    return chat_response.choices[0].message.content

# Titre de l'application
st.title("Chatbot avec Streamlit")
st.write("Bienvenue sur l'interface de chatbot. Posez-moi des questions ou téléchargez un fichier !")

# Initialisation de l'historique des conversations
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Formulaire d'entrée utilisateur
with st.form(key='chat_form', clear_on_submit=True):
    # Placeholder pour les questions
    user_input = st.text_input("Vous :", key="input", placeholder="Pose-moi une question et je réponds avec style !")
    submit_button = st.form_submit_button(label='Envoyer')

if submit_button and user_input:
    # Ajout d'un spinner pour indiquer que le bot réfléchit
    with st.spinner('Le bot réfléchit...'):
        response = generate_response(user_input)
    
    # Ajout de l'entrée utilisateur et de la réponse à l'historique
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Limitation de l'historique à 10 messages pour éviter une accumulation infinie
if len(st.session_state.chat_history) > 10:
    st.session_state.chat_history.pop(0)

# Affichage de l'historique des échanges
for sender, message in st.session_state.chat_history:
    if sender == "Vous":
        st.markdown(f'**{sender}:** {message}')
    else:
        st.markdown(f'*{sender}:* {message}')

# Ajout d'un bouton pour réinitialiser l'historique
if st.button('Réinitialiser'):
    st.session_state.chat_history = []

# Ajout d'une fonctionnalité simple pour télécharger des fichiers
st.write("Téléchargez un fichier ci-dessous :")
uploaded_file = st.file_uploader("Choisissez un fichier", type=['txt', 'csv', 'png', 'jpg'])

if uploaded_file is not None:
    # Afficher un message de confirmation de l'upload
    st.success(f"Fichier {uploaded_file.name} téléchargé avec succès !")

