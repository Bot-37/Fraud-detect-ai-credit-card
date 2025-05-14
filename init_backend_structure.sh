#!/bin/bash

# Set root directory
ROOT_DIR="backend"

# Remove old backend directory if it exists
rm -rf $ROOT_DIR

# Create directory structure
mkdir -p $ROOT_DIR/api/routes
mkdir -p $ROOT_DIR/api/schemas
mkdir -p $ROOT_DIR/app/logs
mkdir -p $ROOT_DIR/app/model
mkdir -p $ROOT_DIR/app/trainer
mkdir -p $ROOT_DIR/app/utils
mkdir -p $ROOT_DIR/app/__pycache__
mkdir -p $ROOT_DIR/data
mkdir -p $ROOT_DIR/models
mkdir -p $ROOT_DIR/__pycache__
mkdir -p $ROOT_DIR/tests

# Create empty Python files
touch $ROOT_DIR/api/__init__.py
touch $ROOT_DIR/api/routes/__init__.py
touch $ROOT_DIR/api/routes/auth.py
touch $ROOT_DIR/api/routes/transactions.py
touch $ROOT_DIR/api/schemas/transaction_schema.py

touch $ROOT_DIR/app/config.py
touch $ROOT_DIR/app/__init__.py
touch $ROOT_DIR/app/logs/fraud_detector.log
touch $ROOT_DIR/app/model/fraud_detector.py
touch $ROOT_DIR/app/__pycache__/__init__.cpython-312.pyc
touch $ROOT_DIR/app/__pycache__/fraud_detector.cpython-312.pyc
touch $ROOT_DIR/app/__pycache__/detector.cpython-312.pyc
touch $ROOT_DIR/app/trainer/trainer.py
touch $ROOT_DIR/app/utils/logger.py
touch $ROOT_DIR/app/utils/preprocessing.py
touch $ROOT_DIR/app/utils/validator.py
touch $ROOT_DIR/app/utils.py

touch $ROOT_DIR/__pycache__/__init__.cpython-312.pyc
touch $ROOT_DIR/requirements.txt
touch $ROOT_DIR/server.py
touch $ROOT_DIR/tests/test_api.py

echo "✅ Backend project structure initialized."
