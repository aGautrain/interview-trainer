# Interview Trainer PostgreSQL Database

This directory contains the PostgreSQL database setup for the Interview Trainer application, including Docker Compose configuration, table creation scripts, and data population utilities.

## 🚀 Quick Start

### Start the Database

```bash
# Start PostgreSQL container
docker-compose -f ../docker-compose.postgres.yml up -d

# Check if the database is running
docker ps
```

### Verify Database Connection

```bash
# Check database status
python manage_db.py status
```

### 4. Populate with Sample Data

```bash
# Install dependencies
pip install -r requirements.txt

# Populate database with sample data
psql -h localhost -U interview_user -d interview_trainer -f init/02_upsert_data.sql
```

## 📁 File Structure

```
database/
├── init/
│   └── 01_create_tables.sql    # Database schema creation
├── 02_upsert_data.sql          # Sample data insertion script
├── manage_db.py                 # Database management utilities
├── requirements.txt             # Python dependencies
├── config.example               # Example environment configuration
└── README.md                    # This file
```

## 🔧 Environment Configuration

### Environment File Setup

1. **Copy the example configuration:**

   ```bash
   cp config.example .env
   ```

2. **Edit the `.env` file** with your preferred values

3. **Never commit the `.env` file** to version control (it's already in `.gitignore`)

## 🗄️ Database Schema

The database includes the following main tables:

### Core Tables

- **users** - User accounts and profiles
- **skills** - Skill definitions and metadata
- **jobs** - Job postings and applications
- **questions** - Training questions
- **exercises** - Coding exercises and challenges

### Training Tables

- **skill_cards** - Skill progress tracking
- **question_skills** - Many-to-many relationship between questions and skills
- **exercise_skills** - Many-to-many relationship between exercises and skills

### Dashboard Tables

- **dashboard_stats** - Overall application statistics
- **llm_config** - LLM configuration settings
- **skill_distribution_data** - Data for skill distribution charts
- **performance_data** - User performance metrics by difficulty level

### Configuration Tables

- **llm_config** - LLM API configuration

## 🛠️ Management Commands

### Database Status

```bash
python manage_db.py status
```

Shows connection status, PostgreSQL version, and table statistics.

### View Schema

```bash
python manage_db.py schema
```

Displays detailed table structure and column information.

### Reset Data

```bash
python manage_db.py reset
```

⚠️ **Warning**: This deletes all data while preserving the table structure.

## 🔧 Database Operations

### Connect to Database

````bash
# Using psql (if installed)
psql -h localhost -U interview_user -d interview_trainer

### Backup and Restore

```bash
# Backup
docker exec interview_trainer_postgres pg_dump -U interview_user interview_trainer > backup.sql

# Restore
docker exec -i interview_trainer_postgres psql -U interview_user interview_trainer < backup.sql
````

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused**

   - Ensure Docker container is running: `docker ps`
   - Check if port 5432 is available: `netstat -an | grep 5432`
   - Verify `POSTGRES_HOST_PORT` in your `.env` file

2. **Authentication Failed**

   - Verify credentials in your `.env` file
   - Check if database was initialized properly
   - Ensure `POSTGRES_USER` and `POSTGRES_PASSWORD` are set correctly

3. **Permission Denied**

   - Ensure the `database/init` directory has proper permissions
   - Check Docker volume mounts

4. **Environment Variables Not Loaded**
   - Ensure `.env` file exists in the `database/` directory
   - Check that `python-dotenv` is installed: `pip install python-dotenv`

### Reset Everything

```bash
# Stop and remove containers
docker-compose -f ../docker-compose.postgres.yml down

# Remove volumes (⚠️ This will delete all data)
docker volume rm interview-trainer_postgres_data

# Start fresh
docker-compose -f ../docker-compose.postgres.yml up -d
```
