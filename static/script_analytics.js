// static/script_analytics.js 
// Client Rendering & Lifecycle Orchestration Engine for Developer Match Matrix

document.addEventListener('DOMContentLoaded', () => {
    // 1. EXTRACT STASHED PAYLOADS FROM BROWSER TRANSACTION CACHE
    const cachedTransactionPayload = localStorage.getItem('active_matching_data');
    
    // Redirect gracefully back to document capture page if cache is blank
    if (!cachedTransactionPayload) {
        alert("No active matching metrics profiles available. Please analyze a specification document first.");
        window.location.href = "/";
        return;
    }

    let parsedPayload;
    try {
        parsedPayload = JSON.parse(cachedTransactionPayload);
    } catch (parseAnomaly) {
        console.error("Critical Failure: Inbound cache matrix corrupt.", parseAnomaly);
        alert("Session error. Redirecting to clean document upload terminal.");
        window.location.href = "/";
        return;
    }

    const { filename, analytics } = parsedPayload;

    // 2. BIND INTERFACE COMPONENTS ARCHITECTURAL HOOKS
    const activeDocTag = document.getElementById('active-doc-tag');
    const poolCountBadge = document.getElementById('pool-count-badge');
    const cardsContainer = document.getElementById('developer-cards-container');

    // Display targeting source info in the navigation tier
    if (activeDocTag && filename) {
        activeDocTag.textContent = `Target File: ${filename}`;
        activeDocTag.classList.remove('hidden');
    }

    // 3. MAP 5-CHANNEL MATPLOTLIB HIGH-RES VISUALIZATION GRAPHS
    if (analytics && analytics.graphs) {
        const graphs = analytics.graphs;
        bindVisualDataStream('matchImgTop', graphs.img_top_matches);
        bindVisualDataStream('matchImgScarcity', graphs.img_skill_scarcity);
        bindVisualDataStream('matchImgBudget', graphs.img_budget_fit);
        bindVisualDataStream('matchImgAvailability', graphs.img_pool_availability);
        bindVisualDataStream('matchImgExperience', graphs.img_experience_density);
    } else {
        console.error("Critical Mapping Error: 5-Channel visualization layer keys missing from transaction payload.");
    }

    // 4. GENERATE TALENT RANKING INTERACTIVE FEED CARDS
    if (analytics && analytics.top_developers && analytics.top_developers.length > 0) {
        const candidatesPool = analytics.top_developers;
        
        // Synchronize numeric counters layout badges
        if (poolCountBadge) {
            poolCountBadge.textContent = `${candidatesPool.length} Top Fits`;
        }

        // Clean out mock placeholder rows safely
        if (cardsContainer) {
            cardsContainer.innerHTML = '';

            candidatesPool.forEach((developerProfile) => {
                const layoutCardNode = document.createElement('div');
                layoutCardNode.className = 'p-4 border border-gray-100 rounded-xl bg-gray-50 hover:border-emerald-300 transition duration-150 space-y-3 shadow-sm';
                
                // Construct structural row strings using defensive escape sanitation models
                layoutCardNode.innerHTML = `
                    <div class="flex items-start justify-between gap-2">
                        <div>
                            <h4 class="font-bold text-gray-800 text-sm">${escapeHtmlText(developerProfile.name)}</h4>
                            <p class="text-xs text-gray-400 font-medium mt-0.5">
                                ${parseInt(developerProfile.experience_years, 10)} Yrs Experience • $${parseFloat(developerProfile.hourly_rate).toFixed(2)}/hr
                            </p>
                        </div>
                        <span class="bg-emerald-50 text-emerald-700 border border-emerald-100 text-xs px-2.5 py-0.5 rounded-full font-bold shrink-0">
                            ${parseFloat(developerProfile.match_score).toFixed(1)}% Match
                        </span>
                    </div>
                    <div class="pt-2 border-t border-dashed border-gray-200">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Matched Skills In Document:</p>
                        <div class="flex flex-wrap gap-1">
                            ${(developerProfile.matched_skills_found || []).map(skillToken => `
                                <span class="bg-blue-50 text-blue-700 text-[10px] px-2 py-0.5 rounded font-medium border border-blue-100 uppercase tracking-wide">
                                    ${escapeHtmlText(skillToken)}
                                </span>
                            `).join('')}
                        </div>
                    </div>
                `;
                cardsContainer.appendChild(layoutCardNode);
            });
        }
    } else {
        console.warn("No suitable developer configurations isolated from requirement parsing vector weights.");
    }

    /**
     * Mounts binary Base64 layout streams smoothly onto targeting image wrappers
     * @param {string} targetImageDomId - Targeting view DOM identifier token string
     * @param {string} structuralBase64DataStream - Inbound base64 payload layout formatting string
     */
    function bindVisualDataStream(targetImageDomId, structuralBase64DataStream) {
        const imageElementPointer = document.getElementById(targetImageDomId);
        if (imageElementPointer && structuralBase64DataStream) {
            imageElementPointer.src = structuralBase64DataStream;
            imageElementPointer.classList.remove('hidden');
        } else if (imageElementPointer) {
            imageElementPointer.classList.add('hidden');
        }
    }

    /**
     * Prevents browser dynamic input injection attacks (Anti-XSS Vector)
     * @param {string} unverifiedString - Raw textual parameter imported from dataset properties
     * @returns {string} Sanitized text payload string values
     */
    function escapeHtmlText(unverifiedString) {
        if (!unverifiedString) return '';
        return String(unverifiedString)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
