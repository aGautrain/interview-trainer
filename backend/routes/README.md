# Routes Directory

This directory contains all the route handlers for the Interview Trainer API, organized by domain for better maintainability and clarity.

## Structure

- **`__init__.py`** - Package initialization and router exports
- **`dashboard.py`** - Dashboard-related endpoints (`/dashboard`, `/dashboard/stats`)
- **`jobs.py`** - Job-related endpoints (`/jobs`, `/jobs/{job_id}`)
- **`skills.py`** - Skills and training endpoints (`/skills`, `/skills/{skill_name}/questions`, `/skills/{skill_name}/exercises`)
- **`legacy.py`** - Legacy endpoints for backward compatibility (`/items/{item_id}`)

## Benefits of This Structure

1. **Separation of Concerns** - Each domain has its own route file
2. **Maintainability** - Easier to find and modify specific endpoints
3. **Scalability** - New domains can be added as separate modules
4. **Testing** - Individual route modules can be tested in isolation
5. **Documentation** - Each module is self-documenting with clear purposes

## Adding New Routes

To add new routes:

1. Create a new route file in this directory (e.g., `users.py`)
2. Define your router with appropriate tags and prefix
3. Import and include it in `main.py`
4. Update `routes/__init__.py` to export the new router

## Example

```python
# routes/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("")
def get_users():
    return {"users": []}
```

Then in `main.py`:

```python
from routes.users import router as users_router
app.include_router(users_router)
```
