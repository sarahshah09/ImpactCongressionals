async function loadData() {
    try {
        // This looks for the data.json file you manually updated
        const response = await fetch('data.json');
        const data = await response.json();
        const container = document.getElementById('dashboard');
        
        // Clear the "Loading" message
        container.innerHTML = ''; 

        for (const [district, candidates] of Object.entries(data)) {
            const card = document.createElement('div');
            card.className = 'card';
            
            let candidateHtml = `<h2>District: ${district}</h2>`;
            
            candidates.forEach(cand => {
                // This creates the bar width based on $2M goal
                const percentage = Math.min((cand.coh / 2000000) * 100, 100); 
                candidateHtml += `
                    <div class="candidate-row">
                        <div class="name">
                            <span>${cand.name} ${cand.is_impact ? '⭐' : ''}</span>
                        </div>
                        <div class="bar-container">
                            <div class="bar ${cand.is_impact ? 'impact' : 'rival'}" style="width: ${percentage}%"></div>
                        </div>
                        <div class="amount">$${cand.coh.toLocaleString()}</div>
                    </div>
                `;
            });
            
            card.innerHTML = candidateHtml;
            container.innerHTML += card.outerHTML;
        }
    } catch (error) {
        console.error("Error loading data:", error);
        document.getElementById('dashboard').innerHTML = "Check back soon for updated FEC data.";
    }
}

loadData();
