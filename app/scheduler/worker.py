import asyncio
from datetime import datetime, time, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from app.config.settings import settings
from app.models.base import get_session
from app.models.datasource import DataSource
from app.scheduler.jobs import fetch_and_process_data, cleanup_old_files

# Globale Scheduler-Instanz
scheduler = None

async def schedule_datasource_jobs():
    """
    Plant Jobs für alle aktiven Datenquellen.
    """
    logger.info("Starte Planung der Datenquellen-Jobs")
    
    # Datenbankverbindung herstellen
    async for session in get_session():
        # Alle Datenquellen abrufen
        # Hinweis: In der Realität würden wir hier einen Filter für aktive Datenquellen hinzufügen
        datasources = await session.query(DataSource).all()
        
        for datasource in datasources:
            # Startzeit für den Job berechnen
            now = datetime.now()
            start_date = datetime.combine(now.date(), datasource.start_time)
            
            # Wenn die Startzeit bereits vergangen ist, auf morgen verschieben
            if start_date < now:
                start_date = start_date + timedelta(days=1)
            
            # Job für die Datenquelle planen
            scheduler.add_job(
                fetch_and_process_data,
                'interval',
                seconds=datasource.frequency.total_seconds(),
                start_date=start_date,
                args=[datasource.id],
                id=f"datasource_{datasource.id}",
                replace_existing=True,
                misfire_grace_time=settings.SCHEDULER_MISFIRE_GRACE_TIME
            )
            
            logger.info(f"Job für Datenquelle '{datasource.name}' geplant: Start um {datasource.start_time}, Intervall {datasource.frequency}")

async def schedule_cleanup_job():
    """
    Plant den Job zur Bereinigung alter Dateien.
    """
    logger.info("Starte Planung des Bereinigungsjobs")
    
    # Bereinigungsjob jeden Tag um Mitternacht ausführen
    scheduler.add_job(
        cleanup_old_files,
        CronTrigger(hour=0, minute=0),
        id="cleanup_old_files",
        replace_existing=True,
        misfire_grace_time=settings.SCHEDULER_MISFIRE_GRACE_TIME
    )
    
    logger.info("Bereinigungsjob geplant: Täglich um Mitternacht")

async def start_scheduler():
    """
    Startet den Scheduler und plant alle Jobs.
    """
    global scheduler
    
    if scheduler is None:
        logger.info("Starte Scheduler")
        scheduler = AsyncIOScheduler()
        
        # Jobs planen
        await schedule_datasource_jobs()
        await schedule_cleanup_job()
        
        # Scheduler starten
        scheduler.start()
        logger.info("Scheduler gestartet")
    else:
        logger.warning("Scheduler läuft bereits")

async def stop_scheduler():
    """
    Stoppt den Scheduler.
    """
    global scheduler
    
    if scheduler is not None and scheduler.running:
        logger.info("Stoppe Scheduler")
        scheduler.shutdown()
        scheduler = None
        logger.info("Scheduler gestoppt")
    else:
        logger.warning("Scheduler läuft nicht")

async def reload_scheduler():
    """
    Aktualisiert die geplanten Jobs im Scheduler.
    """
    global scheduler
    
    if scheduler is not None and scheduler.running:
        logger.info("Aktualisiere Scheduler-Jobs")
        
        # Alle existierenden Jobs löschen
        for job in scheduler.get_jobs():
            job.remove()
        
        # Jobs neu planen
        await schedule_datasource_jobs()
        await schedule_cleanup_job()
        
        logger.info("Scheduler-Jobs aktualisiert")
    else:
        logger.warning("Scheduler läuft nicht, kann Jobs nicht aktualisieren")