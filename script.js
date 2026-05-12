async function loadData() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        const container = document.getElementById('dashboard');
        container.innerHTML = ''; // Clear the "Loading" message

        for (const [district, candidates] of Object.entries(data)) {
            const card = document.createElement('div');
            card.className = 'card';
            
            let candidateHtml = `<h2>District: ${district}</h2>`;
            
            candidates.forEach(cand => {
                const percentage = Math.min((cand.coh / 2000000) * 100, 100); // Scale to $2M
                candidateHtml += `
                    <div class="candidate-row">
                        <div class="name">${cand.name} ${cand.is_impact ? '⭐' : ''}</div>
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
        document.getElementById('dashboard').innerHTML = "Error loading financial data.";
    }
}

loadData();
