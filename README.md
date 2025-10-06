# Job Tracker Server

A simple HTTP server for capturing job application data from browser extensions.

## Docker Setup

### Using Docker Compose (Recommended)

1. Build and start the server:
   ```bash
   docker-compose up --build
   ```

2. The server will be available at `http://localhost:8766`

3. To stop the server:
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. Build the image:
   ```bash
   docker build -t job-tracker-server .
   ```

2. Run the container:
   ```bash
   docker run -p 8766:8766 -v $(pwd)/job-tracker.md:/app/job-tracker.md job-tracker-server
   ```

## Data Persistence

The `job-tracker.md` file is mounted as a volume to ensure data persists between container restarts.

## API Endpoints

- `POST /` - Capture job application data
  - Body: JSON with fields: `company`, `role`, `url`, `source`
  - Response: `200 OK` on success

## Development

To run locally without Docker:
```bash
python capture_server.py
```
