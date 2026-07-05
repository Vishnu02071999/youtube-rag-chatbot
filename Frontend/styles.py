def load_css():
    return """
    <style>

    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Hide Streamlit default menu and footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main App */
    .stApp {
        background:
            linear-gradient(
            180deg,
            #0E1117 0%,
            #111827 100%
            );
    }

    

    /* Chat bubble (Assistant) */
    .assistant-message {
        background-color: #1F2937;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: white;
    }

    /* Chat bubble (User) */
    .user-message {
        background-color: #2563EB;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: white;
    }

    /* Timestamp */
    .timestamp {
        color: #FFD700;
        font-size: 14px;
        margin-top: 8px;
    }

    /* Sidebar title */
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Smooth Fade Animation */

    @keyframes fadeIn {

        from {
            opacity: 0;
            transform: translateY(10px);
        }

        to {
            opacity: 1;
            transform: translateY(0px);
        }

    }

    .assistant-message,
    .user-message {

        animation: fadeIn 0.3s ease-in-out;

    }

    /* ==========================================
   HERO SECTION
========================================== */

.hero{

    display:flex;

    flex-direction:column;

    align-items:center;

    justify-content:center;

    height:75vh;

    animation:fadeIn .5s ease;

}

/* ==========================================
   Camera Icon
========================================== */

.hero-icon{

    font-size:85px;

    margin-bottom:20px;

    animation:pulse 2s infinite ease-in-out;

    text-shadow:
        0 0 10px #ff0000,
        0 0 20px #ff0000,
        0 0 40px #ff0000;

}

/* ==========================================
   Main Title
========================================== */

.hero-title{

    font-family:'Press Start 2P', cursive;

    font-size:40px;

    color:#FF0000;

    text-align:center;

    line-height:1.4;

    text-shadow:
        0 0 6px #ff0000,
        0 0 12px #ff0000,
        0 0 24px #ff0000,
        0 0 42px #ff4d4d,
        0 0 70px #ff4d4d;

}

/* ==========================================
   Subtitle
========================================== */

.hero-subtitle{

    color:#D0D0D0;

    font-size:20px;

    margin-top:25px;

    text-align:center;

    line-height:1.8;

}

/* ==========================================
   Divider
========================================== */

.hero-divider{

    width:250px;

    height:3px;

    background:#FF0000;

    margin-top:30px;

    margin-bottom:30px;

    box-shadow:
        0 0 10px #ff0000,
        0 0 20px #ff0000;

}

/* ==========================================
   Pulse Animation
========================================== */

@keyframes pulse{

    0%{

        transform:scale(1);

        text-shadow:
            0 0 10px #ff0000,
            0 0 20px #ff0000;

    }

    50%{

        transform:scale(1.08);

        text-shadow:
            0 0 20px #ff0000,
            0 0 40px #ff0000,
            0 0 60px #ff0000;

    }

    100%{

        transform:scale(1);

        text-shadow:
            0 0 10px #ff0000,
            0 0 20px #ff0000;

    }

}
/* ==========================================
   Welcome Card
========================================== */

.welcome-card{

    background:#161B22;

    border:1px solid #30363D;

    border-radius:15px;

    padding:20px;

    color:white;

    text-align:center;

    margin-bottom:25px;

}
/* ==========================================
   Instructions Card
========================================== */

.instructions{

    width:650px;

    max-width:90%;

    background:#161B22;

    border:1px solid #30363D;

    border-radius:18px;

    padding:30px;

    margin-top:35px;

    text-align:center;

    color:white;

    font-size:18px;

    line-height:2;

    box-shadow:
        0 0 20px rgba(255,0,0,.15);

}

.instructions span{

    color:#FF3B3B;

    font-weight:bold;

}

</style>
    """
