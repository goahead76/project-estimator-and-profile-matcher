# =====================================================================
# app/services/matcher.py - Developer Requirement Profile Matcher Engine
# =====================================================================

import io
import re
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def clean_skill_string_to_set(skill_entry):
    """
    Parses and sanitizes various Kaggle CSV string formatting variants 
    (e.g. '["Python", "SQL"]', 'Java; C++', or 'React, Node') into a clean clean text set.
    """
    if pd.isna(skill_entry):
        return set()
    raw_str = str(skill_entry).lower()
    # Strip brackets, quotes, and standard array artifacts from text fields
    cleaned = re.sub(r'[\[\]\'\"“”]', '', raw_str)
    # Split by common delimiters: commas, semicolons, or pipes
    tokens = re.split(r'[,;|]', cleaned)
    return {token.strip() for token in tokens if token.strip()}

# =====================================================================
# VISUALIZATION GRAPH COMPILERS (5-CHANNELS MAPS)
# =====================================================================

def plot_top_matches(df_top):
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    bars = ax.barh(df_top['Developer_Name'], df_top['Match_Score_Pct'], color='#2563eb', height=0.5, zorder=2)
    ax.set_xlabel('Skill Match Percentage (%)', fontweight='bold', fontsize=9, color='#374151')
    ax.grid(True, axis='x', linestyle='--', alpha=0.3, zorder=1)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f' {width:.1f}%', xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(3, 0), textcoords="offset points", ha='left', va='center', fontsize=8, fontweight='bold', color='#1e3a8a')
        
    plt.title('1. Top Developer Fit Requirements Match', fontsize=10, fontweight='bold', pad=10, color='#1f2937')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

def plot_skill_scarcity(missing_keyword_counts):
    labels = [k.upper() for k, _ in missing_keyword_counts[:6]]
    values = [v for _, v in missing_keyword_counts[:6]]
    if not labels: labels, values = ["NONE"], [0]

    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    bars = ax.bar(labels, values, color='#f59e0b', width=0.4, zorder=2)
    ax.set_ylabel('Missing Count in Pool', fontweight='bold', fontsize=9, color='#374151')
    ax.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=1)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#b45309')

    plt.title('2. Project Resource Deficit & Skill Scarcity', fontsize=10, fontweight='bold', pad=10, color='#1f2937')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

def plot_budget_vs_fit(df_pool):
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    scatter = ax.scatter(df_pool['Hourly_Rate'], df_pool['Match_Score_Pct'], 
                         c=df_pool['Experience_Years'], cmap='viridis', s=60, alpha=0.8, edgecolors='none', zorder=2)
    ax.set_xlabel('Hourly Rate ($/hr)', fontweight='bold', fontsize=9, color='#374151')
    ax.set_ylabel('Match Accuracy (%)', fontweight='bold', fontsize=9, color='#374151')
    ax.grid(True, linestyle=':', alpha=0.4, zorder=1)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Experience Seniority (Years)', fontsize=8, fontweight='bold', color='#374151')
    cbar.ax.tick_params(labelsize=7)

    plt.title('3. Talent Efficiency Cost Value Matrix', fontsize=10, fontweight='bold', pad=10, color='#1f2937')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

def plot_pool_availability(df_pool):
    categories = ['Perfect Fit (>80%)', 'Strong Match (50-80%)', 'Niche Resource (<50%)']
    counts = [
        len(df_pool[df_pool['Match_Score_Pct'] >= 80]),
        len(df_pool[(df_pool['Match_Score_Pct'] >= 50) & (df_pool['Match_Score_Pct'] < 80)]),
        len(df_pool[df_pool['Match_Score_Pct'] < 50])
    ]
    if sum(counts) == 0: counts = [0, 0, 1]
        
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    colors = ['#10b981', '#3b82f6', '#9ca3af']
    
    ax.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140, colors=colors,
           textprops=dict(color="#374151", fontsize=8), wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))

    plt.title('4. Structural Resource Pool Segment Breakdown', fontsize=10, fontweight='bold', pad=10, color='#1f2937')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

def plot_experience_density(df_top):
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    ax.plot(df_top['Developer_Name'], df_top['Experience_Years'], color='#8b5cf6', marker='p', markersize=6, linewidth=1.5, zorder=2)
    ax.set_ylabel('Years of Field Experience', fontweight='bold', fontsize=9, color='#374151')
    ax.tick_params(axis='x', rotation=15, labelsize=7)
    ax.grid(True, linestyle=':', alpha=0.4, zorder=1)
    
    for x, y in zip(df_top['Developer_Name'], df_top['Experience_Years']):
        ax.annotate(f'{y} yrs', (x, y), xytext=(0, 6), textcoords="offset points", ha='center', va='bottom', fontsize=7, color='#6d28d9', fontweight='bold')

    plt.title('5. Experience Seniority Curve of Top Profiles', fontsize=10, fontweight='bold', pad=10, color='#1f2937')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

# =====================================================================
# SECTION 3: CORE MATCHER CALCULATOR INTERFACE
# =====================================================================

def match_developers_and_visualize(extracted_keywords, csv_path: str):
    """
    Ingests extracted project requirements keywords, runs comparative vector calculations
    against developer profile data frames, and compiles base64 analytics charts.
    """
    # Fallback placeholder dataset generation if target Kaggle CSV is missing locally
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        # Expected column contracts map layout to fall back on cleanly
                # Expected column contracts map layout to fall back on cleanly if the CSV is missing
        mock_data = {
            "Developer_Name": ["Alex Rivera", "Devon Chen", "Sarah Jenkins", "Michael Amadi", "Elena Rostova", "Hiroshi Tanaka"],
            "Skills": ["sql, api, cloud, integration", "web development, database, ui/ux", "data science, analytics, sql, python", "cloud, database, security", "ui/ux, design, front-end", "integration, api, backend, web development"],
            "Hourly_Rate": [45.0, 60.0, 55.0, 70.0, 40.0, 65.0],
            "Experience_Years": [3, 5, 4, 7, 2, 6]
        }
        df = pd.DataFrame(mock_data)


    project_requirements_set = {str(kw).lower().strip() for kw in extracted_keywords if str(kw).strip()}
    
    if not project_requirements_set:
        # Avoid zero breaks by running default evaluations across the base set
        project_requirements_set = {"sql", "api", "database", "analytics"}

    scores = []
    missing_counter = {}

    for idx, row in df.iterrows():
        dev_skills = clean_skill_string_to_set(row.get('Skills', ''))
        
        # Calculate intersection sets between requirements and resource capability profiles
        matching_skills = project_requirements_set.intersection(dev_skills)
        missing_skills = project_requirements_set.difference(dev_skills)
        
        # Track which required skills are hardest to find in the developer pool
        for skill in missing_skills:
            missing_counter[skill] = missing_counter.get(skill, 0) + 1
            
        score_pct = (len(matching_skills) / len(project_requirements_set)) * 100 if project_requirements_set else 0
        scores.append({
            "index": idx,
            "match_pct": round(score_pct, 1),
            "matched_skills_list": list(matching_skills)
        })

    df_scores = pd.DataFrame(scores)
    df['Match_Score_Pct'] = df_scores['match_pct']
    df['Matched_Skills'] = df_scores['matched_skills_list']

    # Sort profiles by matching index efficiency
    df_sorted = df.sort_values(by=['Match_Score_Pct', 'Experience_Years'], ascending=[False, False])
    df_top_5 = df_sorted.head(5).copy()
    
    # Sort missing skills metrics
    sorted_missing = sorted(missing_counter.items(), key=lambda x: x[1], reverse=True)

    # Compile the 5-Channel base64 visualization reports
    img_top_matches = plot_top_matches(df_top_5)
    img_skill_scarcity = plot_skill_scarcity(sorted_missing)
    img_budget_fit = plot_budget_vs_fit(df)
    img_pool_availability = plot_pool_availability(df)
    img_experience_density = plot_experience_density(df_top_5)

    # Package clean JSON response data structures for the frontend layout
    best_profiles = []
    for _, row in df_top_5.iterrows():
        best_profiles.append({
            "name": row['Developer_Name'],
            "skills": row['Skills'],
            "hourly_rate": float(row['Hourly_Rate']),
            "experience_years": int(row['Experience_Years']),
            "match_score": float(row['Match_Score_Pct']),
            "matched_skills_found": row['Matched_Skills']
        })

    return {
        "top_developers": best_profiles,
        "graphs": {
            "img_top_matches": img_top_matches,
            "img_skill_scarcity": img_skill_scarcity,
            "img_budget_fit": img_budget_fit,
            "img_pool_availability": img_pool_availability,
            "img_experience_density": img_experience_density
        }
    }
