"""Tools package for the Job Application Assistant."""

from .document_processor import (
    DocumentProcessor,
    JobDescriptionExtractor,
    process_cv_file,
    extract_job_description
)

__all__ = [
    "DocumentProcessor",
    "JobDescriptionExtractor", 
    "process_cv_file",
    "extract_job_description"
]
