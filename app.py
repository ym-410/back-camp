from flask import Flask, request

app = Flask(__name__)

rooms = [
        {
            "id": 1,
            "name": "Room 101",
            "capacity": 30
        },
        {
            "id": 2,
            "name": "Room 102",
            "capacity": 20
        }
]

@app.route("/hello")
def hello():
    return "Hello", 201

@app.route("/rooms")
def get_rooms():
    return rooms

@app.route("/rooms/<int:room_id>")
def get_room(room_id):
    for room in rooms:
        if room["id"] == room_id:
            return room
    return {"error": "room_not_found"}, 404

@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json()
    new_room = {
            "id": len(rooms) + 1,
            "name": data["name"],
            "capacity": data["capacity"]
    }

    rooms.append(new_room)

    return new_room, 201

if __name__ == "__main__":
    app.run(debug=True)
