from flask import Flask,jsonify,request,make_response,Response
from mongo_module import Mongo

connection_string="mongodb://localhost:27017"
app=Flask(__name__)
mongo=Mongo(connection_string)

@app.route("/create",methods=["POST"])
def create():
    try:
        if mongo.create(data=request.json["data"]):
            return jsonify({"result": "success"}), 201
        else:
            return jsonify({"result": "failed"}), 304
    except Exception as e:
        print(f"create :: error occured :: {e}")
        return jsonify({"result": "failed"}), 500

@app.route("/delete/<string:task_id>",methods=["DELETE"])
def delete(task_id):
    try:
        if mongo.delete(task_id=task_id):
            return jsonify({"result": "success"}), 201
        else:
            return jsonify({"result": "failed"}), 304
    except Exception as e:
        print(f"create :: error occured :: {e}")
        return jsonify({"result": "failed"}), 500

@app.route("/update/<string:task_id>",methods=["PUT"])
def update(task_id):
    try:
        result = mongo.update(task_id = task_id, data=request.json["data"])
        if result:
            return jsonify({"result":"success"}), 201
        elif result == None:
            return jsonify({"result":"file not found"}), 404
        else:
            return jsonify({"result":"failed"}), 304
    except Exception as e:
        print(f"update :: error occured :: {e}")
        return jsonify({"result":"failed"}), 500
    

@app.route("/record/<string:task_id>",methods=["GET"])
def record(task_id):
    try:
        result = mongo.record(task_id = task_id)
        if result:
            return jsonify({"Record":result})
        else:
            return jsonify({"Record":"file not found"}), 404
    except Exception as e:
        print(f"update :: error occured :: {e}")
        return jsonify({"result":"failed"}), 500
            

@app.route("/task",methods=["GET"])
def list():
    try:
        result=mongo.list()
        return jsonify({"List_of_all_data": result})
    except Exception as e:
        print(f"list :: error occured :: {e}")
        return jsonify({"r esult": "NOT WORKING"}), 500


if __name__=="__main__":
    app.run(host="0.0.0.0",port=9000,debug=True)



