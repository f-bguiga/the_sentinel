# #!/bin/bash

# # 1. Check for Drift
# python src/monitor.py
# STATUS=$?

# # 2. If exit code is 100, trigger retraining
# if [ $STATUS -eq 100 ]; then
#     print "🔄 Starting Automated Retraining..."
#     python src/train.py
#     python src/promote_model.py
#     print "🚀 System Healed: New model is now @champion."
# else
#     print "😴 Everything is fine. No action needed."
# fi
#!/bin/bash

echo "🧐 Step 1: Data Validation..."
python src/setup_gx.py || exit 1

echo "🧪 Step 2: Training..."
python src/train.py || exit 1

echo "📦 Step 3: Promotion..."
python src/promote_model.py || exit 1

echo "🛡️ Step 4: Automated Model Testing..."
pytest tests/test_model.py || { echo "❌ Model Logic Failed!"; exit 1; }

echo "🚀 All Gates Passed! Ready for Docker Deploy."
# docker-compose up --build -d