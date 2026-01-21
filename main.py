from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, engine, Base, Destination as DestinationModel
from schemas import Destination, DestinationCreate, DestinationUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Bucket List API",
    description="Manage your travel destinations and bucket list",
    version="1.0.0"
)

@app.post("/destinations/", response_model=Destination, tags=["Destinations"], summary="Add a new destination")
def create_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    """Create a new travel destination with place name, country, priority, and optional notes."""
    db_destination = DestinationModel(**destination.model_dump())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

@app.get("/destinations/", response_model=List[Destination], tags=["Destinations"], summary="Get all destinations")
def get_destinations(db: Session = Depends(get_db)):
    """Retrieve all travel destinations from your bucket list."""
    return db.query(DestinationModel).all()

@app.get("/destinations/{destination_id}", response_model=Destination, tags=["Destinations"], summary="Get a specific destination")
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    """Retrieve a single destination by its ID."""
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination

@app.put("/destinations/{destination_id}", response_model=Destination, tags=["Destinations"], summary="Update a destination")
def update_destination(destination_id: int, destination_update: DestinationUpdate, db: Session = Depends(get_db)):
    """Update any field of an existing destination."""
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    for field, value in destination_update.model_dump(exclude_unset=True).items():
        setattr(destination, field, value)
    
    db.commit()
    db.refresh(destination)
    return destination

@app.delete("/destinations/{destination_id}", tags=["Destinations"], summary="Delete a destination")
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    """Remove a destination from your bucket list."""
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    db.delete(destination)
    db.commit()
    return {"message": "Destination deleted"}

@app.patch("/destinations/{destination_id}/visited", tags=["Destinations"], summary="Toggle visited status")
def toggle_visited(destination_id: int, db: Session = Depends(get_db)):
    """Mark a destination as visited or unvisited."""
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    destination.visited = not destination.visited
    db.commit()
    return {"visited": destination.visited}