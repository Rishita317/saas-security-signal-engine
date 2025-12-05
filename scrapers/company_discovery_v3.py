"""
Company Discovery Engine V3 - 1000+ Companies Without Google Search

NEW STRATEGY:
1. Direct ATS pattern enumeration (Greenhouse, Lever, Workday, Ashby, etc.)
2. VC portfolio job boards (Sequoia, a16z, Accel, Khosla, etc.)
3. Security-specific job boards (infosec-jobs, cybersecurityjobboard, clearedjobs)
4. Indeed as seed → backtrack to ATS URLs
5. RSS feeds for conversation signals

NO GOOGLE SEARCH - All direct scraping!
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict, Set
import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class CompanyDiscoveryV3:
    """
    Discovers 1000+ companies using direct scraping (NO Google Search!)

    Sources:
    1. Indeed (PRIMARY) - 400+ companies
    2. VC Portfolio Boards - 200+ companies
    3. Workday Direct - 150+ companies
    4. Greenhouse Direct - 100+ companies
    5. Lever Direct - 50+ companies
    6. Security Job Boards - 100+ companies
    """

    def __init__(self):
        self.companies = {}
        self.driver = None

        # Security keywords (expanded with internships!)
        self.security_keywords = [
            # Core Security Roles
            "Security Engineer", "Cybersecurity Engineer", "Information Security Engineer",
            "Security Analyst", "Security Architect", "Security Consultant",

            # Cloud & SaaS Security
            "Cloud Security Engineer", "Cloud Security Architect", "SaaS Security",
            "SSPM Engineer", "Cloud Security Analyst",

            # Application Security
            "Application Security Engineer", "AppSec Engineer", "Product Security Engineer",
            "Software Security Engineer",

            # Specialized Security
            "DevSecOps Engineer", "Security Operations Engineer", "SOC Analyst",
            "Threat Intelligence Analyst", "Vulnerability Management", "Penetration Tester",
            "Security Researcher",

            # Compliance & Governance
            "Security Compliance Engineer", "GRC Analyst", "Compliance Engineer",
            "Risk Analyst", "Privacy Engineer",

            # Identity & Access
            "Identity Security Engineer", "IAM Engineer", "Access Management",

            # Incident Response
            "Incident Response Analyst", "Security Incident Response", "SIEM Engineer",
            "Detection Engineer",

            # Leadership
            "Security Manager", "CISO", "Security Director", "Security Lead",

            # Emerging Areas
            "AI Security Engineer", "ML Security", "Data Security Engineer",
            "Container Security", "Kubernetes Security", "API Security Engineer",

            # INTERNSHIPS (NEW - expands job count significantly!)
            "Security Intern", "Cybersecurity Intern", "Information Security Intern",
            "Cloud Security Intern", "AppSec Intern", "Security Engineering Intern",
            "SOC Intern", "Security Analyst Intern", "DevSecOps Intern",
            "Threat Intelligence Intern", "Security Research Intern",
        ]

        # VC Portfolio Job Boards (NO GOOGLE NEEDED!) - EXPANDED TO 25+ VCs
        self.vc_portfolios = {
            # Tier 1 VCs
            "Sequoia": "https://www.sequoiacap.com/companies/",
            "a16z": "https://a16z.com/portfolio/",
            "Accel": "https://www.accel.com/companies",
            "Khosla": "https://www.khoslaventures.com/portfolio/",
            "Lightspeed": "https://lsvp.com/portfolio/",
            "Greylock": "https://greylock.com/portfolio/",
            "Founders Fund": "https://foundersfund.com/companies/",

            # Tier 2 VCs (High Quality)
            "Insight Partners": "https://www.insightpartners.com/portfolio/",
            "Index Ventures": "https://www.indexventures.com/portfolio",
            "General Catalyst": "https://www.generalcatalyst.com/companies",
            "Bessemer": "https://www.bvp.com/portfolio",
            "NEA": "https://www.nea.com/portfolio",
            "Benchmark": "https://www.benchmark.com/portfolio/",
            "IVP": "https://www.ivp.com/portfolio/",
            "Kleiner Perkins": "https://www.kleinerperkins.com/portfolio",

            # Security-Focused VCs
            "YL Ventures": "https://www.ylventures.com/portfolio",
            "Team8": "https://www.team8.vc/portfolio/",
            "Ballistic Ventures": "https://www.ballisticventures.com/portfolio",
            "DataTribe": "https://datatribe.com/portfolio/",

            # Tech-Heavy VCs
            "Battery Ventures": "https://www.battery.com/portfolio/",
            "Menlo Ventures": "https://menlovc.com/portfolio/",
            "CRV": "https://www.crv.com/portfolio",
            "GGV Capital": "https://www.ggvc.com/portfolio/",
            "Redpoint": "https://www.redpoint.com/companies/",
            "Felicis": "https://www.felicis.com/portfolio",
        }

        # Security Publishers for RSS
        self.top_publishers = {
            "Cisco Security": "https://blogs.cisco.com/security/feed",
            "Microsoft Security": "https://www.microsoft.com/security/blog/feed/",
            "Palo Alto Networks": "https://www.paloaltonetworks.com/blog/feed/",
            "CrowdStrike": "https://www.crowdstrike.com/blog/feed/",
            "IBM Security": "https://securityintelligence.com/feed/",
            "Fortinet": "https://www.fortinet.com/blog/rss.xml",
            "Check Point": "https://blog.checkpoint.com/feed/",
            "Okta": "https://www.okta.com/blog/feed/",
            "Broadcom Security": "https://www.broadcom.com/blog/feed",
            "TLDR Sec": "https://tldrsec.com/feed/"
        }

    def _init_selenium_driver(self):
        """Initialize Selenium WebDriver with improved cleanup"""
        if self.driver is not None:
            self._close_selenium_driver()

        try:
            # Kill any stuck ChromeDriver processes first
            import subprocess
            try:
                subprocess.run(['pkill', '-9', 'chromedriver'], capture_output=True, timeout=5)
                subprocess.run(['pkill', '-9', 'Google Chrome for Testing'], capture_output=True, timeout=5)
            except:
                pass

            chrome_options = Options()
            chrome_options.add_argument('--headless=new')  # Use new headless mode
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--dns-prefetch-disable')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Set page load timeout
            chrome_options.page_load_strategy = 'eager'  # Don't wait for full page load

            service = Service(ChromeDriverManager().install())
            service.creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0

            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)  # 30 second timeout
            self.driver.set_script_timeout(30)
            self.driver.implicitly_wait(10)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            print("   ✅ Selenium WebDriver initialized successfully")
        except Exception as e:
            print(f"   ⚠️  Failed to initialize Selenium: {str(e)[:200]}")
            self.driver = None

    def _close_selenium_driver(self):
        """Close Selenium WebDriver with proper cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            finally:
                self.driver = None

                # Force kill any remaining processes
                import subprocess
                try:
                    subprocess.run(['pkill', '-9', 'chromedriver'], capture_output=True, timeout=2)
                except:
                    pass

    def discover_all(self, companies_target: int = 1000, posts_target: int = 50) -> List[Dict]:
        """
        Main discovery pipeline - NO GOOGLE SEARCH!

        Target: 1000+ companies from multiple sources
        """
        print("=" * 70)
        print("🚀 COMPANY DISCOVERY ENGINE V3 - NO GOOGLE SEARCH")
        print("=" * 70)
        print(f"\nTarget: {companies_target} companies, {posts_target} quality posts")
        print("Strategy: Direct scraping only (NO Google dependency!)")
        print("\n" + "=" * 70)

        try:
            # Phase 1: Hiring Signal Discovery
            self._discover_hiring_signals(companies_target)

            # Phase 2: Conversation Signal Discovery
            self._discover_conversation_signals(posts_target)

        finally:
            self._close_selenium_driver()

        # Generate company tracker
        tracker = self._generate_company_tracker()
        self._print_summary(tracker)

        return tracker

    def _discover_hiring_signals(self, target_count: int):
        """Discover companies with hiring signals"""
        print(f"\n🔍 HIRING SIGNAL DISCOVERY")
        print("=" * 70)
        print(f"Target: {target_count} companies")
        print("Method: Direct ATS scraping (NO Google!)\n")

        companies_discovered = set()

        # Source 1: Indeed (PRIMARY - Most reliable)
        print("1️⃣ Indeed Job Search (PRIMARY SOURCE)...")
        companies_discovered.update(
            self._scrape_indeed(max_companies=min(400, target_count))
        )

        # Source 2: VC Portfolio Boards (NEW - High quality companies!)
        if len(companies_discovered) < target_count:
            print(f"\n2️⃣ VC Portfolio Job Boards (Sequoia, a16z, Accel, etc.)...")
            companies_discovered.update(
                self._scrape_vc_portfolios(max_companies=min(200, target_count - len(companies_discovered)))
            )

        # Source 3: Workday Direct Scraping
        if len(companies_discovered) < target_count:
            print(f"\n3️⃣ Workday ATS Direct Discovery...")
            companies_discovered.update(
                self._scrape_workday_direct(max_companies=min(150, target_count - len(companies_discovered)))
            )

        # Source 4: Greenhouse Direct
        if len(companies_discovered) < target_count:
            print(f"\n4️⃣ Greenhouse ATS Discovery...")
            companies_discovered.update(
                self._scrape_greenhouse_direct(max_companies=min(100, target_count - len(companies_discovered)))
            )

        # Source 5: Lever Direct
        if len(companies_discovered) < target_count:
            print(f"\n5️⃣ Lever ATS Discovery...")
            companies_discovered.update(
                self._scrape_lever_direct(max_companies=min(50, target_count - len(companies_discovered)))
            )

        # Source 6: Security Job Boards
        if len(companies_discovered) < target_count:
            print(f"\n6️⃣ Security-Specific Job Boards...")
            companies_discovered.update(
                self._scrape_security_job_boards(max_companies=target_count - len(companies_discovered))
            )

        print(f"\n📊 Total unique companies discovered: {len(companies_discovered)}")

    def _scrape_indeed(self, max_companies: int) -> Set[str]:
        """Scrape Indeed (same as before - this works!)"""
        discovered = set()

        print(f"   ℹ️  Using {min(50, len(self.security_keywords))} keywords to discover companies")

        try:
            num_keywords = min(len(self.security_keywords), (max_companies // 10) + 1)

            for keyword in self.security_keywords[:num_keywords]:
                if len(discovered) >= max_companies:
                    break

                self._init_selenium_driver()
                if not self.driver:
                    continue

                try:
                    search_term = keyword.replace(' ', '+')
                    url = f"https://www.indeed.com/jobs?q={search_term}&l="

                    print(f"   Searching: {keyword}...")
                    self.driver.get(url)

                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
                    )
                    time.sleep(2)

                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    job_cards = soup.find_all('div', class_='job_seen_beacon')

                    print(f"      Found {len(job_cards)} job listings")

                    for card in job_cards:
                        if len(discovered) >= max_companies:
                            break

                        # Multiple strategies to extract company name (robust for headless mode)
                        company_name = None

                        # Strategy 1: Try data-testid attribute
                        company_elem = card.find('span', {'data-testid': 'company-name'})
                        if company_elem:
                            company_name = self._clean_company_name(company_elem.text.strip())

                        # Strategy 2: Try class containing 'company'
                        if not company_name:
                            company_elem = card.find(['span', 'div'], class_=re.compile(r'company', re.I))
                            if company_elem:
                                company_name = self._clean_company_name(company_elem.text.strip())

                        # Strategy 3: Try attribute containing 'company'
                        if not company_name:
                            company_elem = card.find(['span', 'div'], attrs={'data-company-name': True})
                            if company_elem:
                                company_name = self._clean_company_name(company_elem.get('data-company-name', ''))

                        # Strategy 4: Look for text after "at" or "by" (fallback)
                        if not company_name:
                            card_text = card.get_text()
                            match = re.search(r'(?:at|by)\s+([A-Z][A-Za-z0-9\s\.\-&]{2,50})', card_text)
                            if match:
                                company_name = self._clean_company_name(match.group(1))

                        # Get job title
                        title_elem = card.find('h2', class_='jobTitle')
                        if not title_elem:
                            title_elem = card.find(['h2', 'h3', 'a'], class_=re.compile(r'title', re.I))

                        # Get job URL
                        link_elem = card.find('a', class_='jcs-JobTitle')
                        if not link_elem:
                            link_elem = card.find('a', href=re.compile(r'/rc/clk|/viewjob'))

                        # Validate and add company
                        if company_name and title_elem:
                            # Filter out invalid company names (UI elements, etc.)
                            if self._is_valid_company_name(company_name):
                                if company_name not in discovered:
                                    discovered.add(company_name)

                                    if company_name not in self.companies:
                                        self.companies[company_name] = {'hiring': [], 'conversations': []}

                                    job_title = title_elem.text.strip()
                                    job_url = f"https://www.indeed.com{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else f"https://www.indeed.com/jobs?q={search_term}"

                                    self.companies[company_name]['hiring'].append({
                                        'title': job_title,
                                        'source': 'Indeed',
                                        'url': job_url,
                                        'location': 'Various'
                                    })

                                    if len(discovered) % 25 == 0:
                                        print(f"      ✅ Found: {len(discovered)} companies so far...")

                    self._close_selenium_driver()
                    time.sleep(3)

                except Exception as e:
                    print(f"      ⚠️  Error searching '{keyword}': {str(e)[:100]}")
                    self._close_selenium_driver()
                    continue

        except Exception as e:
            print(f"   ⚠️  Indeed search error: {str(e)}")

        finally:
            self._close_selenium_driver()

        print(f"   ✅ Indeed: Discovered {len(discovered)} companies")
        return discovered

    def _scrape_vc_portfolios(self, max_companies: int) -> Set[str]:
        """
        NEW METHOD: Scrape VC portfolio pages directly!

        VCs list all their portfolio companies → many have security jobs
        This avoids Google entirely!
        """
        discovered = set()

        print(f"   ℹ️  Scraping VC portfolio companies (NO Google needed!)...")

        # Try each VC portfolio
        for vc_name, vc_url in self.vc_portfolios.items():
            if len(discovered) >= max_companies:
                break

            try:
                print(f"      Scanning {vc_name} portfolio...")

                response = requests.get(
                    vc_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    timeout=15
                )

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                # Different VCs have different HTML structures
                # Look for common patterns: links, company names, etc.
                company_links = []

                # Strategy 1: Look for links that might be companies
                for link in soup.find_all('a', href=True):
                    text = link.get_text(strip=True)
                    href = link['href']

                    # Skip navigation/social links
                    if any(skip in href.lower() for skip in ['twitter', 'linkedin', 'facebook', 'instagram', 'about', 'team', 'contact', 'news']):
                        continue

                    # Company names are usually 2-50 chars
                    if 2 <= len(text) <= 50 and text and not text.startswith('#'):
                        company_links.append(text)

                # Strategy 2: Look for company names in specific containers
                # Common patterns: div.company, div.portfolio-item, li.company-name
                for pattern in [
                    {'class_': re.compile(r'company|portfolio|startup')},
                    {'class_': re.compile(r'card|item|grid-item')}
                ]:
                    for elem in soup.find_all(['div', 'li', 'article'], pattern):
                        text = elem.get_text(strip=True)
                        if 2 <= len(text) <= 50:
                            company_links.append(text)

                # Clean and add companies
                for company_name in company_links:
                    # Basic cleaning
                    company_name = company_name.strip()
                    company_name = re.sub(r'\s+', ' ', company_name)

                    # Skip if too short or has weird characters
                    if len(company_name) < 2 or not re.match(r'^[A-Za-z0-9\s\.\-&]+$', company_name):
                        continue

                    # Skip common false positives
                    if company_name.lower() in ['view all', 'learn more', 'read more', 'see more', 'portfolio', 'companies']:
                        continue

                    discovered.add(company_name)

                    if len(discovered) % 25 == 0:
                        print(f"      ✅ Found: {len(discovered)} companies so far...")

                    if len(discovered) >= max_companies:
                        break

            except Exception as e:
                print(f"      ⚠️  Error scraping {vc_name}: {str(e)[:100]}")
                continue

        print(f"   ✅ VC Portfolios: Found {len(discovered)} companies")
        return discovered

    def _scrape_workday_direct(self, max_companies: int) -> Set[str]:
        """
        NEW METHOD: Direct Workday scraping without Google

        Strategy:
        1. Use Indeed companies as seed
        2. Try building Workday URLs: {company}.wd1.myworkdayjobs.com
        3. If exists, scrape all security jobs
        """
        discovered = set()

        print(f"   ℹ️  Direct Workday ATS discovery...")

        # Use existing companies as seeds
        seed_companies = list(self.companies.keys())[:100]  # Try first 100

        for company_name in seed_companies:
            if len(discovered) >= max_companies:
                break

            try:
                # Convert company name to URL-friendly format
                company_slug = company_name.lower()
                company_slug = re.sub(r'[^a-z0-9]+', '', company_slug)

                if not company_slug:
                    continue

                # Try common Workday URL patterns
                workday_urls = [
                    f"https://{company_slug}.wd1.myworkdayjobs.com",
                    f"https://{company_slug}.wd5.myworkdayjobs.com",
                    f"https://{company_slug}.wd12.myworkdayjobs.com",
                ]

                for workday_url in workday_urls:
                    try:
                        response = requests.get(
                            workday_url,
                            headers={'User-Agent': 'Mozilla/5.0'},
                            timeout=5,
                            allow_redirects=True
                        )

                        # If we get a 200, this company has Workday
                        if response.status_code == 200 and 'workday' in response.url.lower():
                            # Try to find security jobs
                            security_jobs_url = f"{workday_url}/search"

                            job_response = requests.get(
                                security_jobs_url,
                                headers={'User-Agent': 'Mozilla/5.0'},
                                timeout=5
                            )

                            if job_response.status_code == 200:
                                soup = BeautifulSoup(job_response.text, 'html.parser')

                                # Look for job listings
                                job_links = soup.find_all('a', href=re.compile(r'/job/'))

                                for job_link in job_links[:5]:  # Check first 5 jobs
                                    job_title = job_link.get_text(strip=True).lower()

                                    # Check if it's a security job
                                    if any(keyword in job_title for keyword in ['security', 'cyber', 'infosec', 'soc', 'threat']):
                                        discovered.add(company_name)

                                        if company_name not in self.companies:
                                            self.companies[company_name] = {'hiring': [], 'conversations': []}

                                        self.companies[company_name]['hiring'].append({
                                            'title': job_link.get_text(strip=True),
                                            'url': urljoin(workday_url, job_link['href']),
                                            'location': 'Multiple Locations',
                                            'source': 'Workday',
                                            'posted_date': 'Recent'
                                        })

                                        if len(discovered) % 10 == 0:
                                            print(f"      ✅ Found: {len(discovered)} companies with Workday...")

                                        break  # Found security jobs, move to next company

                            break  # Found valid Workday instance, no need to try other URLs

                    except requests.exceptions.RequestException:
                        continue  # Try next URL pattern

            except Exception as e:
                continue  # Skip this company

        print(f"   ✅ Workday Direct: Found {len(discovered)} companies")
        return discovered

    def _scrape_greenhouse_direct(self, max_companies: int) -> Set[str]:
        """Direct Greenhouse scraping without Google"""
        discovered = set()

        print(f"   ℹ️  Direct Greenhouse ATS discovery...")

        # Use existing companies as seeds
        seed_companies = list(self.companies.keys())[:100]

        for company_name in seed_companies:
            if len(discovered) >= max_companies:
                break

            try:
                # Convert company name to URL slug
                company_slug = company_name.lower()
                company_slug = re.sub(r'[^a-z0-9]+', '-', company_slug)
                company_slug = company_slug.strip('-')

                if not company_slug:
                    continue

                # Try Greenhouse URL pattern
                greenhouse_url = f"https://boards.greenhouse.io/{company_slug}"

                response = requests.get(
                    greenhouse_url,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=5,
                    allow_redirects=True
                )

                # If we get a 200 and it's still a greenhouse URL, company exists
                if response.status_code == 200 and 'greenhouse' in response.url.lower():
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for job listings
                    job_listings = soup.find_all('div', class_=re.compile(r'opening|job'))
                    if not job_listings:
                        job_listings = soup.find_all('a', href=re.compile(r'/jobs/\d+'))

                    # Check for security-related jobs
                    for job in job_listings[:10]:
                        job_text = job.get_text(strip=True).lower()

                        if any(keyword in job_text for keyword in ['security', 'cyber', 'infosec', 'soc', 'threat', 'devsecops']):
                            discovered.add(company_name)

                            if company_name not in self.companies:
                                self.companies[company_name] = {'hiring': [], 'conversations': []}

                            # Try to extract job details
                            job_link = job.find('a') if job.name != 'a' else job
                            if job_link and job_link.get('href'):
                                job_url = urljoin(greenhouse_url, job_link['href'])
                                job_title = job_link.get_text(strip=True)

                                self.companies[company_name]['hiring'].append({
                                    'title': job_title,
                                    'url': job_url,
                                    'location': 'Multiple Locations',
                                    'source': 'Greenhouse',
                                    'posted_date': 'Recent'
                                })

                            if len(discovered) % 10 == 0:
                                print(f"      ✅ Found: {len(discovered)} companies on Greenhouse...")

                            break  # Found security jobs, move to next company

            except Exception as e:
                continue

        print(f"   ✅ Greenhouse Direct: Found {len(discovered)} companies")
        return discovered

    def _scrape_lever_direct(self, max_companies: int) -> Set[str]:
        """Direct Lever scraping without Google"""
        discovered = set()

        print(f"   ℹ️  Direct Lever ATS discovery...")

        # Use existing companies as seeds
        seed_companies = list(self.companies.keys())[:100]

        for company_name in seed_companies:
            if len(discovered) >= max_companies:
                break

            try:
                # Convert company name to URL slug
                company_slug = company_name.lower()
                company_slug = re.sub(r'[^a-z0-9]+', '-', company_slug)
                company_slug = company_slug.strip('-')

                if not company_slug:
                    continue

                # Try Lever URL pattern
                lever_url = f"https://jobs.lever.co/{company_slug}"

                response = requests.get(
                    lever_url,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=5,
                    allow_redirects=True
                )

                # If we get a 200 and it's still a lever URL, company exists
                if response.status_code == 200 and 'lever.co' in response.url.lower():
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for job listings (Lever uses specific classes)
                    job_listings = soup.find_all('div', class_=re.compile(r'posting|position'))
                    if not job_listings:
                        job_listings = soup.find_all('a', class_=re.compile(r'posting'))

                    # Check for security-related jobs
                    for job in job_listings[:10]:
                        job_text = job.get_text(strip=True).lower()

                        if any(keyword in job_text for keyword in ['security', 'cyber', 'infosec', 'soc', 'threat', 'devsecops']):
                            discovered.add(company_name)

                            if company_name not in self.companies:
                                self.companies[company_name] = {'hiring': [], 'conversations': []}

                            # Try to extract job details
                            job_link = job.find('a') if job.name != 'a' else job
                            if job_link and job_link.get('href'):
                                job_url = urljoin(lever_url, job_link['href'])
                                if not job_url.startswith('http'):
                                    job_url = f"https://jobs.lever.co{job_link['href']}"
                                job_title = job_link.get_text(strip=True)

                                self.companies[company_name]['hiring'].append({
                                    'title': job_title,
                                    'url': job_url,
                                    'location': 'Multiple Locations',
                                    'source': 'Lever',
                                    'posted_date': 'Recent'
                                })

                            if len(discovered) % 10 == 0:
                                print(f"      ✅ Found: {len(discovered)} companies on Lever...")

                            break  # Found security jobs, move to next company

            except Exception as e:
                continue

        print(f"   ✅ Lever Direct: Found {len(discovered)} companies")
        return discovered

    def _scrape_security_job_boards(self, max_companies: int) -> Set[str]:
        """
        NEW METHOD: Scrape cybersecurity-specific job boards

        Boards:
        - infosec-jobs.com
        - cybersecurityjobboard.com
        - clearedjobs.net
        """
        discovered = set()

        print(f"   ℹ️  Scraping security-specific job boards...")

        # Security job board URLs
        security_boards = {
            'InfoSec Jobs': 'https://www.infosec-jobs.com/jobs/',
            'CyberSecurity Jobsite': 'https://www.cybersecurityjobsite.com/jobs/',
            'Cleared Jobs': 'https://www.clearancejobs.com/jobs/cybersecurity'
        }

        for board_name, board_url in security_boards.items():
            if len(discovered) >= max_companies:
                break

            try:
                print(f"      Scanning {board_name}...")

                response = requests.get(
                    board_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    timeout=10
                )

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                # Different boards have different structures, look for common patterns
                # Look for job listings
                job_containers = []

                # Strategy 1: Look for common job container classes
                for pattern in ['job', 'listing', 'position', 'posting', 'result']:
                    job_containers.extend(soup.find_all(['div', 'li', 'article'], class_=re.compile(pattern, re.I)))

                # Strategy 2: Look for links to job pages
                job_links = soup.find_all('a', href=re.compile(r'/job[s]?/|/position[s]?/|/career[s]?/', re.I))
                job_containers.extend(job_links)

                # Extract company names from job listings
                for container in job_containers[:50]:  # Check first 50 listings
                    if len(discovered) >= max_companies:
                        break

                    try:
                        # Try to find company name
                        company_elem = container.find(['span', 'div', 'p', 'a'], class_=re.compile(r'company|employer|organization', re.I))

                        if not company_elem:
                            # Try to extract from text
                            text = container.get_text(strip=True)
                            # Look for patterns like "Company: XYZ" or "at XYZ"
                            company_match = re.search(r'(?:at|company:|employer:)\s*([A-Z][A-Za-z0-9\s\.\-&]{2,50})', text, re.I)
                            if company_match:
                                company_name = company_match.group(1).strip()
                            else:
                                continue
                        else:
                            company_name = company_elem.get_text(strip=True)

                        # Clean company name
                        company_name = re.sub(r'\s+', ' ', company_name)

                        # Validate company name
                        if 2 <= len(company_name) <= 100 and not company_name.lower() in ['jobs', 'security', 'careers']:
                            discovered.add(company_name)

                            if company_name not in self.companies:
                                self.companies[company_name] = {'hiring': [], 'conversations': []}

                            # Try to extract job title and URL
                            job_link = container.find('a') if container.name != 'a' else container
                            if job_link:
                                job_title = job_link.get_text(strip=True)[:200]
                                job_url = urljoin(board_url, job_link.get('href', ''))

                                self.companies[company_name]['hiring'].append({
                                    'title': job_title,
                                    'url': job_url,
                                    'location': 'Multiple Locations',
                                    'source': board_name,
                                    'posted_date': 'Recent'
                                })

                            if len(discovered) % 10 == 0:
                                print(f"      ✅ Found: {len(discovered)} companies...")

                    except Exception:
                        continue

            except Exception as e:
                print(f"      ⚠️  Error scraping {board_name}: {str(e)[:100]}")
                continue

        print(f"   ✅ Security Job Boards: Found {len(discovered)} companies")
        return discovered

    def _scrape_ashby(self, max_companies: int) -> Set[str]:
        """
        NEW METHOD: Scrape Ashby ATS (ashbyhq.com)
        Used by many high-growth SaaS companies
        """
        discovered = set()
        print(f"   ℹ️  Scraping Ashby ATS...")

        # Try common Ashby URL patterns for existing companies
        seed_companies = list(self.companies.keys())[:200]

        for company_name in seed_companies:
            if len(discovered) >= max_companies:
                break

            try:
                # Convert company name to slug
                company_slug = company_name.lower().replace(' ', '-')
                company_slug = re.sub(r'[^a-z0-9\-]+', '', company_slug)

                if not company_slug or len(company_slug) < 2:
                    continue

                # Try Ashby URL pattern
                ashby_url = f"https://jobs.ashbyhq.com/{company_slug}"

                response = requests.get(
                    ashby_url,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=5,
                    allow_redirects=True
                )

                if response.status_code == 200 and 'ashbyhq' in response.url.lower():
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for security jobs
                    job_listings = soup.find_all(['a', 'div'], string=re.compile(r'security|cyber|infosec|soc|threat|devsecops|appsec|cloud\s*security|iam', re.I))

                    if job_listings:
                        discovered.add(company_name)

                        for job in job_listings[:5]:
                            job_link = job if job.name == 'a' else job.find_parent('a')
                            if job_link and job_link.get('href'):
                                job_url = urljoin(ashby_url, job_link['href'])
                                job_title = job.get_text(strip=True)

                                self.companies[company_name]['hiring'].append({
                                    'title': job_title,
                                    'url': job_url,
                                    'location': 'Multiple Locations',
                                    'source': 'Ashby',
                                    'posted_date': 'Recent'
                                })

                        if len(discovered) % 10 == 0:
                            print(f"      ✅ Found: {len(discovered)} companies on Ashby...")

            except:
                continue

        print(f"   ✅ Ashby: Found {len(discovered)} companies")
        return discovered

    def _scrape_hiring_cafe(self, max_companies: int) -> Set[str]:
        """
        NEW METHOD: Scrape Hiring.cafe
        Curated list of tech/SaaS companies hiring
        """
        discovered = set()
        print(f"   ℹ️  Scraping Hiring.cafe...")

        try:
            # Hiring.cafe has a curated list of companies
            url = "https://hiring.cafe/"

            response = requests.get(
                url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for company listings
                company_links = soup.find_all('a', href=re.compile(r'/company/|/companies/'))

                for link in company_links[:max_companies]:
                    try:
                        company_name = link.get_text(strip=True)

                        if 2 <= len(company_name) <= 100:
                            # Visit company page to check for security jobs
                            company_url = urljoin(url, link['href'])

                            company_response = requests.get(
                                company_url,
                                headers={'User-Agent': 'Mozilla/5.0'},
                                timeout=5
                            )

                            if company_response.status_code == 200:
                                company_soup = BeautifulSoup(company_response.text, 'html.parser')

                                # Look for security-related jobs
                                security_jobs = company_soup.find_all(string=re.compile(r'security|cyber|infosec|soc|threat|devsecops|appsec', re.I))

                                if security_jobs:
                                    discovered.add(company_name)

                                    if company_name not in self.companies:
                                        self.companies[company_name] = {'hiring': [], 'conversations': []}

                                    # Extract job details
                                    for job_elem in security_jobs[:3]:
                                        job_link = job_elem.find_parent('a')
                                        if job_link and job_link.get('href'):
                                            job_url = urljoin(company_url, job_link['href'])

                                            self.companies[company_name]['hiring'].append({
                                                'title': job_elem.strip(),
                                                'url': job_url,
                                                'location': 'Various',
                                                'source': 'Hiring.cafe',
                                                'posted_date': 'Recent'
                                            })

                                    if len(discovered) % 10 == 0:
                                        print(f"      ✅ Found: {len(discovered)} companies...")

                    except:
                        continue

        except Exception as e:
            print(f"      ⚠️  Error scraping Hiring.cafe: {str(e)[:100]}")

        print(f"   ✅ Hiring.cafe: Found {len(discovered)} companies")
        return discovered

    def _scrape_smartrecruiters(self, max_companies: int) -> Set[str]:
        """
        NEW METHOD: Scrape SmartRecruiters
        Common ATS for cybersecurity and enterprise tech
        """
        discovered = set()
        print(f"   ℹ️  Scraping SmartRecruiters...")

        # Try SmartRecruiters URL patterns for existing companies
        seed_companies = list(self.companies.keys())[:200]

        for company_name in seed_companies:
            if len(discovered) >= max_companies:
                break

            try:
                # Convert company name to slug
                company_slug = company_name.lower().replace(' ', '')
                company_slug = re.sub(r'[^a-z0-9]+', '', company_slug)

                if not company_slug or len(company_slug) < 2:
                    continue

                # SmartRecruiters URL pattern
                sr_url = f"https://careers.smartrecruiters.com/{company_slug}"

                response = requests.get(
                    sr_url,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=5,
                    allow_redirects=True
                )

                if response.status_code == 200 and 'smartrecruiters' in response.url.lower():
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for security jobs
                    job_listings = soup.find_all(['a', 'div', 'h3'], string=re.compile(r'security|cyber|infosec|soc|threat|devsecops|appsec|cloud\s*security', re.I))

                    if job_listings:
                        discovered.add(company_name)

                        for job in job_listings[:5]:
                            job_link = job if job.name == 'a' else job.find_parent('a')
                            if job_link and job_link.get('href'):
                                job_url = urljoin(sr_url, job_link['href'])
                                if not job_url.startswith('http'):
                                    job_url = f"https://careers.smartrecruiters.com{job_link['href']}"

                                job_title = job.get_text(strip=True)

                                self.companies[company_name]['hiring'].append({
                                    'title': job_title,
                                    'url': job_url,
                                    'location': 'Multiple Locations',
                                    'source': 'SmartRecruiters',
                                    'posted_date': 'Recent'
                                })

                        if len(discovered) % 10 == 0:
                            print(f"      ✅ Found: {len(discovered)} companies on SmartRecruiters...")

            except:
                continue

        print(f"   ✅ SmartRecruiters: Found {len(discovered)} companies")
        return discovered

    def _scrape_bamboohr(self, max_companies: int) -> Set[str]:
        """
        NEW METHOD: Scrape BambooHR
        Used by many mid-size SaaS/security companies
        """
        discovered = set()
        print(f"   ℹ️  Scraping BambooHR...")

        # Try BambooHR URL patterns for existing companies
        seed_companies = list(self.companies.keys())[:200]

        for company_name in seed_companies:
            if len(discovered) >= max_companies:
                break

            try:
                # Convert company name to slug
                company_slug = company_name.lower().replace(' ', '')
                company_slug = re.sub(r'[^a-z0-9]+', '', company_slug)

                if not company_slug or len(company_slug) < 2:
                    continue

                # BambooHR URL pattern
                bamboo_url = f"https://{company_slug}.bamboohr.com/careers/"

                response = requests.get(
                    bamboo_url,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=5,
                    allow_redirects=True
                )

                if response.status_code == 200 and 'bamboohr' in response.url.lower():
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for security jobs
                    job_listings = soup.find_all(['a', 'div', 'li'], string=re.compile(r'security|cyber|infosec|soc|threat|devsecops|appsec|cloud\s*security|iam', re.I))

                    if job_listings:
                        discovered.add(company_name)

                        for job in job_listings[:5]:
                            job_link = job if job.name == 'a' else job.find_parent('a')
                            if job_link and job_link.get('href'):
                                job_url = urljoin(bamboo_url, job_link['href'])
                                if not job_url.startswith('http'):
                                    job_url = f"https://{company_slug}.bamboohr.com{job_link['href']}"

                                job_title = job.get_text(strip=True)

                                self.companies[company_name]['hiring'].append({
                                    'title': job_title,
                                    'url': job_url,
                                    'location': 'Multiple Locations',
                                    'source': 'BambooHR',
                                    'posted_date': 'Recent'
                                })

                        if len(discovered) % 10 == 0:
                            print(f"      ✅ Found: {len(discovered)} companies on BambooHR...")

            except:
                continue

        print(f"   ✅ BambooHR: Found {len(discovered)} companies")
        return discovered

    def _discover_conversation_signals(self, target_posts: int):
        """Discover conversation signals from RSS feeds"""
        print(f"\n💬 CONVERSATION SIGNAL DISCOVERY")
        print("=" * 70)
        print(f"Target: {target_posts} quality posts from Top 10 publishers")

        posts_collected = 0

        for publisher, rss_url in self.top_publishers.items():
            if posts_collected >= target_posts:
                break

            print(f"\n   Scanning: {publisher}...")

            try:
                response = requests.get(rss_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')[:10]  # Get up to 10 recent posts

                for item in items:
                    if posts_collected >= target_posts:
                        break

                    title = item.find('title')
                    link = item.find('link')
                    pub_date = item.find('pubDate')

                    if title and link:
                        title_text = title.text.strip()
                        link_text = link.text.strip()

                        # Filter for security-relevant content
                        if any(keyword in title_text.lower() for keyword in [
                            'security', 'threat', 'vulnerability', 'attack', 'breach',
                            'ransomware', 'malware', 'phishing', 'zero-day', 'exploit',
                            'cloud', 'saas', 'sspm', 'iam', 'compliance', 'encryption'
                        ]):
                            # Add to companies dict
                            if publisher not in self.companies:
                                self.companies[publisher] = {'hiring': [], 'conversations': []}

                            self.companies[publisher]['conversations'].append({
                                'title': title_text,
                                'url': link_text,
                                'published_at': pub_date.text if pub_date else 'Recent',
                                'source': 'RSS Feed'
                            })

                            posts_collected += 1
                            print(f"      ✅ {title_text[:60]}...")

                print(f"   ✅ {publisher}: {len([p for p in self.companies.get(publisher, {}).get('conversations', [])])} relevant posts")

            except Exception as e:
                print(f"   ⚠️  Error scanning {publisher}: {str(e)[:50]}")
                continue

        print(f"\n📊 Total quality posts discovered: {posts_collected}")

    def _is_valid_company_name(self, name: str) -> bool:
        """
        Validate that extracted text is actually a company name, not UI elements

        Filters out:
        - HTML fragments (e.g., "e account", "sign inorcreate")
        - Navigation elements
        - Generic text
        """
        if not name or len(name) < 2:
            return False

        # Must be reasonable length (2-100 chars)
        if len(name) > 100:
            return False

        # Filter out UI text fragments
        invalid_patterns = [
            r'\btosign\b', r'\binorcreate\b', r'\baccount\b.*\bsave\b',
            r'^e\s', r'^e$', r'need\s*to', r'sign\s*in', r'create\s*an',
            r'POST\s*A\s*JOB', r'apply\s*for', r'maximum\s*exposure',
            r'^Hiring\s*Companies$', r'^Latest\s*News$', r'Why\s*choose',
            r'need.*account', r'You\s*need', r'Apply$',
            r'^ed\s*Today', r'^es\s*to\s*apply', r'^terson\s', r'^ion\s',
            r'See\s*wha$', r'Description\s*See', r'Not\s*Specified'
        ]

        for pattern in invalid_patterns:
            if re.search(pattern, name, re.IGNORECASE):
                return False

        # Must contain at least one letter
        if not re.search(r'[A-Za-z]', name):
            return False

        # Filter out generic phrases
        generic_terms = {
            'job', 'apply', 'save', 'account', 'login', 'sign in',
            'post a job', 'latest news', 'hiring companies', 'careers',
            'you need', 'create an account', 'maximum exposure',
            'ed today', 'ed todayts', 'ed todaysecret', 'terson air force bas',
            'es to apply for maximum exposure', 'ion engineer'
        }

        if name.lower().strip() in generic_terms:
            return False

        # Must start with letter or number (not special char)
        if not re.match(r'^[A-Za-z0-9]', name):
            return False

        return True

    def _clean_company_name(self, name: str) -> str:
        """Clean and standardize company names"""
        name = re.sub(r'\s+(Inc\.|LLC|Corp|Corporation|Ltd|Limited|Co\.)$', '', name, flags=re.IGNORECASE)
        name = name.strip()
        return name if len(name) > 1 else None

    def _generate_company_tracker(self) -> List[Dict]:
        """Generate company tracker data"""
        tracker = []

        for company_name, data in self.companies.items():
            role_count = len(data['hiring'])
            post_count = len(data['conversations'])

            if role_count > 0 and post_count > 0:
                activity_type = 'both'
                priority_score = 3
            elif role_count > 0:
                activity_type = 'hiring_only'
                priority_score = 2
            elif post_count > 0:
                activity_type = 'talking_only'
                priority_score = 1
            else:
                # Include companies even with no data yet (from VC/discovery)
                activity_type = 'discovered'
                priority_score = 0

            tracker.append({
                'company_name': company_name,
                'activity_type': activity_type,
                'role_count': role_count,
                'post_count': post_count,
                'priority_score': priority_score,
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            })

        # Sort by priority
        tracker.sort(key=lambda x: (x['priority_score'], x['role_count'] + x['post_count']), reverse=True)

        return tracker

    def _print_summary(self, tracker: List[Dict]):
        """Print discovery summary"""
        high_priority = [c for c in tracker if c['activity_type'] == 'both']
        hiring_only = [c for c in tracker if c['activity_type'] == 'hiring_only']
        talking_only = [c for c in tracker if c['activity_type'] == 'talking_only']

        print("\n" + "=" * 70)
        print("📊 DISCOVERY SUMMARY")
        print("=" * 70)
        print(f"\n🎯 HIGH PRIORITY (Both Hiring + Talking): {len(high_priority)}")
        for c in high_priority[:5]:
            print(f"   {c['company_name']:30} | {c['role_count']} roles | {c['post_count']} posts")

        print(f"\n📢 HIRING ONLY: {len(hiring_only)}")
        for c in hiring_only[:10]:
            print(f"   {c['company_name']:30} | {c['role_count']} roles")

        print(f"\n💬 TALKING ONLY: {len(talking_only)}")
        for c in talking_only[:5]:
            print(f"   {c['company_name']:30} | {c['post_count']} posts")

        print(f"\n📊 TOTAL COMPANIES DISCOVERED: {len(tracker)}")


if __name__ == "__main__":
    engine = CompanyDiscoveryV3()
    tracker = engine.discover_all(companies_target=1000, posts_target=50)

    print(f"\n✅ Discovery complete!")
    print(f"📊 Discovered {len(tracker)} companies")
