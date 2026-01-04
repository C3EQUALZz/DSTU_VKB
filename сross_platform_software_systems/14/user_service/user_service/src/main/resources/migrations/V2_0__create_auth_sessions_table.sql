-- Create auth_sessions table with foreign key to users
CREATE TABLE auth_sessions (
    id VARCHAR PRIMARY KEY,
    user_id UUID NOT NULL,
    expiration TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT fk_auth_sessions_user_id 
        FOREIGN KEY (user_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE
);

-- Create index on user_id for faster lookups and foreign key performance
CREATE INDEX idx_auth_sessions_user_id ON auth_sessions(user_id);

-- Create index on expiration for cleanup queries
CREATE INDEX idx_auth_sessions_expiration ON auth_sessions(expiration);