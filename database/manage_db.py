#!/usr/bin/env python3
"""
Database management script for Interview Trainer PostgreSQL database.
Provides functions to check database status, reset data, and perform maintenance.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'interview_trainer'),
    'user': os.getenv('DB_USER', 'interview_user'),
    'password': os.getenv('DB_PASSWORD', 'interview_password')
}

def connect_to_db():
    """Establish connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def check_database_status():
    """Check if the database is running and accessible"""
    conn = connect_to_db()
    if not conn:
        print("❌ Database connection failed")
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print("✅ Database connection successful")
        print(f"📊 PostgreSQL version: {version.split(',')[0]}")
        
        # Check table counts
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes
            FROM pg_stat_user_tables 
            ORDER BY schemaname, tablename
        """)
        
        tables = cursor.fetchall()
        if tables:
            print("\n📋 Table statistics:")
            for table in tables:
                print(f"  {table[1]}: {table[2]} inserts, {table[3]} updates, {table[4]} deletes")
        else:
            print("\n📋 No tables found")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking database status: {e}")
        conn.close()
        return False

def reset_database():
    """Reset all data in the database (keep structure)"""
    conn = connect_to_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Get confirmation
        response = input("⚠️  This will delete ALL data from the database. Are you sure? (yes/no): ")
        if response.lower() != 'yes':
            print("Operation cancelled")
            return False
        
        # Delete data from all tables (in correct order due to foreign keys)
        tables = [
            'users',
            'skills',
            'jobs',
            'questions',
            'exercises',
            'skill_cards',
            'dashboard_stats',
            'skill_distribution_data',
            'performance_data',
            'llm_config',
            'question_skills',
            'exercise_skills'
        ]
        
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")
        
        conn.commit()
        print("✅ Database reset completed successfully")
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error resetting database: {e}")
        conn.close()
        return False

def show_table_info():
    """Show detailed information about all tables"""
    conn = connect_to_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Get table information
        cursor.execute("""
            SELECT 
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        if columns:
            current_table = None
            print("📋 Database schema:")
            for col in columns:
                if col[0] != current_table:
                    current_table = col[0]
                    print(f"\n🔸 Table: {current_table}")
                
                nullable = "NULL" if col[3] == "YES" else "NOT NULL"
                default = f" DEFAULT {col[4]}" if col[4] else ""
                print(f"  {col[1]}: {col[2]} {nullable}{default}")
        else:
            print("No tables found")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error getting table info: {e}")
        conn.close()
        return False

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Interview Trainer Database Management')
    parser.add_argument('action', choices=['status', 'reset', 'schema'], 
                       help='Action to perform')
    
    args = parser.parse_args()
    
    if args.action == 'status':
        check_database_status()
    elif args.action == 'reset':
        reset_database()
    elif args.action == 'schema':
        show_table_info()
    else:
        print("Invalid action. Use 'status', 'reset', or 'schema'")

if __name__ == "__main__":
    main()
