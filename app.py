from flask import Flask, jsonify, request, Response 
from service import get_knowledge, add_knowledge, get_allKnowledge
from exceptions import DublicateException

app = Flask(__name__, template_folder="templates")

produse = [
     {"id": 1, "nume": "Laptop", "pret": 3500},
     {"id": 2, "nume": "Mouse", "pret": 150}
]


@app.route('/', methods=['GET'])
def home():
    return "Bine ai venit in API-ul meu!"

@app.route('/test-diacritice', methods=['GET'])
def test_diacritice():
    return Response("șțăîâ - diacritice OK", content_type="text/plain; charset=utf-8")

@app.route('/produse', methods=['GET'])
def get_produse():
    try:
        content = get_allKnowledge()
        if not content:
            return jsonify({"eroare": "Nu exista produse"})
        return jsonify(content)
    except Exception as e:
        return jsonify({"eroare": str(e)}), 500

@app.route('/produse/<int:produs_id>', methods=['GET'])
def get_produs(produs_id):
    try:
        content = get_knowledge(produs_id) #Extragem un produs din baza de date
        if not content:
            return jsonify({"eroare": "Produsul nu a fost gasit"})
        return jsonify(content)
    except Exception as e:
        return jsonify({"eroare": str(e)}), 200
    

@app.route('/add_produs/', methods=['POST'])
def add_produs():
    date_primite = request.get_json()
    if not date_primite:
        return jsonify({"eroare": "Lipsesc datele complet"}), 400
    
    nume_nou = date_primite.get('nume')
    pret_nou = date_primite.get('pret')
    if not nume_nou or not pret_nou:
        return jsonify({"eroare": "Lipsesc date (nume sau pret)"}), 400
    
    next_id = max([p['id'] for p in produse], default=0) + 1
    try: #Exception handling, blocul de cod "asculta" exceptii(erori) si returneaza in functie de eroare
        item = add_knowledge(nume_nou, pret_nou)
        return jsonify({
            "message": "Produsul a fost adăugat",
            "data": item
        }), 201
    except Exception as e: #Nu se mai returneaza obiectul, ci doar eroarea
        return jsonify({"eroare": str(e)}), 409 #str "intreaba" obiectul daca are o metoda de string. foarte interesant
    #clasa Exception, pe care o mosteneste, contine astfel de metoda
    nou_produs = {
        "id": next_id,
        "nume": nume_nou,
        "pret": pret_nou
}

    produse.append(nou_produs)
    return jsonify(nou_produs), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)



