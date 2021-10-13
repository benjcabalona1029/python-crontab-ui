from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import cronservice
from models import Job
from utils import watch_err_files, load_logs
from database import SessionLocal, engine, JobRequest

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def update_displayed_schedule(db: Session = Depends(get_db)) -> None:
    jobs = db.query(Job).all()
    for job in jobs:
        job.next_run = cronservice.get_next_schedule(job.name)
        job.status = watch_err_files(job.name)


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    update_displayed_schedule(db)
    jobs = db.query(Job).all()
    output = {"request": request, "jobs": jobs}
    return templates.TemplateResponse("home.html", output)


@app.get("/jobs/{job_id}")
async def get_jobs(job_id: int, request: Request, db: Session = Depends(get_db)):
    job_update = db.query(Job).filter(Job.id == job_id).first()
    output = {"request": request, "job_update": job_update}
    return templates.TemplateResponse("jobs.html", output)


@app.get("/logs/{job_id}")
async def get_logs(job_id: int, request: Request, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id)
    update_log = {
        "err_log": load_logs(job.first().name, status=False),
        "log": load_logs(job.first().name, "log", status=False),
    }
    job.update(update_log)
    db.commit()
    output = {"request": request, "job": update_log}
    return templates.TemplateResponse("logs.html", output)


@app.post("/create_job/")
async def create_job(job_request: JobRequest, db: Session = Depends(get_db)):
    job = Job()
    job.command = job_request.command
    job.name = job_request.name
    job.schedule = job_request.schedule
    try:
        cronservice.add_cron_job(job.command, job.name, job.schedule)
        job.next_run = cronservice.get_next_schedule(job.name)
        db.add(job)
        db.commit()
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid Cron Expression")
    return job_request


@app.put("/update_job/{job_id}/")
async def update_job(
    job_id: int, job_request: JobRequest, db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(Job.id == job_id)
    cronservice.update_cron_job(
        job_request.command,
        job_request.name,
        job_request.schedule,
        existing_job.first().name,
    )
    existing_job.update(job_request.__dict__)
    existing_job.update({"next_run": cronservice.get_next_schedule(job_request.name)})
    db.commit()
    return {"msg": "Successfully updated data."}


@app.get("/run_job/{job_id}/")
async def run_job(job_id: int, db: Session = Depends(get_db)):
    chosen_job = db.query(Job).filter(Job.id == job_id).first()
    chosen_name = chosen_job.name
    cronservice.run_manually(chosen_name)
    return {"msg": "Successfully run job."}


@app.delete("/job/{job_id}/")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    job_update = db.query(Job).filter(Job.id == job_id).first()
    cronservice.delete_cron_job(job_update.name)
    db.delete(job_update)
    db.commit()
    return {"INFO": f"Deleted {job_id} Successfully"}
