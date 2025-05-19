
from app import app, db
from models import Project

# Use application context
with app.app_context():
    # Get all projects
    projects = Project.query.all()
    
    # Count projects
    project_count = len(projects)
    
    # Delete all projects (cascade will automatically delete related blog posts)
    for project in projects:
        db.session.delete(project)
    
    # Commit the changes
    db.session.commit()
    
    print(f"Successfully deleted {project_count} projects and their related blog posts.")
