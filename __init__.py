from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)
def sauvegarder_donnees(resultats):
    with open('resultats_electeurs.csv', 'a', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        if fichier.tell() == 0:  # Écrit l'en-tête si le fichier est vide
            writer.writerow(['Clé', 'Valeur'])
        for key, value in resultats.items():
            writer.writerow([key, value])
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        NOM = request.form['fname']
        PRENOM = request.form['lname']
        JOUR_DE_NAISSANCE = request.form['jour_de_naissance']
        MOIS_DE_NAISSANCE = request.form['mois_de_naissance']
        ANNEE_DE_NAISSANCE = request.form['annee_de_naissance']
        
        the_data = f"nomfamille={NOM}&prenom={PRENOM}&jour={JOUR_DE_NAISSANCE}&mois={MOIS_DE_NAISSANCE}&annee={ANNEE_DE_NAISSANCE}&search_cei_individu=Lancer+la+recherche"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        response = requests.post("https://cei.ci/liste-electorale-definitive-2023/", data=the_data, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        RESULTATS_ELECTEURS = soup.select("div.elementor-shortcode")[1].select('h6')
        
        RESULTATS = {}
        for res in RESULTATS_ELECTEURS:
            KEY = res.text.split(":")[0].strip()
            VALUE = res.text.split(":")[1].strip() if ":" in res.text else ""
            RESULTATS[KEY] = VALUE
        
        if RESULTATS:  # Vérifie si des résultats ont été trouvés
            sauvegarder_donnees(RESULTATS)
            resultat_html = '<br>'.join([f'{key}: {value}' for key, value in RESULTATS.items()])
            return render_template('notfound.html', title="resultat" , resultat=resultat_html)
        else:
            return redirect(url_for('inscription'))
    return render_template('home.html', title="Bienvenue sur le projet de Karamoko DIABY")





@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Logique pour traiter les données d'inscription ici
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('inscription.html', title="Inscription")


if __name__ == '__main__':
    app.run(debug=True)

