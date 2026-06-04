#!/bin/bash

# ============================================================================
# Setup Script for Flask Application Database
# ============================================================================
# This script creates a PostgreSQL user, database, and tables for the Flask app
# ============================================================================

# Set variables at the top - makes it easy to change values
USERNAME="k29"
PASSWORD="1234"
DATABASE="flaskdb"
POSTGRES_USER="postgres"  # Default PostgreSQL admin user
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
APP_FILE="myapp.py"

# Color output for better readability (optional)
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ">>> Creating Python virutal enviroment..."
python3 -m venv .venv

echo ">>> Activating virtual environment..."
source .venv/bin/activate

echo ">>> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}Starting database setup...${NC}"

# ============================================================================
# Step 1: Create PostgreSQL User
# ============================================================================
echo "Creating user '$USERNAME' with password '$PASSWORD'..."

# Use sudo to run as postgres user, then use psql (PostgreSQL command line)
# The -c flag allows us to run a single SQL command
sudo -u $POSTGRES_USER psql -c "CREATE USER $USERNAME WITH PASSWORD '$PASSWORD';"

# Check if the command succeeded (exit code 0 means success)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ User created successfully${NC}"
else
    echo -e "${RED}✗ Failed to create user or user already exists${NC}"
fi

# ============================================================================
# Step 2: Create Database
# ============================================================================
echo "Creating database '$DATABASE'..."

# Create the database owned by the user we just created
sudo -u $POSTGRES_USER psql -c "CREATE DATABASE $DATABASE OWNER $USERNAME;" 2>/dev/null || echo "Database may already exist"

# Grant schema privileges so k29 can create tables
sudo -u $POSTGRES_USER psql -d $DATABASE -c "GRANT CREATE ON SCHEMA public TO $USERNAME;"
sudo -u $POSTGRES_USER psql -d $DATABASE -c "GRANT USAGE ON SCHEMA public TO $USERNAME;"

echo -e "${GREEN}✓ Database created/ready${NC}"


# ============================================================================
# Step 3: Execute SQL Scripts to Create Tables and Insert Data
# ============================================================================
echo "Creating tables and inserting sample data..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SQL_DIR="$SCRIPT_DIR/sql_scripts"

# Check if sql_scripts directory exists
if [ ! -d "$SQL_DIR" ]; then
    echo -e "${RED}✗ SQL scripts directory not found at $SQL_DIR${NC}"
    exit 1
fi

# Array of SQL files to execute (in order of dependency)
# First create tables, then insert sample data
SQL_FILES=(
    "flusers.sql"
    "albums.sql"
    "photos.sql"
    "flfriends.sql"
    "comments.sql"
    "tags.sql"
    "phototags.sql"
    "likes.sql"
    "insert_users.sql"
    "insert_albums.sql"
    "insert_photos.sql"
    "insert_friends.sql"
    "insert_tags.sql"
    "insert_phototags.sql"
    "insert_comments.sql"
    "insert_likes.sql"
)

# Loop through each SQL file and execute it
# Run as the k29 user to ensure proper table ownership
for sql_file in "${SQL_FILES[@]}"; do
    file_path="$SQL_DIR/$sql_file"
    
    # Check if file exists before running
    if [ -f "$file_path" ]; then
        echo "  - Executing $sql_file..."
        # Execute the SQL file as the k29 user on the flaskdb database
        # Use PGPASSWORD to provide password without prompting
        PGPASSWORD=$PASSWORD psql -h $DATABASE_HOST -p $DATABASE_PORT -U $USERNAME -d $DATABASE -f "$file_path"
        
        if [ $? -eq 0 ]; then
            echo -e "    ${GREEN}✓ $sql_file executed${NC}"
        else
            echo -e "    ${RED}✗ Failed to execute $sql_file${NC}"
        fi
    else
        echo -e "    ${RED}✗ File not found: $file_path${NC}"
    fi
done

# ============================================================================
# Step 4: Grant Privileges (Optional but recommended)
# ============================================================================
echo "Granting privileges to user '$USERNAME'..."

sudo -u $POSTGRES_USER psql -d $DATABASE -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $USERNAME;"
sudo -u $POSTGRES_USER psql -d $DATABASE -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $USERNAME;"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Privileges granted${NC}"
fi

# ============================================================================
# Completion Message
# ============================================================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Database name: $DATABASE"
echo "Username: $USERNAME"
echo "Password: $PASSWORD"
echo ""
echo "You can now connect with:"
echo "  psql -U $USERNAME -d $DATABASE -h localhost"
echo ""
echo " Starting Flask application on http://127.0.0.1:5000"
python3 $APP_FILE