# The "help" command (default) - prints available commands
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies locally (Poetry)"
	@echo "  make up         - Start services (Docker)"
	@echo "  make down       - Stop services"
	@echo "  make logs       - View backend logs"
	@echo "  make clean      - Remove temporary files"

# Install local dependencies for development (so VS Code works)
install:
	cd backend && poetry install
	cd consumer && poetry install

# Start the full system
up:
	docker compose up --build -d

# Stop the system
down:
	docker compose down

# View logs for the backend
logs:
	docker compose logs -f backend

# Clean up junk files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +