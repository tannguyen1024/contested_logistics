from flask import (
    Flask,
    request,
    render_template,
    Response,
    jsonify,
)

app = Flask(__name__)
street1 = [358, 805]
street2 = [217, 733]
port1 = [150, 631]
port2 = [365, 456]
port3 = [298, 197]
port4 = [151, 360]
rendezvous1 = [231, 536]
rendezvous2 = [269, 324]
conflict1 = [450, 624]
conflict2 = [427, 444]
conflict3 = [344, 285]


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# RETURN HARDCODED JSON
@app.route("/api/routes")
def get_routes():
    scenario = request.args.get("scenario", "default")

    if scenario == "option1":
        data = [
            {
                "type": "plane",
                "ammo": 4,
                "food": 2,
                "fuel": 5,
                "route": [[358, 805], [450, 624], [231, 536], [151, 360]],
            },
            {
                "type": "boat",
                "ammo": 2,
                "food": 1,
                "fuel": 6,
                "route": [[358, 805], [217, 733], [150, 631]],
            },
            {
                "type": "tank",
                "ammo": 1,
                "food": 2,
                "fuel": 2,
                "route": [[358, 805], [365, 456], [269, 324], [298, 197]],
            },
        ]
    elif scenario == "option2":
        data = [
            {
                "type": "plane",
                "ammo": 3,
                "food": 7,
                "fuel": 2,
                "route": [street1, [450, 624], conflict2, [151, 360]],
            },
            {
                "type": "plane",
                "ammo": 5,
                "food": 3,
                "fuel": 2,
                "route": [[358, 805], [217, 733], [150, 631]],
            },
        ]
    elif scenario == "option3":
        data = [
            {
                "type": "plane",
                "ammo": 8,
                "food": 7,
                "fuel": 2,
                "route": [port3, conflict3, conflict2, conflict1, street1],
            },
            {
                "type": "boat",
                "ammo": 1,
                "food": 2,
                "fuel": 2,
                "route": [street2, [365, 456], [269, 324], port4],
            },
        ]

    return jsonify(data)


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
