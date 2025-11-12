# --- SES KONTROLLERİ (Ana Sayfa) ---
    col_kapat, col_ac, col_volume_slider = st.columns([1, 1, 6]) 

    if st.session_state['music_enabled']:
        with col_kapat:
            if st.button("🔊 Kapat", key="btn_kapat_ses", use_container_width=True):
                st.session_state['music_enabled'] = False
                st.rerun()
        with col_volume_slider:
            # Ses seviyesi kaydırıcısı
            new_volume = st.slider("Ses Seviyesi", 0.0, 1.0, st.session_state['music_volume'], step=0.1, key="music_volume_slider")
            if new_volume != st.session_state['music_volume']:
                st.session_state['music_volume'] = new_volume
                st.rerun()
    elif st.session_state['music_url']: 
        with col_ac:
            if st.button("🔇 Aç", key="btn_ac_ses", use_container_width=True):
                st.session_state['music_enabled'] = True
                st.rerun()
