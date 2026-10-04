-- CareerAI Seed Data
-- Comprehensive realistic tech careers, skills, requirements, and default admin

-- 1. Default Admin Account (Password: Admin@12345 -> pbkdf2:sha256 hash)
INSERT OR IGNORE INTO users (id, username, email, password_hash, role) VALUES 
(1, 'admin', 'admin@careerai.com', 'scrypt:32768:8:1$Gceni2jwXaIUjSxC$8e2f6b5a69852f22b5d7589559452c63b5c41a05c66651ce3c88a6bb1c5bb50b226f8c592e5962bbafbbcf584d15c72e8bd2b72dacbf92721cd1947a9d3e5923', 'admin');

-- 2. Skills Seed Data
INSERT OR IGNORE INTO skills (id, name, category, description) VALUES
-- Technical Skills
(1, 'Python', 'technical', 'Core Python programming, OOP, data structures, and standard library'),
(2, 'Java', 'technical', 'Java SE/EE, JVM architecture, Spring Boot, enterprise patterns'),
(3, 'C', 'technical', 'Procedural C programming, pointers, low-level memory management'),
(4, 'C++', 'technical', 'Modern C++ (11/14/17/20), STL, high-performance computing'),
(5, 'JavaScript', 'technical', 'Modern ECMAScript, asynchronous programming, DOM, Web APIs'),
(6, 'SQL', 'technical', 'Relational database querying, joins, indexing, window functions'),
(7, 'HTML/CSS', 'technical', 'Semantic HTML5, CSS3, Flexbox, Grid, responsive UI design'),
(8, 'Machine Learning', 'technical', 'Supervised/unsupervised algorithms, scikit-learn, validation, metrics'),
(9, 'Deep Learning', 'technical', 'Neural networks, PyTorch/TensorFlow, CNNs, RNNs, Transformers'),
(10, 'Data Analysis', 'technical', 'Data wrangling, Pandas, NumPy, statistical testing, EDA'),
(11, 'Cloud', 'technical', 'AWS, Azure, GCP cloud architecture, compute, storage, IAM'),
(12, 'Cybersecurity', 'technical', 'Network defense, threat modeling, vulnerability analysis, cryptography'),
(13, 'Networking', 'technical', 'TCP/IP, OSI model, routing, DNS, HTTP/HTTPS, protocols'),
(14, 'Database', 'technical', 'Database design, normalization, ACID, MySQL, PostgreSQL, NoSQL'),
(15, 'Git/GitHub', 'technical', 'Version control, branching strategies, merge conflicts, CI workflows'),

-- Soft Skills
(16, 'Communication', 'soft', 'Verbal and written clarity, technical documentation, stakeholder updates'),
(17, 'Leadership', 'soft', 'Project ownership, mentoring peers, driving initiatives, decision making'),
(18, 'Teamwork', 'soft', 'Cross-functional collaboration, active listening, code reviews'),
(19, 'Problem Solving', 'soft', 'Algorithmic thinking, debugging complex issues, root cause analysis'),
(20, 'Analytical Thinking', 'soft', 'Data-driven reasoning, critical evaluation of trade-offs and metrics'),
(21, 'Creativity', 'soft', 'Innovative solution design, intuitive UI patterns, novel architectures'),
(22, 'Presentation', 'soft', 'Delivering tech demos, slide decks, explaining architecture to non-tech'),
(23, 'Time Management', 'soft', 'Sprint planning, estimating tasks, delivering under deadlines');

-- 3. Interests Seed Data
INSERT OR IGNORE INTO interests (id, name, category, description) VALUES
(1, 'Artificial Intelligence', 'AI & Data', 'Building autonomous agents, heuristics, cognitive systems'),
(2, 'Machine Learning', 'AI & Data', 'Predictive modeling, scikit-learn, statistical learning'),
(3, 'Data Science', 'AI & Data', 'Deriving business insights from massive datasets, visual analytics'),
(4, 'Software Development', 'Engineering', 'Designing scalable modular backend & desktop applications'),
(5, 'Web Development', 'Engineering', 'Full-stack responsive web systems and interactive client apps'),
(6, 'Mobile Development', 'Engineering', 'Native & cross-platform applications for Android and iOS'),
(7, 'Cybersecurity', 'Security & Infrastructure', 'Penetration testing, security auditing, digital forensics'),
(8, 'Cloud Computing', 'Security & Infrastructure', 'Infrastructure-as-code, multi-cloud hosting, serverless'),
(9, 'DevOps', 'Security & Infrastructure', 'CI/CD automation, Docker containers, Kubernetes orchestration'),
(10, 'UI/UX', 'Design', 'User research, wireframing, high-fidelity Figma prototypes'),
(11, 'Research', 'Academic', 'Writing academic papers, empirical experimentation, novel algorithms'),
(12, 'Business/Management', 'Management', 'Product strategy, agile scrum mastery, client collaboration');

-- 4. Careers Seed Data (12 Industry Roles)
INSERT OR IGNORE INTO careers (id, code, title, category, description, required_qualification, experience_level, average_salary_range, difficulty, outlook, responsibilities, project_suggestions) VALUES
(1, 'AIML_ENG', 'AI/ML Engineer', 'AI & Data Science', 
 'Designs, trains, tests, and deploys machine learning models and intelligent software systems into scalable production environments.',
 'B.Tech / M.Tech in CSE / AI & ML or related field', 'Entry to Mid Level', '₹7 - 18 LPA ($95k - $160k)', 'Advanced', 'Extremely High Growth (+38% YoY)',
 '1. Develop production-ready ML and Deep Learning models.\n2. Build data pipelines for feature extraction and normalization.\n3. Implement model monitoring, drift detection, and retraining.\n4. Optimize inference latency and deploy models via REST APIs / Docker.',
 '1. End-to-End Predictive Maintenance with Scikit-Learn and FastAPI\n2. Object Detection & Tracking with PyTorch & OpenCV\n3. Conversational QA Engine with Vector Search & Embeddings'),

(2, 'DATA_SCI', 'Data Scientist', 'AI & Data Science',
 'Leverages statistical analysis, machine learning algorithms, and domain expertise to extract actionable intelligence from structured and unstructured data.',
 'B.Tech / B.Sc in CSE, Data Science, Statistics, or Math', 'Entry to Mid Level', '₹6.5 - 16 LPA ($90k - $150k)', 'Advanced', 'High Growth (+28% YoY)',
 '1. Conduct comprehensive Exploratory Data Analysis (EDA) on complex datasets.\n2. Formulate hypotheses and design rigorous A/B experiments.\n3. Build predictive regression, classification, and clustering models.\n4. Communicate statistical findings and business recommendations to executives.',
 '1. Customer Churn Prediction and Lifetime Value Analysis\n2. Credit Risk Scoring Model with Explainable AI (SHAP)\n3. Healthcare Prognosis Classifier using Clinical Tabular Data'),

(3, 'DATA_ANL', 'Data Analyst', 'Data Analytics',
 'Gathers, inspects, cleans, and visualizes organizational data to help business leaders make informed tactical and strategic decisions.',
 'B.Tech / B.Sc in CSE, IT, Business, or Economics', 'Entry Level', '₹4.5 - 10 LPA ($65k - $105k)', 'Moderate', 'Steady High Demand',
 '1. Write performant SQL queries to extract data from enterprise data warehouses.\n2. Design interactive business intelligence dashboards in Tableau/Power BI.\n3. Clean messy operational spreadsheets and automate data reporting.\n4. Identify trends, bottlenecks, and KPIs across operational business units.',
 '1. E-Commerce Sales Performance & KPI Dashboard\n2. Supply Chain Logistics Optimization and Delay Analysis\n3. Financial Fraud Detection and Anomaly Reporting'),

(4, 'SDE', 'Software Engineer', 'Software Engineering',
 'Engineers robust, scalable, and maintainable software systems, services, and backend APIs following clean code and architectural design patterns.',
 'B.Tech / B.E in Computer Science or Information Technology', 'Entry to Mid Level', '₹6 - 18 LPA ($85k - $150k)', 'Intermediate', 'Consistently High Demand',
 '1. Design and maintain high-throughput backend services and microservices.\n2. Write clean, tested, and modular code in Python, Java, or C++.\n3. Collaborate on Git pull requests, code reviews, and architectural RFCs.\n4. Debug production incidents and optimize database queries and memory usage.',
 '1. Distributed Task Queue & Asynchronous Job Scheduler\n2. Enterprise Role-Based Access Control (RBAC) Microservice\n3. High-Concurrency REST API with In-Memory Caching (Redis)'),

(5, 'WEB_DEV', 'Web Developer', 'Web Engineering',
 'Builds high-performance, dynamic, and responsive web applications, integrating elegant user interfaces with secure backend web servers.',
 'B.Tech, BCA, or B.Sc in Computer Science / IT', 'Entry Level', '₹4.5 - 12 LPA ($70k - $120k)', 'Moderate', 'High Demand',
 '1. Develop responsive client-side web components with modern HTML/CSS/JavaScript.\n2. Implement RESTful / GraphQL APIs with robust validation and security.\n3. Manage state, local storage, and client-server asynchronous communication.\n4. Ensure cross-browser compatibility and web accessibility standards.',
 '1. Full-Stack E-Learning Management System with Live Progress\n2. Real-Time Collaborative Workspace with WebSockets\n3. SaaS Analytics Portal with Interactive Dashboards'),

(6, 'MOB_DEV', 'Mobile Developer', 'Mobile Engineering',
 'Architects and builds native and cross-platform mobile apps for smartphones and tablets, prioritizing touch interaction, offline sync, and smooth 60fps UI.',
 'B.Tech / BCA / B.Sc in Computer Science', 'Entry to Mid Level', '₹5 - 14 LPA ($75k - $130k)', 'Intermediate', 'Growing Demand',
 '1. Build cross-platform applications using Flutter / React Native or native Android (Kotlin) / iOS (Swift).\n2. Integrate device sensors (camera, GPS, biometrics) and push notifications.\n3. Optimize app memory footprint, battery consumption, and rendering pipeline.\n4. Publish and maintain apps across Google Play Store and Apple App Store.',
 '1. Fitness Tracker App with Geofencing and Local SQLite Storage\n2. Peer-to-Peer Marketplace with In-App Payments & Chat\n3. Personal Finance & Budget Planner with Interactive Charts'),

(7, 'CYBER_SEC', 'Cybersecurity Analyst', 'Security & Infrastructure',
 'Defends organizational digital assets, networks, and confidential databases against cyber attacks, unauthorized breaches, and security vulnerabilities.',
 'B.Tech in CSE / Cyber Security / Information Technology', 'Entry to Mid Level', '₹6 - 15 LPA ($85k - $145k)', 'Advanced', 'Critical Shortage (+32% YoY)',
 '1. Monitor network traffic and SIEM alerts for malicious intrusion patterns.\n2. Conduct vulnerability assessments, penetration tests, and code security audits.\n3. Implement encryption protocols, firewall rules, and zero-trust policies.\n4. Lead incident response drills and compile post-mortem security reports.',
 '1. Automated Vulnerability Scanner & Port Audit Tool in Python\n2. Network Packet Analyzer & Intrusion Detection System (IDS)\n3. Web Application Security Scanner (OWASP Top 10)'),

(8, 'CLOUD_ENG', 'Cloud Engineer', 'Cloud & Systems',
 'Plans, builds, and manages enterprise cloud infrastructure across AWS, Microsoft Azure, and GCP, optimizing resilience, elasticity, and cost.',
 'B.Tech in Computer Science / IT / Cloud Technology', 'Entry to Mid Level', '₹6.5 - 17 LPA ($90k - $155k)', 'Intermediate to Advanced', 'Rapid Growth',
 '1. Provision and orchestrate cloud resources using Infrastructure as Code (Terraform).\n2. Configure Virtual Private Clouds (VPCs), subnets, security groups, and routing.\n3. Implement auto-scaling, load balancing, and high availability architectures.\n4. Monitor cloud billing, security compliance, and disaster recovery replication.',
 '1. Multi-Tier High-Availability Web Architecture on AWS/Azure\n2. Serverless Event-Driven Data Processing Pipeline\n3. Cloud Cost Monitoring and Resource Cleanup Automation Tool'),

(9, 'DEVOPS_ENG', 'DevOps Engineer', 'Cloud & Systems',
 'Bridges the gap between software development and IT operations by automating CI/CD pipelines, container orchestration, and continuous observability.',
 'B.Tech in Computer Science / IT / Systems Engineering', 'Entry to Mid Level', '₹7 - 18 LPA ($95k - $160k)', 'Advanced', 'Extremely High Demand',
 '1. Build automated continuous integration and continuous deployment (CI/CD) pipelines.\n2. Containerize microservices with Docker and orchestrate with Kubernetes.\n3. Implement centralized logging and metrics monitoring (Prometheus, Grafana).\n4. Champion Site Reliability Engineering (SRE) practices and uptime SLA targets.',
 '1. Automated GitOps CI/CD Pipeline with Docker & GitHub Actions\n2. Kubernetes Cluster Deployment with Autoscaling & Ingress\n3. System Observability Stack with Prometheus, Grafana, and Alertmanager'),

(10, 'UIUX_DES', 'UI/UX Designer', 'Design & Product',
 'Crafts intuitive, visually engaging, and user-centric digital experiences by conducting UX research, creating wireframes, and building polished interactive prototypes.',
 'B.Des / B.Tech / BCA / Human-Computer Interaction', 'Entry Level', '₹4.5 - 12 LPA ($65k - $115k)', 'Moderate', 'Steady High Demand',
 '1. Conduct user interviews, create personas, and map out user journey flows.\n2. Design low-fidelity wireframes and interactive high-fidelity Figma prototypes.\n3. Establish and govern scalable component design systems and style guides.\n4. Perform usability testing and iterate designs based on quantitative telemetry.',
 '1. Complete Fintech Mobile App Design System & Prototype in Figma\n2. SaaS Workflow Redesign with User Journey & Accessibility Audit\n3. Design System UI Kit with Dark/Light Tokens and Micro-Interactions'),

(11, 'DB_ADMIN', 'Database Administrator', 'Data Infrastructure',
 'Oversees the integrity, performance, backup, and security of mission-critical relational and NoSQL database management systems.',
 'B.Tech in Computer Science / IT / Information Systems', 'Entry to Mid Level', '₹5.5 - 13 LPA ($75k - $125k)', 'Intermediate', 'Consistent Demand',
 '1. Monitor query execution plans, indexes, and cache hit ratios for performance.\n2. Implement robust automated database backup and disaster recovery procedures.\n3. Configure database replication, clustering, and high-availability failover.\n4. Manage user permissions, encryption-at-rest, and data masking compliance.',
 '1. High-Performance MySQL Replication & Failover Cluster Setup\n2. Automated Database Health Check & Slow-Query Alerting Tool\n3. Database Migration & Schema Versioning Tool with Rollback Support'),

(12, 'AI_RES', 'AI Researcher', 'AI & Research',
 'Pushes the boundaries of artificial intelligence through empirical experimentation, novel neural architectures, and scientific publication in top-tier conferences.',
 'M.Tech / B.Tech (Honors) / Ph.D. in CSE, AI, Applied Math', 'Entry to Advanced', '₹9 - 25 LPA ($110k - $200k)', 'Very Advanced', 'High Prestige & Growth',
 '1. Formulate novel mathematical theories and machine learning algorithms.\n2. Implement cutting-edge research papers in PyTorch from scratch.\n3. Benchmark models on standard academic datasets (ImageNet, GLUE, HumanEval).\n4. Author peer-reviewed scientific papers for CVPR, NeurIPS, ICML, or ICLR.',
 '1. Novel Self-Attention Mechanism Benchmark for Long Sequences\n2. Continual Learning Framework Preventing Catastrophic Forgetting\n3. Robustness Evaluation of Vision Transformers under Adversarial Noise');

-- 5. Career Skills Matrix (Required Levels 0-10 & Importance)
-- Career 1: AI/ML Engineer
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(1, 1, 8, 'critical'), -- Python
(1, 8, 8, 'critical'), -- Machine Learning
(1, 9, 7, 'critical'), -- Deep Learning
(1, 10, 8, 'high'),     -- Data Analysis
(1, 6, 7, 'high'),     -- SQL
(1, 14, 6, 'medium'),  -- Database
(1, 11, 6, 'medium'),  -- Cloud
(1, 15, 7, 'high'),    -- Git/GitHub
(1, 19, 8, 'critical'),-- Problem Solving
(1, 20, 8, 'critical'),-- Analytical Thinking
(1, 18, 7, 'medium'),  -- Teamwork
(1, 16, 6, 'medium');  -- Communication

-- Career 2: Data Scientist
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(2, 1, 8, 'critical'), -- Python
(2, 8, 8, 'critical'), -- Machine Learning
(2, 10, 9, 'critical'),-- Data Analysis
(2, 6, 8, 'critical'), -- SQL
(2, 9, 6, 'medium'),   -- Deep Learning
(2, 14, 7, 'high'),    -- Database
(2, 15, 6, 'medium'),  -- Git/GitHub
(2, 19, 8, 'high'),    -- Problem Solving
(2, 20, 9, 'critical'),-- Analytical Thinking
(2, 16, 8, 'high'),    -- Communication
(2, 22, 7, 'high');    -- Presentation

-- Career 3: Data Analyst
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(3, 1, 6, 'medium'),   -- Python
(3, 6, 9, 'critical'), -- SQL
(3, 10, 9, 'critical'),-- Data Analysis
(3, 14, 7, 'high'),    -- Database
(3, 8, 5, 'medium'),   -- Machine Learning
(3, 16, 8, 'critical'),-- Communication
(3, 20, 8, 'critical'),-- Analytical Thinking
(3, 22, 8, 'high'),    -- Presentation
(3, 19, 7, 'high');    -- Problem Solving

-- Career 4: Software Engineer
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(4, 1, 7, 'high'),     -- Python
(4, 2, 8, 'critical'), -- Java
(4, 4, 7, 'high'),     -- C++
(4, 6, 7, 'high'),     -- SQL
(4, 14, 7, 'high'),    -- Database
(4, 13, 6, 'medium'),  -- Networking
(4, 15, 8, 'critical'),-- Git/GitHub
(4, 19, 9, 'critical'),-- Problem Solving
(4, 18, 8, 'high'),    -- Teamwork
(4, 20, 7, 'high');    -- Analytical Thinking

-- Career 5: Web Developer
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(5, 5, 9, 'critical'), -- JavaScript
(5, 7, 9, 'critical'), -- HTML/CSS
(5, 1, 6, 'medium'),   -- Python
(5, 6, 6, 'medium'),   -- SQL
(5, 14, 6, 'medium'),  -- Database
(5, 15, 7, 'high'),    -- Git/GitHub
(5, 13, 6, 'medium'),  -- Networking
(5, 21, 7, 'high'),    -- Creativity
(5, 19, 7, 'high'),    -- Problem Solving
(5, 18, 7, 'medium');  -- Teamwork

-- Career 6: Mobile Developer
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(6, 2, 8, 'critical'), -- Java
(6, 5, 7, 'high'),     -- JavaScript
(6, 14, 6, 'medium'),  -- Database
(6, 15, 7, 'high'),    -- Git/GitHub
(6, 13, 6, 'medium'),  -- Networking
(6, 21, 7, 'high'),    -- Creativity
(6, 19, 8, 'critical'),-- Problem Solving
(6, 18, 7, 'medium');  -- Teamwork

-- Career 7: Cybersecurity Analyst
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(7, 12, 9, 'critical'),-- Cybersecurity
(7, 13, 9, 'critical'),-- Networking
(7, 1, 7, 'high'),     -- Python
(7, 3, 6, 'medium'),   -- C
(7, 15, 6, 'medium'),  -- Git/GitHub
(7, 19, 9, 'critical'),-- Problem Solving
(7, 20, 9, 'critical'),-- Analytical Thinking
(7, 16, 7, 'medium');  -- Communication

-- Career 8: Cloud Engineer
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(8, 11, 9, 'critical'),-- Cloud
(8, 13, 8, 'critical'),-- Networking
(8, 12, 7, 'high'),    -- Cybersecurity
(8, 1, 6, 'medium'),   -- Python
(8, 15, 7, 'high'),    -- Git/GitHub
(8, 14, 6, 'medium'),  -- Database
(8, 19, 8, 'critical'),-- Problem Solving
(8, 18, 7, 'medium');  -- Teamwork

-- Career 9: DevOps Engineer
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(9, 11, 8, 'critical'),-- Cloud
(9, 15, 9, 'critical'),-- Git/GitHub
(9, 1, 7, 'high'),     -- Python
(9, 13, 8, 'critical'),-- Networking
(9, 12, 7, 'high'),    -- Cybersecurity
(9, 14, 6, 'medium'),  -- Database
(9, 19, 8, 'critical'),-- Problem Solving
(9, 18, 8, 'high'),    -- Teamwork
(9, 23, 8, 'high');    -- Time Management

-- Career 10: UI/UX Designer
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(10, 7, 7, 'high'),    -- HTML/CSS
(10, 5, 5, 'medium'),  -- JavaScript
(10, 21, 9, 'critical'),-- Creativity
(10, 16, 8, 'critical'),-- Communication
(10, 22, 8, 'high'),   -- Presentation
(10, 18, 8, 'high'),   -- Teamwork
(10, 20, 7, 'medium'); -- Analytical Thinking

-- Career 11: Database Administrator
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(11, 6, 9, 'critical'),-- SQL
(11, 14, 9, 'critical'),-- Database
(11, 1, 6, 'medium'),  -- Python
(11, 11, 7, 'high'),   -- Cloud
(11, 12, 7, 'high'),   -- Cybersecurity
(11, 19, 8, 'critical'),-- Problem Solving
(11, 20, 8, 'high');   -- Analytical Thinking

-- Career 12: AI Researcher
INSERT OR IGNORE INTO career_skills (career_id, skill_id, required_level, importance) VALUES
(12, 1, 9, 'critical'),-- Python
(12, 8, 9, 'critical'),-- Machine Learning
(12, 9, 9, 'critical'),-- Deep Learning
(12, 10, 8, 'high'),   -- Data Analysis
(12, 4, 7, 'medium'),  -- C++
(12, 19, 9, 'critical'),-- Problem Solving
(12, 20, 9, 'critical'),-- Analytical Thinking
(12, 16, 8, 'high'),   -- Communication
(12, 22, 7, 'medium'); -- Presentation
