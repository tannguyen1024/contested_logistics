from flask import (
    Flask,
    request,
    render_template,
    Response,
    jsonify,
)
import math

app = Flask(__name__, static_folder="static")

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

ROUTES_DATA = {
    "option1": [
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
    ],
    "option2": [
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
    ],
    "option3": [
        {
            "type": "tank",
            "ammo": 2,
            "food": 3,
            "fuel": 3,
            "route": [[383, 605], [342, 794]],
        },
        {
            "type": "plane",
            "ammo": 3,
            "food": 2,
            "fuel": 1,
            "route": [[269, 324], [160, 297]],
        },
    ],
}


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/reset", methods=["POST"])
def reset_nodes():
    global nodes
    global ROUTES_DATA
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
    ROUTES_DATA = {
        "option1": [
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
        ],
        "option2": [
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
        ],
        "option3": [
            {
                "type": "tank",
                "ammo": 2,
                "food": 3,
                "fuel": 3,
                "route": [[383, 605], [342, 794]],
            },
            {
                "type": "plane",
                "ammo": 3,
                "food": 2,
                "fuel": 1,
                "route": [[269, 324], [160, 297]],
            },
        ],
    }
    return jsonify({"message": "Nodes reset to default"})


@app.route("/api/routes")
def get_routes():
    scenario = request.args.get("scenario", "default")
    data = ROUTES_DATA.get(scenario, [])
    return jsonify(data)


# ADD NODES / VERTICES
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


@app.route("/api/nodes")
def get_points():
    global nodes
    threshold = 250  # minimum edge distance by pixel between two nodes
    edges = []

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if distance(nodes[i]["coords"], nodes[j]["coords"]) <= threshold:
                edges.append({"from": nodes[i]["coords"], "to": nodes[j]["coords"]})

    return jsonify({"nodes": nodes, "edges": edges})


@app.route("/api/continue", methods=["POST"])
def continue_scenario():
    global nodes
    global ROUTES_DATA
    data = request.get_json()
    selected_scenario = data.get("selectedScenario")

    if not selected_scenario:
        return jsonify({"error": "No scenario selected"}), 400

    print("Received scenario:", selected_scenario)

    if selected_scenario == "option1":
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
            # {"coords": [426, 381], "type": "conflict", "label": "Conflict 1"},
            {"coords": [342, 794], "type": "conflict", "label": "Conflict 2"},
            {"coords": [145, 530], "type": "conflict", "label": "Conflict 3"},
            {"coords": [160, 297], "type": "conflict", "label": "Conflict 4"},
        ]
        ROUTES_DATA = {
            "option1": [
                {
                    "type": "tank",
                    "ammo": 2,
                    "food": 1,
                    "fuel": 1,
                    "route": [[309, 238], [195, 392]],
                },
                {
                    "type": "tank",
                    "ammo": 1,
                    "food": 1,
                    "fuel": 3,
                    "route": [[383, 605], [342, 794]],
                },
            ],
            "option2": [
                {
                    "type": "tank",
                    "ammo": 3,
                    "food": 7,
                    "fuel": 2,
                    "route": [[309, 238], [235, 278]],
                },
                {
                    "type": "boat",
                    "ammo": 1,
                    "food": 3,
                    "fuel": 1,
                    "route": [[309, 238], [269, 324]],
                },
            ],
            "option3": [
                {
                    "type": "tank",
                    "ammo": 2,
                    "food": 3,
                    "fuel": 3,
                    "route": [[217, 733], [342, 794]],
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
            ],
        }
    elif selected_scenario == "option2":
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
            {"coords": [375, 125], "type": "conflict", "label": "Conflict 5"},
        ]
        ROUTES_DATA = {
            "option1": [
                {
                    "type": "plane",
                    "ammo": 2,
                    "food": 1,
                    "fuel": 1,
                    "route": [[241, 546], [145, 530]],
                },
                {
                    "type": "tank",
                    "ammo": 1,
                    "food": 1,
                    "fuel": 3,
                    "route": [[383, 605], [342, 794]],
                },
            ],
            "option2": [
                {
                    "type": "tank",
                    "ammo": 3,
                    "food": 7,
                    "fuel": 2,
                    "route": [[309, 238], [235, 278]],
                },
                {
                    "type": "plane",
                    "ammo": 1,
                    "food": 3,
                    "fuel": 1,
                    "route": [[449, 237], [375, 125]],
                },
            ],
            "option3": [
                {
                    "type": "tank",
                    "ammo": 2,
                    "food": 3,
                    "fuel": 3,
                    "route": [[217, 733], [426, 381]],
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
            ],
        }
    elif selected_scenario == "option3":
        nodes = [
            {"coords": [449, 237], "type": "airstrip", "label": "Airstrip 1"},
            {"coords": [217, 733], "type": "airstrip", "label": "Airstrip 2"},
            {"coords": [383, 605], "type": "conflict", "label": "Conflict 1"},
            {"coords": [160, 623], "type": "port", "label": "Port 1"},
            {"coords": [235, 278], "type": "port", "label": "Port 2"},
            {"coords": [309, 238], "type": "port", "label": "Port 3"},
            {"coords": [195, 392], "type": "port", "label": "Port 4"},
            {"coords": [241, 546], "type": "rendezvous", "label": "Rendezvous 1"},
            {"coords": [269, 324], "type": "rendezvous", "label": "Rendezvous 2"},
            # {"coords": [426, 381], "type": "conflict", "label": "Conflict 1"},
            {"coords": [342, 794], "type": "conflict", "label": "Conflict 2"},
            {"coords": [145, 530], "type": "conflict", "label": "Conflict 3"},
            {"coords": [160, 297], "type": "conflict", "label": "Conflict 4"},
        ]
        ROUTES_DATA = {
            "option1": [
                {
                    "type": "tank",
                    "ammo": 2,
                    "food": 1,
                    "fuel": 1,
                    "route": [[309, 238], [195, 392]],
                }
            ],
            "option2": [
                {
                    "type": "boat",
                    "ammo": 1,
                    "food": 3,
                    "fuel": 1,
                    "route": [[269, 324], [145, 530]],
                },
            ],
            "option3": [
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
            ],
        }

    return jsonify({"message": f"Scenario {selected_scenario} received"}), 200


# DIRAC CHOOSES RECOMMENDATION
@app.route("/api/recommendation")
def recommend():
    recommended = get_recommended_option()
    return jsonify({"recommended": recommended})


# RECOMMENDED BASED ON TOTAL FUEL
def get_recommended_option():
    totals = {}
    for option, routes in ROUTES_DATA.items():
        total_fuel = sum(r["fuel"] for r in routes)
        totals[option] = total_fuel
    recommended = min(totals, key=totals.get)
    return recommended


# CONTACT US
@app.route("/contact")
def contact_html():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
