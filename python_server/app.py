"""
Python Flask Server for Search Engine
A simple search engine with SQLite database and inverted index
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import sqlite3
import os
import time

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'frontend'), static_url_path='')
CORS(app)

# Configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'search_index.db')


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database with sample data if not exists"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            url TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inverted_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            document_id INTEGER NOT NULL,
            frequency INTEGER DEFAULT 1,
            positions TEXT,
            FOREIGN KEY (document_id) REFERENCES documents(id),
            UNIQUE(word, document_id)
        )
    ''')
    
    # Create indexes for faster searching
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_word ON inverted_index(word)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_document ON inverted_index(document_id)')
    
    # Check if we have sample data
    cursor.execute('SELECT COUNT(*) FROM documents')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert sample data
        sample_documents = [
            {
                "title": "Introduction to Python Programming",
                "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python was created by Guido van Rossum and first released in 1991. It has become one of the most popular programming languages in the world, used for web development, data science, artificial intelligence, and more.",
                "url": "https://example.com/python-intro",
                "category": "Programming"
            },
            {
                "title": "Getting Started with C++ Development",
                "content": "C++ is a powerful, high-performance programming language that extends C with object-oriented features. It is widely used in system programming, game development, embedded systems, and high-performance applications. C++ provides low-level memory manipulation while supporting high-level abstractions like classes and templates. Modern C++ (C++11 and later) includes many features like smart pointers, lambda expressions, and move semantics.",
                "url": "https://example.com/cpp-tutorial",
                "category": "Programming"
            },
            {
                "title": "Web Development with HTML, CSS, and JavaScript",
                "content": "Web development involves creating websites and web applications using HTML for structure, CSS for styling, and JavaScript for interactivity. HTML (HyperText Markup Language) defines the content and structure of web pages. CSS (Cascading Style Sheets) controls the visual presentation. JavaScript adds dynamic behavior and enables modern interactive web experiences. Together, these technologies form the foundation of front-end web development.",
                "url": "https://example.com/web-dev-basics",
                "category": "Web Development"
            },
            {
                "title": "Database Design and SQL Fundamentals",
                "content": "Databases are organized collections of structured data. SQL (Structured Query Language) is the standard language for managing relational databases. Key concepts include tables, rows, columns, primary keys, foreign keys, and indexes. Common operations include SELECT for querying data, INSERT for adding records, UPDATE for modifying data, and DELETE for removing records. Database normalization helps organize data efficiently and reduce redundancy.",
                "url": "https://example.com/sql-basics",
                "category": "Database"
            },
            {
                "title": "Machine Learning and Artificial Intelligence",
                "content": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. Key concepts include supervised learning, unsupervised learning, and reinforcement learning. Popular algorithms include linear regression, decision trees, neural networks, and deep learning. Python libraries like TensorFlow, PyTorch, and scikit-learn are commonly used for machine learning development.",
                "url": "https://example.com/ml-intro",
                "category": "AI/ML"
            },
            {
                "title": "RESTful API Design Best Practices",
                "content": "REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs use HTTP methods like GET, POST, PUT, and DELETE to perform operations on resources. Best practices include using meaningful URLs, proper HTTP status codes, versioning, authentication, and documentation. JSON is the most common data format for REST APIs. Good API design improves developer experience and system maintainability.",
                "url": "https://example.com/rest-api-guide",
                "category": "Web Development"
            },
            {
                "title": "Cloud Computing with AWS, Azure, and Google Cloud",
                "content": "Cloud computing provides on-demand access to computing resources over the internet. Major providers include Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP). Services include compute (EC2, Virtual Machines), storage (S3, Blob Storage), databases (RDS, Cloud SQL), and serverless computing (Lambda, Cloud Functions). Cloud computing enables scalability, cost efficiency, and global reach for applications.",
                "url": "https://example.com/cloud-computing",
                "category": "Cloud"
            },
            {
                "title": "Version Control with Git and GitHub",
                "content": "Git is a distributed version control system that tracks changes in source code during software development. Key concepts include repositories, commits, branches, merging, and pull requests. GitHub is a popular platform for hosting Git repositories and collaborating on projects. Commands like git clone, git add, git commit, git push, and git pull are essential for daily workflows. Branching strategies like GitFlow help manage releases.",
                "url": "https://example.com/git-guide",
                "category": "DevOps"
            },
            {
                "title": "Docker and Container Technologies",
                "content": "Docker is a platform for developing, shipping, and running applications in containers. Containers are lightweight, standalone packages that include everything needed to run software. Docker images define container configurations, while Docker Compose manages multi-container applications. Kubernetes orchestrates containers at scale. Containerization improves consistency across development, testing, and production environments.",
                "url": "https://example.com/docker-basics",
                "category": "DevOps"
            },
            {
                "title": "Cybersecurity Fundamentals and Best Practices",
                "content": "Cybersecurity protects computer systems, networks, and data from digital attacks. Key areas include network security, application security, information security, and operational security. Common threats include malware, phishing, ransomware, and social engineering. Best practices include using strong passwords, enabling two-factor authentication, keeping software updated, and regular security audits. Understanding encryption and secure coding practices is essential.",
                "url": "https://example.com/cybersecurity",
                "category": "Security"
            },
            {
                "title": "Mobile App Development for iOS and Android",
                "content": "Mobile app development creates applications for smartphones and tablets. Native development uses Swift for iOS and Kotlin/Java for Android. Cross-platform frameworks like React Native, Flutter, and Xamarin enable building apps for multiple platforms from a single codebase. Key considerations include responsive design, performance optimization, offline functionality, and app store guidelines. Mobile development requires understanding touch interfaces and mobile-specific patterns.",
                "url": "https://example.com/mobile-dev",
                "category": "Mobile"
            },
            {
                "title": "Data Structures and Algorithms",
                "content": "Data structures organize and store data efficiently for access and modification. Common structures include arrays, linked lists, stacks, queues, trees, graphs, and hash tables. Algorithms are step-by-step procedures for solving problems. Key algorithm categories include sorting, searching, graph traversal, and dynamic programming. Understanding Big O notation helps analyze algorithm efficiency. These concepts are fundamental to computer science and software engineering.",
                "url": "https://example.com/dsa-guide",
                "category": "Computer Science"
            },
            {
                "title": "Agile Software Development Methodology",
                "content": "Agile is an iterative approach to software development that emphasizes flexibility, collaboration, and customer feedback. Key frameworks include Scrum, Kanban, and XP (Extreme Programming). Scrum uses sprints, daily standups, and retrospectives. Agile values working software over comprehensive documentation and responding to change over following a fixed plan. User stories, backlogs, and continuous integration are common agile practices.",
                "url": "https://example.com/agile-methodology",
                "category": "Project Management"
            },
            {
                "title": "Search Engine Optimization (SEO) Techniques",
                "content": "SEO improves website visibility in search engine results. Key factors include keyword optimization, quality content, page speed, mobile-friendliness, and backlinks. On-page SEO involves optimizing individual pages with proper titles, meta descriptions, and header tags. Off-page SEO builds authority through external links and social signals. Technical SEO ensures search engines can crawl and index content effectively. Analytics tools track rankings and traffic.",
                "url": "https://example.com/seo-guide",
                "category": "Marketing"
            },
            {
                "title": "Introduction to Blockchain Technology",
                "content": "Blockchain is a distributed ledger technology that records transactions across multiple computers securely. Each block contains a cryptographic hash of the previous block, creating an immutable chain. Blockchain powers cryptocurrencies like Bitcoin and Ethereum, but has applications in supply chain, healthcare, voting, and more. Smart contracts enable automated, trustless transactions. Consensus mechanisms like Proof of Work and Proof of Stake validate transactions.",
                "url": "https://example.com/blockchain-intro",
                "category": "Technology"
            },
            {
                "title": "Natural Language Processing and Text Analysis",
                "content": "Natural Language Processing (NLP) enables computers to understand and process human language. Applications include sentiment analysis, machine translation, chatbots, and text summarization. Key techniques include tokenization, stemming, lemmatization, and named entity recognition. Deep learning models like transformers (BERT, GPT) have revolutionized NLP. Python libraries like NLTK, spaCy, and Hugging Face provide NLP tools and pre-trained models.",
                "url": "https://example.com/nlp-basics",
                "category": "AI/ML"
            },
            {
                "title": "Software Testing and Quality Assurance",
                "content": "Software testing ensures applications work correctly and meet requirements. Types include unit testing, integration testing, system testing, and acceptance testing. Test-driven development (TDD) writes tests before code. Automated testing frameworks like JUnit, pytest, and Selenium reduce manual effort. Quality assurance encompasses the entire development process to prevent defects. Code reviews, static analysis, and continuous testing improve software quality.",
                "url": "https://example.com/software-testing",
                "category": "Quality Assurance"
            },
            {
                "title": "Linux System Administration Guide",
                "content": "Linux is an open-source operating system widely used for servers, embedded systems, and development. Key concepts include the file system hierarchy, permissions, processes, and services. Essential commands include ls, cd, grep, chmod, sudo, and systemctl. Package managers like apt and yum install software. Shell scripting automates tasks. Understanding networking, security, and performance monitoring is crucial for system administration.",
                "url": "https://example.com/linux-admin",
                "category": "System Administration"
            },
            {
                "title": "Microservices Architecture Design",
                "content": "Microservices architecture structures applications as a collection of loosely coupled services. Each service is independently deployable, scalable, and maintainable. Benefits include flexibility, resilience, and team autonomy. Challenges include distributed system complexity, data consistency, and service communication. API gateways, service discovery, and container orchestration support microservices. Event-driven architecture and message queues enable asynchronous communication between services.",
                "url": "https://example.com/microservices",
                "category": "Architecture"
            },
            {
                "title": "Big Data Analytics and Processing",
                "content": "Big data refers to extremely large datasets that require specialized tools for processing and analysis. The three Vs define big data: Volume, Velocity, and Variety. Technologies include Hadoop for distributed storage, Spark for processing, and Kafka for streaming. Data warehouses and data lakes store structured and unstructured data. Business intelligence tools visualize insights. Big data enables predictive analytics, real-time processing, and data-driven decision making.",
                "url": "https://example.com/big-data",
                "category": "Data Engineering"
            }
        ]
        
        for doc in sample_documents:
            cursor.execute('''
                INSERT INTO documents (title, content, url, category)
                VALUES (?, ?, ?, ?)
            ''', (doc['title'], doc['content'], doc['url'], doc['category']))
            
            doc_id = cursor.lastrowid
            
            # Build inverted index
            words = tokenize(doc['title'] + ' ' + doc['content'])
            word_freq = {}
            for pos, word in enumerate(words):
                if word not in word_freq:
                    word_freq[word] = {'count': 0, 'positions': []}
                word_freq[word]['count'] += 1
                word_freq[word]['positions'].append(pos)
            
            for word, data in word_freq.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO inverted_index (word, document_id, frequency, positions)
                    VALUES (?, ?, ?, ?)
                ''', (word, doc_id, data['count'], json.dumps(data['positions'])))
        
        conn.commit()
        print(f"Initialized database with {len(sample_documents)} sample documents")
    
    conn.close()


def tokenize(text):
    """Simple tokenizer - splits text into lowercase words"""
    import re
    # Remove special characters and split
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                  'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                  'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
                  'those', 'it', 'its', 'as', 'if', 'then', 'than', 'so', 'such'}
    return [w for w in words if w not in stop_words and len(w) > 1]


def search_database(query, page=1, limit=10):
    """Search the database using the inverted index"""
    start_time = time.time()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tokenize query
    query_words = tokenize(query)
    
    if not query_words:
        return {'results': [], 'total': 0, 'search_time': 0}
    
    # Search using inverted index
    placeholders = ','.join('?' * len(query_words))
    
    # Get document IDs and calculate relevance score
    cursor.execute(f'''
        SELECT document_id, 
               SUM(frequency) as total_freq,
               COUNT(DISTINCT word) as matched_words
        FROM inverted_index 
        WHERE word IN ({placeholders})
        GROUP BY document_id
        ORDER BY matched_words DESC, total_freq DESC
    ''', query_words)
    
    doc_scores = cursor.fetchall()
    total_results = len(doc_scores)
    
    # Paginate
    offset = (page - 1) * limit
    paginated_docs = doc_scores[offset:offset + limit]
    
    results = []
    for doc_score in paginated_docs:
        doc_id = doc_score['document_id']
        
        cursor.execute('''
            SELECT id, title, content, url, category
            FROM documents WHERE id = ?
        ''', (doc_id,))
        
        doc = cursor.fetchone()
        if doc:
            # Create snippet
            content = doc['content']
            snippet = create_snippet(content, query_words)
            
            results.append({
                'id': doc['id'],
                'title': doc['title'],
                'snippet': snippet,
                'url': doc['url'],
                'category': doc['category'],
                'score': doc_score['matched_words'] * 10 + doc_score['total_freq']
            })
    
    conn.close()
    
    search_time = time.time() - start_time
    
    return {
        'results': results,
        'total': total_results,
        'search_time': search_time,
        'page': page,
        'limit': limit
    }


def create_snippet(content, query_words, max_length=200):
    """Create a snippet highlighting query terms"""
    content_lower = content.lower()
    
    # Find the first occurrence of any query word
    best_pos = len(content)
    for word in query_words:
        pos = content_lower.find(word)
        if pos != -1 and pos < best_pos:
            best_pos = pos
    
    # Create snippet around the found position
    start = max(0, best_pos - 50)
    end = min(len(content), start + max_length)
    
    snippet = content[start:end]
    
    # Add ellipsis if needed
    if start > 0:
        snippet = '...' + snippet
    if end < len(content):
        snippet = snippet + '...'
    
    return snippet


# Search function wrapper
def perform_search(query, page=1, limit=10):
    """Perform search using the Python implementation"""
    return search_database(query, page, limit)


# Routes
@app.route('/')
def index():
    """Serve the main search page"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/script.js')
def serve_script():
    """Serve JavaScript file"""
    return send_from_directory(app.static_folder, 'script.js')


@app.route('/style.css')
def serve_style():
    """Serve CSS file"""
    return send_from_directory(app.static_folder, 'style.css')


@app.route('/api/search', methods=['POST'])
def search():
    """Handle search requests"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'Query is required'}), 400
    
    query = data.get('query', '').strip()
    page = data.get('page', 1)
    limit = data.get('limit', 10)
    
    if not query:
        return jsonify({'error': 'Query cannot be empty'}), 400
    
    # Perform search using Python implementation
    results = perform_search(query, page, limit)
    
    return jsonify(results)


@app.route('/api/index', methods=['POST'])
def add_document():
    """Add a new document to the index"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO documents (title, content, url, category)
            VALUES (?, ?, ?, ?)
        ''', (
            data['title'],
            data['content'],
            data.get('url', ''),
            data.get('category', 'General')
        ))
        
        doc_id = cursor.lastrowid
        
        # Build inverted index
        words = tokenize(data['title'] + ' ' + data['content'])
        word_freq = {}
        for pos, word in enumerate(words):
            if word not in word_freq:
                word_freq[word] = {'count': 0, 'positions': []}
            word_freq[word]['count'] += 1
            word_freq[word]['positions'].append(pos)
        
        for word, freq_data in word_freq.items():
            cursor.execute('''
                INSERT OR REPLACE INTO inverted_index (word, document_id, frequency, positions)
                VALUES (?, ?, ?, ?)
            ''', (word, doc_id, freq_data['count'], json.dumps(freq_data['positions'])))
        
        conn.commit()
        
        return jsonify({
            'message': 'Document added successfully',
            'id': doc_id
        })
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        conn.close()


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get index statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM documents')
    doc_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT word) FROM inverted_index')
    word_count = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'documents': doc_count,
        'unique_words': word_count
    })


# Initialize database on module load (for Render/Gunicorn)
print("Initializing database...")
init_database()
print("Database initialized.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Search Engine Server on port {port}...")
    print(f"Open http://localhost:{port} in your browser")
    app.run(host='0.0.0.0', port=port, debug=False)
