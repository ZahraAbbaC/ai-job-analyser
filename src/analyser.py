import re

def analyse_job(description: str) -> dict:
    description_lower = description.lower()
    word_count = len(description.split())
    skills = ['python', 'sql', 'docker', 'fastapi']
    skills_mentioned = {}
    for skill in skills: 
        skills_mentioned[f'mention_of_{skill}'] = bool(re.search(r'\b' + skill + r'\b', description_lower))
    result = {
        'word_count': word_count,
        **skills_mentioned
    }
    return result
