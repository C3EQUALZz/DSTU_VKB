from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from combined_languages.theory_of_information.backend.fifth_semestr import (
    first_laboratory_router as fifth_sem_first_laboratory_router,
    second_laboratory_router as fifth_sem_second_laboratory_router,
    third_laboratory_router as fifth_sem_third_laboratory_router,
    fourth_laboratory_router as fifth_sem_fourth_laboratory_router,
)

app = FastAPI(
    title="Лабораторные по теории информации",
    version="1.0.0",
    root_path="/api",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(fifth_sem_first_laboratory_router)
app.include_router(fifth_sem_second_laboratory_router)
app.include_router(fifth_sem_third_laboratory_router)
app.include_router(fifth_sem_fourth_laboratory_router)
