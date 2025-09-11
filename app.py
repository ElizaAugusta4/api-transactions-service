from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
import models, schemas
from database import get_db, engine

app = FastAPI(title="Transactions Service", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Transactions Service running!"}

@app.post("/transactions", response_model=schemas.TransactionOut, status_code=201)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    account = db.query(models.Account).get(transaction.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions", response_model=List[schemas.TransactionOut])
def list_transactions(
    account_id: Optional[int] = Query(None, description="Filtrar por ID da conta"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    db: Session = Depends(get_db),
):
    q = db.query(models.Transaction)
    if account_id is not None:
        q = q.filter(models.Transaction.account_id == account_id)
    if category:
        q = q.filter(models.Transaction.category == category)
    return q.order_by(models.Transaction.occurred_at.desc(), models.Transaction.id.desc()).all()

@app.get("/transactions/{tx_id}", response_model=schemas.TransactionOut)
def get_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return tx

@app.put("/transactions/{tx_id}", response_model=schemas.TransactionOut)
def update_transaction(tx_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    if transaction.account_id != tx.account_id:
        account = db.query(models.Account).get(transaction.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
    for field, value in transaction.dict().items():
        setattr(tx, field, value)
    db.commit()
    db.refresh(tx)
    return tx

@app.delete("/transactions/{tx_id}", status_code=204)
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    db.delete(tx)
    db.commit()
    return
