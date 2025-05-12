TTLens – TTL Analyzer for Apache Cassandra

TTLens is a lightweight, web-based diagnostic tool designed to analyze TTL (Time-To-Live) behavior in Apache Cassandra and DSE clusters.

This tool helps support engineers and SREs diagnose issues related to data expiry, inconsistencies, and SLA violations by scanning TTLs at both column and table levels, and intelligently inferring row-level expiry.

⸻

Features
	•	Connects to live Cassandra clusters using the Python driver
	•	Supports .cql schema uploads for extracting table-level TTLs
	•	Scans TTL at the column level using SELECT ttl(column)
	•	Infers row-level expiry using minimum TTL or table default TTL
	•	Displays TTLs in a structured DataFrame
	•	Allows CSV export of TTL scan results
	•	Visualizes TTLs bucketed by expiry ranges (future enhancement)

⸻

Tech Stack
	•	Python
	•	Streamlit
	•	Cassandra Python Driver (cassandra-driver)
	•	Plotly (for future TTL decay charts)
	•	Docker (used for local testing)

⸻

GenAI Contribution

This tool was developed as part of Project Catalyst with full support from Generative AI (ChatGPT) throughout all stages:
	•	Use case brainstorming
	•	TTL query logic development
	•	Code generation for Streamlit and backend
	•	Debugging integration with Cassandra clusters
	•	Documentation and sample data creation

⸻

Getting Started

1. Clone the Repository

git clone https://github.com/your-username/ttlens.git
cd ttlens

Replace your-username with your GitHub username.

2. Set Up a Python Virtual Environment

For Windows:

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

For macOS/Linux:

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

3. Install Required Python Packages

pip install streamlit cassandra-driver



⸻

Running the Application

streamlit run app/main.py

The app will open in your browser at http://localhost:8501

⸻

Setting Up Apache Cassandra Using Docker

1. Install Docker
	•	Windows/macOS: Download and install Docker Desktop from Docker’s official website
	•	Linux (Ubuntu):

# Update the apt package index
sudo apt-get update

# Install packages to allow apt to use a repository over HTTPS
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add the Docker APT repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

# Update the apt package index again
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce

# Start Docker
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

2. Run Apache Cassandra Using Docker

# Pull the latest Cassandra image
docker pull cassandra:latest

# Run Cassandra in a Docker container
docker run --name cassandra -d -p 9042:9042 cassandra:latest

3. Access Cassandra Using cqlsh

# Access the Cassandra container's shell
docker exec -it cassandra bash

# Inside the container, launch cqlsh
cqlsh



⸻

Creating a Sample Keyspace and Table

-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS ttlens_test
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- Use the keyspace
USE ttlens_test;

-- Create a table with default TTL
CREATE TABLE users (
    user_id text PRIMARY KEY,
    name text,
    email text,
    last_login timestamp
) WITH default_time_to_live = 3600;

-- Insert data with column-level TTL
INSERT INTO users (user_id, name, email, last_login)
VALUES ('user1', 'Alice', 'alice@example.com', toTimestamp(now()))
USING TTL 1800;

-- Insert data without specifying TTL (inherits table TTL)
INSERT INTO users (user_id, name, email, last_login)
VALUES ('user2', 'Bob', 'bob@example.com', toTimestamp(now()));

-- Insert data with no TTL
INSERT INTO users (user_id, name, email, last_login)
VALUES ('user3', 'Carol', 'carol@example.com', toTimestamp(now()))
USING TTL 0;



⸻

Testing the Setup
	1.	Ensure your Python virtual environment is activated.
	2.	Run the Streamlit application:

streamlit run app/main.py

	3.	In the web interface:
	•	Connect to the Cassandra cluster using localhost and port 9042.
	•	Select the keyspace ttlens_test and table users.
	•	Input the partition key column as user_id.
	•	Enter partition key values (user1, user2, user3) to view TTL information.
	•	Export the results as needed.

⸻

Git Workflow: Updating, Committing, and Pushing Changes

1. Pull the Latest Changes from the Remote Repository

Before making new changes, ensure your local repository is up-to-date to avoid conflicts:

git pull origin main

Replace main with your branch name if different.

2. Check the Status of Your Local Repository

To see which files have been modified, added, or deleted:

git status

3. Stage Your Changes

To add specific files to the staging area:

git add path/to/your/file.py

To stage all modified files:

git add .

4. Commit Your Changes

After staging, commit your changes with a descriptive message:

git commit -m "Add feature X to improve Y"

5. Push Your Changes to the Remote Repository

Once committed, push your changes to the remote repository:

git push origin main

Again, replace main with your branch name if different.

6. View Commit History

To review the commit history:

git log --oneline --graph --decorate



⸻

License

This project is licensed under the MIT License.

⸻
