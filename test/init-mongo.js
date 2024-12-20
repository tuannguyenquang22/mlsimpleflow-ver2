db = db.getSiblingDB('mlsimpleflow_gateway');
db.createCollection('user');
db.createCollection('token');

db = db.getSiblingDB('mlsimpleflow_dataset');
db.createCollection('datasets');

db = db.getSiblingDB('mlsimpleflow_model');
db.createCollection('tasks');
db.createCollection('results');