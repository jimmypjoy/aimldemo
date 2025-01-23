from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from threading import Thread
import uvicorn

app = FastAPI()

# Define a data model for the credit review record
class CreditReview(BaseModel):
    cagid: str
    creationDate: date
    creditReviewType: str  # Values: ANNUAL_REVIEW, INTERIM_REVIEW, CREDIT_MEMO
    camId: str
    approvedBy: str
    tfa: float

# Dummy credit review records
credit_reviews = [
    {
        "cagid": "123",
        "creationDate": "2024-01-15",
        "creditReviewType": "ANNUAL_REVIEW",
        "camId": "CAM001",
        "approvedBy": "SOEID001",
        "tfa": 5000000.00
    },
    {
        "cagid": "123",
        "creationDate": "2024-02-10",
        "creditReviewType": "INTERIM_REVIEW",
        "camId": "CAM002",
        "approvedBy": "SOEID002",
        "tfa": 2500000.00
    },
    {
        "cagid": "456",
        "creationDate": "2024-03-20",
        "creditReviewType": "CREDIT_MEMO",
        "camId": "CAM003",
        "approvedBy": "SOEID003",
        "tfa": 750000.00
    },
    {
        "cagid": "789",
        "creationDate": "2023-11-05",
        "creditReviewType": "ANNUAL_REVIEW",
        "camId": "CAM004",
        "approvedBy": "SOEID004",
        "tfa": 3000000.00
    },
    {
        "cagid": "123",
        "creationDate": "2023-12-15",
        "creditReviewType": "ANNUAL_REVIEW",
        "camId": "CAM005",
        "approvedBy": "SOEID001",
        "tfa": 6000000.00
    },
    {
        "cagid": "999",
        "creationDate": "2022-07-19",
        "creditReviewType": "INTERIM_REVIEW",
        "camId": "CAM006",
        "approvedBy": "SOEID006",
        "tfa": 1200000.00
    },
    {
        "cagid": "888",
        "creationDate": "2021-09-23",
        "creditReviewType": "CREDIT_MEMO",
        "camId": "CAM007",
        "approvedBy": "SOEID007",
        "tfa": 4500000.00
    },
    {
        "cagid": "555",
        "creationDate": "2023-05-01",
        "creditReviewType": "ANNUAL_REVIEW",
        "camId": "CAM008",
        "approvedBy": "SOEID008",
        "tfa": 9500000.00
    },
    {
        "cagid": "777",
        "creationDate": "2024-06-18",
        "creditReviewType": "INTERIM_REVIEW",
        "camId": "CAM009",
        "approvedBy": "SOEID009",
        "tfa": 1800000.00
    },
    {
        "cagid": "333",
        "creationDate": "2020-03-30",
        "creditReviewType": "CREDIT_MEMO",
        "camId": "CAM010",
        "approvedBy": "SOEID010",
        "tfa": 200000.00
    }
]

# Endpoint to fetch credit review data
@app.get("/getCreditReviewData", response_model=List[CreditReview])
def get_credit_review_data(
    cagid: str = Query(..., description="Customer CAGID"),
    creationDate: Optional[date] = Query(None, description="Filter by creation date"),
    creditReviewType: Optional[str] = Query(None, description="Filter by credit review type"),
    approvedBy: Optional[str] = Query(None, description="Filter by approver SOEID"),
    tfa: Optional[float] = Query(None, description="Filter by total facility amount")
):
    # Filtering logic
    filtered_reviews = [review for review in credit_reviews if review["cagid"] == cagid]

    if creationDate:
        filtered_reviews = [review for review in filtered_reviews if review["creationDate"] == creationDate.isoformat()]
    
    if creditReviewType:
        filtered_reviews = [review for review in filtered_reviews if review["creditReviewType"] == creditReviewType]

    if approvedBy:
        filtered_reviews = [review for review in filtered_reviews if review["approvedBy"] == approvedBy]

    if tfa:
        filtered_reviews = [review for review in filtered_reviews if review["tfa"] == tfa]

    if not filtered_reviews:
        raise HTTPException(status_code=404, detail="No matching credit review data found")

    return filtered_reviews

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Credit Review API"}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()