from browser_use import Agent, Browser, BrowserProfile, ChatBrowserUse, Tools, ActionResult, BrowserSession
import asyncio
import os
import base64

# ─── Custom tools ─────────────────────────────────────────────────────────────
tools = Tools()

@tools.action('Ask the human operator for missing information')
async def ask_human(question: str, browser_session: BrowserSession) -> ActionResult:
    print(f'\n{"="*60}')
    print(f'🤖 Agent needs your input:')
    print(f'   {question}')
    print(f'{"="*60}')
    answer = input('Your answer: ').strip()
    return ActionResult(extracted_content=answer)


@tools.action('Upload a resume/CV file to the file input on the page automatically')
async def upload_resume(browser_session: BrowserSession) -> ActionResult:
    resume_path = RESUME_PATH

    if not resume_path or not os.path.exists(resume_path):
        return ActionResult(
            error=f"Resume file not found at: '{resume_path}'. "
                  "Please set the RESUME_PATH variable at the top of this script."
        )

    with open(resume_path, 'rb') as f:
        file_data = base64.b64encode(f.read()).decode('utf-8')

    file_name = os.path.basename(resume_path)
    mime_type = _get_mime_type(file_name)

    js_script = f"""(...args) => {{
        const inputs = document.querySelectorAll('input[type="file"]');
        if (inputs.length === 0) {{
            return 'ERROR: No file input found on the page';
        }}

        let target = inputs[0];
        for (const inp of inputs) {{
            const label = (inp.getAttribute('name') || '') +
                          (inp.getAttribute('id') || '') +
                          (inp.getAttribute('accept') || '');
            if (/resume|cv|upload/i.test(label)) {{
                target = inp;
                break;
            }}
        }}

        const byteChars = atob('{file_data}');
        const byteNums = new Array(byteChars.length);
        for (let i = 0; i < byteChars.length; i++) {{
            byteNums[i] = byteChars.charCodeAt(i);
        }}
        const byteArray = new Uint8Array(byteNums);
        const file = new File([byteArray], '{file_name}', {{ type: '{mime_type}' }});

        const dt = new DataTransfer();
        dt.items.add(file);
        target.files = dt.files;

        target.dispatchEvent(new Event('change', {{ bubbles: true }}));
        target.dispatchEvent(new Event('input', {{ bubbles: true }}));

        return 'SUCCESS: Uploaded {file_name} to input[name="' + (target.name || target.id || '?') + '"]';
    }}"""

    page = await browser_session.get_current_page()
    result = await page.evaluate(js_script)

    if str(result).startswith('ERROR'):
        return ActionResult(error=result)

    return ActionResult(extracted_content=f"✅ Resume uploaded automatically: {result}")


def _get_mime_type(filename: str) -> str:
    ext = filename.lower().rsplit('.', 1)[-1]
    return {
        'pdf':  'application/pdf',
        'doc':  'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'txt':  'text/plain',
    }.get(ext, 'application/octet-stream')


# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
RESUME_PATH       = "./Arul_Murugan_Fullstack_Resume.pdf"       # <── CHANGE IF NEEDED
COVER_LETTER_PATH = "./Arul_Murugan_Cover_Letter.docx"          # <── Cover letter file

# ─── Load cover letter text ───────────────────────────────────────────────────
def load_cover_letter(path: str) -> str:
    """Extract plain text from cover letter .docx for use in form fields."""
    try:
        import zipfile, re
        with zipfile.ZipFile(path, "r") as z:
            xml = z.read("word/document.xml").decode("utf-8")
        text = re.sub(r"<[^>]+>", " ", xml)
        text = re.sub(r"\s+", " ", text).strip()
        return text
    except Exception as e:
        print(f"⚠️  Could not load cover letter from '{path}': {e}")
        return "[Cover letter file not found — please paste manually]"

COVER_LETTER_TEXT = load_cover_letter(COVER_LETTER_PATH) if os.path.exists(COVER_LETTER_PATH) else "[Cover letter file missing]"

# ─── COMPLETE CANDIDATE PROFILE ───────────────────────────────────────────────
PROFILE = f"""
==================================================
PERSONAL INFORMATION
==================================================
Full Name         : Arul Murugan J
First Name        : Arul
Last Name         : Murugan J
Date of Birth     : 06 October 2001
Gender            : Male
Marital Status    : Unmarried
Nationality       : Indian
Languages Known   : English, Tamil

==================================================
CONTACT INFORMATION
==================================================
Primary Phone     : +91-7539904141
Secondary Phone   : +91-9047942707
Primary Email     : arulmurugan.code@gmail.com
Current Address   : 20, 5th Cross St, Madambakkam, Guduvancheri, Chennai, Tamil Nadu 603202
Permanent Address : 20, 5th Cross St, Madambakkam, Guduvancheri, Chennai, Tamil Nadu 603202
City              : Chennai
State             : Tamil Nadu
Country           : India
PIN Code          : 603202

==================================================
PROFESSIONAL LINKS
==================================================
LinkedIn          : https://linkedin.com/in/arul-murugan-j
GitHub            : https://github.com/arulmurugan01
Portfolio         : N/A

==================================================
CURRENT EMPLOYMENT
==================================================
Employment Status : Currently Not Working (Available Immediately)
Last Company      : Piccosoft Software Labs Pvt Ltd
Last Designation  : Full Stack Developer
Join Date         : March 2024
End Date          : February 22, 2026
Duration          : ~2 Years
Location          : Chennai, Tamil Nadu
Notice Period     : Immediate (0 Days) — Currently Not Working

==================================================
PREVIOUS EMPLOYMENT
==================================================
Company           : Struzon Technologies
Designation       : System Administrator
Join Date         : October 2022
End Date          : December 2023
Duration          : ~1 Year 2 Months
Location          : Tamil Nadu

==================================================
TOTAL EXPERIENCE
==================================================
Total IT Experience    : 3+ Years
Relevant Experience    : 2 Years (Full Stack Development)
Domain                 : Software Development / Full Stack / Web Applications

==================================================
COMPENSATION
==================================================
Current / Last CTC     : ₹1,56,000 per annum (₹13,000/month in-hand)
Expected CTC           : ₹4,30,000 per annum (₹35,000/month)
Open to Negotiate      : Yes

==================================================
JOB PREFERENCES
==================================================
Open to Relocation     : Yes
Preferred Locations    : Chennai, Bangalore, Hyderabad, Coimbatore
Open to Remote         : Yes
Open to Hybrid         : Yes
Interview Availability : Immediate / Weekdays

==================================================
EDUCATION
==================================================
Degree       : Bachelor of Science — Visual Communication
College      : Sree Amman Arts and Science College
Location     : Erode, Tamil Nadu
Join Year    : June 2018
Pass Year    : 2021
Duration     : 3 Years

==================================================
TECHNICAL SKILLS
==================================================
Languages            : JavaScript, TypeScript
Frontend             : React.js, HTML5, CSS3
Backend              : Node.js, Express.js, RESTful APIs, TypeORM, WebSocket, Socket.IO
Databases            : MySQL, Database Design, Query Optimization
Caching / Messaging  : Redis, RabbitMQ
Cloud / DevOps       : AWS (EC2, S3), Docker, Linux, Nginx
Auth & Security      : JWT, OAuth 2.0, RBAC
Architecture         : Microservices, Event-Driven Systems
AI / Automation      : RAG-Based AI Integration, OpenAI API Integration, MCP Server
Tools                : Git, GitHub, Postman, VS Code

==================================================
KEY PROJECTS
==================================================
1. AI-Powered Job Intelligence Platform
   Stack : Node.js, React.js, MySQL, Redis, RabbitMQ, Docker, Nginx, OpenAI
   - Microservices-based architecture
   - Event-driven pipelines with RabbitMQ
   - Real-time logs via WebSockets
   - RAG-based AI resume generation
   - Dockerized multi-service deployment

2. E-Commerce Platform
   Stack : React.js, Node.js, TypeScript, MySQL, Redis, AWS
   - Product catalog & order workflows
   - JWT/RBAC authentication
   - Payment integration
   - Reduced API latency by 35%

3. Blogging & CMS Platform
   Stack : Node.js, Express.js, MySQL
   - SEO-optimized CMS
   - Normalized DB schema
   - RESTful architecture

==================================================
PROFESSIONAL HEADLINE (Use for LinkedIn / Job Portals)
==================================================
Full Stack Developer | React.js · Node.js · TypeScript | Microservices · Redis · RabbitMQ | AWS · Docker | AI Integration

==================================================
SHORT SUMMARY (50-100 words — Use for Short Bio Fields)
==================================================
Full Stack Developer with 2+ years of experience building scalable web applications using React.js, Node.js, and TypeScript. Skilled in microservices architecture, Redis caching, RabbitMQ event-driven pipelines, Docker containerization, and AWS deployments. Hands-on experience integrating AI features using OpenAI APIs and RAG pipelines. Previously worked as a System Administrator with Linux server management experience. Seeking a challenging role to build impactful products.

==================================================
DETAILED PROFESSIONAL SUMMARY (200+ words — Use for Long Summary / Cover Letter Fields)
==================================================
I am Arul Murugan J, a Full Stack Developer with over 2 years of hands-on experience designing and building production-grade web applications. My core expertise lies in React.js for frontend development and Node.js with TypeScript for scalable backend systems.

At Piccosoft Software Labs, I contributed to building high-performance applications using microservices architecture, implemented event-driven communication pipelines with RabbitMQ, and improved system performance through Redis caching and MySQL query optimization. I deployed and managed multi-service applications using Docker on AWS EC2 and handled static assets via S3. I also integrated AI capabilities using OpenAI APIs and RAG pipelines, enabling intelligent features within business applications.

Prior to my development role, I worked as a System Administrator at Struzon Technologies, where I managed Linux servers, monitored production infrastructure, and implemented security hardening and backup strategies — giving me a well-rounded understanding of both development and operations.

I am passionate about writing clean, maintainable code and delivering robust software solutions. I thrive in Agile environments and enjoy collaborating with cross-functional teams to solve real-world problems. I am immediately available, open to relocation, and excited to contribute to a high-impact engineering team.

==================================================
COVER LETTER (Use when a Cover Letter field appears)
==================================================
{COVER_LETTER_TEXT}

==================================================
COMMON SCREENING QUESTION ANSWERS
==================================================
Are you authorized to work in India?             : Yes
Are you willing to relocate?                     : Yes
Are you currently employed?                      : No, currently not working
What is your notice period?                      : Immediate — available to join right away
Do you have experience with React.js?            : Yes, 2 years
Do you have experience with Node.js?             : Yes, 2 years
Do you have experience with TypeScript?          : Yes
Do you have experience with AWS?                 : Yes — EC2 and S3
Do you have experience with Docker?              : Yes
Do you have experience with Microservices?       : Yes
Do you have experience with REST APIs?           : Yes
Do you have experience with MySQL?               : Yes
Do you have experience with Redis?               : Yes
Do you have experience with RabbitMQ?            : Yes
Are you a fresher or experienced?                : Experienced
Years of experience?                             : 2 years (Full Stack), 3+ years total IT
Highest qualification?                           : Bachelor of Science — Visual Communication (2021)
Why are you looking for a change?                : Seeking better growth opportunities and a challenging role that aligns with my full stack skills
"""

# ─── TASK ─────────────────────────────────────────────────────────────────────
JOB_LINK = "https://www.linkedin.com/jobs/view/4375520497"

TASK = f"""
You are an expert AI Job Application Agent. Your job is to open the application form and fill it completely and accurately using the candidate profile provided.

==================================================
CANDIDATE PROFILE
==================================================
{PROFILE}

==================================================
STEP 1 — OPEN APPLICATION
==================================================
Navigate to this job link:
{JOB_LINK}

Wait until the page is fully loaded before proceeding.

==================================================
STEP 2 — FILL ALL FORM FIELDS
==================================================
Fill every visible field using the candidate profile above.

Field mapping rules:
- "Name / Full Name"         → Arul Murugan J
- "First Name"               → Arul
- "Last Name"                → Murugan J
- "Email"                    → arulmurugan.code@gmail.com
- "Phone / Mobile"           → 7539904141
- "Location / City"          → Chennai, Tamil Nadu, India
- "Current Company"          → Piccosoft Software Labs Pvt Ltd
- "Current Designation"      → Full Stack Developer
- "Total Experience"         → 2 Years (or 3 if asking total IT)
- "Notice Period"             → Immediate / 0 Days
- "Current CTC"              → 1,56,000 per annum
- "Expected CTC"             → 4,30,000 per annum
- "LinkedIn"                 → https://linkedin.com/in/arul-murugan-j
- "GitHub"                   → https://github.com/arulmurugan01
- "Headline / Title"         → Use PROFESSIONAL HEADLINE from profile
- "Summary / Bio"            → Use SHORT SUMMARY or DETAILED SUMMARY based on field size
- "Cover Letter"             → Use COVER LETTER from profile
- "Skills"                   → Fill from TECHNICAL SKILLS section
- "Highest Qualification"    → Bachelor of Science — Visual Communication
- "College / University"     → Sree Amman Arts and Science College, Erode
- "College / University - location'     → Erode, Tamil Nadu, India
- "Year of Passing"          → 2021

If a dropdown exists → select the closest matching option.
If a field is not in the profile → use ask_human tool.
Do NOT leave any required field empty.

AUTOCOMPLETE / DROPDOWN FALLBACK RULES:
- If you type into an input and an autocomplete suggestion list appears → click the best matching suggestion.
- If NO suggestion appears or the list is empty after typing → use ask_human tool with the message: "Please manually select or type the value for the field: [field name]. Current typed value was: [value]" and wait for the user to act.
- If a dropdown (select box) cannot be set programmatically → use ask_human tool with: "Please manually select '[expected value]' from the dropdown: [field name]"
- If a location/city/country autocomplete fails to resolve → ask_human: "Please click and select the location from the suggestions for field: [field name]"
- After ask_human returns, verify the field now has a value before moving on. If still empty, ask again.

==================================================
STEP 3 — RESUME UPLOAD
==================================================
When you encounter a resume/CV file upload field:
1. Call upload_resume tool — it injects the file via JavaScript automatically.
2. Wait 2 seconds.
3. Confirm the filename appears on the page.
4. If upload_resume fails → use ask_human as fallback.

IMPORTANT: Do NOT click the file input button manually.
IMPORTANT: Do NOT use the upload_file tool — always use upload_resume instead.

==================================================
STEP 4 — SCREENING / KNOCKOUT QUESTIONS
==================================================
Answer all yes/no and text screening questions using the COMMON SCREENING QUESTION ANSWERS section in the profile.

For any question not covered → use ask_human tool.

==================================================
STEP 5 — FINAL REVIEW
==================================================
Scroll the entire page top to bottom and check:
- All required fields are filled
- No red validation errors visible
- Required checkboxes are checked
- Resume upload is confirmed

Fix anything missing before proceeding.

==================================================
STEP 6 — SUBMIT
==================================================
Once all fields are verified:
- Click the Submit / Apply / Send Application button.
- If a confirmation screen appears → report success with the confirmation message.
- If an error appears → fix it and retry.

==================================================
GENERAL RULES
==================================================
- Use ask_human ONLY when information is truly missing from the profile
- Be careful with dropdowns — select the best matching option
- Do NOT navigate away from the application page
- Do NOT guess or hallucinate any information not in the profile
- Output a single clean final status line — no bullet points or newlines in final result
"""


async def main():
    resume_abs_path = os.path.abspath(RESUME_PATH)

    if not os.path.exists(resume_abs_path):
        print(f"⚠️  WARNING: Resume file not found at: '{resume_abs_path}'")
        print("   Please update the RESUME_PATH variable at the top of the script.")
        print("   The agent will still run but resume upload will fail without it.\n")

    browser = Browser(cdp_url="http://localhost:9222")

    agent = Agent(
        task=TASK,
        llm=ChatBrowserUse(),
        browser=browser,
        tools=tools,
        available_file_paths=[resume_abs_path] if os.path.exists(resume_abs_path) else [],
    )

    result = await agent.run()
    print("\n" + "="*60)
    print("✅ Agent finished. Final report:")
    print("="*60)
    print(result.final_result())

if __name__ == "__main__":
    asyncio.run(main())