// Client Rendering & Lifecycle Orchestration Engine for Developer Match Matrix
document.addEventListener('DOMContentLoaded', () => {
    // EXTRACT STASHED PAYLOADS FROM BROWSER TRANSACTION CACHE
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

    //  BIND INTERFACE COMPONENTS ARCHITECTURAL HOOKS
    const activeDocTag = document.getElementById('active-doc-tag');
    const poolCountBadge = document.getElementById('pool-count-badge');
    const cardsContainer = document.getElementById('developer-cards-container');

    // Display targeting source info in the navigation tier
    if (activeDocTag && filename) {
        activeDocTag.textContent = `Target File: ${filename}`;
        activeDocTag.classList.remove('hidden');
    }

    // MAP 8-CHANNEL MATPLOTLIB HIGH-RES VISUALIZATION GRAPHS
    if (analytics && analytics.graphs) {
        const graphs = analytics.graphs;
        bindVisualDataStream('matchImgTop', graphs.img_top_matches);
        bindVisualDataStream('matchImgScarcity', graphs.img_skill_scarcity);
        bindVisualDataStream('matchImgBudget', graphs.img_budget_fit);
        bindVisualDataStream('matchImgAvailability', graphs.img_pool_availability);
        bindVisualDataStream('matchImgExperience', graphs.img_experience_density);
        bindVisualDataStream('matchImgHeatmap', graphs.img_competency_heatmap);
        bindVisualDataStream('matchImgROI', graphs.img_roi_quadrants);
        bindVisualDataStream('matchImgBreadth', graphs.img_skill_breadth);
    } else {
        console.error("Critical Mapping Error: 8-Channel visualization layer keys missing from transaction payload.");
    }

    //  GENERATE TALENT RANKING INTERACTIVE FEED CARDS
    if (analytics && analytics.top_developers && analytics.top_developers.length > 0) {
        const candidatesPool = analytics.top_developers;
        // Synchronize numeric counters layout badges
        if (poolCountBadge) {
            poolCountBadge.textContent = `${candidatesPool.length} Top Fits`;
        }

        if (cardsContainer) {
            cardsContainer.innerHTML = '';

            candidatesPool.forEach((developerProfile) => {
                const layoutCardNode = document.createElement('div');
                layoutCardNode.style.padding = '1rem';
                layoutCardNode.style.backgroundColor = '#f9fafb';
                layoutCardNode.style.borderRadius = '0.75rem';
                layoutCardNode.style.border = '1px solid #e5e7eb';
                layoutCardNode.style.display = 'flex';
                layoutCardNode.style.flexDirection = 'column';
                layoutCardNode.style.gap = '0.75rem';
                layoutCardNode.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
                
                layoutCardNode.innerHTML = `
                    <div style="display: flex; align-items: start; justify-content: space-between; gap: 0.5rem;">
                        <div>
                            <h4 style="font-weight: 700; color: #1f2937; font-size: 0.875rem;">${escapeHtmlText(developerProfile.name)}</h4>
                            <p style="font-size: 0.75rem; color: #9ca3af; font-weight: 500; margin-top: 0.125rem;">
                                ${parseInt(developerProfile.experience_years, 10)} Yrs Experience • $${parseFloat(developerProfile.hourly_rate).toFixed(2)}/hr
                            </p>
                        </div>
                        <span style="background-color: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; font-size: 0.75rem; padding: 0.125rem 0.625rem; border-radius: 9999px; font-weight: 700; white-space: nowrap;">
                            ${parseFloat(developerProfile.match_score).toFixed(1)}% Match
                        </span>
                    </div>
                    <div style="padding-top: 0.5rem; border-top: 1px dashed #e5e7eb;">
                        <p style="font-size: 10px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">Matched Skills In Document:</p>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.25rem;">
                            ${(developerProfile.matched_skills_found || []).map(skillToken => `
                                <span style="background-color: #eff6ff; color: #1e40af; border: 1px solid #dbeafe; font-size: 10px; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-weight: 500; text-transform: uppercase;">
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