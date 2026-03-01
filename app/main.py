from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from io import BytesIO
import matplotlib.pyplot as plt

from app.agent import answer_question
from app.data_loader import load_data
from app.visualizer import create_chart

app = FastAPI()

df = load_data()
last_chart = None


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask_question(query: Query):
    global last_chart

    answer = answer_question(query.question)

    # simple AI chart decision
    q = query.question.lower()
    chart_type = None

    if "age" in q:
        chart_type = "age_histogram"
    elif "fare" in q:
        chart_type = "fare_histogram"
    elif "survival" in q or "survived" in q:
        chart_type = "survival_count"

    last_chart = create_chart(df, chart_type)

    return {
        "answer": answer,
        "show_chart": last_chart is not None
    }


@app.get("/chart")
def get_chart():
    global last_chart

    if last_chart is None:
        return JSONResponse(
            content={"error": "No chart available"},
            status_code=404
        )

    buffer = BytesIO()
    last_chart.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)

    plt.close(last_chart)
    last_chart = None

    return StreamingResponse(buffer, media_type="image/png")