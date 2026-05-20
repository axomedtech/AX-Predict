# Step 1
mysql -u root -p < db/setup.sql
mysql -u root -p < db/setup.sql

# Step 2
pip install -r requirements.txt

# Step 3
python src/train_model.py

# Step 4
python src/predict.py

# Step 5
python -m patient_manager.view_patients

# Step 6
python -m flask_app.app

# Step 7
http://127.0.0.1:5000/
http://127.0.0.1:5000/admin

