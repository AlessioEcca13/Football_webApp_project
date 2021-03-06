# Recruitment Player Tool :soccer:


#### Progetto realizzato per il corso di Football Data Intelligence organizzato da Sics in collaborazione con Soccerment.


:bar_chart: Per la realizzazione dello stesso sono stati utilizzati 3 differenti dataset di elevata qualitÃ :
- metriche tecniche (SICS)
- metriche avanzate (Soccerment)
- prestazione fisica (Skillcorner)
In aggiunta a questi e' stato eseguito inoltre dello scraping su:
- Transfermarket (per recuperare info della bio e le immagini )
- Capology (stipendio annuale + info) :bar_chart:

Per l' analisi sono state utilizzate tutte le metriche scalate e normalizzate su 90 minuti.
Si e' optato inoltre per il non utilizzo dei portieri ( In ottica similarita' posseggono caratteristiche troppo differenti dai giocatori di movimento  ) 

:heavy_exclamation_mark: :bulb: **Nota:** I valori di similaritÃ  tra i giocatori sono stati calcolati basandosi strettamente su un '**output di tipo statistico sulle circa 300 features a disposizione per i giocatori** 

:snake: E' stata infatti condotta in primis un'analisi delle componenti principali (PCA) in modo da andare a ridurre la dimensionalitÃ  del campione. Successivamente il sistema di raccomandazione e' stato creato mediante una cluster analysis condotta tramite l'utilizzo di K-Means e della cosine similarity.

Click to view:  https://share.streamlit.io/alessioecca13/football_webapp_project/main/web_app.py

Per ulteriori informazioni :email: ecca13@hotmail.it
