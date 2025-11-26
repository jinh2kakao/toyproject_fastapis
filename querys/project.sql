-- SQL Schema and CRUD Queries for AI Novel Production Dashboard
-- Based on HTML UI structure provided by the user.

-- DDL: Create the 'projects' table if it does not exist.
-- Corresponds to the overall project data structure displayed in the dashboard and created via the modal.
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL, -- Corresponds to #projectTitle (Modal Input)
    genre VARCHAR(50),           -- Corresponds to #projectGenre (Modal Select) - assuming VARCHAR for simplicity, could be INT for genre ID
    logline TEXT,                -- Corresponds to #projectLogline (Modal Textarea)
    image_url VARCHAR(255) DEFAULT 'https://example.com/default-project-image.png', -- Corresponds to Dashboard Card Image, with a logical default
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Corresponds to Dashboard Metadata (Time)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- System field for creation timestamp
);

-- INSERT: Query to add a new project from the Modal inputs.
-- Used when a user creates a new project via the 'New Project Modal'.
INSERT INTO projects (title, genre, logline)
VALUES (:title, :genre, :logline);

-- SELECT: Query to fetch all projects to render the Dashboard Grid cards.
-- Used to populate the main dashboard with existing projects.
SELECT id, title, genre, logline, image_url, updated_at, created_at
FROM projects
ORDER BY updated_at DESC;

-- UPDATE: Query to update project details.
-- Used to modify an existing project's details, potentially from an edit modal or settings page.
UPDATE projects
SET
    title = :title,
    genre = :genre,
    logline = :logline,
    image_url = :image_url,
    updated_at = CURRENT_TIMESTAMP -- Explicitly update timestamp
WHERE id = :id;

-- DELETE: Query to delete a project by ID.
-- Used when a user chooses to remove a project from the system.
DELETE FROM projects
WHERE id = :id;
