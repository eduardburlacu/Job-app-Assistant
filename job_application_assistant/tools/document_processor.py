"""Document processing utilities for CV/resume and job descriptions."""

import re
import requests
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from pathlib import Path
import logging
from urllib.parse import urlparse

if TYPE_CHECKING:
    from bs4 import BeautifulSoup as BS4BeautifulSoup
else:
    BS4BeautifulSoup = Any

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import docx2txt
except ImportError:
    docx2txt = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from job_application_assistant.models.data_models import JobDescription, UserProfile

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Utility class for processing various document types."""
    
    def __init__(self):
        """Initialize the document processor."""
        pass
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        if not pdfplumber:
            raise ImportError("pdfplumber is required for PDF processing")
        
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        if not docx2txt:
            raise ImportError("docx2txt is required for DOCX processing")
        
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {e}")
            return ""
    
    def process_cv_file(self, file_path: str) -> str:
        """Process CV/resume file and extract text."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return self.extract_text_from_pdf(str(file_path))
        elif suffix == '.docx':
            return self.extract_text_from_docx(str(file_path))
        elif suffix == '.txt':
            return self.extract_text_from_txt(str(file_path))
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def parse_cv_content(self, cv_text: str) -> Dict[str, Any]:
        """Parse CV content to extract structured information."""
        # Simple regex-based parsing - could be enhanced with NLP
        parsed_data = {
            "skills": [],
            "experience": [],
            "education": [],
            "contact_info": {}
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, cv_text)
        if emails:
            parsed_data["contact_info"]["email"] = emails[0]
        
        # Extract phone numbers
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        phones = re.findall(phone_pattern, cv_text)
        if phones:
            parsed_data["contact_info"]["phone"] = phones[0]
        
        # Extract skills (simple keyword matching)
        skill_keywords = [
            "Python", "JavaScript", "Java", "C++", "React", "Node.js",
            "Machine Learning", "Data Science", "SQL", "MongoDB",
            "Docker", "Kubernetes", "AWS", "Azure", "Git", "Linux"
        ]
        
        found_skills = []
        for skill in skill_keywords:
            if skill.lower() in cv_text.lower():
                found_skills.append(skill)
        parsed_data["skills"] = found_skills
        
        return parsed_data


class JobDescriptionExtractor:
    """Extract job descriptions from various sources."""
    
    def __init__(self):
        """Initialize the job description extractor."""
        pass
    
    def extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extract job description from URL with platform-specific parsing."""
        if not BeautifulSoup:
            raise ImportError("beautifulsoup4 is required for web scraping")
        
        try:
            # Identify platform
            platform = self._identify_platform(url)
            logger.info(f"Detected platform: {platform} for URL: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Use platform-specific parsing
            if platform == 'linkedin':
                return self._parse_linkedin_job(soup, url)
            elif platform == 'indeed':
                return self._parse_indeed_job(soup, url)
            else:
                return self._parse_generic_job(soup, url)
                
        except Exception as e:
            logger.error(f"Error extracting job description from URL: {e}")
            return {"error": str(e), "url": url}
    
    def _identify_platform(self, url: str) -> str:
        """Identify the job platform from URL."""
        parsed_url = urlparse(url.lower())
        domain = parsed_url.netloc
        
        if 'linkedin.com' in domain:
            return 'linkedin'
        elif 'indeed.com' in domain:
            return 'indeed'
        elif 'glassdoor.com' in domain:
            return 'glassdoor'
        else:
            return 'generic'
    
    def _parse_linkedin_job(self, soup: Any, url: str) -> Dict[str, Any]:
        """Parse LinkedIn job posting with improved extraction."""
        job_data = {
            "title": "Unknown Position",
            "company": "Unknown Company",
            "description": "",
            "location": "Unknown Location",
            "url": url,
            "platform": "LinkedIn",
            "requirements": [],
            "employment_type": "Unknown"
        }
        
        try:
            # Extract job title - LinkedIn uses specific selectors
            title_selectors = [
                'h1.t-24.t-bold.inline',
                'h1[data-automation-id="job-title"]',
                '.jobs-unified-top-card__job-title h1',
                'h1.jobs-unified-top-card__job-title',
                '.job-details-jobs-unified-top-card__job-title h1'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    job_data["title"] = title_elem.get_text().strip()
                    logger.info(f"Found job title: {job_data['title']}")
                    break
            
            # Extract company name - Make sure it's NOT LinkedIn
            company_selectors = [
                'span.jobs-unified-top-card__company-name a',
                'a[data-automation-id="company-name"]',
                '.job-details-jobs-unified-top-card__company-name a',
                'span.jobs-unified-top-card__company-name',
                '.jobs-unified-top-card__primary-description a'
            ]
            
            for selector in company_selectors:
                company_elem = soup.select_one(selector)
                if company_elem:
                    company_text = company_elem.get_text().strip()
                    # Ensure we're not getting "LinkedIn" as the company
                    if company_text and company_text.lower() not in ['linkedin', 'linkedin corporation']:
                        job_data["company"] = company_text
                        logger.info(f"Found company: {job_data['company']}")
                        break
            
            # If we still have "Unknown Company", try alternative methods
            if job_data["company"] == "Unknown Company":
                # Look for company in meta tags or structured data
                meta_company = soup.find('meta', {'property': 'og:description'})
                if meta_company:
                    content = meta_company.get('content', '')
                    # Try to extract company from description
                    company_match = re.search(r'at\s+([^.]+)', content)
                    if company_match:
                        job_data["company"] = company_match.group(1).strip()
            
            # Extract location
            location_selectors = [
                'span.jobs-unified-top-card__bullet',
                '[data-automation-id="job-location"]',
                '.jobs-unified-top-card__primary-description-container span'
            ]
            
            for selector in location_selectors:
                location_elem = soup.select_one(selector)
                if location_elem:
                    location_text = location_elem.get_text().strip()
                    # Make sure it's actually a location, not other metadata
                    if location_text and not any(skip in location_text.lower() 
                                               for skip in ['linkedin', 'ago', 'applicant']):
                        job_data["location"] = location_text
                        break
            
            # Extract job description
            description_selectors = [
                'div.jobs-description__content',
                '[data-automation-id="job-description"]',
                '.job-details-jobs-unified-top-card__job-description',
                'div.jobs-box__content'
            ]
            
            for selector in description_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    # Get text but preserve some structure
                    description_text = desc_elem.get_text(separator='\n', strip=True)
                    if description_text and len(description_text) > 50:
                        job_data["description"] = description_text
                        break
            
            # If no specific description found, get general content but filter out LinkedIn UI
            if not job_data["description"]:
                all_text = soup.get_text(separator=' ', strip=True)
                # Filter out LinkedIn-specific UI text
                filtered_text = re.sub(r'LinkedIn.*?Sign in.*?Join now', '', all_text, flags=re.DOTALL)
                if len(filtered_text) > 100:
                    job_data["description"] = filtered_text[:2000]
            
            # Extract employment type from description or UI elements
            description_lower = job_data["description"].lower()
            if 'full-time' in description_lower or 'full time' in description_lower:
                job_data["employment_type"] = "Full-time"
            elif 'part-time' in description_lower or 'part time' in description_lower:
                job_data["employment_type"] = "Part-time"
            elif 'contract' in description_lower:
                job_data["employment_type"] = "Contract"
            elif 'internship' in description_lower:
                job_data["employment_type"] = "Internship"
            
            # Extract requirements
            if job_data["description"]:
                job_data["requirements"] = self._extract_requirements_from_text(job_data["description"])
            
            logger.info(f"Successfully parsed LinkedIn job: {job_data['title']} at {job_data['company']}")
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn job: {str(e)}")
            job_data["error"] = f"LinkedIn parsing error: {str(e)}"
        
        return job_data
    
    def _parse_indeed_job(self, soup: Any, url: str) -> Dict[str, Any]:
        """Parse Indeed job posting."""
        return self._parse_generic_job(soup, url, platform="Indeed")
    
    def _parse_generic_job(self, soup: Any, url: str, platform: str = "Generic") -> Dict[str, Any]:
        """Generic job parsing for unknown platforms."""
        job_data = {
            "title": "Unknown Position",
            "company": "Unknown Company",
            "description": "",
            "location": "Unknown Location",
            "url": url,
            "platform": platform,
            "requirements": []
        }
        
        try:
            # Common selectors for job sites
            title_selectors = [
                'h1', '.job-title', '.jobsearch-JobInfoHeader-title',
                '[data-testid="job-title"]', '.job-header-title'
            ]
            
            company_selectors = [
                '.company', '.employer', '.company-name',
                '[data-testid="company-name"]', '.jobsearch-InlineCompanyRating'
            ]
            
            # Extract title
            for selector in title_selectors:
                element = soup.select_one(selector)
                if element:
                    job_data["title"] = element.get_text(strip=True)
                    break
            
            # Extract company
            for selector in company_selectors:
                element = soup.select_one(selector)
                if element:
                    job_data["company"] = element.get_text(strip=True)
                    break
            
            # Extract description (get all text content)
            job_data["description"] = soup.get_text(separator=' ', strip=True)
            
            # Extract requirements
            if job_data["description"]:
                job_data["requirements"] = self._extract_requirements_from_text(job_data["description"])
            
        except Exception as e:
            logger.error(f"Error in generic parsing: {str(e)}")
            job_data["error"] = f"Generic parsing error: {str(e)}"
        
        return job_data
    
    def _extract_requirements_from_text(self, text: str) -> List[str]:
        """Extract requirements and skills from job description text."""
        requirements = []
        
        # Common requirement patterns
        patterns = [
            r'(?:require[sd]?|must have|need|looking for)[:\s-]*([^.!?]+)',
            r'(?:experience with|knowledge of|proficient in|familiar with)[:\s-]*([^.!?]+)',
            r'(?:skills?)[:\s-]*([^.!?]+)',
            r'(?:\d+\+?\s*years?)[^.]*?(?:experience|exp)[^.]*?(?:in|with)\s+([^.!?]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Clean up the match
                cleaned = re.sub(r'[^\w\s,+#/-]', '', match).strip()
                if cleaned and len(cleaned) > 3 and len(cleaned) < 100:
                    # Split by common delimiters and add individual requirements
                    sub_requirements = [req.strip() for req in re.split(r'[,;]', cleaned) if req.strip()]
                    requirements.extend(sub_requirements)
        
        # Remove duplicates and return top 10
        seen = set()
        unique_requirements = []
        for req in requirements:
            req_lower = req.lower()
            if req_lower not in seen and len(req) > 2:
                seen.add(req_lower)
                unique_requirements.append(req)
        
        return unique_requirements[:10]
    
    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract job information from plain text with enhanced parsing."""
        # Clean the text first
        text = text.strip()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        job_data = {
            "title": "Unknown Position",
            "company": "Unknown Company",
            "description": text,
            "requirements": [],
            "skills": [],
            "location": "Unknown Location"
        }
        
        try:
            # Enhanced extraction for copied LinkedIn job posts
            if len(lines) > 0:
                # First line is often the job title
                potential_title = lines[0]
                if len(potential_title) < 100 and not potential_title.lower().startswith(('about', 'we are', 'job')):
                    job_data["title"] = potential_title
                
                # Second line might be company name
                if len(lines) > 1:
                    potential_company = lines[1]
                    if (len(potential_company) < 50 and 
                        not potential_company.lower().startswith(('location', 'we are', 'job', 'about')) and
                        not re.match(r'^[A-Z]{2,}$', potential_company)):  # Not all caps abbreviation
                        job_data["company"] = potential_company
            
            # Look for company name patterns (only if we don't have a good one already)
            if job_data["company"] == "Unknown Company":
                company_patterns = [
                    r'([A-Z][a-zA-Z\s&.,-]+?(?:\s+Inc\.?|\s+LLC|\s+Corp\.?|\s+Ltd\.?|\s+Co\.?))',  # Company with suffix
                    r'(?:at|@)\s+([A-Z][a-zA-Z\s&.,-]{2,40})(?:\s|$)',  # "at Company Name"
                    r'Company:\s*([^\n]+)',                    # "Company: Name"
                    r'([A-Z][a-zA-Z\s&.,-]+)\s+is\s+(?:looking|seeking|hiring)',  # "Company Name is looking"
                    r'Join\s+([A-Z][a-zA-Z\s&.,-]+?)(?:\s|$)',  # "Join Company Name"
                ]
                
                for pattern in company_patterns:
                    match = re.search(pattern, text, re.MULTILINE)
                    if match:
                        company_candidate = match.group(1).strip()
                        # Filter out common false positives
                        if (len(company_candidate) < 50 and 
                            not any(skip in company_candidate.lower() for skip in 
                                   ['linkedin', 'apply', 'position', 'role', 'job', 'experience', 'years'])):
                            job_data["company"] = company_candidate
                            break
            
            # Look for location patterns
            location_patterns = [
                r'Location:\s*([^\n]+)',
                r'(?:Based in|Located in)\s+([^\n,]+)',
                r'([A-Z][a-zA-Z\s]+,\s*[A-Z]{2,})',  # City, State/Country
                r'(Remote|Hybrid|On-site)',
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    location_candidate = match.group(1).strip()
                    if len(location_candidate) < 50:
                        job_data["location"] = location_candidate
                        break
            
            # Extract requirements with better patterns
            job_data["requirements"] = self._extract_requirements_from_text(text)
            
            # Extract skills
            job_data["skills"] = self._extract_skills_from_text(text)
            
            logger.info(f"Extracted from text: {job_data['title']} at {job_data['company']}")
            
        except Exception as e:
            logger.error(f"Error extracting from text: {str(e)}")
            job_data["error"] = f"Text parsing error: {str(e)}"
        
        return job_data
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from job description text."""
        # Common technical skills to look for
        skill_keywords = [
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby", "PHP",
            "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "Spring",
            "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Git", "GitHub",
            "Machine Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn",
            "HTML", "CSS", "Sass", "Bootstrap", "Tailwind", "REST", "GraphQL", "API",
            "Linux", "Unix", "Windows", "macOS", "Bash", "PowerShell",
            "Agile", "Scrum", "DevOps", "CI/CD", "Microservices", "API Design"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skill_keywords:
            # Look for exact matches or common variations
            if (skill.lower() in text_lower or 
                skill.lower().replace('.', '') in text_lower or
                skill.lower().replace('-', '') in text_lower):
                found_skills.append(skill)
        
        return found_skills[:15]  # Return top 15 skills


# Global instances
document_processor = DocumentProcessor()
job_extractor = JobDescriptionExtractor()


def process_cv_file(file_path: str) -> UserProfile:
    """Process a CV file and return a UserProfile."""
    cv_text = document_processor.process_cv_file(file_path)
    parsed_data = document_processor.parse_cv_content(cv_text)
    
    return UserProfile(
        name=parsed_data["contact_info"].get("name", "User"),
        email=parsed_data["contact_info"].get("email", ""),
        phone=parsed_data["contact_info"].get("phone"),
        cv_text=cv_text,
        skills=parsed_data["skills"],
        experience=parsed_data["experience"],
        education=parsed_data["education"]
    )


def extract_job_description(source: str) -> JobDescription:
    """Extract job description from URL or text."""
    if source.startswith(('http://', 'https://')):
        job_data = job_extractor.extract_from_url(source)
    else:
        job_data = job_extractor.extract_from_text(source)
    
    return JobDescription(
        title=job_data.get("title", ""),
        company=job_data.get("company", ""),
        description=job_data.get("description", ""),
        requirements=job_data.get("requirements", []),
        skills=job_data.get("skills", []),
        location=job_data.get("location"),
        url=job_data.get("url")
    )
