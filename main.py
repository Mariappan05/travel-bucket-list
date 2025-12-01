from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, engine, Base, Destination as DestinationModel
from schemas import Destination, DestinationCreate, DestinationUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Bucket List API")

@app.post("/destinations/", response_model=Destination)
def create_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    db_destination = DestinationModel(**destination.dict())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

@app.get("/destinations/", response_model=List[Destination])
def get_destinations(db: Session = Depends(get_db)):
    return db.query(DestinationModel).all()

@app.get("/destinations/{destination_id}", response_model=Destination)
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination

@app.put("/destinations/{destination_id}", response_model=Destination)
def update_destination(destination_id: int, destination_update: DestinationUpdate, db: Session = Depends(get_db)):
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    for field, value in destination_update.dict(exclude_unset=True).items():
        setattr(destination, field, value)
    
    db.commit()
    db.refresh(destination)
    return destination

@app.delete("/destinations/{destination_id}")
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    db.delete(destination)
    db.commit()
    return {"message": "Destination deleted"}

@app.patch("/destinations/{destination_id}/visited")
def toggle_visited(destination_id: int, db: Session = Depends(get_db)):
    destination = db.query(DestinationModel).filter(DestinationModel.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    destination.visited = not destination.visited
    db.commit()
    return {"visited": destination.visited}