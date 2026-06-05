from difflib import SequenceMatcher

SYNONYMS = {
    'programmer': ['developer', 'coder', 'software engineer', 'engineer', 'software developer'],
    'developer': ['programmer', 'coder', 'software engineer', 'engineer', 'software developer'],
    'coder': ['programmer', 'developer', 'software engineer', 'engineer'],
    'engineer': ['developer', 'programmer', 'software engineer', 'software developer'],
    'software engineer': ['programmer', 'developer', 'coder', 'software developer'],
    'software developer': ['programmer', 'developer', 'coder', 'software engineer'],
    'analyst': ['data analyst', 'business analyst', 'researcher', 'reporting analyst'],
    'data analyst': ['analyst', 'business analyst', 'data scientist', 'reporting'],
    'business analyst': ['analyst', 'data analyst', 'consultant', 'researcher'],
    'data scientist': ['data analyst', 'machine learning', 'ml engineer', 'ai engineer'],
    'designer': ['ui designer', 'ux designer', 'graphic designer', 'creative', 'visual designer'],
    'ui designer': ['designer', 'ux designer', 'graphic designer', 'frontend'],
    'ux designer': ['designer', 'ui designer', 'product designer', 'user experience'],
    'graphic designer': ['designer', 'visual designer', 'creative', 'illustrator'],
    'manager': ['lead', 'head', 'director', 'supervisor', 'team lead'],
    'lead': ['manager', 'head', 'director', 'senior', 'team lead'],
    'director': ['manager', 'head', 'lead', 'executive'],
    'supervisor': ['manager', 'lead', 'team lead', 'coordinator'],
    'marketing': ['digital marketing', 'advertising', 'brand', 'communications', 'promotions'],
    'digital marketing': ['marketing', 'social media', 'seo', 'content marketing'],
    'sales': ['business development', 'account manager', 'client relations', 'revenue'],
    'business development': ['sales', 'account manager', 'partnerships', 'growth'],
    'account manager': ['sales', 'client relations', 'business development', 'customer success'],
    'finance': ['accounting', 'accountant', 'financial', 'treasury', 'budgeting'],
    'accountant': ['finance', 'accounting', 'financial analyst', 'bookkeeper'],
    'financial analyst': ['accountant', 'finance', 'analyst', 'investment analyst'],
    'bookkeeper': ['accountant', 'accounting', 'finance'],
    'hr': ['human resources', 'recruitment', 'talent acquisition', 'people', 'people operations'],
    'human resources': ['hr', 'recruitment', 'talent acquisition', 'people operations'],
    'recruiter': ['hr', 'human resources', 'talent acquisition', 'headhunter'],
    'talent acquisition': ['recruiter', 'hr', 'human resources', 'recruitment'],
    'data': ['analytics', 'database', 'sql', 'reporting', 'bi'],
    'database': ['sql', 'data', 'dba', 'database administrator'],
    'frontend': ['ui', 'react', 'javascript', 'web developer', 'ui developer'],
    'backend': ['server', 'api', 'django', 'python', 'java', 'node'],
    'fullstack': ['full stack', 'frontend', 'backend', 'web developer'],
    'full stack': ['fullstack', 'frontend', 'backend', 'web developer'],
    'devops': ['infrastructure', 'cloud', 'deployment', 'sysadmin', 'site reliability'],
    'cloud': ['devops', 'aws', 'azure', 'infrastructure', 'deployment'],
    'admin': ['administrator', 'administration', 'support', 'coordinator', 'office manager'],
    'administrator': ['admin', 'administration', 'support', 'coordinator'],
    'coordinator': ['admin', 'administrator', 'assistant', 'officer', 'executive assistant'],
    'support': ['helpdesk', 'customer service', 'admin', 'assistant', 'customer support'],
    'customer service': ['support', 'helpdesk', 'customer success', 'client relations'],
    'consultant': ['advisor', 'specialist', 'analyst', 'contractor'],
    'specialist': ['consultant', 'expert', 'analyst', 'advisor'],
    'project manager': ['pm', 'program manager', 'delivery manager', 'scrum master'],
    'scrum master': ['project manager', 'agile coach', 'delivery manager'],
    'product manager': ['pm', 'product owner', 'project manager'],
    'product owner': ['product manager', 'pm', 'business analyst'],
    'qa': ['quality assurance', 'tester', 'quality engineer', 'test engineer'],
    'tester': ['qa', 'quality assurance', 'test engineer', 'quality engineer'],
    'security': ['cybersecurity', 'information security', 'infosec', 'network security'],
    'cybersecurity': ['security', 'information security', 'infosec', 'penetration testing'],
    'network': ['networking', 'network engineer', 'infrastructure', 'systems'],
    'systems': ['network', 'infrastructure', 'sysadmin', 'it'],
    'it': ['information technology', 'systems', 'tech support', 'helpdesk'],
    'machine learning': ['ml', 'ai', 'data science', 'deep learning', 'artificial intelligence'],
    'artificial intelligence': ['ai', 'machine learning', 'ml', 'deep learning'],
    'content': ['copywriter', 'content writer', 'editor', 'writer', 'journalist'],
    'writer': ['content', 'copywriter', 'editor', 'journalist', 'communications'],
    'copywriter': ['writer', 'content', 'creative writer', 'marketing'],
    'legal': ['lawyer', 'solicitor', 'paralegal', 'compliance', 'counsel'],
    'lawyer': ['legal', 'solicitor', 'counsel', 'attorney'],
    'operations': ['ops', 'operations manager', 'business operations', 'logistics'],
    'logistics': ['supply chain', 'operations', 'warehouse', 'distribution'],
}


def expand_query(query):
    words = query.lower().split()
    expanded = set(words)
    for word in words:
        if word in SYNONYMS:
            for s in SYNONYMS[word]:
                expanded.add(s)
    full_query = query.lower()
    if full_query in SYNONYMS:
        for s in SYNONYMS[full_query]:
            expanded.add(s)
    return list(expanded)


def fuzzy_check(query, text):
    terms = expand_query(query)
    for term in terms:
        for q_word in term.split():
            if q_word in text.lower():
                return True
            for t_word in text.lower().split():
                if SequenceMatcher(None, q_word, t_word).ratio() >= 0.7:
                    return True
    return False
