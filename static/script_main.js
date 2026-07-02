// static/script_main.js
// Main JavaScript driver for PDF Filter Dashboard Analytics System

document.addEventListener('DOMContentLoaded', () => {
    // Core Form and UI Controls Element Binding
    const uploadForm = document.getElementById('upload-form');
    const pdfInput = document.getElementById('pdf-file');
    const keywordsInput = document.getElementById('keywords');
    const submitBtn = document.getElementById('submit-btn');
    const fileStatusText = document.getElementById('file-status');
    
    // Status Trackers, Loaders, and Main Structural View Panels
    const loaderView = document.getElementById('loader');
    const analyticsPanel = document.getElementById('analytics-panel');
    const placeholderView = document.getElementById('placeholder-view');
    const globalMatchBadge = document.getElementById('match-badge');

    // Safe early exit if form isn't present (e.g., on analytics.html)
    if (!uploadForm) return;

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Quad-Grid Matrix Image Graphs Array Configuration
    const graphSlots = {
        category: document.getElementById('chartImgCategory'),
        density: document.getElementById('chartImgDensity'),
        footprint: document.getElementById('chartImgFootprint'),
        composition: document.getElementById('chartImgComposition')
    };

    // Parsed Data Categorized Stream Stream Container Registry
    const metricSections = {
        constraints: {
            wrapper: document.getElementById('section-constraints'),
            container: document.getElementById('section-constraints')?.querySelector('.container'),
            badge: document.getElementById('section-constraints')?.querySelector('.badge')
        },
        techstack: {
            wrapper: document.getElementById('section-techstack'),
            container: document.getElementById('section-techstack')?.querySelector('.container'),
            badge: document.getElementById('section-techstack')?.querySelector('.badge')
        },
        timeline: {
            wrapper: document.getElementById('section-timeline'),
            container: document.getElementById('section-timeline')?.querySelector('.container'),
            badge: document.getElementById('section-timeline')?.querySelector('.badge')
        },
        other: {
            wrapper: document.getElementById('section-other'),
            container: document.getElementById('section-other')?.querySelector('.container'),
            badge: document.getElementById('section-other')?.querySelector('.badge')
        }
    };

    // Intercept Upload Submission Event for Analytical Evaluation
    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (!pdfInput.files || !pdfInput.files[0]) return;
        const targetFile = pdfInput.files[0];

        // Display Operational State across UI Component Layers
        toggleInterfaceLoadingState(true);
        updateStatusLabel(`Analyzing metadata: ${targetFile.name}`);

        // Prepare Multipart Form Payload for secure transmission
        const transactionPayload = new FormData();
        transactionPayload.append('file', targetFile);
        transactionPayload.append('keywords', keywordsInput.value.trim());

        try {
            // Transaction pipeline targeting the active analytical routing system
            const backendResponse = await fetch('/filtered-data', {
                method: 'POST',
                body: transactionPayload
            });

            if (!backendResponse.ok) {
                const errData = await backendResponse.json();
                throw new Error(errData.detail || `Execution Pipeline Fault Status: ${backendResponse.status}`);
            }

            const computationPayload = await backendResponse.json();
            renderDashboardAnalytics(computationPayload);

        } catch (pipelineExecutionError) {
            console.error('Critical Engine Error Status:', pipelineExecutionError);
            alert(`Failed to accurately complete extraction: ${pipelineExecutionError.message}`);
            resetDashboardView();
        } finally {
            toggleInterfaceLoadingState(false);
        }
    });

    function toggleInterfaceLoadingState(isLoading) {
        if (submitBtn) {
            submitBtn.disabled = isLoading;
            if (isLoading) submitBtn.classList.add('opacity-50');
            else submitBtn.classList.remove('opacity-50');
        }
        if (isLoading) {
            loaderView?.classList.remove('hidden');
            analyticsPanel?.classList.add('hidden');
            placeholderView?.classList.add('hidden');
            hideDataSectionStreams();
        } else {
            loaderView?.classList.add('hidden');
        }
    }

    function updateStatusLabel(logMessage) {
        if (fileStatusText) {
            fileStatusText.textContent = logMessage;
            fileStatusText.classList.remove('hidden');
        }
    }

    function hideDataSectionStreams() {
        Object.values(metricSections).forEach(section => {
            if (section.wrapper) section.wrapper.classList.add('hidden');
            if (section.container) section.container.innerHTML = '';
            if (section.badge) section.badge.textContent = '0';
        });
        globalMatchBadge?.classList.add('hidden');
    }

    function resetDashboardView() {
        placeholderView?.classList.remove('hidden');
        analyticsPanel?.classList.add('hidden');
        fileStatusText?.classList.add('hidden');
        hideDataSectionStreams();
    }

    function renderDashboardAnalytics(responsePayload) {
        if (placeholderView) placeholderView.classList.add('hidden');
        
        if (fileStatusText && responsePayload.filename) {
            fileStatusText.textContent = `Active File: ${responsePayload.filename}`;
            fileStatusText.classList.remove('hidden');
        }

        if (globalMatchBadge && responsePayload.total_matches_found !== undefined) {
            globalMatchBadge.textContent = `${responsePayload.total_matches_found} Matches`;
            globalMatchBadge.classList.remove('hidden');
        }

        // 1. Process and Map Matrix Charts 
        if (responsePayload) {
            mapGraphicOutput(graphSlots.category, responsePayload.img_category);
            mapGraphicOutput(graphSlots.density, responsePayload.img_density);
            mapGraphicOutput(graphSlots.footprint, responsePayload.img_footprint);
            mapGraphicOutput(graphSlots.composition, responsePayload.img_composition);
            analyticsPanel?.classList.remove('hidden');
        }

        // 2. Construct Dynamically Categorized Text Blocks Inside Streams Layout
        if (responsePayload.results && responsePayload.results.length > 0) {
            hideDataSectionStreams(); // clear out pre-existing data safely
            
            let counts = { constraints: 0, techstack: 0, timeline: 0, other: 0 };

            responsePayload.results.forEach(item => {
                // RESTORED KEYWORD HIGHLIGHTING LOGIC
                let highlightedText = item.sentence || '';
                if (item.matched_keywords) {
                    item.matched_keywords.forEach(keyword => {
                        const safeKeyword = escapeRegExp(keyword);
                        const regex = new RegExp(`\\b(${safeKeyword})\\b`, 'gi');
                        highlightedText = highlightedText.replace(regex, `<mark class="bg-yellow-200 text-yellow-900 rounded px-1 font-medium">$1</mark>`);
                    });
                }

                const blockCard = document.createElement('div');
                blockCard.className = 'p-4 bg-white rounded-lg border border-gray-100 hover:border-gray-300 transition duration-150 shadow-sm space-y-3';
                
                blockCard.innerHTML = `
                    <p class="text-sm text-gray-700 leading-relaxed font-normal">${highlightedText}</p>
                    <div class="flex flex-wrap gap-2 pt-1 border-t border-dashed border-gray-100">
                        ${item.categories.map(cat => `
                            <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-0.5 rounded font-semibold border border-blue-100 uppercase tracking-wider">${escapeHtml(cat)}</span>
                        `).join('')}
                    </div>
                `;

                let matchedAny = false;
                if (item.categories.includes('Constraints') && metricSections.constraints.container) {
                    metricSections.constraints.container.appendChild(blockCard.cloneNode(true));
                    counts.constraints++;
                    matchedAny = true;
                }
                if (item.categories.includes('Tech Stack') && metricSections.techstack.container) {
                    metricSections.techstack.container.appendChild(blockCard.cloneNode(true));
                    counts.techstack++;
                    matchedAny = true;
                }
                if (item.categories.includes('Timeline') && metricSections.timeline.container) {
                    metricSections.timeline.container.appendChild(blockCard.cloneNode(true));
                    counts.timeline++;
                    matchedAny = true;
                }
                if ((!matchedAny || item.categories.includes('Other')) && metricSections.other.container) {
                    metricSections.other.container.appendChild(blockCard.cloneNode(true));
                    counts.other++;
                }
            });

            // Toggle visibilities based on structural match counts
            if (counts.constraints > 0) {
                metricSections.constraints.wrapper.classList.remove('hidden');
                metricSections.constraints.badge.textContent = counts.constraints;
            }
                        if (counts.techstack > 0) {
                metricSections.techstack.wrapper.classList.remove('hidden');
                metricSections.techstack.badge.textContent = counts.techstack;
            }
            if (counts.timeline > 0) {
                metricSections.timeline.wrapper.classList.remove('hidden');
                metricSections.timeline.badge.textContent = counts.timeline;
            }
            if (counts.other > 0) {
                metricSections.other.wrapper.classList.remove('hidden');
                metricSections.other.badge.textContent = counts.other;
            }
        } else {
            placeholderView?.classList.remove('hidden');
        }

        // 3. RESTORED DETAILED REDIRECT AND BUTTON STATE UNLOCK MANAGEMENT
        if (responsePayload.matching_analytics) {
            localStorage.setItem('active_matching_data', JSON.stringify({
                filename: responsePayload.filename,
                analytics: responsePayload.matching_analytics
            }));

            // Unlock and style structural page navigation elements
            const devBtn = document.getElementById('find-developer-btn');
            const devTip = document.getElementById('find-dev-tip');
            
            if (devBtn) {
                devBtn.classList.remove('opacity-50', 'pointer-events-none');
            }
            if (devTip) {
                devTip.textContent = "Talent metrics loaded! Click above to evaluate matching developers.";
                devTip.classList.remove('text-gray-400');
                devTip.classList.add('text-emerald-600', 'font-medium');
            }
        }
    }

    function mapGraphicOutput(imageDOMTarget, visualSourceUri) {
        if (visualSourceUri && imageDOMTarget) {
            imageDOMTarget.src = visualSourceUri;
            imageDOMTarget.classList.remove('hidden');
        } else if (imageDOMTarget) {
            imageDOMTarget.classList.add('hidden');
        }
    }

    function escapeHtml(unsafeString) {
        if (!unsafeString) return '';
        return unsafeString
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});

