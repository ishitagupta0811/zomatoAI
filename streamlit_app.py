import streamlit as st
import threading
import os
import sys

st.set_page_config(page_title="Zomato AI Backend Server", page_icon="🚀")

st.title("Zomato AI Backend Server")
st.write("This Streamlit application acts as the deployment host for the Zomato AI Backend.")

# Function to run the FastAPI server in the background
def run_fastapi():
    # Adding the project root to sys.path if needed
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if root_dir not in sys.path:
        sys.path.append(root_dir)
        
    os.system(f"{sys.executable} -m uvicorn Phase2_BackendIntegration.backend.main:app --host 0.0.0.0 --port 8000")

# Start FastAPI in a background thread so Streamlit doesn't block
if 'fastapi_started' not in st.session_state:
    st.session_state.fastapi_started = True
    threading.Thread(target=run_fastapi, daemon=True).start()

st.success("FastAPI backend initialization triggered on port 8000!")

st.markdown("""
### Deployment Info
- **Backend:** FastAPI (Running via Streamlit Cloud)
- **Frontend:** Next.js (Deployed on Vercel)
""")
