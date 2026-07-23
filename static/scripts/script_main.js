document.addEventListener('DOMContentLoaded', () => {
    //interface binding hooks
    const uploadForm = document.getElementById('upload-form');
    const pdfInput = document.getElementById('pdf-file');
    const keywordsInput = document.getElementById('keywords');
    const submitBtn = document.getElementById('submit-btn');
    const fileStatusText = document.getElementById('file-status');
    
    const loaderView = document.getElementById('loader');
    const analyticsPanel = document.getElementById('analytics-panel');
    const placeholderView = document.getElementById('placeholder-view');
    const globalMatchBadge = document.getElementById('match-badge');

    //early exist if file not found
    if (!uploadForm) return;

    // safely escape regex characters during matching
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // 4-Channel Document Analysis Matrix  Image
    const graphSlots = {
        category: document.getElementById('chartImgCategory'),
        density: document.getElementById('chartImgDensity'),
        footprint: document.getElementById('chartImgFootprint'),
        composition: document.getElementById('chartImgComposition')
    };

    //container for text string
    const metricSections = {
        constraints: {
            wrapper: document.getElementById('section-constraints'),
            container: document.getElementById('section-constraints')?.querySelector('.stream-cards-container-slot'),
            badge: document.getElementById('section-constraints')?.querySelector('.section-counter-badge')
        },
        techstack: {
            wrapper: document.getElementById('section-techstack'),
            container: document.getElementById('section-techstack')?.querySelector('.stream-cards-container-slot'),
            badge: document.getElementById('section-techstack')?.querySelector('.section-counter-badge')
        },
        timeline: {
            wrapper: document.getElementById('section-timeline'),
            container: document.getElementById('section-timeline')?.querySelector('.stream-cards-container-slot'),
            badge: document.getElementById('section-timeline')?.querySelector('.section-counter-badge')
        },
        other: {
            wrapper: document.getElementById('section-other'),
            container: document.getElementById('section-other')?.querySelector('.stream-cards-container-slot'),
            badge: document.getElementById('section-other')?.querySelector('.section-counter-badge')
        }
    };

    // multipart submission intercept
    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (!pdfInput.files || pdfInput.files.length === 0) 
            return;

        const targetFile = pdfInput.files[0];
        // Shift processing visibility parameters layout
        toggleInterfaceLoadingState(true);
        updateStatusLabel(`Analyzing metadata: ${targetFile.name}`);

        // Package transaction parameters using multipart boundary models
        const transactionPayload = new FormData();
        transactionPayload.append('file', targetFile);
        transactionPayload.append('keywords', keywordsInput.value.trim());

        try {
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

    // UI mutation management
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

    // RENDERING PARSED DATA FEEDS AND HIGH-RES MATRIX GRAPHICS
    function renderDashboardAnalytics(responsePayload) {
        // Hiding the placeholder view automatically cleans up the summary paragraph
        if (placeholderView) placeholderView.classList.add('hidden');
        
        if (fileStatusText && responsePayload.filename) {
            fileStatusText.textContent = `Active File: ${responsePayload.filename}`;
            fileStatusText.classList.remove('hidden');
        }

        if (globalMatchBadge && responsePayload.total_matches_found !== undefined) {
            globalMatchBadge.textContent = `${responsePayload.total_matches_found} Matches`;
            globalMatchBadge.classList.remove('hidden');
        }
        // Mount the 4 Base64 Matplotlib image strings onto their image tags
        mapGraphicOutput(graphSlots.category, responsePayload.img_category);
        mapGraphicOutput(graphSlots.density, responsePayload.img_density);
        mapGraphicOutput(graphSlots.footprint, responsePayload.img_footprint);
        mapGraphicOutput(graphSlots.composition, responsePayload.img_composition);
        
        if (analyticsPanel) analyticsPanel.classList.remove('hidden');

        // Distribute sentences into individual container feeds
        if (responsePayload.results && responsePayload.results.length > 0) {
            hideDataSectionStreams(); // Reset previous outputs
            
            let counts = { constraints: 0, techstack: 0, timeline: 0, other: 0 };

            responsePayload.results.forEach(item => {
                // Apply background highlights to keywords discovered in the text block
                let highlightedText = item.sentence || '';
                if (item.matched_keywords) {
                    item.matched_keywords.forEach(keyword => {
                        const safeKeyword = escapeRegExp(keyword);
                        const regex = new RegExp(`\\b(${safeKeyword})\\b`, 'gi');
                        highlightedText = highlightedText.replace(regex, `<mark class="bg-yellow-200">$1</mark>`);
                    });
                }

                // item card using single class styles matching index.css
                const blockCard = document.createElement('div');
                blockCard.style.padding = '1rem';
                blockCard.style.backgroundColor = '#ffffff';
                blockCard.style.borderRadius = '0.5rem';
                blockCard.style.border = '1px solid #e5e7eb';
                blockCard.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
                blockCard.style.display = 'flex';
                blockCard.style.flexDirection = 'column';
                blockCard.style.gap = '0.5rem';
                
                blockCard.innerHTML = `
                    <p style="font-size: 0.875rem; line-height: 1.5; color: #374151;">${highlightedText}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.25rem; padding-top: 0.5rem; border-top: 1px dashed #f3f4f6;">
                        ${item.categories.map(cat => `
                            <span style="font-size: 0.675rem; font-weight: 600; text-transform: uppercase; background-color: #eff6ff; color: #1e40af; padding: 0.125rem 0.375rem; border-radius: 0.25rem; border: 1px solid #dbeafe;">${escapeHtml(cat)}</span>
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

            // Make columns visible for extracted data cards
            if (counts.constraints > 0 && metricSections.constraints.wrapper) {
                metricSections.constraints.wrapper.classList.remove('hidden');
                metricSections.constraints.badge.textContent = counts.constraints;
            }
            if (counts.techstack > 0 && metricSections.techstack.wrapper) {
                metricSections.techstack.wrapper.classList.remove('hidden');
                metricSections.techstack.badge.textContent = counts.techstack;
            }
            if (counts.timeline > 0 && metricSections.timeline.wrapper) {
                metricSections.timeline.wrapper.classList.remove('hidden');
                metricSections.timeline.badge.textContent = counts.timeline;
            }
            if (counts.other > 0 && metricSections.other.wrapper) {
                metricSections.other.wrapper.classList.remove('hidden');
                metricSections.other.badge.textContent = counts.other;
            }
        } else {
            placeholderView?.classList.remove('hidden');
        }

        // CACHE ANALYTICS PAYLOADS AND ACTIVATE LINK REDIRECTION
        if (responsePayload.matching_analytics) {
            localStorage.setItem('active_matching_data', JSON.stringify({
                filename: responsePayload.filename,
                analytics: responsePayload.matching_analytics
            }));

            // Clear look tracking classes on the navigation button
            const devBtn = document.getElementById('find-developer-btn');
            const devTip = document.getElementById('find-dev-tip');
            
            if (devBtn) {
                devBtn.classList.remove('opacity-50', 'pointer-events-none');
            }
            if (devTip) {
                devTip.textContent = "Talent metrics loaded! Click above to evaluate matching developers.";
                devTip.style.color = '#059669';
                devTip.style.fontWeight = '600';
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
