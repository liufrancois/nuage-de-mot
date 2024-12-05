from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)

nlp = spacy.load("fr_core_news_sm")

motVide = []

def mot_vide():
    with open("mot_vide.txt", mode="r", encoding="utf-8") as f:
        mot = f.readline()
        while mot:
            motVide.append(mot.strip())
            mot = f.readline()
    print(motVide)

@app.route('/projet', methods=['POST'])
def lemmatize():
    data = request.json
    texte = data.get("text", "")
    texte += " "
    
    if not texte:
        return jsonify({"error": "Aucun texte reçu."}), 400
    
    inutile = ["?", ".", ";", ",", "!", "(", ")", "'", "\"", " ", "", "‘", "’", "*", "\n", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
               "<", ">", ":", "=", "#", "$", "%", "&", "/", "\\", "|", "{", "}", "[", "]", "~", "^", "`", "+", "_", "@", "©", "€", "°", "§"]
    
    occurence = {}
    mot = ""
    # J'ai choisi de vérifier caractère par caractère (même si c'est moins optimisé) 
    # car je n'étais pas sûr de ce que l'on avait le droit d'utiliser, comme les 
    # expressions régulières ou la méthode .split().
    for caractere in texte.lower():
        # Si le mot n'est pas terminé ajouté le caractére
        if caractere not in inutile:
            mot += caractere
        # Si le mot est terminé le lematiser et l'ajouter au dictionnaire
        else:
            # Lematiser les mot du texte
            doc = nlp(mot)
            lemmes = [token.lemma_ for token in doc]
            mot = lemmes[0].strip() if lemmes else mot
            if len(mot) > 2 and mot not in motVide:
                occurence[mot] = occurence.get(mot, 0) + 1
            mot = ""
    # trié dans l'ordre décroissant et ne prendre que les 50 premiers
    occurence = sorted(occurence.items(), key=lambda item: item[1], reverse=True)
    #print(occurence)
    occurence = dict(occurence[:80])
    print(f"{occurence}")

    # Retourner les occurrences en format JSON
    return jsonify(occurences=occurence)

if __name__ == "__main__":
    mot_vide()
    app.run(debug=True)
