#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Create a run script
echo '#!/bin/bash
source venv/bin/activate
streamlit run main.py' > run.sh

# Make scripts executable
chmod +x run.sh

echo "Setup complete! You can now run the application by double-clicking run.sh" 