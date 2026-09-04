-- GramBiz AI Database Schema (MySQL)

CREATE DATABASE IF NOT EXISTS grambiz_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE grambiz_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Entrepreneurs / Profile Table
CREATE TABLE IF NOT EXISTS entrepreneurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    village_town VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100),
    business_type VARCHAR(100),
    business_status VARCHAR(50) DEFAULT 'Planning', -- Operational, Planning, Expanding
    years_in_business DECIMAL(4,1) DEFAULT 0,
    number_of_workers INT DEFAULT 1,
    initial_investment DECIMAL(12,2) DEFAULT 0,
    monthly_revenue DECIMAL(12,2) DEFAULT 0,
    monthly_expenses DECIMAL(12,2) DEFAULT 0,
    current_savings DECIMAL(12,2) DEFAULT 0,
    existing_loan DECIMAL(12,2) DEFAULT 0,
    goals VARCHAR(550), -- JSON or comma separated string
    is_onboarded TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Business Profiles Details
CREATE TABLE IF NOT EXISTS business_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    business_name VARCHAR(150),
    business_category VARCHAR(100),
    target_customers VARCHAR(255),
    products_services TEXT,
    expected_monthly_sales DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Financial Records Summary
CREATE TABLE IF NOT EXISTS financial_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    record_date DATE NOT NULL,
    total_revenue DECIMAL(12,2) DEFAULT 0,
    total_expenses DECIMAL(12,2) DEFAULT 0,
    net_profit DECIMAL(12,2) DEFAULT 0,
    health_score INT DEFAULT 75,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. Expenses Table
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    expense_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL, -- Raw Material, Transport, Electricity, Rent, Labour, Marketing, Other
    description VARCHAR(255),
    amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 6. Revenues Table
CREATE TABLE IF NOT EXISTS revenues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    revenue_date DATE NOT NULL,
    product_service VARCHAR(150) NOT NULL,
    quantity INT DEFAULT 1,
    amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 7. Business Recommendations Table
CREATE TABLE IF NOT EXISTS business_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recommendation_text TEXT NOT NULL,
    category VARCHAR(50), -- Cost Reduction, Sales Boost, Cash Flow, Opportunity
    is_read TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 8. Chat History Table
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    sender VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 9. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message VARCHAR(255) NOT NULL,
    type VARCHAR(50) DEFAULT 'info', -- info, warning, success
    is_read TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
