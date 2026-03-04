document.addEventListener('DOMContentLoaded', () => {
    const searchbar = document.getElementById('searchbar');
    const suggestionBox = document.querySelector('.suggestions');

    searchbar.onkeyup = async function() {
        let query = searchbar.value.trim();

        if (query.length > 2) {
            try {
                const response = await fetch('/live-search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ "query": query })
                }); 

                const suggestions = await response.json();
                
                display(suggestions, suggestionBox);

            } catch (error) {
                console.error("Search failed:", error);
            }
        } else {
            suggestionBox.innerHTML = "";
        }
    };

    searchbar.addEventListener('blur', () => {
        setTimeout(() => {
            suggestionBox.style.display = 'none';
        }, 200);
    });

    searchbar.addEventListener('focus', () => {
        if (searchbar.value.trim().length > 2) {
            suggestionBox.style.display = 'block';
        }
    });
});

function display(suggestions, container) {
    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = "<ul><li>No results found</li></ul>";
        return;
    }

    const htmlContent = suggestions.map((item) => {
        return `<li>${item}</li>`;
    }).join('');

    container.innerHTML = `<ul>${htmlContent}</ul>`;
}