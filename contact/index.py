from flask import Flask, jsonify, json, request

app = Flask(__name__)


@app.route('/contacts', methods=['GET'])
def get_contacts():
    with open('phonenumbers.json') as json_file:
        return jsonify(json.load(json_file))


@app.route("/delete/<fullname>", methods=['DELETE'])
def delete_contact(fullname):
    with open('phonenumbers.json') as json_file:
        contacts = json.load(json_file)
    if fullname in contacts:
        contacts.pop(fullname)
        with open('phonenumbers.json', 'w') as json_file:
            json.dump(contacts, json_file, indent=2)
        return jsonify(contacts)
    else:
        return "There is no contact with this fullname"


@app.route('/add', methods=['POST'])
def add_contact():
    with open('phonenumbers.json') as json_file:
        users = json.load(json_file)
        new_user = json.loads(request.data.decode("utf-8"))
        users.update(new_user)
        with open('phonenumbers.json', 'w') as json_file:
            json.dump(users, json_file, indent=2)
        return jsonify(users)


@app.route('/update', methods=['PUT'])
def update_contact():
    with open('phonenumbers.json') as json_file:
        users = json.load(json_file)
        new_user = json.loads(request.data.decode("utf-8"))
        if new_user["full_name"] in users:
            for number, change_type in new_user["changes"].items():

                if change_type[0] == "delete":
                    if number in users[new_user["full_name"]]["numbers"]:
                        users[new_user["full_name"]]["numbers"].pop(number)

                elif change_type[0] == "add":
                    users[new_user["full_name"]]["numbers"][number] = change_type[1]

                elif change_type[0] == "edit":
                    if number in users[new_user["full_name"]]["numbers"]:
                        if change_type[1] == "phone" or change_type[1] == "home":
                            users[new_user["full_name"]]["numbers"][number] = change_type[1]
                        else:
                            users[new_user["full_name"]]["numbers"][change_type[1]] = \
                                users[new_user["full_name"]]["numbers"][number]
                            users[new_user["full_name"]]["numbers"].pop(number)
            with open('phonenumbers.json', 'w') as json_file:
                json.dump(users, json_file, indent=2)
            return jsonify(users)
        else:
            return "There is no contact with this fullname"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
