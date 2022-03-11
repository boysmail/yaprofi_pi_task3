from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

promos = [
    {"id": 1,
     "name": "Promo 1",
     "description": "Description 1",
     "prizes": [
         {
             "id": 1,
             "description": "Prize description"
         }
     ],
     "participants": [
         {
             "id": 1,
             "name": "Anton"
         }
     ]},
    {"id": 2, "name": "Promo 2", "description": "Description 1", "prizes": [], "participants": []},
]

categories = [
    {"id": 1, "name": "Cat 1"},
    {"id": 2, "name": "Cat 2"},
]


def error(error_id):
    if error_id == 404:
        return make_response(jsonify({"error": "Not Found"}), 404)
    elif error_id == 400:
        return make_response(jsonify({"error": "Bad Request"}), 400)
    elif error_id == 409:
        return make_response(jsonify({"error": "Conflict"}), 409)


@app.route('/')
def hello_world():
    return 'Hello World!'


# done
@app.route('/promo', methods=['POST'])
def post_promo():
    if not request.json or not "name" in request.json:
        return error(400)
    promo = {
        "id": promos[-1]["id"] + 1,
        "name": request.json["name"],
        "description": request.json.get('description', ""),
        "prizes": [],
        "participants": []
    }
    promos.append(promo)
    return jsonify(promos[-1]["id"]), 201


# done
@app.route('/promo', methods=['GET'])
def get_promo():
    clean_promo = []
    for i in range(len(promos)):
        clean_promo.append({
            "id": promos[i]["id"],
            "name": promos[i]["name"],
            "description": promos[i]["description"]
        }
        )
    return jsonify(clean_promo)


# done
@app.route('/promo/<int:promo_id>', methods=['GET'])
def get_promo_by_id(promo_id):
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    if len(promo) == 0:
        return error(404)
    return jsonify(promo)


# done
@app.route('/promo/<int:promo_id>', methods=['PUT'])
def put_promo_by_id(promo_id):
    if not request.json:
        return error(400)
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    if len(promo) == 0 or request.json.get("name") == "":
        return error(404)

    promo[0]["name"] = request.json.get("name", promo[0]["name"])
    promo[0]["description"] = request.json.get("description", promo[0]["description"])
    return jsonify(promo), 202


# done
@app.route('/promo/<int:promo_id>', methods=['DELETE'])
def delete_product_by_id(promo_id):
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    if len(promo) == 0:
        return error(404)
    promos.remove(promo[0])
    return jsonify({"result": True})

# done
@app.route('/promo/<int:promo_id>/participant', methods=['POST'])
def post_participant_by_promo(promo_id):
    if not request.json or not "name" in request.json:
        return error(400)
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    participant = {
        "id": promo[0]["participants"][-1]["id"] + 1,
        "name": request.json["name"],
    }
    promo[0]["participants"].append(participant)
    return jsonify(promo[0]["participants"][-1]["id"]), 201

#done
@app.route('/promo/<int:promo_id>/participant/<int:participant_id>', methods=['DELETE'])
def delete_participant_by_id(promo_id, participant_id):
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    if len(promo) == 0:
        return error(404)
    participant = list(filter(lambda tmp: tmp['id'] == participant_id, promo[0]["participants"]))
    if len(participant) == 0:
        return error(404)

    promo[0]["participants"].remove(participant[0])
    return jsonify({"result": True})

# done
@app.route('/promo/<int:promo_id>/prize', methods=['POST'])
def post_prize_by_promo(promo_id):
    if not request.json or not "description" in request.json:
        return error(400)
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    prize = {
        "id": promo[0]["prizes"][-1]["id"] + 1,
        "description": request.json["description"]
    }
    promo[0]["prizes"].append(prize)
    return jsonify(promo[0]["prizes"][-1]["id"]), 201


@app.route('/promo/<int:promo_id>/prize/<int:prize_id>', methods=['DELETE'])
def delete_prize_by_id(promo_id, prize_id):
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    if len(promo) == 0:
        return error(404)
    prize = list(filter(lambda tmp: tmp['id'] == prize_id, promo[0]["prizes"]))
    if len(prize) == 0:
        return error(404)

    promo[0]["prizes"].remove(prize[0])
    return jsonify({"result": True})


@app.route('/promo/<int:promo_id>/raffle', methods=['POST'])
def raffle(promo_id):
    promo = list(filter(lambda tmp: tmp['id'] == promo_id, promos))
    if len(promo[0]["participants"]) != len(promo[0]["prizes"]):
        error(409)
    else:
        winner_list = []




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
