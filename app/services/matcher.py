import io
import re
import base64
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def clean_skill_string_to_set(skill_entry):
    if pd.isna(skill_entry):
        return set()
    raw_str = str(skill_entry).lower()
    # Strip brackets, quotes, and standard array artifacts from text fields
    cleaned = re.sub(r'[\[\]\'\"“”]', '', raw_str)
    # Split by common delimiters- commas, semicolons, or pipes
    tokens = re.split(r'[,;|]', cleaned)
    return {token.strip() for token in tokens if token.strip()}

# visualization on graphs (8 channel)
def plot_top_matches(df_top):
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    bars = ax.barh(df_top['Developer_Name'], df_top['Match_Score_Pct'], color='#2563eb', height=0.5, zorder=2)
    ax.set_xlabel('Skill Match Percentage (%)', fontweight='bold', fontsize=9, color='#374151')
    ax.set_xlim(0, 100)
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
    ax.set_ylim(0, 100) 
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
    ax.set_ylim(0, 100)
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
    fig, ax = plt.subplots(figsize=(6, 2.8), dpi=110)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.plot(df_top['Developer_Name'], df_top['Experience_Years'], color='#8b5cf6', marker='p', markersize=5, linewidth=1.2, zorder=2)
    ax.set_ylabel('Years of Field Experience', fontweight='bold', fontsize=8, color='#374151')
    ax.tick_params(axis='x', rotation=12, labelsize=7)
    ax.tick_params(axis='y', labelsize=8)
    ax.grid(True, linestyle=':', alpha=0.4, zorder=1)
    max_val = df_top['Experience_Years'].max() if not df_top.empty else 5
    ax.set_ylim(0, max_val * 1.2)
    for x, y in zip(df_top['Developer_Name'], df_top['Experience_Years']):
        ax.annotate(f'{y} yrs', (x, y), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=7, color='#6d28d9', fontweight='bold')
    plt.title('5. Experience Seniority Curve of Top Profiles', fontsize=9, fontweight='bold', pad=8, color='#1f2937')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

# --- ENHANCED CHART 6: COMPETENCY HEATMAP MATRIX ---
def plot_competency_heatmap(df_top, project_requirements):
    req_list = list(project_requirements)[:8]  # Limit to top 8 to prevent overlap text
    if not req_list: 
        req_list = ["No Keywords Found"]
    
    if df_top.empty:
        dev_names = ["No Candidates"]
        heatmap_matrix = np.zeros((1, len(req_list)))
    else:
        dev_names = df_top['Developer_Name'].tolist()
        heatmap_matrix = np.zeros((len(dev_names), len(req_list)))
        
        for dev_idx, (_, row) in enumerate(df_top.iterrows()):
            matched_set = set([s.lower() for s in row.get('Matched_Skills', [])])
            for req_idx, req in enumerate(req_list):
                if req.lower() in matched_set:
                    heatmap_matrix[dev_idx, req_idx] = 1

    # Increase resolution and change proportions slightly for clean text fit
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=120)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Use a premium YlGnBu (Yellow-Green-Blue) palette matching the Emerald theme
    cax = ax.matshow(heatmap_matrix, cmap='YlGnBu', vmin=0, vmax=1.3, aspect='auto')
    
    # Configure axes with modern typography styles
    ax.set_xticks(range(len(req_list)))
    ax.set_yticks(range(len(dev_names)))
    ax.set_xticklabels([r.upper() for r in req_list], fontsize=7, rotation=35, ha='left', color='#4b5563', fontweight='600')
    ax.set_yticklabels(dev_names, fontsize=7, color='#1f2937', fontweight='600')
    
    # Hide outer structural spines for a frameless look
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    # Inject crisp white gridlines to simulate independent dashboard badges
    ax.set_xticks(np.arange(-.5, len(req_list), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(dev_names), 1), minor=True)
    ax.grid(which='minor', color='#ffffff', linestyle='-', linewidth=2.5)
    ax.tick_params(which='minor', bottom=False, left=False)
    ax.tick_params(axis='x', pad=6)
    
    plt.title('6. Candidate Target Competency Matrix Map', fontsize=10, fontweight='bold', pad=32, color='#1f2937')
    fig.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"


# --- ENHANCED CHART 7: ROI VALUE LEVERAGE QUADRANTS ---
def plot_roi_quadrants(df_pool):
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=120)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    if df_pool.empty:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return f"data:image/png;base64,{base64.b64encode(b'').decode('utf-8')}"
        
    rates = df_pool['Hourly_Rate'].astype(float)
    scores = df_pool['Match_Score_Pct'].astype(float)
      
    # Dynamic axis padding bounds calculations
    x_min, x_max = rates.min() * 0.85, rates.max() * 1.15
    y_min, y_max = 0, 100
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    
    avg_rate = df_pool['Hourly_Rate'].mean() if not df_pool.empty else 50
    avg_score = df_pool['Match_Score_Pct'].mean() if not df_pool.empty else 50
    
    # RENDER BACKGROUND QUADRANT COLOR PATCHES (Soft Opacity Fills)
    ax.axvspan(x_min, avg_rate, ymin=(avg_score-y_min)/(y_max-y_min), ymax=1, color='#e6f4ea', alpha=0.6, zorder=1)
    ax.axvspan(avg_rate, x_max, ymin=(avg_score-y_min)/(y_max-y_min), ymax=1, color='#e8f0fe', alpha=0.4, zorder=1)
    
    # Add dashed boundary quadrant marker axis separators 
    ax.axvline(x=avg_rate, color='#9ca3af', linestyle='--', linewidth=1.2, alpha=0.7, zorder=2)
    ax.axhline(y=avg_score, color='#9ca3af', linestyle='--', linewidth=1.2, alpha=0.7, zorder=2)
    
    # Modern scatter dots
    ax.scatter(rates, scores, color='#1e3a8a', s=55, edgecolor='#ffffff', linewidth=1.2, alpha=0.95, zorder=4)
    
    # Fixed quadrant titles pinned securely to layout corners using relative axis boundaries
    ax.text(0.04, 0.94, '🎯 High Fit / Low Cost\n     (Optimal Target)', 
            transform=ax.transAxes, fontsize=7.5, color='#0f5132', fontweight='bold', va='top', ha='left', zorder=5)
    ax.text(0.96, 0.94, '💎 High Fit / High Cost\n     (Premium Elite)', 
            transform=ax.transAxes, fontsize=7.5, color='#084298', fontweight='bold', va='top', ha='right', zorder=5)
    
    # Labels and grid optimizations
    ax.set_xlabel('Hourly Cost ($/hr)', fontsize=8, fontweight='bold', color='#4b5563', labelpad=6)
    ax.set_ylabel('Match Fit Score (%)', fontsize=8, fontweight='bold', color='#4b5563', labelpad=6)
    ax.tick_params(labelsize=7, colors='#6b7280')
    ax.grid(True, linestyle=':', alpha=0.25, color='#cbd5e1', zorder=3)
    
    for spine in ax.spines.values():
        spine.set_color('#e5e7eb')
    
    # NATIVE MATPLOTLIB LABEL DE-CONGESTION SYSTEM
    # Checks for overlapping points and steps them systematically in opposite directions
    seen_positions = {}
    for _, row in df_pool.iterrows():
        short_name = row['Developer_Name'].split()[0] if ' ' in str(row['Developer_Name']) else str(row['Developer_Name'])
        rx, ry = round(float(row['Hourly_Rate']), 1), round(float(row['Match_Score_Pct']), 1)
        
        pos_key = (rx, ry)
        if pos_key in seen_positions:
            seen_positions[pos_key] += 1
        else:
            seen_positions[pos_key] = 0
            
        # Rotate offsets across 4 diagonal positions if data coordinates collapse on same spot
        count = seen_positions[pos_key]
        offsets = [
            (6, 4, 'left', 'bottom'),    # Top Right
            (-6, -6, 'right', 'top'),    # Bottom Left
            (6, -6, 'left', 'top'),      # Bottom Right
            (-6, 4, 'right', 'bottom')   # Top Left
        ]
        ox, oy, ha_align, va_align = offsets[count % len(offsets)]
        
        ax.annotate(short_name, (row['Hourly_Rate'], row['Match_Score_Pct']),
                    xytext=(ox, oy), textcoords="offset points", 
                    ha=ha_align, va=va_align, fontsize=6.5, weight='700', color='#374151', zorder=6)
    
    plt.title('7. Value Leverage Index (ROI Quadrants)', fontsize=10, fontweight='bold', pad=10, color='#1f2937')
    fig.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

# --- NEW CHART 8: TALENT VERSATILITY METRICS ---
def plot_talent_versatility(df_top):
    fig, ax = plt.subplots(figsize=(12, 3.2), dpi=110)  # Wider layout span for the full-width slot
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    if df_top.empty:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return f"data:image/png;base64,{base64.b64encode(b'').decode('utf-8')}"
        
    dev_names = df_top['Developer_Name'].tolist()
    total_skills_count = [len(clean_skill_string_to_set(row.get('Skills', ''))) for _, row in df_top.iterrows()]

    bars = ax.bar(dev_names, total_skills_count, color='#0d9488', width=0.35, zorder=2)
    ax.set_ylabel('Total Known Skills Inventory', fontweight='bold', fontsize=8, color='#374151')
    ax.set_ylim(0, 25)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=1)
    ax.tick_params(axis='x', labelsize=8)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)} Skills', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#115e59')
                    
    plt.title('8. Talent Versatility Volume (Total Stack Depth)', fontsize=9, fontweight='bold', pad=8, color='#1f2937')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
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
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        mock_data = {
            "Developer_Name": ["Alex Rivera", "Devon Chen", "Sarah Jenkins", "Michael Amadi", "Elena Rostova", "Hiroshi Tanaka"],
            "Skills": ["sql, api, cloud, integration", "web development, database, ui/ux", "data science, analytics, sql, python", "cloud, database, security", "ui/ux, design, front-end", "integration, api, backend, web development"],
            "Hourly_Rate": [45.0, 60.0, 55.0, 70.0, 40.0, 65.0],
            "Experience_Years": [3, 5, 4, 7, 2, 6]
        }
        df = pd.DataFrame(mock_data)

    project_requirements_set = {str(kw).lower().strip() for kw in extracted_keywords if str(kw).strip()}
    
    if not project_requirements_set:
        project_requirements_set = {"sql", "api", "database", "analytics"}

    scores = []
    missing_counter = {}

    for idx, row in df.iterrows():
        dev_skills = clean_skill_string_to_set(row.get('Skills', ''))
        
        matching_skills = project_requirements_set.intersection(dev_skills)
        missing_skills = project_requirements_set.difference(dev_skills)
        
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

    df_sorted = df.sort_values(by=['Match_Score_Pct', 'Experience_Years'], ascending=[False, False])
    df_top_5 = df_sorted.head(5).copy()
    
    sorted_missing = sorted(missing_counter.items(), key=lambda x: x[1], reverse=True)

    # Compile ALL 8 base64 visualization reports
    img_top_matches = plot_top_matches(df_top_5)
    img_skill_scarcity = plot_skill_scarcity(sorted_missing)
    img_budget_fit = plot_budget_vs_fit(df)
    img_pool_availability = plot_pool_availability(df)
    img_experience_density = plot_experience_density(df_top_5)
    img_competency_heatmap = plot_competency_heatmap(df_top_5, project_requirements_set) # <-- ADDED
    img_roi_quadrants = plot_roi_quadrants(df)                                          # <-- ADDED
    img_skill_breadth = plot_talent_versatility(df_top_5)                                # <-- ADDED

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

    # Ensure your backend return payload keys match static/script_analytics.js perfectly!
    return {
        "top_developers": best_profiles,
        "graphs": {
            "img_top_matches": img_top_matches,
            "img_skill_scarcity": img_skill_scarcity,
            "img_budget_fit": img_budget_fit,
            "img_pool_availability": img_pool_availability,
            "img_experience_density": img_experience_density,
            "img_competency_heatmap": img_competency_heatmap, # <-- ADDED
            "img_roi_quadrants": img_roi_quadrants,           # <-- ADDED
            "img_skill_breadth": img_skill_breadth            # <-- ADDED
        }
    }
