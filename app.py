from flask import (
    Flask,
    request,
    render_template,
    Response,
    jsonify,
)
import math

app = Flask(__name__, static_folder="static")


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/routes")
def get_routes():
    scenario = request.args.get("scenario", "default")

    if scenario == "option1":
        data = [
            {
                "type": "tank",
                "ammo": 2,
                "food": 1,
                "fuel": 1,
                "route": [[449, 237], [426, 381]],
            },
            {
                "type": "tank",
                "ammo": 1,
                "food": 1,
                "fuel": 3,
                "route": [[449, 237], [309, 238]],
            },
        ]
    elif scenario == "option2":
        data = [
            {
                "type": "boat",
                "ammo": 3,
                "food": 7,
                "fuel": 2,
                "route": [[235, 278], [269, 324]],
            },
            {
                "type": "plane",
                "ammo": 1,
                "food": 3,
                "fuel": 1,
                "route": [[217, 733], [160, 623]],
            },
            {
                "type": "plane",
                "ammo": 3,
                "food": 6,
                "fuel": 2,
                "route": [[383, 605], [241, 546]],
            },
        ]
    elif scenario == "option3":
        data = [
            {
                "type": "tank",
                "ammo": 2,
                "food": 3,
                "fuel": 3,
                "route": [[383, 605], [426, 381]],
            },
            {
                "type": "boat",
                "ammo": 3,
                "food": 2,
                "fuel": 1,
                "route": [[217, 733], [241, 546]],
            },
            {
                "type": "plane",
                "ammo": 3,
                "food": 2,
                "fuel": 2,
                "route": [[449, 237], [269, 324]],
            },
        ]

    return jsonify(data)


# ADD NODES / VERTICES
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


@app.route("/api/nodes")
def get_points():
    nodes = [
        {"coords": [449, 237], "type": "airstrip", "label": "Airstrip 1"},
        {"coords": [217, 733], "type": "airstrip", "label": "Airstrip 2"},
        {"coords": [383, 605], "type": "airstrip", "label": "Airstrip 3"},
        {"coords": [160, 623], "type": "port", "label": "Port 1"},
        {"coords": [235, 278], "type": "port", "label": "Port 2"},
        {"coords": [309, 238], "type": "port", "label": "Port 3"},
        {"coords": [195, 392], "type": "port", "label": "Port 4"},
        {"coords": [241, 546], "type": "rendezvous", "label": "Rendezvous 1"},
        {"coords": [269, 324], "type": "rendezvous", "label": "Rendezvous 2"},
        {"coords": [426, 381], "type": "conflict", "label": "Conflict 1"},
        {"coords": [342, 794], "type": "conflict", "label": "Conflict 2"},
        {"coords": [145, 530], "type": "conflict", "label": "Conflict 3"},
        {"coords": [160, 297], "type": "conflict", "label": "Conflict 4"},
    ]

    threshold = 250  # minimum edge distance by pixel between two nodes
    edges = []

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if distance(nodes[i]["coords"], nodes[j]["coords"]) <= threshold:
                edges.append({"from": nodes[i]["coords"], "to": nodes[j]["coords"]})

    return jsonify({"nodes": nodes, "edges": edges})


# @app.route("/api/all_routes")
# def get_all_routes():
#     return jsonify(
#         {
#             "scenario1": [
#                 {
#                     "type": "plane",
#                     "ammo": 10,
#                     "food": 5,
#                     "fuel": 3,
#                     "route": [[358, 805], [450, 624], [231, 536], [151, 360]],
#                 },
#                 ...,
#             ],
#             "scenario2": [
#                 {
#                     "type": "tank",
#                     "ammo": 6,
#                     "food": 4,
#                     "fuel": 2,
#                     "route": [[358, 805], [217, 733], [150, 631]],
#                 },
#                 ...,
#             ],
#             "scenario3": [
#                 {
#                     "type": "boat",
#                     "ammo": 3,
#                     "food": 6,
#                     "fuel": 2,
#                     "route": [port2, conflict3, rendezvous1, street2],
#                 },
#                 ...,
#             ],
#         }
#     )


# TIME & FREQUENCY
# @app.route("/taking_data")
# def run_taking_data():
#     com_port = str(request.args.get("com_port", "COM3"))
#     delay = float(request.args.get("delay", 14.25))
#     resolution = float(request.args.get("resolution", 10000))
#     acquisition = float(request.args.get("acquisition", 20))
#     Index, Counts, f, FCounts = taking_data.main(
#         com_port, delay, resolution, acquisition
#     )

#     # CREATE JSON AND SEND PLOT DATA TO FRONT END
#     return jsonify(
#         {
#             "time": {"x": Index.tolist(), "y": Counts.tolist()},
#             "freq": {
#                 "x": f[len(f) // 2 :].tolist(),
#                 "y": FCounts[len(FCounts) // 2 :].tolist(),
#             },
#         }
#     )


# DELAY SCAN
# @app.route("/find_target")
# def stream_find_target():
#     com_port = str(request.args.get("com_port", "COM3"))
#     d_min = float(request.args.get("d_min", 8))
#     d_max = float(request.args.get("d_max", 12))
#     d_int = float(request.args.get("d_int", 0.2))
#     acquisition = float(request.args.get("acquisition", 20))

#     # STREAM IN DATA TO FRONT END
#     def generate():
#         yield from find_target.main(com_port, d_min, d_max, d_int, acquisition)

#     return Response(generate(), mimetype="text/event-stream")


# CONTACT US
@app.route("/contact")
def contact_html():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
