import io
import re
import pypdf
import spacy
import base64
import matplotlib
# Force Matplotlib to run in a headless background worker state
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Initialize SpaCy pipeline layer
nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])

MANDATORY_CATEGORIES = {
    "Tech Stack": ["sql", "analytics", "data science", "web development", "ui/ux", "api", "database", "cloud", "integration"],
    "Timeline": ["timeline", "deadline", "milestone", "phase", "duration", "weeks", "months", "schedule", "go-live"],
    "Team Size": ["team", "engineer", "developer", "resource", "designer", "architect", "headcount", "fte"],
    "Constraints": ["must", "shall", "required", "sla", "compliance", "uptime", "budget"]
}

#Standard conversational fluff and layout phrases to ignore completely for NOISE REDUCTION
CONVERSATIONAL_FLUFF = [
    "in this section", "we will discuss", "as mentioned above", 
    "welcome to", "thank you for", "intended to look", "table of contents",
    "all rights reserved", "confidential document", "click here to"
]

# ==========================================
# MATPLOTLIB ENGINE GRAPH GENERATORS
# ==========================================
def plot_category_chart(chart_metrics):
    categories = list(chart_metrics.keys())
    counts = list(chart_metrics.values())
    trend_values = [round(val * 1.5) for val in counts]

    fig, ax1 = plt.subplots(figsize=(6, 3.8), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#ffffff')
    
    bars = ax1.bar(categories, counts, color='#3b82f6', width=0.45, label='Matches', zorder=2)
    ax1.set_ylabel('Matches Count', color='#1e3a8a', fontweight='bold', fontsize=9)
    ax1.tick_params(axis='y' ,labelcolor='#1e3a8a', labelsize=8 )
    ax1.tick_params(axis='x', labelsize=8)
    ax1.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=1)
    
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{int(height)}',
                     xy=(bar.get_x()  + bar.get_width()/2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1e3a8a')
    
    ax2 = ax1.twinx()
    line, = ax2.plot(categories, trend_values, color='#10b981', marker='o', linewidth=2, label='Trend', zorder=3)
    ax2.set_ylabel('Trend Scale', color='#065f46', fontweight='bold', fontsize=9)
    ax2.tick_params(axis='y', labelcolor='#065f46', labelsize=8)

    for x, y in zip(categories, trend_values):
        ax2.annotate(f'{y}', (x, y), xytext=(0, 6), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, color='#065f46', fontweight='bold')
    
    plt.title('1. Category Evaluation Matrix Map', fontsize=10, fontweight='bold', pad=10, color='#374151')
    fig.tight_layout()
    buf=io.BytesIO()   #temporary stream of bytes inside computer ram
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    buf.seek(0)       #extract the raw binary image data stream out of ram
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}" #data URL schema
                                    #translate complex binary   #convert raw base64 bytes obj -> standard pyhton script
                                    # -> standard ASCII
def plot_density_chart(keyword_density):
    if not keyword_density: keyword_density = {"NONE": 0}
    sorted_kws = sorted(keyword_density.items(), key=lambda x: x[1], reverse=True)[:8]
    labels = [k.upper() for k, _ in sorted_kws]
    values = [v for _, v in sorted_kws]

    fig, ax = plt.subplots(figsize=(6, 3.8), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    bars = ax.barh(labels, values, color='#10b981', height=0.5, zorder=2)
    ax.set_xlabel('Occurrences Count', color='#374151', fontweight='bold', fontsize=9)
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(True, axis='x', linestyle='--', alpha=0.3, zorder=1)
    ax.invert_yaxis()

    for bar in bars:
        width = bar.get_width()
        ax.annotate(f' {int(width)}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=8, fontweight='bold', color='#065f46')

    plt.title('2. Top Keyword Density Vectors', fontsize=10, fontweight='bold', pad=10, color='#374151')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

def plot_page_footprint_chart(page_metrics):
    if not page_metrics: page_metrics = [0]
    pages = [f"P{i+1}" for i in range(len(page_metrics))]

    fig, ax = plt.subplots(figsize=(6, 3.8), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    ax.plot(pages, page_metrics, color='#8b5cf6', marker='s', markersize=4, linewidth=1.5, zorder=2)
    ax.set_ylabel('Character Density Weight', color='#374151', fontweight='bold', fontsize=9)
    ax.set_xlabel('Document Page Sequences', color='#374151', fontweight='bold', fontsize=9)
    ax.tick_params(axis='both', labelsize=7)
    ax.grid(True, linestyle=':', alpha=0.4, zorder=1)

    for x, y in zip(pages, page_metrics):
        ax.annotate(f'{y}', (x, y), xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, color='#5b21b6')

    plt.title('3. Document Volume Footprint per Page', fontsize=10, fontweight='bold', pad=10, color='#374151')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

def plot_composition_chart(chart_metrics):
    labels = list(chart_metrics.keys())
    sizes = list(chart_metrics.values())
    if sum(sizes) == 0:
        labels, sizes = ["Neutral Content"], [1]
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

    fig, ax = plt.subplots(figsize=(6, 3.8), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                  startangle=90, colors=colors[:len(labels)],
                                  textprops=dict(color="#374151", fontsize=8),
                                  wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_weight('bold')
        autotext.set_color('white')

    plt.title('4. Context Diversity Composition Ratio', fontsize=10, fontweight='bold', pad=10, color='#374151')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

# ==========================================
# CORE EXTRACTION PARSER AND NOISE FILTER
# ==========================================

async def extract_and_filter_pdf(pdf_file, custom_keywords: str = ""):
    pdf_bytes = await pdf_file.read()
    pdf_stream = io.BytesIO(pdf_bytes)
    pdf_reader = pypdf.PdfReader(pdf_stream)
    
    extracted_text_pieces = []
    page_metrics = []
    
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            # 2. NOISE REDUCTION: Standardize whitespaces and strip out broken newline artifacts
            clean_text = re.sub(r'\s+', ' ', text).strip()
            extracted_text_pieces.append(clean_text)
            page_metrics.append(len(clean_text))
        else:
            page_metrics.append(0)
            
    combined_text = " ".join(extracted_text_pieces)

    runtime_categories = {k: v.copy() for k, v in MANDATORY_CATEGORIES.items()}
    if custom_keywords and custom_keywords.strip():
        custom_kws = [kw.lower().strip() for kw in custom_keywords.split(",") if kw.strip()]
        runtime_categories["Custom Searches"] = custom_kws

    doc_nlp = nlp(combined_text)
    
    filtered_sentences = []
    chart_metrics = {cat: 0 for cat in runtime_categories.keys()}
    keyword_density = {}

    for sent in doc_nlp.sents:
        sentence_str = sent.text.strip()
        
        # 3. NOISE REDUCTION: Ignore numeric table lists, short fragments, or giant run-on sections
        if len(sentence_str) < 25 or len(sentence_str) > 300:
            continue
            
        sentence_lower = sentence_str.lower()
        
        # 4. NOISE REDUCTION: Drop standard corporate document conversational filler
        if any(fluff in sentence_lower for fluff in CONVERSATIONAL_FLUFF):
            continue
        
        matched_kws = []
        sentence_categories = []
        
        # 5. NOISE REDUCTION: Force word boundaries (\b) so "api" won't trigger on "shaping"
        for category, kw_list in runtime_categories.items():
            found_kws = []
            for kw in kw_list:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, sentence_lower):
                    found_kws.append(kw)
            
            if found_kws:
                matched_kws.extend(found_kws)
                sentence_categories.append(category)
                chart_metrics[category] += 1
                
                for kw in found_kws:
                    keyword_density[kw] = keyword_density.get(kw, 0) + 1
        
        if matched_kws:
            filtered_sentences.append({
                "sentence": sentence_str,
                "matched_keywords": list(set(matched_kws)),
                "categories": list(set(sentence_categories))
            })

    return {
        "status": "success",
        "filename": pdf_file.filename,
        "total_matches_found": len(filtered_sentences),
        "img_category": plot_category_chart(chart_metrics),
        "img_density": plot_density_chart(keyword_density),
        "img_footprint": plot_page_footprint_chart(page_metrics),
        "img_composition": plot_composition_chart(chart_metrics),"results": filtered_sentences,
         "all_matched_keywords": list(keyword_density.keys()) # adding this line for matching developer in match.py
    }