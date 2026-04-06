import streamlit as st
import requests
import json

# Configuración premium de Streamlit
st.set_page_config(page_title="Smart Chat Assistant", page_icon="💬", layout="wide")

st.markdown("""
<style>
    .stChatFloatingInputContainer { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .phase-badge { 
        font-size: 0.8rem; 
        background-color: #3b3b3b; 
        padding: 2px 8px; 
        border-radius: 10px; 
        color: #ddd; 
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("💬 Smart Chat Assistant")
st.caption("Conversación con Pipeline Inteligente (Llama 3.2)")

# Configuración de API
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

def stream_ollama_chat(messages, model):
    """Generador para interactuar con la API de Chat de Ollama con streaming"""
    payload = {
        "model": model,
        "messages": messages,
        "stream": True
    }
    try:
        response = requests.post(OLLAMA_CHAT_URL, json=payload, stream=True, timeout=60)
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if not chunk.get("done"):
                        yield chunk.get("message", {}).get("content", "")
        else:
            yield f"Error de API: {response.status_code}"
    except Exception as e:
        yield f"Error de conexión: {str(e)}"

# Inicialización de estado de sesión para el historial
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Ajustes")
    model_name = st.text_input("Modelo", "llama3.2")
    st.info("💡 Este chatbot analiza y pule cada respuesta internamente antes de finalizar.")
    if st.button("Limpiar Chat"):
        st.session_state.messages = []
        st.rerun()

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de Usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Lógica del Asistente con Pipeline
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # FASE 1: ANÁLISIS (Interno)
        with st.status("Fase 1: Analizando contexto...", expanded=False) as status:
            analysis_msg = [{"role": "user", "content": f"Analiza esta consulta en el contexto de nuestra charla: {prompt}. Responde con tu estrategia en una frase."}]
            analysis = ""
            for chunk in stream_ollama_chat(analysis_msg, model_name):
                analysis += chunk
            st.write(f"**Estrategia:** {analysis}")
            status.update(label="Análisis completado ", state="complete")

        # FASE 2: GENERACIÓN PRINCIPAL (Visible & Streaming)
        with st.status("Fase 2: Redactando respuesta...", expanded=True) as status_gen:
            # La generación principal usa st.session_state.messages (historial)
            for chunk in stream_ollama_chat(st.session_state.messages, model_name):
                full_response += chunk
                placeholder.markdown(full_response + "▌")
            
            if not full_response:
                full_response = "Lo siento, no he podido generar una respuesta ahora mismo."
                
            placeholder.markdown(full_response)
            status_gen.update(label="Respuesta principal generada ✅", state="complete", expanded=False)
        
        # FASE 3: REFINAMIENTO (Post-procesamiento)
        with st.expander("Fase 3: Ver optimización y notas"):
            refine_msg = [{"role": "user", "content": f"Mejora ligeramente la estructura de esta respuesta (sin cambiar el sentido): {full_response}"}]
            st.write_stream(stream_ollama_chat(refine_msg, model_name))

    # Guardar respuesta del asistente en el historial
    st.session_state.messages.append({"role": "assistant", "content": full_response})
