-- Body Composition Assessment Database Schema
-- Run this SQL in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS body_assessments (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    height_cm DECIMAL(5, 1) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    weight_kg DECIMAL(5, 1) NOT NULL,
    bmi DECIMAL(4, 1) NOT NULL,
    body_fat_percent DECIMAL(4, 1) NOT NULL,
    visceral_fat_percent DECIMAL(4, 1) NOT NULL,
    resting_metabolism INTEGER NOT NULL,
    metabolic_age INTEGER NOT NULL,
    whole_body_subcutaneous DECIMAL(4, 1) NOT NULL,
    whole_body_muscle DECIMAL(4, 1) NOT NULL,
    trunk_subcutaneous DECIMAL(4, 1) NOT NULL,
    trunk_muscle DECIMAL(4, 1) NOT NULL,
    arms_subcutaneous DECIMAL(4, 1) NOT NULL,
    arms_muscle DECIMAL(4, 1) NOT NULL,
    legs_subcutaneous DECIMAL(4, 1) NOT NULL,
    legs_muscle DECIMAL(4, 1) NOT NULL,
    email_sent BOOLEAN DEFAULT FALSE,
    email_sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_body_assessments_email ON body_assessments(email);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_body_assessments_created_at ON body_assessments(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE body_assessments ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (for now - adjust based on your security needs)
CREATE POLICY "Allow all operations on body_assessments" ON body_assessments
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to call the function
CREATE TRIGGER update_body_assessments_updated_at
    BEFORE UPDATE ON body_assessments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Optional: Create a view for quick statistics
CREATE OR REPLACE VIEW assessment_statistics AS
SELECT 
    COUNT(*) as total_assessments,
    AVG(age) as avg_age,
    AVG(bmi) as avg_bmi,
    AVG(body_fat_percent) as avg_body_fat,
    COUNT(DISTINCT email) as unique_clients,
    MAX(created_at) as last_assessment_date
FROM body_assessments;
